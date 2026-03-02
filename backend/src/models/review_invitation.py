from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ReviewInvitationStatus = Literal["pending", "accepted", "rejected"]


@dataclass(frozen=True)
class ReviewInvitation:
    id: str
    paper_id: str
    reviewer_id: str
    status: ReviewInvitationStatus = "pending"
    email_failed: bool = False
