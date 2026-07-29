"""Phase 3 — mentee-mentor mapping: board, mentorship type, pairing."""
import pytest

from tests.conftest import register_and_login

pytestmark = pytest.mark.asyncio


async def _uid(client, admin, role, search):
    users = (await client.get("/api/users", params={"role": role, "search": search}, headers=admin)).json()
    return users["items"][0]["id"]


async def test_mapping_flow(client):
    admin = {"Authorization": await register_and_login(client, "admin@example.com", "admin")}
    cohort = (await client.post(
        "/api/cohorts",
        json={"name": "Map", "program": "P", "start_date": "2026-01-01",
              "end_date": "2026-06-01", "status": "active", "max_mentees": 5},
        headers=admin,
    )).json()

    await client.post("/api/public/apply/mentor", json={
        "full_name": "Disc Mentor", "email": "dm@example.com", "discipline": "CS"})
    await client.post("/api/public/apply/student", json={
        "full_name": "Map Mentee", "email": "mm@example.com", "cohort_id": cohort["id"]})

    mentor_id = await _uid(client, admin, "mentor", "dm")
    mentee_id = await _uid(client, admin, "mentee", "mm")

    board = (await client.get("/api/mapping/board", params={"cohort_id": cohort["id"]}, headers=admin)).json()
    assert len(board["mentees"]) == 1
    assert any(mt["user_id"] == mentor_id for mt in board["mentors"])

    # Assign a mentorship type.
    r = await client.post("/api/mapping/mentee-type",
                          json={"mentee_id": mentee_id, "mentorship_type": "cohort"}, headers=admin)
    assert r.status_code == 200, r.text

    # Pair one-on-one.
    r = await client.post("/api/mapping/pair",
                          json={"mentor_id": mentor_id, "mentee_id": mentee_id, "cohort_id": cohort["id"]},
                          headers=admin)
    assert r.status_code == 201, r.text

    board = (await client.get("/api/mapping/board", params={"cohort_id": cohort["id"]}, headers=admin)).json()
    mentee = board["mentees"][0]
    assert mentee["current_mentor_name"] == "Disc Mentor"
    assert mentee["mentorship_type"] == "one_on_one"  # pairing forces one-on-one

    pairs = (await client.get("/api/pairs", headers=admin)).json()
    assert len(pairs) == 1


async def test_mapping_requires_admin(client):
    rtok = {"Authorization": await register_and_login(client, "m@example.com", "mentee")}
    assert (await client.get("/api/mapping/board", headers=rtok)).status_code == 403
