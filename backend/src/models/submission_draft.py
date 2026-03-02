from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SubmissionDraft:
    data: dict
    complete: bool
