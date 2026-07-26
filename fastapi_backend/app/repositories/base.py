"""Generic async CRUD repository."""
import uuid
from typing import Generic, TypeVar

from sqlalchemy import delete as sa_delete
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Reusable async CRUD operations for a single ORM model."""

    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, obj_id: uuid.UUID) -> ModelType | None:
        return await db.get(self.model, obj_id)

    async def list(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def count(self, db: AsyncSession) -> int:
        result = await db.execute(select(func.count()).select_from(self.model))
        return int(result.scalar_one())

    async def create(self, db: AsyncSession, data: dict) -> ModelType:
        obj = self.model(**data)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def update(
        self, db: AsyncSession, obj: ModelType, data: dict
    ) -> ModelType:
        for key, value in data.items():
            setattr(obj, key, value)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def delete(self, db: AsyncSession, obj: ModelType) -> None:
        await db.delete(obj)
        await db.commit()

    async def delete_all(self, db: AsyncSession) -> None:
        await db.execute(sa_delete(self.model))
        await db.commit()
