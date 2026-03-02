from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from services.auth_logger import AuthLogEntry, log_auth_event
from services.log_redactor import redact_upload_metadata


@dataclass(frozen=True)
class UploadLogContext:
    submission_id: str
    trace_id: Optional[str] = None


def log_upload_event(event: str, context: UploadLogContext, message: str | None = None) -> None:
    safe_message = redact_upload_metadata(message) if message else None
    log_auth_event(
        AuthLogEntry(
            event=event,
            user_id=None,
            message=safe_message,
            trace_id=context.trace_id,
        )
    )
