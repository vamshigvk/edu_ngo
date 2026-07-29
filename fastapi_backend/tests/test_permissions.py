"""Authorization enforcement + the public application flow."""
import pytest

from tests.conftest import register_and_login

pytestmark = pytest.mark.asyncio


async def test_api_requires_token(client):
    # No Authorization header -> 401 across the management surface.
    for path in ("/api/users", "/api/cohorts", "/api/pairs", "/api/resources"):
        resp = await client.get(path)
        assert resp.status_code == 401, f"{path} -> {resp.status_code}"


async def test_dashboard_emp_requires_admin(client):
    # A mentee token must not reach the admin dashboard (403), nor the anon user (401).
    assert (await client.get("/dashboard/emp")).status_code == 401

    header = await register_and_login(client, "mentee@example.com", "mentee")
    resp = await client.get("/dashboard/emp", headers={"Authorization": header})
    assert resp.status_code == 403

    # ...but the mentee CAN see the mentee portal.
    resp = await client.get("/dashboard/mentee", headers={"Authorization": header})
    assert resp.status_code == 200


async def test_admin_can_list_users(client):
    header = await register_and_login(client, "admin2@example.com", "admin")
    resp = await client.get("/api/users", headers={"Authorization": header})
    assert resp.status_code == 200
    body = resp.json()
    assert "items" in body and "total" in body
    assert body["total"] >= 1


async def test_user_search_and_role_filter(client):
    header = await register_and_login(client, "admin3@example.com", "admin")
    auth = {"Authorization": header}
    await client.post(
        "/api/users",
        json={"email": "grace.hopper@example.com", "full_name": "Grace Hopper",
              "role": "mentor"},
        headers=auth,
    )
    resp = await client.get(
        "/api/users", params={"role": "mentor", "search": "grace"}, headers=auth
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["total"] == 1
    assert body["items"][0]["email"] == "grace.hopper@example.com"


async def test_public_apply_flow_is_open(client):
    # An active cohort must exist for the student flow.
    admin = await register_and_login(client, "admin4@example.com", "admin")
    await client.post(
        "/api/cohorts",
        json={"name": "C", "program": "P", "start_date": "2026-01-01",
              "end_date": "2026-06-01", "status": "active", "max_mentees": 5},
        headers={"Authorization": admin},
    )

    # No token needed for the public endpoints.
    resp = await client.get("/api/public/cohorts")
    assert resp.status_code == 200 and len(resp.json()) == 1

    resp = await client.post(
        "/api/public/apply/mentor",
        json={"full_name": "Mentor One", "email": "mentor1@example.com",
              "country": "India", "about": "hi"},
    )
    assert resp.status_code == 201, resp.text

    resp = await client.post(
        "/api/public/apply/student",
        json={"full_name": "Student One", "email": "student1@example.com",
              "country": "India", "education": "bachelors", "rural_urban": "rural"},
    )
    assert resp.status_code == 201, resp.text


async def test_public_apply_cannot_create_admin(client):
    # The public payload has no role field; the server pins mentor/mentee.
    resp = await client.post(
        "/api/public/apply/mentor",
        json={"full_name": "X", "email": "x@example.com", "role": "admin"},
    )
    assert resp.status_code == 201
    user_id = resp.json()["user_id"]

    admin = await register_and_login(client, "admin5@example.com", "admin")
    got = await client.get(
        f"/api/users/{user_id}", headers={"Authorization": admin}
    )
    assert got.json()["role"] == "mentor"
