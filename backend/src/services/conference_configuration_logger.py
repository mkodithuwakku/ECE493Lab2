from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from services.auth_logger import AuthLogEntry, log_auth_event


@dataclass(frozen=True)
class ConferenceConfigurationLogContext:
    admin_id: Optional[str]
    trace_id: Optional[str] = None


def log_conference_configuration_event(
    event: str,
    context: ConferenceConfigurationLogContext,
    message: str | None = None,
) -> None:
    log_auth_event(
        AuthLogEntry(
            event=event,
            user_id=context.admin_id,
            message=message,
            trace_id=context.trace_id,
        )
    )
