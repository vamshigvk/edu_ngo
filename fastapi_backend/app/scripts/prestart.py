"""Container start-up hook: create tables, then seed demo data if the DB is empty.

Run automatically by the Docker entrypoint before the API server starts.
Unlike ``seed`` (which always purges), this is safe to run on every boot — it
only seeds when there are no users yet, so restarts keep existing data.

Run manually with:  python -m app.scripts.prestart
"""
import asyncio

from sqlalchemy import func, select

from app.core.database import AsyncSessionLocal, Base, engine
from app.models.user import User
from app.scripts.seed import seed


async def main() -> None:
    # 1) Ensure the schema exists.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 2) Count existing users to decide whether to seed.
    async with AsyncSessionLocal() as db:
        user_count = (
            await db.execute(select(func.count()).select_from(User))
        ).scalar_one()

    if user_count == 0:
        print("Empty database detected — seeding demo data...")
        await seed()  # seed() disposes the engine when it finishes.
    else:
        print(f"Database already seeded ({user_count} users) — skipping seed.")
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
