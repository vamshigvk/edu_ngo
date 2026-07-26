"""Factory that builds a standard CRUD APIRouter for a resource.

Keeps the 11 simple resources DRY: list / create / retrieve / update / delete
with consistent status codes, pagination, and Swagger metadata.
"""
import uuid
from typing import Any

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.base import CRUDService


def build_crud_router(
    *,
    service: CRUDService,
    prefix: str,
    tag: str,
    read_schema: type[BaseModel],
    create_schema: type[BaseModel],
    update_schema: type[BaseModel],
    id_name: str = "item_id",
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=[tag])
    singular = tag.rstrip("s")

    @router.get("", response_model=list[read_schema], summary=f"List {tag}")
    async def list_items(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: AsyncSession = Depends(get_db),
    ):
        return await service.list(db, skip=skip, limit=limit)

    @router.post(
        "",
        response_model=read_schema,
        status_code=status.HTTP_201_CREATED,
        summary=f"Create a {singular}",
    )
    async def create_item(payload: create_schema, db: AsyncSession = Depends(get_db)):
        return await service.create(db, payload.model_dump(exclude_unset=False))

    @router.get(
        "/{item_id}", response_model=read_schema, summary=f"Retrieve a {singular}"
    )
    async def get_item(item_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
        return await service.get_or_404(db, item_id)

    @router.put(
        "/{item_id}", response_model=read_schema, summary=f"Replace a {singular}"
    )
    async def replace_item(
        item_id: uuid.UUID,
        payload: create_schema,
        db: AsyncSession = Depends(get_db),
    ):
        return await service.update(db, item_id, payload.model_dump(exclude_unset=False))

    @router.patch(
        "/{item_id}",
        response_model=read_schema,
        summary=f"Partially update a {singular}",
    )
    async def update_item(
        item_id: uuid.UUID,
        payload: update_schema,
        db: AsyncSession = Depends(get_db),
    ):
        data: dict[str, Any] = payload.model_dump(exclude_unset=True)
        return await service.update(db, item_id, data)

    @router.delete(
        "/{item_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary=f"Delete a {singular}",
    )
    async def delete_item(item_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
        await service.delete(db, item_id)

    return router
