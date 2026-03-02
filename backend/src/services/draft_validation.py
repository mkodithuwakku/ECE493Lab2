from __future__ import annotations

import re
from dataclasses import dataclass

MISSING_MINIMUM_MESSAGE = "Submission is missing required draft information."
INVALID_DATA_PREFIX = "Submission data is invalid: "

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class DraftValidationError(RuntimeError):
    pass


@dataclass(frozen=True)
class DraftValidationResult:
    status: str
    message: str | None
    data: dict | None = None
    complete: bool = False


class DraftValidator:
    def validate(self, payload: dict) -> DraftValidationResult:
        try:
            return self._validate(payload)
        except Exception as exc:
            raise DraftValidationError("validation failure") from exc

    def _validate(self, payload: dict) -> DraftValidationResult:
        data = payload if isinstance(payload, dict) else {}

        title = _normalize_str(data.get("title"))
        abstract = _normalize_str(data.get("abstract"))
        authors = _normalize_list(data.get("authors"))
        contact_email = _normalize_str(data.get("contact_email"))

        issues: list[str] = []

        if contact_email and not EMAIL_REGEX.match(contact_email):
            issues.append("contact email is invalid")

        if _contains_unsupported_characters([title, abstract, contact_email]):
            issues.append("unsupported characters detected")

        if _contains_unsupported_characters(authors):
            issues.append("unsupported characters detected")

        if issues:
            message = INVALID_DATA_PREFIX + "; ".join(dict.fromkeys(issues))
            return DraftValidationResult(status="invalid", message=message)

        missing_minimum = not title or not abstract or not authors
        complete = not missing_minimum

        if missing_minimum:
            return DraftValidationResult(
                status="missing_minimum",
                message=MISSING_MINIMUM_MESSAGE,
                data=data,
                complete=False,
            )

        return DraftValidationResult(status="valid", message=None, data=data, complete=complete)


def _normalize_str(value: object | None) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_list(value: object | None) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return [str(value).strip()] if str(value).strip() else []


def _contains_unsupported_characters(values: list[str]) -> bool:
    for value in values:
        for char in value:
            if char in "<>":
                return True
            if ord(char) < 32 and char not in "\n\r\t":
                return True
            if not char.isprintable() and char not in "\n\r\t":
                return True
    return False
