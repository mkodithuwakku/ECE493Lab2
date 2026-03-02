from __future__ import annotations

from services.metadata_service import MetadataSaveResult


def map_metadata_result(result: MetadataSaveResult) -> tuple[int, dict]:
    if result.status == "missing_fields":
        return 400, {"message": result.message}
    if result.status == "invalid_fields":
        return 400, {"message": result.message}
    if result.status == "locked":
        return 409, {"message": result.message}
    if result.status == "validation_error":
        return 500, {"message": result.message}
    if result.status == "storage_error":
        return 500, {"message": result.message}
    return 500, {"message": result.message}
