from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

PaymentStatus = Literal["successful", "declined", "canceled", "failed"]


@dataclass(frozen=True)
class PaymentRecord:
    payment_id: str
    registration_id: str
    status: PaymentStatus
    transaction_id: str | None = None
    receipt: str | None = None
