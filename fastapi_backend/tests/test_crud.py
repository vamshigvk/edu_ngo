"""CRUD coverage for representative resources."""


async def test_cohort_crud(admin_client):
    client = admin_client
    payload = {
        "name": "Cohort A",
        "program": "SWE",
        "start_date": "2026-01-01",
        "end_date": "2026-06-01",
        "status": "active",
        "max_mentees": 10,
    }
    resp = await client.post("/api/cohorts", json=payload)
    assert resp.status_code == 201, resp.text
    cohort = resp.json()
    cid = cohort["id"]

    resp = await client.get("/api/cohorts")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    resp = await client.get(f"/api/cohorts/{cid}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Cohort A"

    resp = await client.patch(f"/api/cohorts/{cid}", json={"name": "Cohort B"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Cohort B"

    resp = await client.delete(f"/api/cohorts/{cid}")
    assert resp.status_code == 204

    resp = await client.get(f"/api/cohorts/{cid}")
    assert resp.status_code == 404


async def test_resource_crud(admin_client):
    client = admin_client
    payload = {"title": "Guide", "type": "guide", "url": "https://x.example/guide"}
    resp = await client.post("/api/resources", json=payload)
    assert resp.status_code == 201, resp.text
    rid = resp.json()["id"]

    resp = await client.get(f"/api/resources/{rid}")
    assert resp.status_code == 200
    assert resp.json()["type"] == "guide"


async def test_user_derived_name_on_pair(admin_client):
    client = admin_client
    # Two users -> a pair -> derived mentor_name/mentee_name populated.
    async def make_user(email, role):
        r = await client.post(
            "/api/users",
            json={"email": email, "full_name": email.split("@")[0], "role": role},
        )
        assert r.status_code == 201, r.text
        return r.json()["id"]

    cohort = (
        await client.post(
            "/api/cohorts",
            json={
                "name": "C", "program": "P", "start_date": "2026-01-01",
                "end_date": "2026-06-01", "status": "active", "max_mentees": 5,
            },
        )
    ).json()
    mentor_id = await make_user("mentor@example.com", "mentor")
    mentee_id = await make_user("mentee@example.com", "mentee")

    resp = await client.post(
        "/api/pairs",
        json={
            "mentor_id": mentor_id,
            "mentee_id": mentee_id,
            "cohort_id": cohort["id"],
        },
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["mentor_name"] == "mentor"
    assert body["mentee_name"] == "mentee"
