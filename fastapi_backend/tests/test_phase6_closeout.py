"""Phase 6 — close of programme: feedback, offers, alumni conversion."""
import pytest

from tests.conftest import register_and_login

pytestmark = pytest.mark.asyncio


async def test_feedback_and_offers(client):
    admin = {"Authorization": await register_and_login(client, "admin@example.com", "admin")}
    mentee = {"Authorization": await register_and_login(client, "mentee@example.com", "mentee")}

    assert (await client.post("/api/closeout/feedback",
                              json={"rating": 5, "comments": "great"}, headers=mentee)).status_code == 201
    assert (await client.post("/api/closeout/offers",
                              json={"university": "Oxford", "status": "admitted"}, headers=mentee)).status_code == 201

    fb = (await client.get("/api/closeout/feedback", headers=admin)).json()
    assert len(fb) == 1 and fb[0]["rating"] == 5
    offers = (await client.get("/api/closeout/offers", headers=admin)).json()
    assert offers[0]["university"] == "Oxford"

    # A mentee can't read the admin close-out lists.
    assert (await client.get("/api/closeout/feedback", headers=mentee)).status_code == 403


async def test_become_mentor(client):
    mentee_hdr = await register_and_login(client, "grad@example.com", "mentee")
    mentee = {"Authorization": mentee_hdr}

    r = await client.post("/api/closeout/become-mentor", headers=mentee)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["role"] == "mentor"
    assert body["is_alumni"] is True

    # Same token now authorizes the mentor dashboard (role read from DB).
    assert (await client.get("/dashboard/mentor", headers=mentee)).status_code == 200
    # ...and no longer the mentee-only close-out submission.
    assert (await client.post("/api/closeout/feedback", json={"rating": 3}, headers=mentee)).status_code == 403
