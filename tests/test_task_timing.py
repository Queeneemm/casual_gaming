from datetime import datetime, timedelta, timezone

from app.services.tasks import is_task_open


def test_task_open_inside_window() -> None:
    now = datetime.now(timezone.utc)
    assert is_task_open(now - timedelta(minutes=1), now + timedelta(minutes=1), now)


def test_task_closed_before_window() -> None:
    now = datetime.now(timezone.utc)
    assert not is_task_open(now + timedelta(minutes=1), now + timedelta(minutes=2), now)
