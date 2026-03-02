from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PaymentDetails:
    amount: float
    currency: str
    line_items: list[str] | None = None
