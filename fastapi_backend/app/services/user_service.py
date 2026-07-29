"""User service — CRUD plus password hashing and email lookup."""
import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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

    @staticmethod
    def _filtered(stmt, *, search: str | None, role: str | None):
        if role:
            stmt = stmt.where(User.role == role)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(
                or_(User.full_name.ilike(like), User.email.ilike(like))
            )
        return stmt

    async def list(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        search: str | None = None,
        role: str | None = None,
    ) -> list[User]:
        stmt = select(User).options(
            selectinload(User.mentor_profile),
            selectinload(User.mentee_profile),
        )
        stmt = self._filtered(stmt, search=search, role=role)
        stmt = stmt.order_by(User.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def count(
        self,
        db: AsyncSession,
        *,
        search: str | None = None,
        role: str | None = None,
    ) -> int:
        stmt = self._filtered(
            select(func.count()).select_from(User), search=search, role=role
        )
        return int((await db.execute(stmt)).scalar_one())

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
