"""Noor chatbot: FAQ-grounded question answering.

Static for now — retrieval over the admin-ingested FAQ table with a keyword
overlap score, no generation. The ``answer_query`` function is the single seam:
swap its body for a lightweight SLM later (grounded on the same retrieved FAQs)
and every caller keeps working unchanged.
"""
import re

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.faq import FAQ
from app.schemas.faq import ChatResponse, ChatSource

# Answers strictly come from published FAQs; when nothing matches we say so.
FALLBACK = (
    "I'm not sure about that one yet. For anything I can't answer, please reach "
    "out via our Contact page or email info@projecteduaccess.com and the team "
    "will be happy to help."
)

_STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "for", "in", "on", "is", "are",
    "do", "does", "how", "what", "when", "where", "which", "can", "i", "my",
    "me", "you", "your", "we", "our", "about", "tell", "with", "at", "be",
}


def _tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", (text or "").lower()) if t not in _STOPWORDS and len(t) > 1}


def _score(query_tokens: set[str], faq: FAQ) -> float:
    """Keyword-overlap score. Question hits weigh more than tags/answer hits."""
    q = _tokens(faq.question)
    tags = {str(t).lower() for t in (faq.tags or [])}
    body = _tokens(faq.answer) | _tokens(faq.category or "")
    score = 3.0 * len(query_tokens & q) + 2.0 * len(query_tokens & tags) + 1.0 * len(query_tokens & body)
    # Strong boost when the query essentially *is* the question (e.g. a chip click).
    if query_tokens and query_tokens <= (q | tags):
        score += 5.0
    return score


async def search_faqs(db: AsyncSession, message: str, limit: int = 3) -> list[tuple[FAQ, float]]:
    result = await db.execute(select(FAQ).where(FAQ.is_published.is_(True)))
    faqs = list(result.scalars().all())
    qt = _tokens(message)
    scored = [(f, _score(qt, f)) for f in faqs]
    scored = [pair for pair in scored if pair[1] > 0]
    scored.sort(key=lambda p: p[1], reverse=True)
    return scored[:limit]


async def answer_query(db: AsyncSession, message: str) -> ChatResponse:
    """FAQ-grounded answer. (SLM integration point — keep signature stable.)"""
    matches = await search_faqs(db, message, limit=3)
    if not matches:
        return ChatResponse(answer=FALLBACK, matched=False, sources=[])

    best, _ = matches[0]
    sources = [ChatSource(question=f.question, category=f.category) for f, _ in matches]
    return ChatResponse(answer=best.answer, matched=True, sources=sources)
