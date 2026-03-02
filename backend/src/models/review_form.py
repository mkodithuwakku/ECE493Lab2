from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReviewForm:
    paper_id: str
    title: str
    form_fields: list[dict]
    manuscript_link: str | None = None
