from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReviewDetail:
    reviewer_id: str
    submitted_at: str
    content_summary: str | None = None


@dataclass(frozen=True)
class ReviewStatus:
    paper_id: str
    reviews_received: int
    reviewers_assigned: int
    review_details: list[ReviewDetail]
