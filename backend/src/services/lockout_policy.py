from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from config.auth_limits import (
    LOCKOUT_DURATION_MINUTES,
    LOCKOUT_THRESHOLD,
    LOCKOUT_WINDOW_MINUTES,
)


@dataclass(frozen=True)
class LockoutState:
    failed_attempts: int
    lockout_until: Optional[datetime]
    last_failed_login_at: Optional[datetime]


def is_locked(state: LockoutState, now: datetime) -> bool:
    if not state.lockout_until:
        return False
    return state.lockout_until > now


def should_lock(attempts: int) -> bool:
    return attempts >= LOCKOUT_THRESHOLD


def compute_lockout_until(now: datetime) -> datetime:
    return now + timedelta(minutes=LOCKOUT_DURATION_MINUTES)


def within_lockout_window(last_failed_login_at: Optional[datetime], now: datetime) -> bool:
    if not last_failed_login_at:
        return False
    return last_failed_login_at >= now - timedelta(minutes=LOCKOUT_WINDOW_MINUTES)
