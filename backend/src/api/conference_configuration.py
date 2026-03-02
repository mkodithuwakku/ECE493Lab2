from __future__ import annotations

from api.conference_configuration_error_mapper import map_configuration_error
from services.conference_configuration_service import ConferenceConfigurationService


def get_conference_configuration(
    service: ConferenceConfigurationService,
    admin_id: str | None,
    is_admin: bool,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    result = service.get_configuration(
        admin_id=admin_id,
        is_admin=is_admin,
        trace_id=trace_id,
    )

    if result.status == "ok" and result.configuration:
        config = result.configuration
        return 200, {
            "submissionDeadline": config.submission_deadline,
            "reviewDeadline": config.review_deadline,
            "conferenceStartDate": config.conference_start_date,
            "conferenceEndDate": config.conference_end_date,
        }

    return map_configuration_error(result)


def update_conference_configuration(
    service: ConferenceConfigurationService,
    admin_id: str | None,
    is_admin: bool,
    payload: dict | None,
    trace_id: str | None = None,
) -> tuple[int, dict]:
    result = service.update_configuration(
        payload=payload,
        admin_id=admin_id,
        is_admin=is_admin,
        trace_id=trace_id,
    )

    if result.status == "saved" and result.configuration:
        return 200, {"message": result.message}

    return map_configuration_error(result)
