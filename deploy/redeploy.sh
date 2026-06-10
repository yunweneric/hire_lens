#!/usr/bin/env bash
#
# Redeploy HireLens on the Ubuntu server.
#
# Pulls latest code, installs deps, rebuilds CSS, migrates the DB,
# collects static files, and restarts the app + nginx.
#
# Usage (on the server):
#   cd /app
#   sudo ./deploy/redeploy.sh
#
# Override defaults with env vars, e.g.:
#   APP_DIR=/srv/hirelens SERVICE=hirelens ./deploy/redeploy.sh
#
set -euo pipefail

# --- Config (override via environment) --------------------------------------
APP_DIR="${APP_DIR:-/app}"
VENV_DIR="${VENV_DIR:-$APP_DIR/venv}"
SERVICE="${SERVICE:-hirelens}"        # systemd unit name for gunicorn
BRANCH="${BRANCH:-main}"
SKIP_GIT="${SKIP_GIT:-0}"             # set to 1 to deploy current working tree
SKIP_NPM="${SKIP_NPM:-0}"             # set to 1 to skip the Tailwind build
SKIP_APT="${SKIP_APT:-0}"             # set to 1 to skip apt install (curl/nodejs)

# --- Helpers ----------------------------------------------------------------
log() { printf '\n\033[1;34m==>\033[0m %s\n' "$*"; }

apt_install() {
  if [[ "$SKIP_APT" == "1" ]]; then
    log "SKIP_APT=1 — skipping apt install"
    return
  fi
  if ! command -v apt-get >/dev/null 2>&1; then
    log "apt-get not found — skipping system package install"
    return
  fi
  log "Installing curl, nodejs, and npm (apt)"
  if [[ "$(id -u)" -eq 0 ]]; then
    apt-get update
    DEBIAN_FRONTEND=noninteractive apt-get install -y curl nodejs npm
  else
    sudo apt-get update
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y curl nodejs npm
  fi
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
  npm install --no-audit --no-fund
  npm run build:css
}

cd "$APP_DIR"

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
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt

# --- 3. Frontend (Tailwind CSS) --------------------------------------------
build_frontend

# --- 4. Database migrations --------------------------------------------------
log "Applying database migrations"
python manage.py migrate --noinput

# --- 5. Static files --------------------------------------------------------
log "Collecting static files"
python manage.py collectstatic --noinput

# --- 6. Sanity check --------------------------------------------------------
log "Running Django system checks"
python manage.py check --deploy || true

# --- 7. Restart services ----------------------------------------------------
log "Restarting $SERVICE"
systemctl restart "$SERVICE"

log "Reloading nginx"
nginx -t && systemctl reload nginx

log "Status"
systemctl --no-pager --lines=0 status "$SERVICE" || true

log "Done. Deploy complete. ✅"
