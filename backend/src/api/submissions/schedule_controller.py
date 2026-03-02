from __future__ import annotations

from api.submissions.schedule_error_mapper import map_schedule_error
from services.schedule_service import ScheduleService


def get_schedule(
    service: ScheduleService,
    submission_id: str,
    user_id: str | None,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    result = service.get_schedule(
        submission_id=submission_id,
        user_id=user_id,
        trace_id=trace_id,
    )

    if result.status in {"published", "unpublished"}:
        response: dict[str, object] = {
            "scheduleStatus": result.schedule_status,
            "entries": [
                {
                    "submissionId": entry.submission_id,
                    "presentationTime": entry.presentation_time,
                    "roomOrLocation": entry.room_or_location,
                }
                for entry in (result.entries or [])
            ],
        }
        if result.message:
            response["message"] = result.message
        if result.warning:
            response["warning"] = result.warning
        return 200, response

    return map_schedule_error(result)
