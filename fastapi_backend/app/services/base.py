"""Generic CRUD service built on top of BaseRepository."""
import uuid
from collections.abc import Callable
from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base
from app.core.exceptions import NotFoundError
from app.repositories.base import BaseRepository

ModelType = TypeVar("ModelType", bound=Base)


class CRUDService(Generic[ModelType]):
    """Reusable CRUD orchestration with not-found handling and optional enrichment.

    ``enrich`` is an optional callback that decorates a loaded ORM instance with
    non-mapped derived attributes (e.g. ``user_name``) before serialization.
    """

    def __init__(
        self,
        model: type[ModelType],
        *,
        enrich: Callable[[ModelType], None] | None = None,
    ):
        self.model = model
        self.repo = BaseRepository(model)
        self._enrich = enrich

    def _decorate(self, obj: ModelType | None) -> ModelType | None:
        if obj is not None and self._enrich is not None:
            self._enrich(obj)
        return obj

    async def get_or_404(self, db: AsyncSession, obj_id: uuid.UUID) -> ModelType:
        obj = await self.repo.get(db, obj_id)
        if obj is None:
            raise NotFoundError(f"{self.model.__name__} '{obj_id}' not found.")
        return self._decorate(obj)

    async def list(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        objs = await self.repo.list(db, skip=skip, limit=limit)
        for obj in objs:
            self._decorate(obj)
        return objs

    async def create(self, db: AsyncSession, data: dict) -> ModelType:
        obj = await self.repo.create(db, data)
        return self._decorate(obj)

    async def update(
        self, db: AsyncSession, obj_id: uuid.UUID, data: dict
    ) -> ModelType:
        obj = await self.get_or_404(db, obj_id)
        obj = await self.repo.update(db, obj, data)
        return self._decorate(obj)

    async def delete(self, db: AsyncSession, obj_id: uuid.UUID) -> None:
        obj = await self.get_or_404(db, obj_id)
        await self.repo.delete(db, obj)
