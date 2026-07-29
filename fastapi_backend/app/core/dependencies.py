"""Reusable FastAPI dependencies: DB session, current user, role guards.

The role/ownership logic ports Django's ``IsCohortManagerOrOwner`` permission:
admins have full access; other roles are constrained by ``require_roles``.
"""
import uuid
from collections.abc import Sequence

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import AuthError, PermissionDeniedError
from app.core.security import decode_access_token
from app.models.enums import UserRole
from app.models.user import User

# tokenUrl drives the Swagger "Authorize" button (OAuth2 password flow).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


async def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not token:
        raise AuthError("Not authenticated.")
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
    except jwt.PyJWTError:
        raise AuthError("Invalid or expired token.")
    if not user_id:
        raise AuthError("Invalid token payload.")

    user = await db.get(User, uuid.UUID(user_id))
    if user is None or not user.is_active:
        raise AuthError("User not found or inactive.")
    return user


def require_roles(*roles: UserRole):
    """Dependency factory enforcing that the current user holds one of ``roles``.

    Admins always pass.
    """
    allowed: Sequence[str] = [r.value for r in roles]

    async def _guard(user: User = Depends(get_current_user)) -> User:
        if user.role == UserRole.ADMIN:
            return user
        if user.role not in allowed:
            raise PermissionDeniedError(
                "You do not have permission to perform this action."
            )
        return user

    return _guard


# Convenience guards.
require_admin = require_roles(UserRole.ADMIN)
require_reviewer = require_roles(UserRole.REVIEWER)  # reviewer or admin
