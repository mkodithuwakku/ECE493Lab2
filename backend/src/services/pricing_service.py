from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Protocol

from api.schemas.pricing import PriceItem
from models.registration_price import RegistrationPrice

NO_PRICING_MESSAGE = "Registration prices are not currently available."
RETRIEVAL_ERROR_MESSAGE = "Registration pricing cannot be retrieved at this time."
PARTIAL_PRICING_MESSAGE = "Some pricing details may be incomplete."


class PricingRetrievalError(RuntimeError):
    pass


@dataclass(frozen=True)
class PricingFetchResult:
    items: List[RegistrationPrice]
    partial: bool = False


class PricingRepository(Protocol):
    def fetch_prices(self) -> PricingFetchResult:
        ...


@dataclass(frozen=True)
class PricingResult:
    status: str
    prices: List[PriceItem]
    message: str | None = None
    warning: str | None = None

    @classmethod
    def ok(cls, prices: List[PriceItem]) -> "PricingResult":
        return cls(status="ok", prices=prices)

    @classmethod
    def empty(cls) -> "PricingResult":
        return cls(status="empty", prices=[], message=NO_PRICING_MESSAGE)

    @classmethod
    def partial(cls, prices: List[PriceItem]) -> "PricingResult":
        return cls(status="partial", prices=prices, warning=PARTIAL_PRICING_MESSAGE)

    @classmethod
    def error(cls) -> "PricingResult":
        return cls(status="error", prices=[], message=RETRIEVAL_ERROR_MESSAGE)


class PricingService:
    def __init__(self, repository: PricingRepository) -> None:
        self._repository = repository

    def get_pricing(self) -> PricingResult:
        try:
            result = self._repository.fetch_prices()
        except PricingRetrievalError:
            return PricingResult.error()

        prices = self._filter_prices(result.items)

        if not prices:
            return PricingResult.empty()

        if result.partial:
            return PricingResult.partial(prices)

        return PricingResult.ok(prices)

    @staticmethod
    def _filter_prices(items: Iterable[RegistrationPrice]) -> List[PriceItem]:
        filtered: List[PriceItem] = []
        for item in items:
            if not item.is_active:
                continue
            filtered.append(
                PriceItem(attendance_type=item.attendance_type.name, amount=item.amount)
            )
        return filtered
