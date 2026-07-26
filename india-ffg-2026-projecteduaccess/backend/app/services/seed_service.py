import secrets
from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import SECRET_KEY
from app.core.logging import get_logger
from app.db.base import SessionLocal
from app.db.init_db import init_db
from app.models.notice import Notice
from app.models.user import User

logger = get_logger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_token() -> str:
    return secrets.token_urlsafe(24)


def create_access_token(user_id: int, role: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": now,
        "exp": now + timedelta(hours=8),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])


def seed_database() -> None:
    logger.info("Seeding database with default data")
    init_db()
    db: Session = SessionLocal()
    try:
        if db.query(User).filter(User.email == "admin@example.com").first() is None:
            user = User(
                email="admin@example.com",
                password_hash=hash_password("password123"),
                password_salt="",
                full_name="System Admin",
                role="admin",
                status="approved",
                verified_as="admin",
                token=None,
                created_at=datetime.utcnow().isoformat(),
            )
            db.add(user)
            db.flush()
            user.token = create_access_token(user.id, "admin")

        if db.query(User).filter(User.email == "mentor@example.com").first() is None:
            user = User(
                email="mentor@example.com",
                password_hash=hash_password("password123"),
                password_salt="",
                full_name="Asha Mentor",
                role="mentor",
                status="approved",
                verified_as="mentor",
                token=None,
                created_at=datetime.utcnow().isoformat(),
            )
            db.add(user)
            db.flush()
            user.token = create_access_token(user.id, "mentor")

        if db.query(User).filter(User.email == "mentee@example.com").first() is None:
            user = User(
                email="mentee@example.com",
                password_hash=hash_password("password123"),
                password_salt="",
                full_name="Kiran Mentee",
                role="mentee",
                status="approved",
                verified_as="mentee",
                token=None,
                created_at=datetime.utcnow().isoformat(),
            )
            db.add(user)
            db.flush()
            user.token = create_access_token(user.id, "mentee")

        if db.query(User).filter(User.email == "student@example.com").first() is None:
            user = User(
                email="student@example.com",
                password_hash=hash_password("password123"),
                password_salt="",
                full_name="Nisha Student",
                role="student",
                status="approved",
                verified_as="student",
                token=None,
                created_at=datetime.utcnow().isoformat(),
            )
            db.add(user)
            db.flush()
            user.token = create_access_token(user.id, "student")

        if db.query(Notice).count() == 0:
            db.add_all(
                [
                    Notice(title="Welcome", body="Please review your verification status on first login.", role="admin", created_at=datetime.utcnow().isoformat()),
                    Notice(title="Mentor update", body="New mentorship slots are available this week.", role="mentor", created_at=datetime.utcnow().isoformat()),
                    Notice(title="Mentee update", body="Your application review is in progress.", role="mentee", created_at=datetime.utcnow().isoformat()),
                    Notice(title="Student update", body="New learning resources have been published.", role="student", created_at=datetime.utcnow().isoformat()),
                ]
            )

        db.commit()
    finally:
        db.close()
