from __future__ import annotations

from api.submissions.metadata_error_mapper import map_metadata_result
from services.metadata_service import MetadataService


def save_metadata(
    service: MetadataService,
    submission_id: str,
    payload: dict | None,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    payload = payload or {}

    result = service.save_metadata(
        submission_id=submission_id,
        payload=payload,
        trace_id=trace_id,
    )

    if result.status == "success":
        return 200, {"message": result.message}

    return map_metadata_result(result)
