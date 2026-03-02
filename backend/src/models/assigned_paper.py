from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AssignedPaper:
    paper_id: str
    title: str | None = None
