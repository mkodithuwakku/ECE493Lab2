from __future__ import annotations

from api.schemas.public_info import (
    ErrorResponse,
    PartialPublicInfoResponse,
    PublicInfoResponse,
)
from services.public_info_service import PublicInfoResult, PublicInfoService


def get_public_info_response(service: PublicInfoService) -> tuple[int, dict]:
    result = service.get_public_info()

    if result.status == "ok":
        response = PublicInfoResponse(
            status="ok",
            announcements=result.announcements,
            information=result.information,
            message=result.message,
        )
        return 200, response.to_dict()

    if result.status == "partial":
        response = PartialPublicInfoResponse(
            status="partial",
            announcements=result.announcements,
            information=result.information,
            warning=result.warning or "",
        )
        return 206, response.to_dict()

    if result.status == "unavailable":
        response = ErrorResponse(message=result.message or "")
        return 503, response.to_dict()

    response = ErrorResponse(message=result.message or "")
    return 500, response.to_dict()
