#!/usr/bin/env bash
#
# Redeploy HireLens on the Ubuntu server.
#
# Pulls latest code, installs deps, rebuilds CSS, migrates the DB,
# collects static files, and restarts the app + nginx.
#
# Usage (on the server):
#   cd /var/www/hirelens
#   sudo ./deploy/redeploy.sh
#
# Override defaults with env vars, e.g.:
#   APP_DIR=/srv/hirelens SERVICE=hirelens ./deploy/redeploy.sh
#
set -euo pipefail

# --- Config (override via environment) --------------------------------------
APP_DIR="${APP_DIR:-/var/www/hirelens}"
VENV_DIR="${VENV_DIR:-$APP_DIR/venv}"
SERVICE="${SERVICE:-hirelens}"        # systemd unit name for gunicorn
BRANCH="${BRANCH:-main}"
SKIP_GIT="${SKIP_GIT:-0}"             # set to 1 to deploy current working tree
SKIP_NPM="${SKIP_NPM:-0}"             # set to 1 to skip the Tailwind build

# --- Helpers ----------------------------------------------------------------
log() { printf '\n\033[1;34m==>\033[0m %s\n' "$*"; }

cd "$APP_DIR"

# --- 1. Latest code ---------------------------------------------------------
if [[ "$SKIP_GIT" != "1" ]]; then
  log "Pulling latest code ($BRANCH)"
  git fetch --all --prune
  git checkout "$BRANCH"
  git pull --ff-only origin "$BRANCH"
else
  log "SKIP_GIT=1 — deploying current working tree"
fi

# --- 2. Python dependencies -------------------------------------------------
log "Installing Python dependencies"
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt

# --- 3. Frontend (Tailwind CSS) --------------------------------------------
if [[ "$SKIP_NPM" != "1" ]]; then
  if command -v npm >/dev/null 2>&1; then
    log "Building Tailwind CSS"
    npm install --no-audit --no-fund
    npm run build:css
  else
    log "npm not found — skipping CSS build (set SKIP_NPM=1 to silence)"
  fi
fi

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
