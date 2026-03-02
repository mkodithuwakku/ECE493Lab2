from __future__ import annotations

from typing import Protocol


class SubmissionRepository(Protocol):
    def associate_manuscript(self, submission_id: str, file_id: str) -> None:
        ...
