"""Pytest fixtures: isolated in-memory SQLite app + async HTTP client."""
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.database import Base, get_db
from app.main import create_app
from app.models import *  # noqa: F401,F403  (register models on metadata)

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def client():
    # A single shared in-memory connection for the whole test.
    engine = create_async_engine(
        TEST_DB_URL, connect_args={"check_same_thread": False}
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    TestSession = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

    async def _get_db_override():
        async with TestSession() as session:
            yield session

    app = create_app()
    app.dependency_overrides[get_db] = _get_db_override

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    await engine.dispose()


async def register_and_login(client: AsyncClient, email: str, role: str = "admin") -> str:
    """Helper: register a user and return a bearer auth header value."""
    await client.post(
        "/auth/register",
        json={
            "email": email,
            "full_name": "Test User",
            "password": "password123",
            "role": role,
        },
    )
    resp = await client.post(
        "/auth/login", data={"username": email, "password": "password123"}
    )
    token = resp.json()["access_token"]
    return f"Bearer {token}"


@pytest_asyncio.fixture
async def admin_client(client: AsyncClient):
    """The shared client, pre-authenticated as an admin.

    Every ``/api`` management endpoint now requires an admin token, so CRUD and
    workflow tests use this fixture instead of the anonymous ``client``.
    """
    header = await register_and_login(client, "admin@example.com", "admin")
    client.headers.update({"Authorization": header})
    return client
