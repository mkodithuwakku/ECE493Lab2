from __future__ import annotations

from api.submissions.draft_error_mapper import map_draft_result
from services.draft_service import DraftService


def save_draft(
    service: DraftService,
    submission_id: str,
    payload: dict | None,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    payload = payload or {}
    data = payload.get("data")
    save_anyway = bool(payload.get("save_anyway", False))

    result = service.save_draft(
        submission_id=submission_id,
        payload=data if isinstance(data, dict) else {},
        save_anyway=save_anyway,
        trace_id=trace_id,
    )

    if result.status == "success":
        return 200, {"message": result.message, "status": result.draft_status}

    return map_draft_result(result)
