"""Auth flow tests: register, login, /me, duplicate email."""
import pytest

from tests.conftest import register_and_login


async def test_health(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


async def test_register_and_login_and_me(client):
    resp = await client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "full_name": "Jane Doe",
            "password": "password123",
            "role": "mentor",
        },
    )
    assert resp.status_code == 201
    assert resp.json()["email"] == "user@example.com"

    resp = await client.post(
        "/auth/login", data={"username": "user@example.com", "password": "password123"}
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    assert token

    resp = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["full_name"] == "Jane Doe"


async def test_duplicate_email_conflicts(client):
    payload = {
        "email": "dup@example.com",
        "full_name": "Dup",
        "password": "password123",
    }
    assert (await client.post("/auth/register", json=payload)).status_code == 201
    resp = await client.post("/auth/register", json=payload)
    assert resp.status_code == 409


async def test_bad_login(client):
    resp = await client.post(
        "/auth/login", data={"username": "nope@example.com", "password": "x"}
    )
    assert resp.status_code == 401


async def test_me_requires_token(client):
    resp = await client.get("/auth/me")
    assert resp.status_code == 401
