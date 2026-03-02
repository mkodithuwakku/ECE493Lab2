from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from services.auth_logger import AuthLogEntry, log_auth_event


@dataclass(frozen=True)
class ReviewFormLogContext:
    paper_id: Optional[str]
    reviewer_id: Optional[str]
    trace_id: Optional[str] = None


def log_review_form_event(
    event: str,
    context: ReviewFormLogContext,
    message: str | None = None,
) -> None:
    log_auth_event(
        AuthLogEntry(
            event=event,
            user_id=context.reviewer_id,
            message=message,
            trace_id=context.trace_id,
        )
    )
