#!/usr/bin/env bash
#
# One-command setup for the whole Project EduAccess stack (db + backend + frontend).
#
# Usage:
#   ./setup.sh          Build images and start the stack (foreground logs stop with Ctrl-C)
#   ./setup.sh up       Same as above but detached (runs in the background)
#   ./setup.sh down     Stop and remove the containers
#   ./setup.sh reset    Stop and DELETE the database volume (fresh seed next start)
#   ./setup.sh logs     Follow logs
#
set -euo pipefail
cd "$(dirname "$0")"

# --- locate docker + compose ------------------------------------------------
if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: Docker is not installed. Install Docker Desktop: https://www.docker.com/products/docker-desktop/"
  exit 1
fi
if ! docker info >/dev/null 2>&1; then
  echo "ERROR: Docker daemon is not running. Start Docker Desktop and try again."
  exit 1
fi
if docker compose version >/dev/null 2>&1; then
  COMPOSE="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE="docker-compose"
else
  echo "ERROR: Docker Compose not found. It ships with Docker Desktop."
  exit 1
fi

print_ready() {
  cat <<'EOF'

============================================================
  Project EduAccess is up!

  Frontend (app) ....... http://localhost:8080
  Backend API .......... http://localhost:8000
  API docs (Swagger) ... http://localhost:8000/docs

  Seeded logins (password: password123)
    admin@example.com          -> admin dashboard (/admin)
    vikram.singh@example.com   -> mentor
    aarav.mehta@example.com    -> mentee

  Stop with:  ./setup.sh down
============================================================
EOF
}

case "${1:-start}" in
  start)
    $COMPOSE up --build
    ;;
  up)
    $COMPOSE up --build -d
    print_ready
    ;;
  down)
    $COMPOSE down
    ;;
  reset)
    $COMPOSE down -v
    echo "Database volume removed. Next start will re-seed demo data."
    ;;
  logs)
    $COMPOSE logs -f
    ;;
  *)
    echo "Usage: ./setup.sh [start|up|down|reset|logs]"
    exit 1
    ;;
esac
