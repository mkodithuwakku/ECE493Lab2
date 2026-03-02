from __future__ import annotations

PASSWORD_MIN_LENGTH = 8


def validate_password(password: str) -> bool:
    if len(password) < PASSWORD_MIN_LENGTH:
        return False
    has_non_letter = any(not ch.isalpha() for ch in password)
    return has_non_letter


def requirements_message() -> str:
    return "Password must be at least 8 characters and include a non-letter character."
