from __future__ import annotations

from typing import Protocol


class SubmissionRepository(Protocol):
    def associate_manuscript(self, submission_id: str, file_id: str) -> None:
        ...

    def is_finalized(self, submission_id: str) -> bool:
        ...
