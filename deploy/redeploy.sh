#!/usr/bin/env bash
#
# Redeploy HireLens on the Ubuntu server or container.
#
# Installs deps, rebuilds CSS, migrates the DB, collects static files,
# and restarts the app + nginx when systemd is available.
#
# Usage:
#   cd /app
#   ./deploy/redeploy.sh
#
# Override defaults with env vars, e.g.:
#   APP_DIR=/srv/hirelens SERVICE=hirelens ./deploy/redeploy.sh
#
set -euo pipefail

# --- Config (override via environment) --------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="${APP_DIR:-$(cd "$SCRIPT_DIR/.." && pwd)}"
VENV_DIR="${VENV_DIR:-$APP_DIR/venv}"
SERVICE="${SERVICE:-hirelens}"        # systemd unit name for gunicorn
BRANCH="${BRANCH:-main}"
SKIP_GIT="${SKIP_GIT:-0}"             # set to 1 to deploy current working tree
SKIP_NPM="${SKIP_NPM:-0}"             # set to 1 to skip the Tailwind build
SKIP_APT="${SKIP_APT:-0}"             # set to 1 to skip apt install
SKIP_SERVICES="${SKIP_SERVICES:-0}"   # set to 1 to skip systemctl/nginx restart
SKIP_SEED_ADMIN="${SKIP_SEED_ADMIN:-0}"  # set to 1 to skip admin user seeding
ADMIN_EMAIL="${ADMIN_EMAIL:-admin@hirelens.com}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-password@123}"

# --- Helpers ----------------------------------------------------------------
log() { printf '\n\033[1;34m==>\033[0m %s\n' "$*"; }

run_as_root() {
  if [[ "$(id -u)" -eq 0 ]]; then
    "$@"
  else
    sudo "$@"
  fi
}

apt_install() {
  if [[ "$SKIP_APT" == "1" ]]; then
    log "SKIP_APT=1 — skipping apt install"
    return
  fi
  if ! command -v apt-get >/dev/null 2>&1; then
    log "apt-get not found — skipping system package install"
    return
  fi
  log "Installing curl, nodejs, npm, and Python tooling (apt)"
  run_as_root apt-get update
  run_as_root env DEBIAN_FRONTEND=noninteractive apt-get install -y \
    curl nodejs npm python3 python3-pip python3-venv
}

activate_python() {
  if [[ -f "$VENV_DIR/bin/activate" ]]; then
    log "Using virtualenv at $VENV_DIR"
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"
    return
  fi

  if command -v python3 >/dev/null 2>&1; then
    log "Creating virtualenv at $VENV_DIR"
    python3 -m venv "$VENV_DIR"
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"
    return
  fi

  echo "python3 not found. Install Python or set VENV_DIR to an existing venv." >&2
  exit 1
}

build_frontend() {
  if [[ "$SKIP_NPM" == "1" ]]; then
    log "SKIP_NPM=1 — skipping CSS build"
    return
  fi

  apt_install

  if [[ -f "${HOME}/.bashrc" ]]; then
    # shellcheck disable=SC1090
    source "${HOME}/.bashrc" || true
  fi

  if ! command -v npm >/dev/null 2>&1; then
    echo "npm not found. Install Node.js on the server or set SKIP_NPM=1." >&2
    exit 1
  fi

  log "Building Tailwind CSS"
  (cd "$APP_DIR" && npm install --no-audit --no-fund && npm run build:css)
}

restart_services() {
  if [[ "$SKIP_SERVICES" == "1" ]]; then
    log "SKIP_SERVICES=1 — skipping service restart"
    return
  fi
  if ! command -v systemctl >/dev/null 2>&1 || [[ ! -d /run/systemd/system ]]; then
    log "systemd not available — skipping service restart"
    return
  fi

  log "Restarting $SERVICE"
  run_as_root systemctl restart "$SERVICE"

  if command -v nginx >/dev/null 2>&1; then
    log "Reloading nginx"
    run_as_root nginx -t
    run_as_root systemctl reload nginx
  fi

  log "Status"
  run_as_root systemctl --no-pager --lines=0 status "$SERVICE" || true
}

cd "$APP_DIR"
log "App directory: $APP_DIR"

# --- 1. Latest code ---------------------------------------------------------
# if [[ "$SKIP_GIT" != "1" ]]; then
#   log "Pulling latest code ($BRANCH)"
#   git fetch --all --prune
#   git checkout "$BRANCH"
#   git pull --ff-only origin "$BRANCH"
# else
#   log "SKIP_GIT=1 — deploying current working tree"
# fi
log "Deploying current working tree (git pull disabled)"

# --- 2. Python dependencies -------------------------------------------------
log "Installing Python dependencies"
activate_python
pip install --upgrade pip
pip install -r requirements.txt

# --- 3. Frontend (Tailwind CSS) --------------------------------------------
build_frontend

# --- 4. Database migrations --------------------------------------------------
log "Applying database migrations"
python manage.py migrate --noinput

# --- 5. Admin user ----------------------------------------------------------
if [[ "$SKIP_SEED_ADMIN" != "1" ]]; then
  log "Ensuring admin user ($ADMIN_EMAIL)"
  python manage.py ensure_admin --email "$ADMIN_EMAIL" --password "$ADMIN_PASSWORD"
else
  log "SKIP_SEED_ADMIN=1 — skipping admin user seeding"
fi

# --- 6. Static files --------------------------------------------------------
log "Collecting static files"
python manage.py collectstatic --noinput

# --- 7. Sanity check --------------------------------------------------------
log "Running Django system checks"
python manage.py check --deploy || true

# --- 8. Restart services ----------------------------------------------------
restart_services

log "Done. Deploy complete. ✅"
