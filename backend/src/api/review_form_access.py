from __future__ import annotations

from api.review_form_error_mapper import map_review_form_error
from services.review_form_service import ReviewFormService


def get_review_form(
    service: ReviewFormService,
    paper_id: str,
    reviewer_id: str | None,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    result = service.get_review_form(
        paper_id=paper_id,
        reviewer_id=reviewer_id,
        trace_id=trace_id,
    )

    if result.status == "ok" and result.form:
        response = {
            "paperId": result.form.paper_id,
            "title": result.form.title,
            "formFields": result.form.form_fields,
        }
        if result.form.manuscript_link:
            response["manuscriptLink"] = result.form.manuscript_link
        return 200, response

    return map_review_form_error(result)
