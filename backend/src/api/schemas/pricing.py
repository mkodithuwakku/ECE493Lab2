from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class PriceItem:
    attendance_type: str
    amount: float


@dataclass(frozen=True)
class PricingResponse:
    status: str
    prices: List[PriceItem]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "prices": [asdict(item) for item in self.prices],
        }


@dataclass(frozen=True)
class PartialPricingResponse:
    status: str
    prices: List[PriceItem]
    warning: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "prices": [asdict(item) for item in self.prices],
            "warning": self.warning,
        }


@dataclass(frozen=True)
class MessageResponse:
    message: str

    def to_dict(self) -> Dict[str, Any]:
        return {"message": self.message}
