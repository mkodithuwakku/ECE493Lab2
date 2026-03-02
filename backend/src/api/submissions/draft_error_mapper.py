from __future__ import annotations

from services.draft_service import DraftSaveResult


def map_draft_result(result: DraftSaveResult) -> tuple[int, dict]:
    if result.status == "invalid":
        return 400, {"message": result.message}
    if result.status == "missing_minimum":
        return 409, {"message": result.message}
    if result.status == "validation_error":
        return 500, {"message": result.message}
    if result.status == "storage_error":
        return 500, {"message": result.message}
    return 500, {"message": result.message}
