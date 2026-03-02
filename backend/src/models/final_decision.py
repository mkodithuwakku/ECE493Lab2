from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FinalDecision:
    paper_id: str
    decision: str
    rationale: str | None = None
    editor_id: str | None = None
