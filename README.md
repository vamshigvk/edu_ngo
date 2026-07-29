# Project EduAccess

A mentorship platform for expanding education access: a **FastAPI** backend, a
**React + Vite** frontend, and a **PostgreSQL** database — all runnable with a
single command via Docker.

```
edu_nogo/
├── fastapi_backend/     FastAPI app (API, auth, scoring/matching engines)
├── frontend/            React + Vite SPA (served by nginx in Docker)
├── others/              Planning docs
├── docker-compose.yml   Orchestrates db + backend + frontend
├── setup.sh             One-command launcher
└── env.example          Optional overrides for Compose
```

---

## 1. Quick start (Docker — recommended)

**Prerequisites:**
- Python 3.12
- [Visual Studio Code](https://code.visualstudio.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running


```bash
./setup.sh up
```

That's it. This builds all three images, starts the stack, creates the database
schema, and seeds demo data on first boot. When it finishes:

| Service | URL |
|---|---|
| **Frontend (the app)** | http://localhost:8080 |
| Backend API | http://localhost:8000 |
| API docs (Swagger UI) | http://localhost:8000/docs |
| PostgreSQL | `localhost:5432` (user/db `ffg`) |

### Seeded logins (password: `password123`)

| Email | Role | Lands on |
|---|---|---|
| `admin@example.com` | admin | `/admin` dashboard |
| `reviewer@example.com` | reviewer | `/review` screening portal |
| `vikram.singh@example.com` | mentor | `/mentor` dashboard |
| `aarav.mehta@example.com` | mentee | `/mentee` dashboard |

### `setup.sh` commands

| Command | Does |
|---|---|
| `./setup.sh` | Build + start in the foreground (Ctrl-C to stop) |
| `./setup.sh up` | Build + start detached (background) |
| `./setup.sh down` | Stop and remove containers |
| `./setup.sh reset` | Stop and **delete the database volume** (fresh seed next start) |
| `./setup.sh logs` | Follow logs |

> Prefer raw Compose? `docker compose up --build` does the same as `./setup.sh`.

### Connect to the database from the PostgreSQL extension

Once the Docker stack is running, the database is exposed on your host at `localhost:5432`.
Use these values in your PostgreSQL extension or any SQL client:

- **Host:** `localhost`
- **Port:** `5432`
- **User:** `ffg`
- **Password:** `ffg_password`
- **Database:** `ffg`
- **SSL:** disabled

Connection string:

```text
postgresql://ffg:ffg_password@localhost:5432/ffg
```

If you are using the VS Code PostgreSQL extension, create a new connection with
those values and connect to the `ffg` database.

---

## 2. How the pieces connect

```
  Browser
    │  http://localhost:8080
    ▼
┌─────────────┐   proxies /api, /auth,     ┌─────────────┐   asyncpg      ┌────────────┐
│  frontend   │   /dashboard, /health  ──▶ │   backend   │  ──────────▶   │  db        │
│ nginx :80   │                            │ FastAPI:8000│                │ postgres   │
│ (SPA build) │ ◀── static assets          │             │ ◀── SQL        │ :5432      │
└─────────────┘                            └─────────────┘                └────────────┘
```

- **Frontend → Backend.** The React app makes **same-origin** requests
  (`VITE_API_BASE` is empty). nginx (`frontend/nginx.conf`) reverse-proxies the
  `/api`, `/auth`, `/dashboard`, and `/health` prefixes to the `backend` service.
  Because it's same-origin, **no CORS setup is needed** in the browser.
- **Backend → Database.** The backend reads `DATABASE_URL` (set by Compose to
  `postgresql+asyncpg://ffg:...@db:5432/ffg`) and talks to Postgres over async
  SQLAlchemy. On startup it runs `app/scripts/prestart.py`, which creates tables
  and seeds demo data **only if the DB is empty** (restarts keep your data).
- **Service discovery.** Compose puts all three containers on one network where
  they reach each other by service name (`db`, `backend`, `frontend`).
  `depends_on` + a Postgres healthcheck guarantee the DB is ready before the
  backend connects.

### Configuration (all optional)

Copy `env.example` to `.env` to override the Compose defaults:

| Variable | Default | Used by |
|---|---|---|
| `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB` | `ffg` / `ffg_password` / `ffg` | db + backend connection string |
| `JWT_SECRET` | `change-me-...` | backend token signing |
| `CORS_ORIGINS` | `*` | backend CORS (relevant only for cross-origin/dev) |

---

## 3. Local development (without Docker)

Useful for hot-reload while coding. Runs against SQLite by default — no Postgres needed.

### Backend

```bash
cd fastapi_backend
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python -m app.scripts.seed        # create + seed the SQLite dev DB (ffg.db)
uvicorn app.main:app --reload     # http://localhost:8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev                       # http://localhost:5173
```

The Vite dev server (`frontend/vite.config.js`) proxies `/api`, `/auth`,
`/dashboard`, and `/health` to `http://localhost:8000`. Point it elsewhere with
`BACKEND_URL=http://host:port npm run dev`.

---

## 4. Frontend ↔ Backend endpoint map

| UI | Backend endpoint(s) |
|---|---|
| Login (`/login`) | `POST /auth/login` (form-encoded) → `GET /auth/me` |
| Student apply (`/apply/student`) | `POST /api/users` → `/api/mentee-profiles` → `/api/applications` → `/api/applications/{id}/submit` |
| Mentor apply (`/apply/mentor`) | `POST /api/users` → `/api/mentor-profiles` |
| Admin (`/admin`) | `GET /api/users`, `/api/pairs`, `/dashboard/emp`, `/api/resources` CRUD |
| Admin → Applications | `GET /api/applications/review-board`, `POST /api/cohorts/{id}/scoring/run`, `POST /api/applications/{id}/reviewers` \| `/system-decision` \| `/admin-decision`, `GET /api/notifications` |
| Reviewer (`/review`) | `GET /api/reviews/assigned`, `POST /api/reviews/{id}/submit` |
| Resources (`/resources`) | `GET /api/public/resources` |

Full, interactive API reference: **http://localhost:8000/docs**.

### Mentee selection pipeline (Phase 1)

The admin **Applications** tab runs the funnel from the programme workflow:
**in-app application** (cohort-configured form) → **disadvantage scoring**
(automated) → **profile screening** by assigned reviewers (Select/Reject) →
**system decision** (score vs. the cohort's `selection_threshold` + reviewer
majority; flags reconciliation on disagreement) → **admin decision**
(Select / Waitlist / Reject). Each admin decision writes a stubbed
**notification** (visible under the Notifications tab) — swap in real email
later without touching callers.

> **Existing database?** The new columns/tables ship as Alembic migrations.
> Run `alembic upgrade head` in `fastapi_backend`, or `./setup.sh reset` for a
> fresh seeded volume. New/empty databases are created automatically on boot.

### Programme lifecycle (Phases 2–6)

Beyond selection, the platform now models the full programme workflow:

- **Onboarding (declarations).** Selected mentors/mentees sign a declaration
  (`POST /auth/declaration`) to formally join; mentor sign-up captures a
  "studied abroad" flag. Dashboards prompt until signed.
- **Mapping.** Admin **Mapping** tab pairs mentees with mentors by discipline
  (same-discipline mentors with spare capacity are suggested) and assigns each
  mentee a **one-on-one** or **cohort** mentorship type (`/api/mapping/*`).
- **Document review portal.** Mentees upload application docs by link; admins
  assign a mentor reviewer; mentors return written feedback (`/api/documents/*`).
- **Workshops & support.** Admins schedule workshops (with YouTube recording
  links); mentors sign up as panellists; mentors/mentees opt into the English
  Language Support Programme (`/api/workshops/*`, `POST /auth/english-support`).
- **Close of programme.** Mentees submit feedback + offer-tracking records and
  can return as a mentor (alumni) (`/api/closeout/*`). Admin **Close-out** tab
  reviews submissions.

Role-based access is enforced throughout: mentee/mentor/reviewer endpoints sit
outside the admin guard with their own per-endpoint role checks, while all other
`/api/*` management routes remain admin-only.

---

## 5. Troubleshooting

- **Port already in use** (`8080`, `8000`, or `5432`): stop whatever holds the
  port, or edit the `ports:` mappings in `docker-compose.yml`.
- **Backend can't reach the DB:** the healthcheck should prevent this; if you
  see connection errors on first boot, `./setup.sh down && ./setup.sh up`.
- **Want a clean database:** `./setup.sh reset` deletes the volume so the next
  start re-seeds from scratch.
- **Frontend shows old data after code changes:** rebuild with
  `docker compose up --build` (or `./setup.sh up`).
