import uuid
from types import SimpleNamespace

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.database import Base
from app.models import User
from app.models.enums import DecisionOutcome, UserRole
from app.services import notification_service


@pytest.mark.asyncio
async def test_log_decision_sends_email_when_smtp_is_configured(monkeypatch):
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)
    async with session_factory() as session:
        user = User(
            email="recipient@example.com",
            full_name="Recipient User",
            role=UserRole.MENTOR,
            hashed_password="hashed",
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        sent_messages = []

        class FakeSMTP:
            def __init__(self, host, port, timeout=None):
                self.host = host
                self.port = port
                self.timeout = timeout

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def starttls(self):
                sent_messages.append(("starttls", self.host, self.port))

            def login(self, username, password):
                sent_messages.append(("login", username, password))

            def send_message(self, message):
                sent_messages.append(("send", message["To"], message["Subject"]))

        monkeypatch.setattr(notification_service.smtplib, "SMTP", FakeSMTP)
        monkeypatch.setattr(
            notification_service,
            "settings",
            SimpleNamespace(
                smtp_host="smtp.example.com",
                smtp_port=587,
                smtp_username="user",
                smtp_password="secret",
                smtp_from_email="from@example.com",
                smtp_use_tls=True,
                smtp_use_ssl=False,
                smtp_timeout_seconds=10,
            ),
        )

        entry = await notification_service.log_decision(
            session,
            decision=DecisionOutcome.SELECT,
            user_id=user.id,
            application_id=uuid.uuid4(),
        )
        await session.commit()

        assert entry.status == "sent"
        assert any(message[0] == "send" for message in sent_messages)
        assert any(
            message[0] == "send" and message[1] == "recipient@example.com"
            for message in sent_messages
        )
