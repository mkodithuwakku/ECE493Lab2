from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from services.auth_logger import AuthLogEntry, log_auth_event
from services.log_redactor import redact_draft_payload


@dataclass(frozen=True)
class DraftLogContext:
    submission_id: str
    trace_id: Optional[str] = None


def log_draft_event(event: str, context: DraftLogContext, message: str | None = None) -> None:
    safe_message = redact_draft_payload(message) if message else None
    log_auth_event(
        AuthLogEntry(
            event=event,
            user_id=None,
            message=safe_message,
            trace_id=context.trace_id,
        )
    )
