from datetime import datetime, timezone


def is_task_open(open_at: datetime, close_at: datetime, now: datetime | None = None) -> bool:
    current = now or datetime.now(timezone.utc)
    return open_at <= current <= close_at
