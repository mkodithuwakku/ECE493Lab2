from __future__ import annotations

from api.submissions.decision_error_mapper import map_decision_error
from services.decision_service import DecisionService


def get_decision(
    service: DecisionService,
    submission_id: str,
    user_id: str | None,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    result = service.get_decision(
        submission_id=submission_id,
        user_id=user_id,
        trace_id=trace_id,
    )

    if result.status in {"recorded", "not_recorded"}:
        response = {
            "decisionStatus": result.decision_status,
            "decisionValue": result.decision_value,
        }
        if result.message:
            response["message"] = result.message
        return 200, response

    return map_decision_error(result)
