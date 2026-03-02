from __future__ import annotations

from api.review_submission_error_mapper import map_review_submission_error
from services.review_submission_service import ReviewSubmissionService


def submit_review(
    service: ReviewSubmissionService,
    paper_id: str,
    reviewer_id: str | None,
    payload: dict | None,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    payload = payload or {}
    field_values = payload.get("fieldValues")

    result = service.submit_review(
        paper_id=paper_id,
        reviewer_id=reviewer_id,
        field_values=field_values,
        trace_id=trace_id,
    )

    if result.status == "success":
        return 200, {"message": result.message}

    return map_review_submission_error(result)
