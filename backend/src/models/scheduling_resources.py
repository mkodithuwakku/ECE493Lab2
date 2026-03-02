from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SchedulingResources:
    rooms: list[str]
    time_slots: list[str]
    conference_dates: list[str] | None = None
