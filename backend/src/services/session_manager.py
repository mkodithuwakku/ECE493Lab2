from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class Session:
    id: str
    user_id: str
    created_at: datetime


class SessionManager(Protocol):
    def create_session(self, user_id: str) -> Session:
        ...

    def terminate_all_sessions(self, user_id: str) -> None:
        ...
