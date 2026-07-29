"""Phase 1 — mentee selection pipeline: scoring, screening, decisions, authЗ."""
import pytest

from tests.conftest import register_and_login

pytestmark = pytest.mark.asyncio


async def _cohort(client, admin, *, threshold=0.0):
    r = await client.post(
        "/api/cohorts",
        json={"name": "C", "program": "P", "start_date": "2026-01-01",
              "end_date": "2026-06-01", "status": "active", "max_mentees": 5,
              "selection_threshold": threshold},
        headers=admin,
    )
    assert r.status_code == 201, r.text
    return r.json()["id"]


async def test_in_app_form_drives_required_validation(client):
    admin = {"Authorization": await register_and_login(client, "admin@example.com", "admin")}
    cid = await _cohort(client, admin)
    # Admin defines a required field for the cohort's in-app form.
    await client.post(
        "/api/form-configs",
        json={"cohort_id": cid, "field_name": "essay", "field_type": "textarea",
              "is_required": True},
        headers=admin,
    )
    # Public form exposes it.
    form = (await client.get(f"/api/public/cohorts/{cid}/form")).json()
    assert any(f["field_name"] == "essay" and f["is_required"] for f in form)

    # Missing the required answer -> submission rejected during the public apply.
    r = await client.post(
        "/api/public/apply/student",
        json={"full_name": "No Essay", "email": "noessay@example.com",
              "cohort_id": cid, "answers": {}},
    )
    assert r.status_code == 400, r.text

    # Providing it succeeds.
    r = await client.post(
        "/api/public/apply/student",
        json={"full_name": "Has Essay", "email": "hasessay@example.com",
              "cohort_id": cid, "answers": {"essay": "hello"}},
    )
    assert r.status_code == 201, r.text


async def test_full_selection_funnel(client):
    admin = {"Authorization": await register_and_login(client, "admin@example.com", "admin")}
    cid = await _cohort(client, admin, threshold=5.0)

    # Disadvantage-scoring rule: +6 when years_experience >= 2 (clears threshold).
    await client.post(
        "/api/scoring-rules",
        json={"cohort_id": cid, "field_name": "years_experience", "weight": 6.0,
              "scoring_logic": {"field": "years_experience", "operator": ">=", "value": 2}},
        headers=admin,
    )
    await client.post(
        "/api/public/apply/student",
        json={"full_name": "Cand", "email": "cand@example.com", "cohort_id": cid,
              "answers": {"years_experience": 3}},
    )
    app_id = (await client.get("/api/applications/review-board", params={"cohort_id": cid}, headers=admin)).json()[0]["id"]

    # Run disadvantage scoring.
    await client.post(f"/api/cohorts/{cid}/scoring/run", headers=admin)
    board = (await client.get("/api/applications/review-board", headers=admin)).json()
    assert board[0]["disadvantage_score"] == 6.0

    # Two reviewers, both Select.
    r1 = await register_and_login(client, "rev1@example.com", "reviewer")
    r2 = await register_and_login(client, "rev2@example.com", "reviewer")
    rev1_id = (await client.get("/auth/me", headers={"Authorization": r1})).json()["id"]
    rev2_id = (await client.get("/auth/me", headers={"Authorization": r2})).json()["id"]

    assigned = await client.post(
        f"/api/applications/{app_id}/reviewers",
        json={"reviewer_ids": [rev1_id, rev2_id]}, headers=admin,
    )
    assert assigned.status_code == 201, assigned.text

    for tok in (r1, r2):
        mine = (await client.get("/api/reviews/assigned", headers={"Authorization": tok})).json()
        assert len(mine) == 1
        review_id = mine[0]["review_id"]
        sub = await client.post(
            f"/api/reviews/{review_id}/submit",
            json={"decision": "select", "description": "strong candidate"},
            headers={"Authorization": tok},
        )
        assert sub.status_code == 200, sub.text

    # System decision: meets threshold + reviewers select -> select, no reconciliation.
    sysd = (await client.post(f"/api/applications/{app_id}/system-decision", headers=admin)).json()
    assert sysd["system_decision"] == "select"
    assert sysd["reconciliation_needed"] is False

    # Admin confirms selection -> status accepted + a notification is logged.
    dec = await client.post(
        f"/api/applications/{app_id}/admin-decision",
        json={"decision": "select", "notes": "welcome"}, headers=admin,
    )
    assert dec.status_code == 200, dec.text
    assert dec.json()["status"] == "accepted"

    notes = (await client.get("/api/notifications", params={"application_id": app_id}, headers=admin)).json()
    assert len(notes) == 1 and notes[0]["template"] == "SELECTION"


async def test_reconciliation_flag_when_reviewers_disagree_with_system(client):
    admin = {"Authorization": await register_and_login(client, "admin@example.com", "admin")}
    cid = await _cohort(client, admin, threshold=100.0)  # nothing clears it
    await client.post(
        "/api/public/apply/student",
        json={"full_name": "Low", "email": "low@example.com", "cohort_id": cid},
    )
    app_id = (await client.get("/api/applications/review-board", headers=admin)).json()[0]["id"]

    rtok = await register_and_login(client, "rev@example.com", "reviewer")
    rid = (await client.get("/auth/me", headers={"Authorization": rtok})).json()["id"]
    await client.post(f"/api/applications/{app_id}/reviewers",
                      json={"reviewer_ids": [rid]}, headers=admin)
    review_id = (await client.get("/api/reviews/assigned", headers={"Authorization": rtok})).json()[0]["review_id"]
    await client.post(f"/api/reviews/{review_id}/submit",
                      json={"decision": "select"}, headers={"Authorization": rtok})

    sysd = (await client.post(f"/api/applications/{app_id}/system-decision", headers=admin)).json()
    # Below threshold -> system rejects, but reviewer said select -> reconcile.
    assert sysd["system_decision"] == "reject"
    assert sysd["reconciliation_needed"] is True


async def test_reviewer_authorization(client):
    admin = {"Authorization": await register_and_login(client, "admin@example.com", "admin")}
    cid = await _cohort(client, admin)
    await client.post(
        "/api/public/apply/student",
        json={"full_name": "A", "email": "a@example.com", "cohort_id": cid},
    )
    app_id = (await client.get("/api/applications/review-board", headers=admin)).json()[0]["id"]

    rtok = {"Authorization": await register_and_login(client, "rev@example.com", "reviewer")}
    # A reviewer may reach the reviewer surface...
    assert (await client.get("/api/reviews/assigned", headers=rtok)).status_code == 200
    # ...but NOT the admin management surface.
    assert (await client.get("/api/applications/review-board", headers=rtok)).status_code == 403
    assert (await client.post(f"/api/applications/{app_id}/admin-decision",
                              json={"decision": "select"}, headers=rtok)).status_code == 403

    # A reviewer cannot submit a review assigned to someone else.
    other = await register_and_login(client, "rev2@example.com", "reviewer")
    other_id = (await client.get("/auth/me", headers={"Authorization": other})).json()["id"]
    await client.post(f"/api/applications/{app_id}/reviewers",
                      json={"reviewer_ids": [other_id]}, headers=admin)
    other_review_id = (await client.get("/api/reviews/assigned", headers={"Authorization": other})).json()[0]["review_id"]
    forbidden = await client.post(
        f"/api/reviews/{other_review_id}/submit",
        json={"decision": "reject"}, headers=rtok,
    )
    assert forbidden.status_code == 403
