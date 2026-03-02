from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from models.paper_assignment import PaperAssignment
from services.review_submission_logger import ReviewSubmissionLogContext
from services.review_submission_logger import log_review_submission_event as log_assignment_event

ASSIGNMENT_SUCCESS_TEMPLATE = "Reviewer(s) assigned to paper {paper_id}."
ASSIGNMENT_UNAUTHENTICATED_MESSAGE = "Please log in to assign reviewers."
ASSIGNMENT_FORBIDDEN_MESSAGE = "You are not authorized to assign reviewers."
ASSIGNMENT_DUPLICATE_MESSAGE = "Reviewer already assigned."
ASSIGNMENT_LIMIT_MESSAGE = "Reviewer cannot be assigned due to workload limits."
ASSIGNMENT_STORAGE_ERROR_MESSAGE = "Assignment could not be saved."
ASSIGNMENT_NOTIFICATION_FAILED_MESSAGE = "Assignment saved, but invitation delivery failed."
REVIEWER_NOT_FOUND_MESSAGE = "Reviewer not found."
INVALID_REVIEWER_MESSAGE = "Invalid reviewer email."
LOGIN_REDIRECT = "/login"


class AssignmentStorageError(RuntimeError):
    pass


class NotificationDeliveryError(RuntimeError):
    pass


class ReviewerDirectory(Protocol):
    def find_reviewer(self, reviewer_id: str) -> dict | None:
        ...

    def is_valid_identifier(self, reviewer_id: str) -> bool:
        ...


class AssignmentRepository(Protocol):
    def is_assigned(self, reviewer_id: str, paper_id: str) -> bool:
        ...

    def save_assignment(self, assignment: PaperAssignment) -> None:
        ...


class ReviewerLimitRepository(Protocol):
    def at_limit(self, reviewer_id: str) -> bool:
        ...


class NotificationService(Protocol):
    def send_invitation(self, reviewer_id: str, paper_id: str) -> None:
        ...


@dataclass(frozen=True)
class AssignmentResult:
    status: str
    message: str | None = None
    reviewer_ids: list[str] | None = None
    errors: list[str] | None = None
    redirect_to: str | None = None

    @classmethod
    def success(cls, paper_id: str, reviewer_ids: list[str]) -> "AssignmentResult":
        return cls(
            status="success",
            message=ASSIGNMENT_SUCCESS_TEMPLATE.format(paper_id=paper_id),
            reviewer_ids=reviewer_ids,
        )

    @classmethod
    def notification_failed(cls, paper_id: str, reviewer_ids: list[str]) -> "AssignmentResult":
        return cls(
            status="notification_failed",
            message=ASSIGNMENT_NOTIFICATION_FAILED_MESSAGE,
            reviewer_ids=reviewer_ids,
        )

    @classmethod
    def unauthenticated(cls) -> "AssignmentResult":
        return cls(
            status="unauthenticated",
            message=ASSIGNMENT_UNAUTHENTICATED_MESSAGE,
            redirect_to=LOGIN_REDIRECT,
        )

    @classmethod
    def forbidden(cls) -> "AssignmentResult":
        return cls(status="forbidden", message=ASSIGNMENT_FORBIDDEN_MESSAGE)

    @classmethod
    def invalid_reviewer(cls, message: str) -> "AssignmentResult":
        return cls(status="invalid", message=message)

    @classmethod
    def duplicate(cls) -> "AssignmentResult":
        return cls(status="duplicate", message=ASSIGNMENT_DUPLICATE_MESSAGE)

    @classmethod
    def limit_reached(cls) -> "AssignmentResult":
        return cls(status="limit", message=ASSIGNMENT_LIMIT_MESSAGE)

    @classmethod
    def storage_error(cls) -> "AssignmentResult":
        return cls(status="error", message=ASSIGNMENT_STORAGE_ERROR_MESSAGE)


class ReviewerAssignmentService:
    def __init__(
        self,
        assignment_repository: AssignmentRepository,
        reviewer_directory: ReviewerDirectory,
        reviewer_limit_repository: ReviewerLimitRepository,
        notification_service: NotificationService,
    ) -> None:
        self._assignment_repository = assignment_repository
        self._reviewer_directory = reviewer_directory
        self._reviewer_limit_repository = reviewer_limit_repository
        self._notification_service = notification_service

    def assign_reviewers(
        self,
        paper_id: str,
        reviewer_ids: list[str] | None,
        editor_id: str | None,
        is_editor: bool,
        trace_id: Optional[str] = None,
    ) -> AssignmentResult:
        context = ReviewSubmissionLogContext(
            paper_id=paper_id,
            reviewer_id=editor_id,
            trace_id=trace_id,
        )

        if not editor_id:
            log_assignment_event("reviewer_assignment_unauthenticated", context)
            return AssignmentResult.unauthenticated()

        if not is_editor:
            log_assignment_event("reviewer_assignment_forbidden", context, ASSIGNMENT_FORBIDDEN_MESSAGE)
            return AssignmentResult.forbidden()

        reviewer_ids = reviewer_ids or []
        if not reviewer_ids:
            return AssignmentResult.invalid_reviewer(REVIEWER_NOT_FOUND_MESSAGE)

        notification_failed = False
        for reviewer_id in reviewer_ids:
            if not self._reviewer_directory.is_valid_identifier(reviewer_id):
                log_assignment_event(
                    "reviewer_assignment_invalid", context, INVALID_REVIEWER_MESSAGE
                )
                return AssignmentResult.invalid_reviewer(INVALID_REVIEWER_MESSAGE)

            reviewer = self._reviewer_directory.find_reviewer(reviewer_id)
            if reviewer is None:
                log_assignment_event(
                    "reviewer_assignment_not_found", context, REVIEWER_NOT_FOUND_MESSAGE
                )
                return AssignmentResult.invalid_reviewer(REVIEWER_NOT_FOUND_MESSAGE)

            if self._assignment_repository.is_assigned(reviewer_id, paper_id):
                log_assignment_event(
                    "reviewer_assignment_duplicate", context, ASSIGNMENT_DUPLICATE_MESSAGE
                )
                return AssignmentResult.duplicate()

            if self._reviewer_limit_repository.at_limit(reviewer_id):
                log_assignment_event(
                    "reviewer_assignment_limit", context, ASSIGNMENT_LIMIT_MESSAGE
                )
                return AssignmentResult.limit_reached()

            try:
                self._assignment_repository.save_assignment(
                    PaperAssignment(paper_id=paper_id, reviewer_id=reviewer_id)
                )
            except AssignmentStorageError:
                log_assignment_event(
                    "reviewer_assignment_storage_error",
                    context,
                    ASSIGNMENT_STORAGE_ERROR_MESSAGE,
                )
                return AssignmentResult.storage_error()
            except Exception:
                log_assignment_event(
                    "reviewer_assignment_storage_error",
                    context,
                    ASSIGNMENT_STORAGE_ERROR_MESSAGE,
                )
                return AssignmentResult.storage_error()

            try:
                self._notification_service.send_invitation(reviewer_id, paper_id)
            except NotificationDeliveryError:
                notification_failed = True

        if notification_failed:
            log_assignment_event(
                "reviewer_assignment_notification_failed",
                context,
                ASSIGNMENT_NOTIFICATION_FAILED_MESSAGE,
            )
            return AssignmentResult.notification_failed(paper_id, reviewer_ids)

        log_assignment_event("reviewer_assignment_success", context)
        return AssignmentResult.success(paper_id, reviewer_ids)
