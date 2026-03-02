from __future__ import annotations

from dataclasses import dataclass

MISSING_FIELDS_MESSAGE = "Missing required fields: {fields}."
INVALID_FIELDS_MESSAGE = "Invalid field values: {fields}."


@dataclass(frozen=True)
class ReviewValidationResult:
    status: str
    missing_fields: list[str] | None = None
    invalid_fields: list[str] | None = None

    @classmethod
    def ok(cls) -> "ReviewValidationResult":
        return cls(status="ok")

    @classmethod
    def missing(cls, fields: list[str]) -> "ReviewValidationResult":
        return cls(status="missing", missing_fields=fields)

    @classmethod
    def invalid(cls, fields: list[str]) -> "ReviewValidationResult":
        return cls(status="invalid", invalid_fields=fields)


class ReviewValidator:
    def __init__(self, *, required_fields: list[str] | None = None) -> None:
        self._required_fields = required_fields or ["overall_score", "comments"]

    def validate(self, field_values: dict) -> ReviewValidationResult:
        missing = [
            field
            for field in self._required_fields
            if field not in field_values or field_values.get(field) in (None, "")
        ]
        if missing:
            return ReviewValidationResult.missing(missing)

        invalid: list[str] = []
        score = field_values.get("overall_score")
        if not isinstance(score, int) or not (1 <= score <= 5):
            invalid.append("overall_score")

        if invalid:
            return ReviewValidationResult.invalid(invalid)

        return ReviewValidationResult.ok()
