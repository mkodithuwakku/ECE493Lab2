from __future__ import annotations

from api.schemas.pricing import MessageResponse, PartialPricingResponse, PricingResponse
from services.pricing_service import PricingResult, PricingService


def get_pricing_response(service: PricingService) -> tuple[int, dict]:
    result = service.get_pricing()

    if result.status == "ok":
        response = PricingResponse(status="ok", prices=result.prices)
        return 200, response.to_dict()

    if result.status == "partial":
        response = PartialPricingResponse(
            status="partial", prices=result.prices, warning=result.warning or ""
        )
        return 206, response.to_dict()

    if result.status == "empty":
        response = MessageResponse(message=result.message or "")
        return 404, response.to_dict()

    response = MessageResponse(message=result.message or "")
    return 500, response.to_dict()
