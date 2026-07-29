"""University-application document review portal service (Phase 4)."""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.models.document import Document
from app.models.enums import DocumentStatus


class DocumentService:
    @staticmethod
    def _decorate(doc: Document) -> Document:
        doc.applicant_name = doc.user.full_name if doc.user else None
        doc.reviewer_name = doc.reviewer.full_name if doc.reviewer else None
        return doc

    async def get_or_404(self, db: AsyncSession, doc_id: uuid.UUID) -> Document:
        doc = await db.get(Document, doc_id)
        if doc is None:
            raise NotFoundError("Document not found.")
        return self._decorate(doc)

    async def create(self, db: AsyncSession, user_id: uuid.UUID, data: dict) -> Document:
        doc = Document(user_id=user_id, **data)
        db.add(doc)
        await db.commit()
        await db.refresh(doc)
        return self._decorate(doc)

    async def _list(self, db: AsyncSession, stmt) -> list[Document]:
        rows = (await db.execute(stmt.order_by(Document.created_at.desc()))).scalars().all()
        return [self._decorate(d) for d in rows]

    async def list_by_user(self, db: AsyncSession, user_id: uuid.UUID) -> list[Document]:
        return await self._list(db, select(Document).where(Document.user_id == user_id))

    async def list_assigned(self, db: AsyncSession, reviewer_id: uuid.UUID) -> list[Document]:
        return await self._list(db, select(Document).where(Document.reviewer_id == reviewer_id))

    async def list_all(self, db: AsyncSession) -> list[Document]:
        return await self._list(db, select(Document))

    async def assign(
        self, db: AsyncSession, doc_id: uuid.UUID, reviewer_id: uuid.UUID
    ) -> Document:
        doc = await self.get_or_404(db, doc_id)
        doc.reviewer_id = reviewer_id
        doc.status = DocumentStatus.ASSIGNED
        db.add(doc)
        await db.commit()
        await db.refresh(doc)
        return self._decorate(doc)

    async def review(
        self, db: AsyncSession, doc_id: uuid.UUID, reviewer_id: uuid.UUID, feedback: str
    ) -> Document:
        doc = await self.get_or_404(db, doc_id)
        if doc.reviewer_id != reviewer_id:
            raise PermissionDeniedError("This document is not assigned to you.")
        doc.feedback = feedback
        doc.status = DocumentStatus.REVIEWED
        db.add(doc)
        await db.commit()
        await db.refresh(doc)
        return self._decorate(doc)


document_service = DocumentService()
