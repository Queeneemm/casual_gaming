from contextlib import asynccontextmanager
import asyncio
import logging

from fastapi import FastAPI
from fastapi.responses import FileResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine

from app.admin_setup import configure_admin
from app.api import admin, auth, tasks
from app.db.session import engine
from app.models.base import Base

logger = logging.getLogger(__name__)


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
    for attempt in range(1, 4):
        try:
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            return
        except SQLAlchemyError as exc:
            logger.warning(
                "Database is unavailable during startup (attempt %s/3): %s",
                attempt,
                exc,
            )
            if attempt == 3:
                logger.warning(
                    "Skipping table initialization after repeated DB connection failures."
                )
                return
            await asyncio.sleep(1)


app = FastAPI(title="Casual Gaming API", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(admin.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
async def frontend() -> FileResponse:
    return FileResponse("app/frontend/index.html")
