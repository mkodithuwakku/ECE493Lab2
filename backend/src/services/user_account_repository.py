from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Protocol


@dataclass(frozen=True)
class UserAccountRecord:
    id: str
    username: str
    email: str
    password_hash: str
    status: str
    failed_login_attempts: int
    lockout_until: Optional[datetime] = None
    last_failed_login_at: Optional[datetime] = None


class UserAccountRepository(Protocol):
    def find_by_identifier(self, identifier: str) -> Optional[UserAccountRecord]:
        ...

    def update_password(self, user_id: str, password_hash: str) -> None:
        ...

    def update_login_failure(
        self,
        user_id: str,
        attempts: int,
        lockout_until: Optional[datetime],
        last_failed_login_at: Optional[datetime],
        status: Optional[str] = None,
    ) -> None:
        ...

    def clear_login_failures(self, user_id: str) -> None:
        ...
