from __future__ import annotations

import re
from dataclasses import dataclass

from models.paper_metadata import PaperMetadata

MISSING_FIELDS_MESSAGE = "Please complete all required metadata fields."
INVALID_METADATA_PREFIX = "Metadata contains invalid information: "

MAX_ABSTRACT_LENGTH = 3000
MAX_KEYWORDS = 10

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class MetadataValidationError(RuntimeError):
    pass


@dataclass(frozen=True)
class MetadataValidationResult:
    status: str
    message: str | None
    metadata: PaperMetadata | None = None


class MetadataValidator:
    def validate(self, payload: dict) -> MetadataValidationResult:
        try:
            return self._validate(payload)
        except Exception as exc:
            raise MetadataValidationError("validation failure") from exc

    def _validate(self, payload: dict) -> MetadataValidationResult:
        author_names = _normalize_list(payload.get("author_names"))
        affiliations = _normalize_list(payload.get("affiliations"))
        contact_email = _normalize_str(payload.get("contact_email"))
        abstract = _normalize_str(payload.get("abstract"))
        keywords = _normalize_list(payload.get("keywords"))
        paper_source = _normalize_str(payload.get("paper_source"))

        missing_fields = []
        if not author_names:
            missing_fields.append("author_names")
        if not affiliations:
            missing_fields.append("affiliations")
        if not contact_email:
            missing_fields.append("contact_email")
        if not abstract:
            missing_fields.append("abstract")
        if not keywords:
            missing_fields.append("keywords")
        if not paper_source:
            missing_fields.append("paper_source")

        if missing_fields:
            return MetadataValidationResult(
                status="missing_fields",
                message=MISSING_FIELDS_MESSAGE,
            )

        issues: list[str] = []

        if not EMAIL_REGEX.match(contact_email):
            issues.append("contact email is invalid")

        if len(abstract) > MAX_ABSTRACT_LENGTH:
            issues.append("abstract must be 3000 characters or fewer")

        if len(keywords) > MAX_KEYWORDS:
            issues.append("keywords must include 10 or fewer entries")

        if _contains_unsupported_characters(author_names + affiliations + keywords):
            issues.append("unsupported characters detected")

        if _contains_unsupported_characters([contact_email, abstract, paper_source]):
            issues.append("unsupported characters detected")

        if issues:
            message = INVALID_METADATA_PREFIX + "; ".join(dict.fromkeys(issues))
            return MetadataValidationResult(status="invalid_fields", message=message)

        metadata = PaperMetadata(
            author_names=author_names,
            affiliations=affiliations,
            contact_email=contact_email,
            abstract=abstract,
            keywords=keywords,
            paper_source=paper_source,
        )

        return MetadataValidationResult(status="valid", message=None, metadata=metadata)


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
