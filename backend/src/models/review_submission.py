from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReviewSubmission:
    paper_id: str
    reviewer_id: str
    field_values: dict
