"""Phase 2 — onboarding: declarations and mentor study-abroad flag."""
import pytest

from tests.conftest import register_and_login

pytestmark = pytest.mark.asyncio


async def test_declaration_signing(client):
    header = await register_and_login(client, "mentee@example.com", "mentee")
    auth = {"Authorization": header}

    me = (await client.get("/auth/me", headers=auth)).json()
    assert me["declaration_signed_at"] is None

    signed = await client.post("/auth/declaration", headers=auth)
    assert signed.status_code == 200, signed.text
    assert signed.json()["declaration_signed_at"] is not None

    me = (await client.get("/auth/me", headers=auth)).json()
    assert me["declaration_signed_at"] is not None


async def test_declaration_requires_auth(client):
    assert (await client.post("/auth/declaration")).status_code == 401


async def test_mentor_apply_captures_study_abroad(client):
    r = await client.post(
        "/api/public/apply/mentor",
        json={"full_name": "Abroad Mentor", "email": "abroad@example.com",
              "discipline": "Computer Science", "studied_abroad": True, "about": "hi"},
    )
    assert r.status_code == 201, r.text

    admin = {"Authorization": await register_and_login(client, "admin@example.com", "admin")}
    users = (await client.get("/api/users", params={"role": "mentor", "search": "abroad"}, headers=admin)).json()
    profile = users["items"][0]["mentor_profile"]
    assert profile["studied_abroad"] is True
    assert profile["discipline"] == "Computer Science"
