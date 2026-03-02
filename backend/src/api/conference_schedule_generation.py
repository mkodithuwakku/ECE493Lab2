from __future__ import annotations

from api.conference_schedule_generation_error_mapper import (
    map_schedule_display_error,
    map_schedule_generation_error,
)
from services.schedule_generation_service import ScheduleGenerationService


def generate_conference_schedule(
    service: ScheduleGenerationService,
    admin_id: str | None,
    is_admin: bool,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    result = service.generate_schedule(
        admin_id=admin_id,
        is_admin=is_admin,
        trace_id=trace_id,
    )

    if result.status == "generated" and result.schedule:
        schedule = result.schedule
        return 200, {
            "message": "Schedule generated successfully.",
            "entries": [
                {
                    "submission_id": entry.submission_id,
                    "presentation_time": entry.presentation_time,
                    "room_or_location": entry.room_or_location,
                }
                for entry in schedule.entries
            ],
            "status": schedule.status,
        }

    return map_schedule_generation_error(result)


def get_generated_conference_schedule(
    service: ScheduleGenerationService,
    admin_id: str | None,
    is_admin: bool,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    result = service.get_generated_schedule(
        admin_id=admin_id,
        is_admin=is_admin,
        trace_id=trace_id,
    )

    if result.status == "found" and result.schedule:
        schedule = result.schedule
        return 200, {
            "entries": [
                {
                    "submission_id": entry.submission_id,
                    "presentation_time": entry.presentation_time,
                    "room_or_location": entry.room_or_location,
                }
                for entry in schedule.entries
            ],
            "status": schedule.status,
        }

    return map_schedule_display_error(result)
