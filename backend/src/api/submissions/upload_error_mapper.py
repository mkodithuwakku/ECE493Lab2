from __future__ import annotations

from services.manuscript_upload_service import UploadResult


def map_upload_result(result: UploadResult) -> tuple[int, dict]:
    if result.status == "validation_failed":
        return 400, {"message": result.message}
    if result.status == "interrupted":
        return 409, {"message": result.message}
    if result.status == "storage_failed":
        return 500, {"message": result.message}
    return 500, {"message": result.message}
