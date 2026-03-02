from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PaymentConfirmation:
    confirmation_id: str
    registration_id: str
    amount: float
    currency: str
    transaction_reference_id: str
    confirmed_at: str
