"""Engine + workflow + dashboard tests (the fixed business logic)."""
import pytest


async def _make_cohort(client):
    resp = await client.post(
        "/api/cohorts",
        json={
            "name": "Engine Cohort", "program": "SWE", "start_date": "2026-01-01",
            "end_date": "2026-06-01", "status": "active", "max_mentees": 20,
        },
    )
    return resp.json()["id"]


async def _make_user(client, email, role):
    resp = await client.post(
        "/api/users",
        json={"email": email, "full_name": email.split("@")[0], "role": role},
    )
    return resp.json()["id"]


async def test_scoring_engine_uses_scoring_logic(admin_client):
    client = admin_client
    cid = await _make_cohort(client)
    uid = await _make_user(client, "applicant@example.com", "mentee")

    # Rule: award weight 5 when years_experience >= 2.
    await client.post(
        "/api/scoring-rules",
        json={
            "cohort_id": cid,
            "field_name": "years_experience",
            "weight": 5.0,
            "scoring_logic": {
                "field": "years_experience", "operator": ">=", "value": 2
            },
        },
    )
    app_resp = await client.post(
        "/api/applications",
        json={
            "user_id": uid, "cohort_id": cid, "status": "submitted",
            "answers": {"years_experience": 3},
        },
    )
    app_id = app_resp.json()["id"]

    resp = await client.post(f"/api/cohorts/{cid}/scoring/run")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["applications_processed"] == 1
    assert body["scores"][0]["score"] == 5.0

    got = await client.get(f"/api/applications/{app_id}")
    assert got.json()["final_score"] == 5.0
    assert got.json()["status"] == "scored"


async def test_matching_engine_generates_pairs(admin_client):
    client = admin_client
    cid = await _make_cohort(client)
    mentor_uid = await _make_user(client, "m@example.com", "mentor")
    mentee_uid = await _make_user(client, "e@example.com", "mentee")

    await client.post(
        "/api/mentor-profiles",
        json={"user_id": mentor_uid, "expertise": ["python"], "max_mentees": 3},
    )
    await client.post(
        "/api/mentee-profiles",
        json={"user_id": mentee_uid, "course": "python", "cohort_id": cid},
    )
    await client.post(
        "/api/matching-rules",
        json={
            "cohort_id": cid,
            "criteria_name": "expertise-course",
            "weight": 1.0,
            "match_logic": {
                "type": "array_intersection",
                "mentor_field": "expertise",
                "mentee_field": "course",
            },
        },
    )

    resp = await client.post(f"/api/cohorts/{cid}/matching/run")
    assert resp.status_code == 200, resp.text
    assert resp.json()["pairs_generated"] == 1

    pairs = (await client.get("/api/pairs")).json()
    assert len(pairs) == 1
    assert pairs[0]["match_score"] == 100.0


async def test_application_submit_and_review(admin_client):
    client = admin_client
    cid = await _make_cohort(client)
    uid = await _make_user(client, "a2@example.com", "mentee")

    # Required field present -> submit succeeds.
    await client.post(
        "/api/form-configs",
        json={
            "cohort_id": cid, "field_name": "essay", "field_type": "textarea",
            "is_required": True,
        },
    )
    app_id = (
        await client.post(
            "/api/applications",
            json={
                "user_id": uid, "cohort_id": cid, "status": "draft",
                "answers": {"essay": "hello"},
            },
        )
    ).json()["id"]

    resp = await client.post(f"/api/applications/{app_id}/submit")
    assert resp.status_code == 200, resp.text
    assert resp.json()["status"] == "submitted"

    resp = await client.post(
        f"/api/applications/{app_id}/review", json={"approve": True}
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "accepted"  # fixed from Django's 'approved'


async def test_submit_missing_required_field_fails(admin_client):
    client = admin_client
    cid = await _make_cohort(client)
    uid = await _make_user(client, "a3@example.com", "mentee")
    await client.post(
        "/api/form-configs",
        json={
            "cohort_id": cid, "field_name": "cv", "field_type": "file_upload",
            "is_required": True,
        },
    )
    app_id = (
        await client.post(
            "/api/applications",
            json={"user_id": uid, "cohort_id": cid, "status": "draft", "answers": {}},
        )
    ).json()["id"]

    resp = await client.post(f"/api/applications/{app_id}/submit")
    assert resp.status_code == 400


async def test_dashboards(admin_client):
    client = admin_client
    await _make_cohort(client)
    for path in ("/dashboard/emp", "/dashboard/mentor", "/dashboard/mentee"):
        resp = await client.get(path)
        assert resp.status_code == 200, resp.text
    emp = (await client.get("/dashboard/emp")).json()
    assert "platform_summary" in emp


async def test_dashboards_are_scoped_to_the_user(client):
    from tests.conftest import register_and_login

    admin = {"Authorization": await register_and_login(client, "admin@example.com", "admin")}

    async def reg(email, role):
        r = await client.post(
            "/auth/register",
            json={"email": email, "full_name": email.split("@")[0],
                  "password": "password123", "role": role},
        )
        return r.json()["id"]

    mentor_id = await reg("mentor@example.com", "mentor")
    mentee_id = await reg("mentee@example.com", "mentee")
    await reg("other.mentor@example.com", "mentor")

    cohort = (await client.post(
        "/api/cohorts",
        json={"name": "C", "program": "P", "start_date": "2026-01-01",
              "end_date": "2026-06-01", "status": "active", "max_mentees": 5},
        headers=admin,
    )).json()
    await client.post(
        "/api/pairs",
        json={"mentor_id": mentor_id, "mentee_id": mentee_id,
              "cohort_id": cohort["id"], "status": "active"},
        headers=admin,
    )

    async def token(email):
        r = await client.post("/auth/login", data={"username": email, "password": "password123"})
        return {"Authorization": f"Bearer {r.json()['access_token']}"}

    # The paired mentor sees exactly their one mentee.
    md = (await client.get("/dashboard/mentor", headers=await token("mentor@example.com"))).json()
    assert md["engagement_metrics"]["assigned_mentees"] == 1
    assert md["mentees"][0]["name"] == "mentee"

    # A different mentor with no pairings sees none.
    other = (await client.get("/dashboard/mentor", headers=await token("other.mentor@example.com"))).json()
    assert other["engagement_metrics"]["assigned_mentees"] == 0

    # The mentee sees their assigned mentor.
    ed = (await client.get("/dashboard/mentee", headers=await token("mentee@example.com"))).json()
    assert ed["my_program_status"]["has_active_match"] is True
    assert ed["mentor"]["name"] == "mentor"
