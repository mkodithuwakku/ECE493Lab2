from __future__ import annotations


def redact_credentials(message: str) -> str:
    redacted = message.replace("password", "[redacted]")
    return redacted


def redact_upload_metadata(message: str | None) -> str | None:
    if message is None:
        return None
    redacted = message.replace("filename", "[redacted]")
    redacted = redacted.replace("file", "[redacted]")
    return redacted
