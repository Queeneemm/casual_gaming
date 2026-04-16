from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    open_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    close_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), index=True)

    team = relationship("Team", back_populates="tasks")
