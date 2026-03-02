from __future__ import annotations


def redact_credentials(message: str) -> str:
    redacted = message.replace("password", "[redacted]")
    return redacted
