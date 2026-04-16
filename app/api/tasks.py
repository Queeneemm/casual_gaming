from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_session
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskRead
from app.services.tasks import is_task_open

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/active", response_model=list[TaskRead])
async def list_active_tasks(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[Task]:
    if not user.team_id:
        return []

    result = await session.execute(select(Task).where(Task.team_id == user.team_id))
    tasks = result.scalars().all()
    now = datetime.now(timezone.utc)
    return [task for task in tasks if is_task_open(task.open_at, task.close_at, now)]
