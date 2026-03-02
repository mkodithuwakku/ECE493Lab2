from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

RegistrationStatus = Literal["registered", "pending_unpaid", "paid_confirmed"]


@dataclass(frozen=True)
class AttendeeRegistration:
    registration_id: str
    attendee_id: str
    attendance_type_id: str | None
    status: RegistrationStatus
    registered_at: str | None = None
