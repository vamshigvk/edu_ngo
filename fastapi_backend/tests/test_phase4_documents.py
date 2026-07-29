"""Phase 4 — document review portal: upload, assign, review, authZ."""
import pytest

from tests.conftest import register_and_login

pytestmark = pytest.mark.asyncio


async def test_document_review_flow(client):
    admin = {"Authorization": await register_and_login(client, "admin@example.com", "admin")}
    mentee = {"Authorization": await register_and_login(client, "mentee@example.com", "mentee")}
    mentor_hdr = await register_and_login(client, "mentor@example.com", "mentor")
    mentor = {"Authorization": mentor_hdr}
    mentor_id = (await client.get("/auth/me", headers=mentor)).json()["id"]

    # Mentee uploads.
    up = await client.post("/api/documents", json={"title": "My SoP", "url": "https://x.example/sop", "doc_type": "sop"}, headers=mentee)
    assert up.status_code == 201, up.text
    doc_id = up.json()["id"]
    assert up.json()["status"] == "pending"

    # Admin assigns the mentor.
    asg = await client.post(f"/api/documents/{doc_id}/assign", json={"reviewer_id": mentor_id}, headers=admin)
    assert asg.status_code == 200 and asg.json()["status"] == "assigned"

    # Mentor sees it and reviews it.
    assigned = (await client.get("/api/documents/assigned", headers=mentor)).json()
    assert len(assigned) == 1 and assigned[0]["id"] == doc_id
    rev = await client.post(f"/api/documents/{doc_id}/review", json={"feedback": "Tighten the intro."}, headers=mentor)
    assert rev.status_code == 200 and rev.json()["status"] == "reviewed"

    # Mentee sees the feedback.
    mine = (await client.get("/api/documents/mine", headers=mentee)).json()
    assert mine[0]["feedback"] == "Tighten the intro."


async def test_document_authorization(client):
    mentee = {"Authorization": await register_and_login(client, "mentee@example.com", "mentee")}
    other_mentor = {"Authorization": await register_and_login(client, "m2@example.com", "mentor")}
    up = await client.post("/api/documents", json={"title": "Doc", "url": "https://x.example/d"}, headers=mentee)
    doc_id = up.json()["id"]

    # A mentee cannot list all documents (admin-only) or the reviewer queue.
    assert (await client.get("/api/documents", headers=mentee)).status_code == 403
    assert (await client.get("/api/documents/assigned", headers=mentee)).status_code == 403
    # A mentor who isn't the assigned reviewer cannot review it.
    r = await client.post(f"/api/documents/{doc_id}/review", json={"feedback": "x"}, headers=other_mentor)
    assert r.status_code == 403
