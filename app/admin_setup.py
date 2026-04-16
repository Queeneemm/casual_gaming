from redis.asyncio import from_url

from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.factory import app as admin_factory
from fastapi_admin.providers.login import UsernamePasswordProvider

from app.core.config import settings


async def configure_admin(app: FastAPI) -> None:
    redis = await from_url(settings.redis_url, decode_responses=True)

    await admin_app.configure(
        logo_url="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png",
        template_folders=[],
        favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        providers=[UsernamePasswordProvider(admin_model=None)],
        redis=redis,
    )
    app.mount("/admin-panel", admin_factory)
