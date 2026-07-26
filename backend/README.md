# FFG Mentorship Platform Backend

Backend service for the FFG mentorship platform built using Django and Django REST Framework.

The application manages:
- Cohorts
- Users
- Mentor and mentee profiles
- Applications
- Matching workflows
- Check-ins
- Resources
- Dashboard data

## Tech Stack

- Python 3.10+
- Django 6.0.7
- Django REST Framework
- SQLite (local development)

## Project Structure

```
ffg/
├── manage.py
├── db.sqlite3
├── openapi.yaml
├── requirements.txt
├── demoapp/
│   ├── settings.py
│   └── urls.py
└── api/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── services.py
    ├── permissions.py
    ├── migrations/
    ├── management/
    │   └── commands/
    │       └── seed_data.py
    └── templates/
        └── dashboard.html
```

## Setup

Clone the repository:

```bash
git clone <repository-url>
cd ffg
```

Create and activate virtual environment:

```bash
python -m venv .venv

source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Database Setup

Run migrations:

```bash
python manage.py migrate
```

Create admin user:

```bash
python manage.py createsuperuser
```

(Optional) Load sample data:

```bash
python manage.py seed_data
```

## Run Application

Start Django server:

```bash
python manage.py runserver
```

Application will be available at:

```
http://127.0.0.1:8000/
```

## Useful URLs

Admin panel:

```
http://127.0.0.1:8000/admin/
```

API root:

```
http://127.0.0.1:8000/api/
```

Dashboard routes:

```
/dashboard/emp/
/dashboard/mentor/
/dashboard/mentee/
```

API details and request/response formats are documented in:

```
openapi.yaml
```

## Validation

Run:

```bash
python manage.py check
```

Expected:

```
System check identified no issues
```

Check migration status:

```bash
python manage.py makemigrations --check
```

Expected:

```
No changes detected
```

## Current Status

Completed:
- Database models and migrations
- REST API structure
- CRUD endpoints
- Matching workflow
- Application submit/review workflow
- Dashboard endpoints
- Seed data support

Pending:
- Authentication integration (JWT)
- Final RBAC hardening
- Scoring engine implementation

## Developer Handoff Notes

The backend is ready for integration with authentication and frontend systems.

For API consumers, use `openapi.yaml` as the source of truth for available endpoints and payload formats.