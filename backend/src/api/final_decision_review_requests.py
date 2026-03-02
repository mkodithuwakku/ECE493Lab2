from __future__ import annotations

from api.final_decision_review_requests_error_mapper import map_review_request_error
from services.additional_review_request_service import AdditionalReviewRequestService


def request_additional_reviews(
    service: AdditionalReviewRequestService,
    paper_id: str,
    editor_id: str | None,
    is_editor: bool,
    payload: dict | None,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    payload = payload or {}
    reviewer_ids = payload.get("reviewerIds")

    result = service.request_reviews(
        paper_id=paper_id,
        reviewer_ids=reviewer_ids,
        editor_id=editor_id,
        is_editor=is_editor,
        trace_id=trace_id,
    )

    if result.status == "success":
        return 200, {"message": result.message}

    return map_review_request_error(result)
