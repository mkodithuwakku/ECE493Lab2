from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.submissions.schedule_controller import get_schedule
from models.conference_schedule import ConferenceSchedule
from models.paper_submission import PaperSubmission
from models.schedule_entry import ScheduleEntry
from services.schedule_service import (
    LOGIN_REDIRECT,
    SCHEDULE_MISSING_ENTRY_WARNING,
    SCHEDULE_NOT_PUBLISHED_MESSAGE,
    SCHEDULE_RETRIEVAL_ERROR_MESSAGE,
    SCHEDULE_UNAUTHENTICATED_MESSAGE,
    ScheduleRetrievalError,
    ScheduleService,
    SubmissionRetrievalError,
)


def test_at_uc11_01_view_published_schedule_entry() -> None:
    submission = PaperSubmission(
        id="sub-1",
        author_ids=["author-1"],
        decision_status="recorded",
        decision_value="accepted",
    )
    schedule = ConferenceSchedule(
        status="published",
        entries=[
            ScheduleEntry(
                submission_id="sub-1",
                presentation_time="2026-06-10T09:00:00",
                room_or_location="Room A",
            )
        ],
    )
    service = ScheduleService(
        schedule_repository=StubScheduleRepository(schedule=schedule),
        submission_repository=StubSubmissionRepository(submission=submission),
    )

    status, response = get_schedule(service, "sub-1", "author-1")

    assert status == 200
    assert response["scheduleStatus"] == "published"
    assert response["entries"][0]["submissionId"] == "sub-1"
    assert response["entries"][0]["presentationTime"] == "2026-06-10T09:00:00"
    assert response["entries"][0]["roomOrLocation"] == "Room A"
    assert "warning" not in response
    assert "message" not in response


def test_at_uc11_02_unauthenticated_redirect() -> None:
    submission = PaperSubmission(
        id="sub-1",
        author_ids=["author-1"],
        decision_status="recorded",
        decision_value="accepted",
    )
    schedule = ConferenceSchedule(status="published", entries=[])
    service = ScheduleService(
        schedule_repository=StubScheduleRepository(schedule=schedule),
        submission_repository=StubSubmissionRepository(submission=submission),
    )

    status, response = get_schedule(service, "sub-1", None)

    assert status == 401
    assert response["message"] == SCHEDULE_UNAUTHENTICATED_MESSAGE
    assert response["redirect_to"] == LOGIN_REDIRECT


def test_at_uc11_03_schedule_unpublished() -> None:
    submission = PaperSubmission(
        id="sub-1",
        author_ids=["author-1"],
        decision_status="recorded",
        decision_value="accepted",
    )
    schedule = ConferenceSchedule(status="unpublished", entries=[])
    service = ScheduleService(
        schedule_repository=StubScheduleRepository(schedule=schedule),
        submission_repository=StubSubmissionRepository(submission=submission),
    )

    status, response = get_schedule(service, "sub-1", "author-1")

    assert status == 200
    assert response["scheduleStatus"] == "unpublished"
    assert response["message"] == SCHEDULE_NOT_PUBLISHED_MESSAGE
    assert response["entries"] == []


def test_at_uc11_04_schedule_retrieval_error() -> None:
    submission = PaperSubmission(
        id="sub-1",
        author_ids=["author-1"],
        decision_status="recorded",
        decision_value="accepted",
    )
    service = ScheduleService(
        schedule_repository=StubScheduleRepository(fail=True),
        submission_repository=StubSubmissionRepository(submission=submission),
    )

    status, response = get_schedule(service, "sub-1", "author-1")

    assert status == 500
    assert response["message"] == SCHEDULE_RETRIEVAL_ERROR_MESSAGE


def test_at_uc11_05_missing_schedule_entry_warning() -> None:
    submission = PaperSubmission(
        id="sub-1",
        author_ids=["author-1"],
        decision_status="recorded",
        decision_value="accepted",
    )
    schedule = ConferenceSchedule(
        status="published",
        entries=[
            ScheduleEntry(
                submission_id="sub-2",
                presentation_time="2026-06-10T11:00:00",
                room_or_location="Room B",
            )
        ],
    )
    service = ScheduleService(
        schedule_repository=StubScheduleRepository(schedule=schedule),
        submission_repository=StubSubmissionRepository(submission=submission),
    )

    status, response = get_schedule(service, "sub-1", "author-1")

    assert status == 200
    assert response["scheduleStatus"] == "published"
    assert response["warning"] == SCHEDULE_MISSING_ENTRY_WARNING
    assert response["entries"][0]["submissionId"] == "sub-2"


class StubScheduleRepository:
    def __init__(self, *, schedule: ConferenceSchedule | None = None, fail: bool = False) -> None:
        self._schedule = schedule
        self._fail = fail

    def fetch_schedule(self) -> ConferenceSchedule:
        if self._fail:
            raise ScheduleRetrievalError("schedule retrieval failed")
        assert self._schedule is not None
        return self._schedule


class StubSubmissionRepository:
    def __init__(self, *, submission: PaperSubmission | None = None, fail: bool = False) -> None:
        self._submission = submission
        self._fail = fail

    def fetch_submission(self, submission_id: str) -> PaperSubmission:
        if self._fail:
            raise SubmissionRetrievalError("submission retrieval failed")
        assert self._submission is not None
        return self._submission
