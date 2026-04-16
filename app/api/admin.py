from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_admin_user
from app.db.session import get_session
from app.models.task import Task
from app.models.team import Team
from app.schemas.task import TaskCreate, TaskRead
from app.schemas.team import TeamCreate, TeamRead

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/teams", response_model=TeamRead)
async def create_team(
    payload: TeamCreate,
    _: object = Depends(get_admin_user),
    session: AsyncSession = Depends(get_session),
) -> Team:
    team = Team(name=payload.name)
    session.add(team)
    await session.commit()
    await session.refresh(team)
    return team


@router.post("/tasks", response_model=TaskRead)
async def create_task(
    payload: TaskCreate,
    _: object = Depends(get_admin_user),
    session: AsyncSession = Depends(get_session),
) -> Task:
    if payload.open_at >= payload.close_at:
        raise HTTPException(status_code=400, detail="open_at must be before close_at")

    task = Task(**payload.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
