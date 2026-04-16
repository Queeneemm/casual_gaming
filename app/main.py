from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from app.admin_setup import configure_admin
from app.api import admin, auth, tasks
from app.db.session import engine
from app.models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables(engine)
    try:
        await configure_admin(app)
    except Exception:
        # FastAPI Admin requires additional setup and running Redis;
        # core API remains available if panel init fails.
        pass
    yield


async def create_tables(async_engine: AsyncEngine) -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI(title="Casual Gaming API", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(admin.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
