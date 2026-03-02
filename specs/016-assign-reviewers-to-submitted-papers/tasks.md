---

description: "Task list for UC-16 Assign Reviewers to Submitted Papers"
---

# Tasks: UC-16 Assign Reviewers to Submitted Papers

**Input**: Design documents from `/specs/016-assign-reviewers-to-submitted-papers/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Not requested in spec; no test tasks included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.
**Scope**: Tasks map to UC-16 and AT-UC16-* only.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create/confirm base directories `src/models/`, `src/services/`, `src/lib/`, `tests/contract/`, `tests/integration/`, `tests/unit/`
- [ ] T002 [P] Create reviewer assignment route module placeholder in `src/lib/reviewer_assignment_routes.js` and register in app router

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [ ] T003 Implement/confirm authentication guard for editor-only access in `src/lib/auth_guard.js`
- [ ] T004 [P] Implement/confirm standardized error response helper in `src/lib/error_responses.js`
- [ ] T005 [P] Implement/confirm audit logging hook in `src/lib/audit_log.js`
- [ ] T006 [P] Define data-access interfaces for reviewers, papers, and assignments in `src/services/reviewer_assignment_repository.js`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Assign Reviewer to Paper (Priority: P1) 🎯 MVP

**Goal**: Editor assigns one eligible reviewer and sees confirmation.

**Independent Test**: Assign a single eligible reviewer and verify confirmation and reviewer list update.

### Implementation for User Story 1

- [ ] T007 [P] [US1] Implement assignment service for single reviewer in `src/services/reviewer_assignment_service.js`
- [ ] T008 [US1] Implement assignment controller for request/response in `src/lib/reviewer_assignment_controller.js`
- [ ] T009 [US1] Wire POST `/papers/{paperId}/reviewers` route in `src/lib/reviewer_assignment_routes.js`
- [ ] T010 [US1] Add confirmation response mapping in `src/lib/reviewer_assignment_view.js`

**Checkpoint**: User Story 1 is functional and independently testable

---

## Phase 4: User Story 2 - Assign Multiple Reviewers (Priority: P2)

**Goal**: Editor assigns multiple eligible reviewers to the same paper.

**Independent Test**: Assign multiple eligible reviewers and verify each appears on the reviewer list with confirmation.

### Implementation for User Story 2

- [ ] T011 [US2] Extend assignment service to support multiple reviewers in `src/services/reviewer_assignment_service.js`
- [ ] T012 [US2] Update controller to handle multiple reviewer inputs in `src/lib/reviewer_assignment_controller.js`

**Checkpoint**: User Story 2 is functional and independently testable

---

## Phase 5: User Story 3 - Require Authorization (Priority: P3)

**Goal**: Only authenticated editors can assign reviewers; others are blocked.

**Independent Test**: Attempt assignment while logged out or as non-editor and verify access is blocked.

### Implementation for User Story 3

- [ ] T013 [US3] Apply authentication/authorization guard to assignment route in `src/lib/reviewer_assignment_routes.js`
- [ ] T014 [US3] Implement non-editor authorization error in `src/lib/error_responses.js`
- [ ] T015 [US3] Log authorization denials in `src/lib/audit_log.js`

**Checkpoint**: User Story 3 is functional and independently testable

---

## Phase 6: User Story 4 - Reject Invalid Reviewer (Priority: P4)

**Goal**: Invalid reviewer identifiers/emails are rejected with specific errors.

**Independent Test**: Submit invalid reviewer id/email and verify “not found” or “invalid email” error.

### Implementation for User Story 4

- [ ] T016 [US4] Validate reviewer existence and email format in `src/services/reviewer_validation_service.js`
- [ ] T017 [US4] Return invalid-reviewer error via `src/lib/error_responses.js`
- [ ] T018 [US4] Log invalid reviewer attempts in `src/lib/audit_log.js`

**Checkpoint**: User Story 4 is functional and independently testable

---

## Phase 7: User Story 5 - Prevent Duplicate Assignment (Priority: P5)

**Goal**: Duplicate reviewer-paper assignments are blocked with a specific message.

**Independent Test**: Attempt to assign an already assigned reviewer and verify “Reviewer already assigned.”

### Implementation for User Story 5

- [ ] T019 [US5] Detect duplicate assignment in `src/services/reviewer_assignment_service.js`
- [ ] T020 [US5] Return duplicate-assignment message via `src/lib/error_responses.js`
- [ ] T021 [US5] Log duplicate assignment attempts in `src/lib/audit_log.js`

**Checkpoint**: User Story 5 is functional and independently testable

---

## Phase 8: User Story 6 - Enforce Assignment Limits (Priority: P6)

**Goal**: Assignment blocked when reviewer workload limit reached.

**Independent Test**: Assign reviewer at limit and verify workload-limit message.

### Implementation for User Story 6

- [ ] T022 [US6] Enforce workload limit in `src/services/reviewer_assignment_service.js`
- [ ] T023 [US6] Return workload-limit message via `src/lib/error_responses.js`
- [ ] T024 [US6] Log workload-limit violations in `src/lib/audit_log.js`

**Checkpoint**: User Story 6 is functional and independently testable

---

## Phase 9: User Story 7 - Handle Notification Failure (Priority: P7)

**Goal**: Notification failure is reported while assignment is still recorded.

**Independent Test**: Simulate notification failure and verify error message and assignment recorded.

### Implementation for User Story 7

- [ ] T025 [US7] Trigger notification send and capture delivery failure in `src/services/reviewer_notification_service.js`
- [ ] T026 [US7] Return notification-failure message via `src/lib/error_responses.js` (assignment recorded)
- [ ] T027 [US7] Log notification failures in `src/lib/audit_log.js`

**Checkpoint**: User Story 7 is functional and independently testable

---

## Phase 10: User Story 8 - Handle Storage Failure (Priority: P8)

**Goal**: Storage failure shows error and no assignment is stored.

**Independent Test**: Simulate storage failure and verify no assignment stored.

### Implementation for User Story 8

- [ ] T028 [US8] Handle storage failure path in `src/services/reviewer_assignment_service.js`
- [ ] T029 [US8] Return storage-failure error via `src/lib/error_responses.js`
- [ ] T030 [US8] Log storage failures in `src/lib/audit_log.js`

**Checkpoint**: User Story 8 is functional and independently testable

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T031 [P] Update `specs/016-assign-reviewers-to-submitted-papers/quickstart.md` if route names or messages differ from planned behavior
- [ ] T032 [P] Run quickstart validation steps and record results in `specs/016-assign-reviewers-to-submitted-papers/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Foundational - no dependencies on other stories
- **User Story 2 (P2)**: Starts after Foundational - depends on US1 assignment service
- **User Story 3 (P3)**: Starts after Foundational - no dependencies on other stories
- **User Story 4 (P4)**: Starts after Foundational - depends on US1 assignment service
- **User Story 5 (P5)**: Starts after Foundational - depends on US1 assignment service
- **User Story 6 (P6)**: Starts after Foundational - depends on US1 assignment service
- **User Story 7 (P7)**: Starts after Foundational - depends on US1 assignment service
- **User Story 8 (P8)**: Starts after Foundational - depends on US1 assignment service

### Parallel Opportunities

- T002, T004, T005, T006 can run in parallel
- Within US1: T007 can run in parallel with T008
- Within US4/US5/US6/US7/US8: service updates and logging can run in parallel if touching different files

---

## Parallel Example: User Story 1

```bash
Task: "Implement assignment service for single reviewer in src/services/reviewer_assignment_service.js"
Task: "Implement assignment controller for request/response in src/lib/reviewer_assignment_controller.js"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. STOP and validate User Story 1 independently

### Incremental Delivery

1. Setup + Foundational
2. User Story 1 → validate (MVP)
3. User Story 2 → validate
4. User Story 3 → validate
5. User Story 4 → validate
6. User Story 5 → validate
7. User Story 6 → validate
8. User Story 7 → validate
9. User Story 8 → validate

