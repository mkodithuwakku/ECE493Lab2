from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from models.conference_schedule import ConferenceSchedule
from services.schedule_publication_logger import (
    SchedulePublicationLogContext,
    log_schedule_publication_event,
)

PUBLISH_UNAUTHENTICATED_MESSAGE = "Please log in to publish the conference schedule."
PUBLISH_FORBIDDEN_MESSAGE = "You are not authorized to publish the conference schedule."
SCHEDULE_NOT_READY_MESSAGE = "Schedule must be finalized and approved before publication."
PUBLISH_SUCCESS_MESSAGE = "Conference schedule published successfully."
PUBLISH_FAILED_MESSAGE = "Publication failed. Please try again."
STATUS_UPDATE_FAILED_MESSAGE = "Schedule could not be published at this time."
NOTIFICATION_FAILED_MESSAGE = "Schedule published, but notifications could not be delivered."
SCHEDULE_NOT_FOUND_MESSAGE = "No schedule is available to publish."
SCHEDULE_RETRIEVAL_ERROR_MESSAGE = "Schedule data is temporarily unavailable."
LOGIN_REDIRECT = "/login"


class ScheduleRetrievalError(RuntimeError):
    pass


class SchedulePublicationError(RuntimeError):
    pass


class ScheduleStatusUpdateError(RuntimeError):
    pass


class NotificationDeliveryError(RuntimeError):
    pass


class ScheduleRepository(Protocol):
    def get_schedule(self) -> ConferenceSchedule | None:
        ...

    def set_published(self, schedule: ConferenceSchedule, admin_id: str) -> ConferenceSchedule:
        ...


class SchedulePublisher(Protocol):
    def publish(self, schedule: ConferenceSchedule) -> None:
        ...


class NotificationService(Protocol):
    def notify_publication(self, schedule: ConferenceSchedule) -> None:
        ...


@dataclass(frozen=True)
class PublicationResult:
    status: str
    schedule: ConferenceSchedule | None = None
    message: str | None = None
    warning: str | None = None
    redirect_to: str | None = None

    @classmethod
    def published(cls, schedule: ConferenceSchedule) -> "PublicationResult":
        return cls(status="published", schedule=schedule, message=PUBLISH_SUCCESS_MESSAGE)

    @classmethod
    def published_with_warning(
        cls, schedule: ConferenceSchedule, warning: str
    ) -> "PublicationResult":
        return cls(
            status="published_with_warning",
            schedule=schedule,
            message=PUBLISH_SUCCESS_MESSAGE,
            warning=warning,
        )

    @classmethod
    def unauthenticated(cls) -> "PublicationResult":
        return cls(
            status="unauthenticated",
            message=PUBLISH_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def forbidden(cls) -> "PublicationResult":
        return cls(status="forbidden", message=PUBLISH_FORBIDDEN_MESSAGE)

    @classmethod
    def not_ready(cls) -> "PublicationResult":
        return cls(status="not_ready", message=SCHEDULE_NOT_READY_MESSAGE)

    @classmethod
    def not_found(cls) -> "PublicationResult":
        return cls(status="not_found", message=SCHEDULE_NOT_FOUND_MESSAGE)

    @classmethod
    def retrieval_error(cls) -> "PublicationResult":
        return cls(status="error", message=SCHEDULE_RETRIEVAL_ERROR_MESSAGE)

    @classmethod
    def publish_failed(cls) -> "PublicationResult":
        return cls(status="publish_failed", message=PUBLISH_FAILED_MESSAGE)

    @classmethod
    def status_update_failed(cls) -> "PublicationResult":
        return cls(status="status_update_failed", message=STATUS_UPDATE_FAILED_MESSAGE)


class SchedulePublicationService:
    def __init__(
        self,
        schedule_repository: ScheduleRepository,
        schedule_publisher: SchedulePublisher,
        notification_service: NotificationService,
    ) -> None:
        self._schedule_repository = schedule_repository
        self._schedule_publisher = schedule_publisher
        self._notification_service = notification_service

    def publish_schedule(
        self,
        admin_id: str | None,
        is_admin: bool,
        trace_id: Optional[str] = None,
    ) -> PublicationResult:
        context = SchedulePublicationLogContext(admin_id=admin_id, trace_id=trace_id)

        if not admin_id:
            log_schedule_publication_event("schedule_publish_unauthenticated", context)
            return PublicationResult.unauthenticated()

        if not is_admin:
            log_schedule_publication_event(
                "schedule_publish_forbidden",
                context,
                PUBLISH_FORBIDDEN_MESSAGE,
            )
            return PublicationResult.forbidden()

        try:
            schedule = self._schedule_repository.get_schedule()
        except ScheduleRetrievalError:
            log_schedule_publication_event(
                "schedule_publish_retrieval_error",
                context,
                SCHEDULE_RETRIEVAL_ERROR_MESSAGE,
            )
            return PublicationResult.retrieval_error()
        except Exception:
            log_schedule_publication_event(
                "schedule_publish_retrieval_error",
                context,
                SCHEDULE_RETRIEVAL_ERROR_MESSAGE,
            )
            return PublicationResult.retrieval_error()

        if schedule is None:
            log_schedule_publication_event(
                "schedule_publish_missing",
                context,
                SCHEDULE_NOT_FOUND_MESSAGE,
            )
            return PublicationResult.not_found()

        if not schedule.is_finalized or not schedule.is_approved:
            log_schedule_publication_event(
                "schedule_publish_not_ready",
                context,
                SCHEDULE_NOT_READY_MESSAGE,
            )
            return PublicationResult.not_ready()

        try:
            self._schedule_publisher.publish(schedule)
        except SchedulePublicationError:
            log_schedule_publication_event(
                "schedule_publish_failed",
                context,
                PUBLISH_FAILED_MESSAGE,
            )
            return PublicationResult.publish_failed()
        except Exception:
            log_schedule_publication_event(
                "schedule_publish_failed",
                context,
                PUBLISH_FAILED_MESSAGE,
            )
            return PublicationResult.publish_failed()

        try:
            published_schedule = self._schedule_repository.set_published(schedule, admin_id)
        except ScheduleStatusUpdateError:
            log_schedule_publication_event(
                "schedule_publish_status_update_failed",
                context,
                STATUS_UPDATE_FAILED_MESSAGE,
            )
            return PublicationResult.status_update_failed()
        except Exception:
            log_schedule_publication_event(
                "schedule_publish_status_update_failed",
                context,
                STATUS_UPDATE_FAILED_MESSAGE,
            )
            return PublicationResult.status_update_failed()

        try:
            self._notification_service.notify_publication(published_schedule)
        except NotificationDeliveryError:
            log_schedule_publication_event(
                "schedule_publish_notification_failed",
                context,
                NOTIFICATION_FAILED_MESSAGE,
            )
            return PublicationResult.published_with_warning(
                published_schedule, NOTIFICATION_FAILED_MESSAGE
            )
        except Exception:
            log_schedule_publication_event(
                "schedule_publish_notification_failed",
                context,
                NOTIFICATION_FAILED_MESSAGE,
            )
            return PublicationResult.published_with_warning(
                published_schedule, NOTIFICATION_FAILED_MESSAGE
            )

        log_schedule_publication_event("schedule_publish_success", context)
        return PublicationResult.published(published_schedule)
