# FFG Mentorship API — FastAPI Backend

Enterprise-grade FastAPI migration of the original Django/DRF backend
(`../django_backend`). Layered architecture (**controllers → services →
repositories → models**), async SQLAlchemy 2.0, Pydantic v2, JWT auth, Alembic
migrations, and auto-generated Swagger/OpenAPI docs.

## Architecture

```
app/
  main.py            # FastAPI app factory (routers, CORS, exception handlers)
  asgi.py            # ASGI entrypoint -> `application`
  openapi.py         # custom OpenAPI schema (JWT bearer security scheme, tags)
  core/              # config, database (async engine), security (JWT/bcrypt),
                     # dependencies (auth guards), exceptions
  models/            # SQLAlchemy 2.0 ORM models (+ shared enums, mixins)
  schemas/           # Pydantic v2 request/response contracts
  repositories/      # async CRUD data-access layer
  services/          # business logic (CRUD + scoring/matching/workflow/dashboard/auth)
  controllers/       # APIRouters (one per resource) + a generic CRUD factory
  api/router.py      # aggregates controllers into /api, /auth, /dashboard
  scripts/seed.py    # demo data seeder
alembic/             # migration environment
tests/               # pytest + httpx async tests
```

## Quickstart

Requires **Python 3.12** (matches the `python:3.12-slim` Docker image).

```bash
cd fastapi_backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp env.example .env          # adjust JWT_SECRET etc.

# Create schema (choose one):
alembic revision --autogenerate -m "initial"   # generate migration
alembic upgrade head                            # apply it
# (the seed script also auto-creates tables if you skip Alembic)

python -m app.scripts.seed   # optional demo data

uvicorn app.asgi:application --reload
```

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc:      http://127.0.0.1:8000/redoc
- Health:     http://127.0.0.1:8000/health

## Authentication

JWT via OAuth2 password flow:

1. `POST /auth/register` — create an account.
2. `POST /auth/login` — get a bearer token (form fields `username`=email, `password`).
3. In Swagger, click **Authorize** and paste the token.

Seeded users use password `password123`.

## Database

Defaults to SQLite (`sqlite+aiosqlite:///./ffg.db`). Switch to PostgreSQL by
setting `DATABASE_URL="postgresql+asyncpg://user:pass@host:5432/ffg"` in `.env` —
no code changes required.

## Endpoint map (parity with Django)

`/api/{cohorts,users,mentor-profiles,mentee-profiles,form-configs,applications,
scoring-rules,matching-rules,pairs,checkins,resources,permissions}` — full CRUD.

Custom actions & views:
- `POST /api/cohorts/{cohort_id}/scoring/run`
- `POST /api/cohorts/{cohort_id}/matching/run`
- `POST /api/applications/{application_id}/submit`
- `POST /api/applications/{application_id}/review`
- `GET  /dashboard/{emp,mentor,mentee}`
- `POST /auth/{register,login}`, `GET /auth/me` (new)

## Fixes applied during migration

The Django code contained bugs that were corrected here (see
`services/scoring_service.py`, `services/application_workflow.py`):
1. Scoring engine now actually runs (Django had a duplicate `CohortViewSet` shadowing it).
2. Scoring reads `scoring_logic` (the real field), not the non-existent `criteria`.
3. Application submit validates against real `ApplicationFormConfig` rows.
4. Review transitions to `accepted`/`rejected` (valid enum), not `approved`.

## Tests

```bash
pytest            # uses an isolated in-memory SQLite database
```
