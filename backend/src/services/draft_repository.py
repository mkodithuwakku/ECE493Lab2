from __future__ import annotations

from typing import Protocol

from models.submission_draft import SubmissionDraft


class DraftRepository(Protocol):
    def save_draft(self, submission_id: str, draft: SubmissionDraft) -> None:
        ...
