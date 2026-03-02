from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "backend" / "src"))

from api.conference_schedule_publication import publish_conference_schedule
from models.conference_schedule import ConferenceSchedule
from models.schedule_entry import ScheduleEntry
from services.schedule_publication_service import (
    NOTIFICATION_FAILED_MESSAGE,
    PUBLISH_FAILED_MESSAGE,
    PUBLISH_SUCCESS_MESSAGE,
    SCHEDULE_NOT_READY_MESSAGE,
    STATUS_UPDATE_FAILED_MESSAGE,
    NotificationDeliveryError,
    SchedulePublicationError,
    SchedulePublicationService,
    ScheduleStatusUpdateError,
)


def test_at_uc23_01_publish_approved_schedule_successfully() -> None:
    schedule = ConferenceSchedule(
        status="unpublished",
        entries=[
            ScheduleEntry(
                submission_id="paper-1",
                presentation_time="2026-03-10T09:00",
                room_or_location="Room A",
            )
        ],
        is_finalized=True,
        is_approved=True,
    )
    repository = StubScheduleRepository(schedule)
    publisher = StubSchedulePublisher()
    notifier = StubNotificationService()
    service = SchedulePublicationService(repository, publisher, notifier)

    status, response = publish_conference_schedule(service, "admin-1", True)

    assert status == 200
    assert response["message"] == PUBLISH_SUCCESS_MESSAGE
    assert repository.schedule.status == "published"

    status, response = publish_conference_schedule(service, "admin-1", True)

    assert status == 200
    assert response["status"] == "published"


def test_at_uc23_02_admin_not_logged_in_then_logs_in() -> None:
    schedule = ConferenceSchedule(
        status="unpublished",
        entries=[],
        is_finalized=True,
        is_approved=True,
    )
    repository = StubScheduleRepository(schedule)
    publisher = StubSchedulePublisher()
    notifier = StubNotificationService()
    service = SchedulePublicationService(repository, publisher, notifier)

    status, response = publish_conference_schedule(service, None, True)

    assert status == 401
    assert response["redirect_to"] == "/login"
    assert repository.schedule.status == "unpublished"

    status, response = publish_conference_schedule(service, "admin-1", True)

    assert status == 200
    assert repository.schedule.status == "published"


def test_at_uc23_03_schedule_not_finalized_or_approved() -> None:
    schedule = ConferenceSchedule(
        status="unpublished",
        entries=[],
        is_finalized=False,
        is_approved=False,
    )
    repository = StubScheduleRepository(schedule)
    publisher = StubSchedulePublisher()
    notifier = StubNotificationService()
    service = SchedulePublicationService(repository, publisher, notifier)

    status, response = publish_conference_schedule(service, "admin-1", True)

    assert status == 400
    assert response["message"] == SCHEDULE_NOT_READY_MESSAGE
    assert repository.schedule.status == "unpublished"


def test_at_uc23_04_publish_fails_due_to_server_error() -> None:
    schedule = ConferenceSchedule(
        status="unpublished",
        entries=[],
        is_finalized=True,
        is_approved=True,
    )
    repository = StubScheduleRepository(schedule)
    publisher = StubSchedulePublisher(fail_publish=True)
    notifier = StubNotificationService()
    service = SchedulePublicationService(repository, publisher, notifier)

    status, response = publish_conference_schedule(service, "admin-1", True)

    assert status == 500
    assert response["message"] == PUBLISH_FAILED_MESSAGE
    assert repository.schedule.status == "unpublished"


def test_at_uc23_05_notification_delivery_fails() -> None:
    schedule = ConferenceSchedule(
        status="unpublished",
        entries=[],
        is_finalized=True,
        is_approved=True,
    )
    repository = StubScheduleRepository(schedule)
    publisher = StubSchedulePublisher()
    notifier = StubNotificationService(fail_notifications=True)
    service = SchedulePublicationService(repository, publisher, notifier)

    status, response = publish_conference_schedule(service, "admin-1", True)

    assert status == 200
    assert response["warning"] == NOTIFICATION_FAILED_MESSAGE
    assert repository.schedule.status == "published"


def test_at_uc23_06_publication_status_update_fails() -> None:
    schedule = ConferenceSchedule(
        status="unpublished",
        entries=[],
        is_finalized=True,
        is_approved=True,
    )
    repository = StubScheduleRepository(schedule, fail_update=True)
    publisher = StubSchedulePublisher()
    notifier = StubNotificationService()
    service = SchedulePublicationService(repository, publisher, notifier)

    status, response = publish_conference_schedule(service, "admin-1", True)

    assert status == 503
    assert response["message"] == STATUS_UPDATE_FAILED_MESSAGE
    assert repository.schedule.status == "unpublished"


class StubScheduleRepository:
    def __init__(self, schedule: ConferenceSchedule, *, fail_update: bool = False) -> None:
        self.schedule = schedule
        self._fail_update = fail_update

    def get_schedule(self) -> ConferenceSchedule | None:
        return self.schedule

    def set_published(self, schedule: ConferenceSchedule, admin_id: str) -> ConferenceSchedule:
        if self._fail_update:
            raise ScheduleStatusUpdateError("update failed")
        self.schedule = ConferenceSchedule(
            status="published",
            entries=schedule.entries,
            is_finalized=schedule.is_finalized,
            is_approved=schedule.is_approved,
            published_at="2026-03-10T12:00",
        )
        return self.schedule


class StubSchedulePublisher:
    def __init__(self, *, fail_publish: bool = False) -> None:
        self._fail_publish = fail_publish

    def publish(self, schedule: ConferenceSchedule) -> None:
        if self._fail_publish:
            raise SchedulePublicationError("publish failed")


class StubNotificationService:
    def __init__(self, *, fail_notifications: bool = False) -> None:
        self._fail_notifications = fail_notifications

    def notify_publication(self, schedule: ConferenceSchedule) -> None:
        if self._fail_notifications:
            raise NotificationDeliveryError("notification failed")
