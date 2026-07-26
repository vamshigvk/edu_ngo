# Project EduAccess — Frontend

React + Vite frontend for Project EduAccess. It consumes the **FastAPI**
backend (`../fastapi_backend`) via JWT authentication.

## Running locally

Start the backend first (defaults to `http://localhost:8000`):

```bash
cd ../fastapi_backend
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python -m app.scripts.seed        # create + seed the SQLite dev DB
uvicorn app.main:app --reload     # serves on :8000
```

Then the frontend:

```bash
npm install
npm run dev                       # serves on :5173
```

The Vite dev server (`vite.config.js`) proxies `/api`, `/auth`, `/dashboard`
and `/health` to the backend, so requests stay same-origin (no CORS in dev).
Point the proxy elsewhere with `BACKEND_URL=http://host:port npm run dev`.

## Configuration

`.env` holds `VITE_API_BASE` — the base URL prepended to every request. Leave
it **empty** in development (the dev proxy handles routing); in production set
it to the backend origin, e.g. `VITE_API_BASE=https://api.example.com`.

## Seeded logins

After `python -m app.scripts.seed`, every user has password `password123`:

| Email | Role | Lands on |
|---|---|---|
| `admin@example.com` | admin | `/admin` dashboard |
| `vikram.singh@example.com` | mentor | `/` |
| `aarav.mehta@example.com` | mentee | `/` |

## How it maps to the backend

| UI | Backend endpoint(s) |
|---|---|
| Login (`/login`) | `POST /auth/login` (form-encoded) → `GET /auth/me` |
| Student apply (`/apply/student`) | `POST /api/users` → `/api/mentee-profiles` → `/api/applications` → `/api/applications/{id}/submit` |
| Mentor apply (`/apply/mentor`) | `POST /api/users` → `/api/mentor-profiles` |
| Admin (`/admin`) | `GET /api/users`, `/api/pairs`, `/dashboard/emp`, `/api/resources` CRUD |
| Resources (`/resources`) | `GET /api/resources` |
