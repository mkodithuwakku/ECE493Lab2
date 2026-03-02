from __future__ import annotations

from typing import Protocol


class StorageError(RuntimeError):
    pass


class UploadInterruptedError(RuntimeError):
    pass


class FileStorageService(Protocol):
    def store_file(self, submission_id: str, filename: str, size_bytes: int) -> str:
        ...
