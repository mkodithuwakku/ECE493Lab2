from __future__ import annotations

from api.conference_schedule_publication_error_mapper import (
    map_schedule_publication_error,
)
from services.schedule_publication_service import SchedulePublicationService


def publish_conference_schedule(
    service: SchedulePublicationService,
    admin_id: str | None,
    is_admin: bool,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    result = service.publish_schedule(
        admin_id=admin_id,
        is_admin=is_admin,
        trace_id=trace_id,
    )

    if result.status in {"published", "published_with_warning"} and result.schedule:
        schedule = result.schedule
        payload = {
            "message": result.message,
            "status": schedule.status,
            "is_finalized": schedule.is_finalized,
            "is_approved": schedule.is_approved,
        }
        if result.warning:
            payload["warning"] = result.warning
        return 200, payload

    return map_schedule_publication_error(result)
