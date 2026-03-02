from __future__ import annotations

from api.submissions.upload_error_mapper import map_upload_result
from services.manuscript_upload_service import ManuscriptUploadService


def upload_manuscript(
    service: ManuscriptUploadService,
    submission_id: str,
    payload: dict | None,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    payload = payload or {}
    filename = payload.get("filename")
    size_bytes = payload.get("size_bytes")

    if not filename or size_bytes is None:
        return 400, {"message": "Filename and size are required."}

    result = service.upload(
        submission_id=submission_id,
        filename=filename,
        size_bytes=int(size_bytes),
        trace_id=trace_id,
    )

    if result.status == "success":
        return 200, {"message": result.message}

    return map_upload_result(result)
