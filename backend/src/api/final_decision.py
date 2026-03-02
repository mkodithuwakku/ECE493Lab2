from __future__ import annotations

from api.final_decision_error_mapper import map_final_decision_error, map_final_decision_view_error
from services.final_decision_service import FinalDecisionAccessService, FinalDecisionService


def record_final_decision(
    service: FinalDecisionService,
    paper_id: str,
    editor_id: str | None,
    is_editor: bool,
    payload: dict | None,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    payload = payload or {}
    decision_value = payload.get("decisionValue")

    result = service.record_decision(
        paper_id=paper_id,
        decision_value=decision_value,
        editor_id=editor_id,
        is_editor=is_editor,
        trace_id=trace_id,
    )

    if result.status == "success":
        response = {"message": result.message}
        if result.warning:
            response["warning"] = result.warning
        return 200, response

    return map_final_decision_error(result)


def get_final_decision(
    service: FinalDecisionAccessService,
    paper_id: str,
    author_id: str | None,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    result = service.get_decision(
        paper_id=paper_id,
        author_id=author_id,
        trace_id=trace_id,
    )

    if result.status == "ok":
        return 200, {"paperId": paper_id, "decisionStatus": result.decision_status}

    return map_final_decision_view_error(result)
