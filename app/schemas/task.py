from datetime import datetime

from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str
    open_at: datetime
    close_at: datetime
    team_id: int


class TaskRead(BaseModel):
    id: int
    title: str
    description: str
    open_at: datetime
    close_at: datetime
    team_id: int

    model_config = {"from_attributes": True}
