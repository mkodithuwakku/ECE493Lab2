from __future__ import annotations

from dataclasses import dataclass

from models.attendance_type import AttendanceType


@dataclass(frozen=True)
class RegistrationPrice:
    id: str
    attendance_type: AttendanceType
    amount: float
    is_active: bool = True
