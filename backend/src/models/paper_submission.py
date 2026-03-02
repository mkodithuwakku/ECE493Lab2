from __future__ import annotations

from dataclasses import dataclass

from models.decision import DecisionStatus, DecisionValue


@dataclass(frozen=True)
class PaperSubmission:
    id: str
    author_ids: list[str]
    decision_status: DecisionStatus
    decision_value: DecisionValue | None = None
