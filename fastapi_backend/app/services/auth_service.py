"""Authentication service — registration and credential verification."""
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthError, ConflictError
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.services.user_service import user_service


class AuthService:
    async def register(self, db: AsyncSession, payload: RegisterRequest) -> User:
        if await user_service.get_by_email(db, payload.email):
            raise ConflictError(
                f"A user with email '{payload.email}' already exists."
            )
        return await user_service.create(
            db,
            {
                "email": payload.email,
                "full_name": payload.full_name,
                "role": payload.role.value,
                "phone": payload.phone,
                "password": payload.password,
            },
        )

    async def authenticate(
        self, db: AsyncSession, email: str, password: str
    ) -> User:
        user = await user_service.get_by_email(db, email)
        if user is None or not verify_password(password, user.hashed_password):
            raise AuthError("Invalid email or password.")
        if not user.is_active:
            raise AuthError("This account is inactive.")
        return user

    def issue_token(self, user: User) -> str:
        return create_access_token(
            subject=str(user.id), extra_claims={"role": user.role, "email": user.email}
        )


auth_service = AuthService()
