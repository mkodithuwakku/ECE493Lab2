from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from services.auth_logger import AuthLogEntry, log_auth_event


@dataclass(frozen=True)
class DecisionLogContext:
    submission_id: str
    user_id: Optional[str]
    trace_id: Optional[str] = None


def log_decision_event(
    event: str,
    context: DecisionLogContext,
    message: str | None = None,
) -> None:
    log_auth_event(
        AuthLogEntry(
            event=event,
            user_id=context.user_id,
            message=message,
            trace_id=context.trace_id,
        )
    )
