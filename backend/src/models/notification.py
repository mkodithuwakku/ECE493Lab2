from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Notification:
    id: str
    paper_id: str
    type: str
    created_at: str
    editor_id: str | None = None
