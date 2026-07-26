#!/bin/sh
set -e

# Prepare the database (create tables + seed demo data on first boot).
echo "==> Preparing database..."
python -m app.scripts.prestart

# Launch the API server.
echo "==> Starting FastAPI (uvicorn) on 0.0.0.0:8000 ..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
