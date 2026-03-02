from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from models.schedule_entry import ScheduleEntry

ScheduleStatus = Literal["published", "unpublished"]


@dataclass(frozen=True)
class ConferenceSchedule:
    status: ScheduleStatus
    entries: list[ScheduleEntry]
