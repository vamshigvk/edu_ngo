"""Phase 5 — workshops, panellist sign-up, English-support opt-in."""
import pytest

from tests.conftest import register_and_login

pytestmark = pytest.mark.asyncio


async def test_workshops_and_signup(client):
    admin = {"Authorization": await register_and_login(client, "admin@example.com", "admin")}
    mentor = {"Authorization": await register_and_login(client, "mentor@example.com", "mentor")}
    mentee = {"Authorization": await register_and_login(client, "mentee@example.com", "mentee")}

    ws = await client.post("/api/workshops", json={
        "title": "SOP Clinic", "audience": "public",
        "recording_url": "https://youtu.be/x"}, headers=admin)
    assert ws.status_code == 201, ws.text
    wid = ws.json()["id"]

    # Any authenticated user can list; only admins create.
    assert (await client.get("/api/workshops", headers=mentee)).status_code == 200
    assert (await client.post("/api/workshops", json={"title": "x"}, headers=mentor)).status_code == 403

    # Mentor signs up as panellist; duplicate is rejected.
    assert (await client.post(f"/api/workshops/{wid}/signup", headers=mentor)).status_code == 200
    assert (await client.post(f"/api/workshops/{wid}/signup", headers=mentor)).status_code == 409
    # Mentees can't be panellists.
    assert (await client.post(f"/api/workshops/{wid}/signup", headers=mentee)).status_code == 403

    listing = (await client.get("/api/workshops", headers=admin)).json()
    assert listing[0]["signup_count"] == 1


async def test_english_support_opt_in(client):
    admin = {"Authorization": await register_and_login(client, "admin@example.com", "admin")}
    mentee = {"Authorization": await register_and_login(client, "mentee@example.com", "mentee")}
    mentee_id = (await client.get("/auth/me", headers=mentee)).json()["id"]

    # Give the mentee a profile, then opt in via the self-serve endpoint.
    await client.post("/api/mentee-profiles", json={"user_id": mentee_id}, headers=admin)
    r = await client.post("/auth/english-support", json={"opt_in": True}, headers=mentee)
    assert r.status_code == 200, r.text

    users = (await client.get("/api/users", params={"role": "mentee", "search": "mentee@"}, headers=admin)).json()
    assert users["items"][0]["mentee_profile"]["english_support_opt_in"] is True
