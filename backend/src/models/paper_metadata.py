from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PaperMetadata:
    author_names: list[str]
    affiliations: list[str]
    contact_email: str
    abstract: str
    keywords: list[str]
    paper_source: str
