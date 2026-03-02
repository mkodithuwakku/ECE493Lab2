from __future__ import annotations


def redact_credentials(message: str) -> str:
    redacted = message.replace("password", "[redacted]")
    return redacted


def redact_upload_metadata(message: str | None) -> str | None:
    if message is None:
        return None
    return "[redacted]"


def redact_metadata_payload(message: str | None) -> str | None:
    if message is None:
        return None
    return "[redacted]"
