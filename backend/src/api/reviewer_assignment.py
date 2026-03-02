from __future__ import annotations

from api.reviewer_assignment_error_mapper import map_assignment_error
from services.reviewer_assignment_service import ReviewerAssignmentService


def assign_reviewers(
    service: ReviewerAssignmentService,
    paper_id: str,
    editor_id: str | None,
    is_editor: bool,
    payload: dict | None,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    payload = payload or {}
    reviewer_ids = payload.get("reviewerIds")

    result = service.assign_reviewers(
        paper_id=paper_id,
        reviewer_ids=reviewer_ids,
        editor_id=editor_id,
        is_editor=is_editor,
        trace_id=trace_id,
    )

    if result.status == "success":
        return 200, {"message": result.message, "reviewerIds": result.reviewer_ids}

    if result.status == "notification_failed":
        return 502, {"message": result.message, "reviewerIds": result.reviewer_ids}

    return map_assignment_error(result)
