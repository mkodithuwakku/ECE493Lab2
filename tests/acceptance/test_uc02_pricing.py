from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.pricing import get_pricing_response
from models.attendance_type import AttendanceType
from models.registration_price import RegistrationPrice
from services.pricing_service import (
    NO_PRICING_MESSAGE,
    PARTIAL_PRICING_MESSAGE,
    RETRIEVAL_ERROR_MESSAGE,
    PricingFetchResult,
    PricingRetrievalError,
    PricingService,
)


class StubPricingRepository:
    def __init__(
        self,
        *,
        items=None,
        partial: bool = False,
        fail_on_fetch: bool = False,
    ) -> None:
        self._items = items or []
        self._partial = partial
        self._fail_on_fetch = fail_on_fetch

    def fetch_prices(self) -> PricingFetchResult:
        if self._fail_on_fetch:
            raise PricingRetrievalError("pricing fetch failed")
        return PricingFetchResult(items=self._items, partial=self._partial)


def test_at_uc02_01_main_success() -> None:
    standard = AttendanceType(id="t1", name="Standard")
    vip = AttendanceType(id="t2", name="VIP")

    repository = StubPricingRepository(
        items=[
            RegistrationPrice(id="p1", attendance_type=standard, amount=199.0),
            RegistrationPrice(id="p2", attendance_type=vip, amount=399.0),
        ]
    )
    service = PricingService(repository)
    status_code, payload = get_pricing_response(service)

    assert status_code == 200
    assert payload["status"] == "ok"
    assert len(payload["prices"]) == 2


def test_at_uc02_02_no_pricing_available() -> None:
    repository = StubPricingRepository(
        items=[
            RegistrationPrice(
                id="p1",
                attendance_type=AttendanceType(id="t1", name="Standard"),
                amount=199.0,
                is_active=False,
            )
        ]
    )
    service = PricingService(repository)
    status_code, payload = get_pricing_response(service)

    assert status_code == 404
    assert payload["message"] == NO_PRICING_MESSAGE


def test_at_uc02_03_retrieval_error() -> None:
    repository = StubPricingRepository(fail_on_fetch=True)
    service = PricingService(repository)
    status_code, payload = get_pricing_response(service)

    assert status_code == 500
    assert payload["message"] == RETRIEVAL_ERROR_MESSAGE


def test_at_uc02_04_partial_pricing_available() -> None:
    repository = StubPricingRepository(
        items=[
            RegistrationPrice(
                id="p1",
                attendance_type=AttendanceType(id="t1", name="Standard"),
                amount=199.0,
            )
        ],
        partial=True,
    )
    service = PricingService(repository)
    status_code, payload = get_pricing_response(service)

    assert status_code == 206
    assert payload["status"] == "partial"
    assert payload["warning"] == PARTIAL_PRICING_MESSAGE
    assert payload["prices"]
