from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Casual Gaming"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60 * 24
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/casual_gaming"
    redis_url: str = "redis://localhost:6379/0"


settings = Settings()
