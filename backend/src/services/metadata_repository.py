from __future__ import annotations

from typing import Protocol

from models.paper_metadata import PaperMetadata


class MetadataRepository(Protocol):
    def save_metadata(self, submission_id: str, metadata: PaperMetadata) -> None:
        ...
