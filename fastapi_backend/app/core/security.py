"""Password hashing (bcrypt) and JWT token utilities."""
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings


# --- Password hashing -------------------------------------------------------
def hash_password(plain_password: str) -> str:
    """Hash a plaintext password with bcrypt and return a utf-8 string."""
    pwd_bytes = plain_password.encode("utf-8")
    hashed = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str | None) -> bool:
    """Verify a plaintext password against a stored bcrypt hash."""
    if not hashed_password:
        return False
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except ValueError:
        return False


# --- JWT --------------------------------------------------------------------
def create_access_token(subject: str, extra_claims: dict | None = None) -> str:
    """Create a signed JWT access token for the given subject (user id)."""
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.access_token_expire_minutes)
    payload: dict = {"sub": subject, "iat": now, "exp": expire}
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT. Raises jwt.PyJWTError on failure."""
    return jwt.decode(
        token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
    )
