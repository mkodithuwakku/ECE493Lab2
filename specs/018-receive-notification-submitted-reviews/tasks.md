---

description: "Task list for UC-18 Receive Notification of Submitted Reviews"
---

# Tasks: UC-18 Receive Notification of Submitted Reviews

**Input**: Design documents from `/specs/018-receive-notification-submitted-reviews/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Not requested by spec; no test tasks included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.
**Scope**: Tasks map to UC-18 and AT-UC18-* only.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create source and test directories per plan in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/` and `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/tests/`
- [ ] T002 [P] Create base module stubs in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/models/` and `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/services/`
- [ ] T003 [P] Create API routing scaffold in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/routes/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Create shared error types for retrieval and delivery failures in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/errors/notifications_errors` 
- [ ] T005 [P] Implement audit/logging helper for notification and review-status events in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/logging/notification_audit`
- [ ] T006 [P] Add authorization guard for editor-only access in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/middleware/editor_auth`
- [ ] T007 Create base data access interfaces for notifications and review status in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/services/review_status_repository` and `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/services/notification_repository`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Editor Receives Review Submission Notification (Priority: P1) 🎯 MVP

**Goal**: Notify the editor on review submission and show updated review status and details.

**Independent Test**: Submit a review, then as editor retrieve a notification and view updated review status and permitted review content.

### Implementation for User Story 1

- [ ] T008 [P] [US1] Add Review model fields needed for status and notification linkage in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/models/review`
- [ ] T009 [P] [US1] Add Notification model fields for review-submitted events in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/models/notification`
- [ ] T010 [P] [US1] Add ReviewStatus model fields in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/models/review_status`
- [ ] T011 [US1] Implement review status update service on submission in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/services/review_status_service`
- [ ] T012 [US1] Implement notification generation service for review submissions in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/services/notification_service`
- [ ] T013 [US1] Implement notification retrieval endpoint `/editor/notifications/reviews` in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/routes/editor_notifications`
- [ ] T014 [US1] Implement review status endpoint `/papers/{paperId}/reviews/status` in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/routes/review_status`
- [ ] T015 [US1] Wire routes into main router in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/routes/index`

**Checkpoint**: User Story 1 is fully functional and independently testable

---

## Phase 4: User Story 2 - Multiple Review Submissions Are Reflected (Priority: P2)

**Goal**: Reflect multiple submissions in status and deliver separate or aggregated notifications.

**Independent Test**: Submit two reviews for the same paper and confirm notification behavior and status counts.

### Implementation for User Story 2

- [ ] T016 [US2] Extend review status service to update counts for multiple submissions in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/services/review_status_service`
- [ ] T017 [US2] Implement per-review notification delivery for multiple submissions in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/services/notification_service`
- [ ] T018 [US2] Update notification retrieval view to return multiple review-submission events in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/routes/editor_notifications`

**Checkpoint**: User Stories 1 and 2 work independently and together

---

## Phase 5: User Story 3 - Review Status Visible Even If Notification Fails (Priority: P2)

**Goal**: Ensure review status remains accessible when notification delivery fails.

**Independent Test**: Simulate notification delivery failure and verify editor can still view status via paper management.

### Implementation for User Story 3

- [ ] T019 [US3] Add notification delivery failure handling without blocking review status updates in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/services/notification_service`
- [ ] T020 [US3] Log notification delivery failures using audit helper in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/logging/notification_audit`

**Checkpoint**: User Stories 1–3 work independently and together

---

## Phase 6: User Story 4 - Authentication Required to View Notifications and Status (Priority: P3)

**Goal**: Require authentication and redirect unauthorized access to login.

**Independent Test**: Attempt to access notification/status routes unauthenticated, then authenticate and re-access.

### Implementation for User Story 4

- [ ] T021 [US4] Apply editor auth guard to notification retrieval route in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/routes/editor_notifications`
- [ ] T022 [US4] Apply editor auth guard to review status route in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/routes/review_status`
- [ ] T023 [US4] Ensure unauthorized access triggers login redirect or 401/403 handling in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/middleware/editor_auth`

**Checkpoint**: User Stories 1–4 work independently and together

---

## Phase 7: User Story 5 - Clear Error on Retrieval Failure (Priority: P3)

**Goal**: Show clear errors for notification/status retrieval failures without exposing internal details.

**Independent Test**: Simulate retrieval errors and confirm safe error messaging with no partial data.

### Implementation for User Story 5

- [ ] T024 [US5] Add retrieval error handling for notification listing in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/routes/editor_notifications`
- [ ] T025 [US5] Add retrieval error handling for review status view in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/routes/review_status`
- [ ] T026 [US5] Ensure error responses do not leak internal details in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/errors/notifications_errors`

**Checkpoint**: All user stories are independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T027 [P] Update contracts to reflect any clarified notification aggregation behavior in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/018-receive-notification-submitted-reviews/contracts/review-notification-api.yaml`
- [ ] T028 [P] Update quickstart steps to reflect final notification behavior in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/018-receive-notification-submitted-reviews/quickstart.md`
- [ ] T029 Run quickstart validation and document findings in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/018-receive-notification-submitted-reviews/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - no dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - builds on US1 services
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - builds on US1 services
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - applies auth guard to US1 endpoints
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - adds retrieval error handling to US1 endpoints

### Parallel Opportunities (Examples)

- US1: T008, T009, T010 can run in parallel
- US1: T011 and T012 can proceed after models are in place, in parallel
- US2: T016 and T017 can run in parallel after US1 services are stable
- US4: T021 and T022 can run in parallel
- US5: T024 and T025 can run in parallel

## Implementation Strategy

- Deliver MVP as User Story 1 first (notification delivery + review status visibility).
- Layer multi-review handling (US2) and notification-failure resilience (US3).
- Add access control enforcement (US4) and retrieval error handling (US5).
- Finish with documentation alignment and quickstart validation.
