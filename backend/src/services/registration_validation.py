from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List

PASSWORD_MIN_LENGTH = 8


@dataclass(frozen=True)
class ValidationResult:
    errors: List[str]
    password_invalid: bool = False


EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_registration(email: str | None, password: str | None) -> ValidationResult:
    errors: List[str] = []
    password_invalid = False

    if not email:
        errors.append("Email is required.")
    elif not EMAIL_REGEX.match(email):
        errors.append("Email format is invalid.")

    if not password:
        errors.append("Password is required.")
    else:
        has_non_letter = any(not ch.isalpha() for ch in password)
        if len(password) < PASSWORD_MIN_LENGTH or not has_non_letter:
            password_invalid = True

    return ValidationResult(errors=errors, password_invalid=password_invalid)
