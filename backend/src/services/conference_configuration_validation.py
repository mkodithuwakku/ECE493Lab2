from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

DATE_FORMAT_ERROR = "{field}: invalid date format"
REQUIRED_FIELD_ERROR = "{field}: required"
DATE_RELATIONSHIP_ERROR = "dateRelationship: {message}"


@dataclass(frozen=True)
class ValidationResult:
    status: str
    errors: list[str]

    @classmethod
    def ok(cls) -> "ValidationResult":
        return cls(status="ok", errors=[])

    @classmethod
    def error(cls, errors: list[str]) -> "ValidationResult":
        return cls(status="error", errors=errors)


class ConferenceConfigurationValidator:
    required_fields = [
        "submissionDeadline",
        "reviewDeadline",
        "conferenceStartDate",
        "conferenceEndDate",
    ]

    def validate(self, payload: dict) -> ValidationResult:
        errors: list[str] = []
        parsed: dict[str, datetime] = {}

        for field in self.required_fields:
            value = payload.get(field)
            if value in (None, ""):
                errors.append(REQUIRED_FIELD_ERROR.format(field=field))
                continue
            if not isinstance(value, str):
                errors.append(DATE_FORMAT_ERROR.format(field=field))
                continue
            try:
                parsed[field] = datetime.fromisoformat(value)
            except ValueError:
                errors.append(DATE_FORMAT_ERROR.format(field=field))

        if all(field in parsed for field in self.required_fields):
            submission = parsed["submissionDeadline"]
            review = parsed["reviewDeadline"]
            start = parsed["conferenceStartDate"]
            end = parsed["conferenceEndDate"]

            if submission >= review:
                errors.append(
                    DATE_RELATIONSHIP_ERROR.format(
                        message="submissionDeadline must be before reviewDeadline"
                    )
                )
            if review >= start:
                errors.append(
                    DATE_RELATIONSHIP_ERROR.format(
                        message="reviewDeadline must be before conferenceStartDate"
                    )
                )
            if start > end:
                errors.append(
                    DATE_RELATIONSHIP_ERROR.format(
                        message="conferenceStartDate must be on or before conferenceEndDate"
                    )
                )

        if errors:
            return ValidationResult.error(errors)

        return ValidationResult.ok()
