from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AcceptedPaper:
    submission_id: str
    title: str
    track: str | None = None
