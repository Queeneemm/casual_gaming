# Casual Gaming (FastAPI + PostgreSQL)

MVP бэкенд для командной игры с друзьями:
- авторизация пользователей;
- распределение по командам через админские эндпоинты;
- задания с окнами доступности (`open_at`/`close_at`);
- базовая интеграция FastAPI Admin (панель монтируется на `/admin-panel`).

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload
```

## ENV

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/casual_gaming
SECRET_KEY=your-secret
REDIS_URL=redis://localhost:6379/0
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

## Основные ручки
- `POST /auth/login`
- `GET /tasks/active`
- `POST /admin/teams`
- `POST /admin/tasks`
- `GET /health`

## Что дальше
- миграции через Alembic;
- полноценные FastAPI Admin модели/ресурсы;
- роли и granular permissions;
- попытки сдачи заданий и scoring/leaderboard.
