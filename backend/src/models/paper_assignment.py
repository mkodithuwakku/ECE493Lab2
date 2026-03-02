from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PaperAssignment:
    paper_id: str
    reviewer_id: str
