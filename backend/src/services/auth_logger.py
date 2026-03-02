from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Optional


@dataclass(frozen=True)
class AuthLogEntry:
    event: str
    identifier: Optional[str] = None
    user_id: Optional[str] = None
    message: Optional[str] = None


def log_auth_event(entry: AuthLogEntry) -> None:
    safe_entry = redact_sensitive(entry)
    payload = json.dumps(asdict(safe_entry))
    # Replace with real logger integration in production.
    print(payload)


def redact_sensitive(entry: AuthLogEntry) -> AuthLogEntry:
    return AuthLogEntry(
        event=entry.event,
        identifier="[redacted]" if entry.identifier else None,
        user_id=entry.user_id,
        message=entry.message.replace("password", "[redacted]") if entry.message else None,
    )
