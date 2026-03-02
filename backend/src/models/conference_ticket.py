from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConferenceTicket:
    ticket_id: str
    registration_id: str
    ticket_code: str
    issued_at: str
