from __future__ import annotations


def is_author(user_id: str, author_ids: list[str]) -> bool:
    return user_id in author_ids


def is_reviewer(user_id: str, reviewer_id: str) -> bool:
    return user_id == reviewer_id
