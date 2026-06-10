#!/usr/bin/env bash
#
# Seed HireLens with curated job postings.
#
# Usage:
#   cd /app
#   ./deploy/seed_jobs.sh
#
# Options are passed through to manage.py seed_jobs, e.g.:
#   ./deploy/seed_jobs.sh --clear
#   JOB_COUNT=10 ./deploy/seed_jobs.sh
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="${APP_DIR:-$(cd "$SCRIPT_DIR/.." && pwd)}"
VENV_DIR="${VENV_DIR:-$APP_DIR/venv}"
JOB_COUNT="${JOB_COUNT:-20}"

log() { printf '\n\033[1;34m==>\033[0m %s\n' "$*"; }

activate_python() {
  if [[ -f "$VENV_DIR/bin/activate" ]]; then
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"
    return
  fi
  if command -v python3 >/dev/null 2>&1; then
    python3 -m venv "$VENV_DIR"
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"
    return
  fi
  echo "python3 not found. Install Python or set VENV_DIR." >&2
  exit 1
}

cd "$APP_DIR"
log "Seeding $JOB_COUNT jobs in $APP_DIR"

activate_python

python manage.py seed_jobs --count "$JOB_COUNT" "$@"

log "Job seeding complete."
