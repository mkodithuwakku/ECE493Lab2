from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Reviewer:
    id: str
    assignment_count: int
    assignment_limit: int
