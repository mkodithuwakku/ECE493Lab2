from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Receipt:
    receipt_id: str
    registration_id: str
    receipt_number: str
    generated_at: str
