"""User service — CRUD plus password hashing and email lookup."""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.core.security import hash_password
from app.models.user import User


class UserService:
    async def get_or_404(self, db: AsyncSession, user_id: uuid.UUID) -> User:
        user = await db.get(User, user_id)
        if user is None:
            raise NotFoundError(f"User '{user_id}' not found.")
        return user

    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def list(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> list[User]:
        result = await db.execute(select(User).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, data: dict) -> User:
        password = data.pop("password", None)
        if await self.get_by_email(db, data["email"]):
            raise ConflictError(f"A user with email '{data['email']}' already exists.")
        if password:
            data["hashed_password"] = hash_password(password)
        user = User(**data)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def update(
        self, db: AsyncSession, user_id: uuid.UUID, data: dict
    ) -> User:
        user = await self.get_or_404(db, user_id)
        password = data.pop("password", None)
        if password:
            user.hashed_password = hash_password(password)
        if "email" in data and data["email"] != user.email:
            existing = await self.get_by_email(db, data["email"])
            if existing and existing.id != user.id:
                raise ConflictError(
                    f"A user with email '{data['email']}' already exists."
                )
        for key, value in data.items():
            setattr(user, key, value)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def delete(self, db: AsyncSession, user_id: uuid.UUID) -> None:
        user = await self.get_or_404(db, user_id)
        await db.delete(user)
        await db.commit()


user_service = UserService()
