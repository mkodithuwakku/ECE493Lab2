from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from models.schedule_entry import ScheduleEntry

ScheduleStatus = Literal["published", "unpublished"]


@dataclass(frozen=True)
class ConferenceSchedule:
    status: ScheduleStatus
    entries: list[ScheduleEntry]
    is_finalized: bool = False
    is_approved: bool = False
    published_at: str | None = None
