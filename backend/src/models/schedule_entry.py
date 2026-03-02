from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScheduleEntry:
    submission_id: str
    presentation_time: str
    room_or_location: str
