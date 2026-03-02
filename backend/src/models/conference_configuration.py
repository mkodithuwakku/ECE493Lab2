from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConferenceConfiguration:
    submission_deadline: str
    review_deadline: str
    conference_start_date: str
    conference_end_date: str
