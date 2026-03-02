---

description: "Task list for UC-15 Submit Completed Paper Review"
---

# Tasks: UC-15 Submit Completed Paper Review

**Input**: Design documents from `/specs/015-submit-completed-paper-review/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Not requested in spec; no test tasks included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.
**Scope**: Tasks map to UC-15 and AT-UC15-* only.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create/confirm base directories `src/models/`, `src/services/`, `src/lib/`, `tests/contract/`, `tests/integration/`, `tests/unit/`
- [ ] T002 [P] Create review submission route module placeholder in `src/lib/review_submission_routes.js` and register in app router

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [ ] T003 Implement/confirm authentication guard for review submission in `src/lib/auth_guard.js`
- [ ] T004 [P] Implement/confirm standardized error response helper in `src/lib/error_responses.js`
- [ ] T005 [P] Implement/confirm audit logging hook in `src/lib/audit_log.js`
- [ ] T006 [P] Define data-access interface for reviews and assignments in `src/services/review_repository.js`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Submit Completed Review (Priority: P1) 🎯 MVP

**Goal**: Logged-in reviewer submits a valid review and receives confirmation.

**Independent Test**: Submit a valid review for an assigned paper and verify confirmation and stored association.

### Implementation for User Story 1

- [ ] T007 [P] [US1] Implement review submission service in `src/services/review_submission_service.js`
- [ ] T008 [P] [US1] Implement review form validation helper in `src/services/review_validation_service.js`
- [ ] T009 [US1] Implement submission controller to assemble request/response in `src/lib/review_submission_controller.js`
- [ ] T010 [US1] Wire POST `/papers/{paperId}/reviews` route in `src/lib/review_submission_routes.js`
- [ ] T011 [US1] Add confirmation response mapping in `src/lib/review_submission_view.js`

**Checkpoint**: User Story 1 is functional and independently testable

---

## Phase 4: User Story 2 - Require Login Before Submission (Priority: P2)

**Goal**: Unauthenticated users are redirected to login and cannot submit reviews.

**Independent Test**: Attempt submission while logged out → redirected to login; after login, submission proceeds.

### Implementation for User Story 2

- [ ] T012 [US2] Apply authentication guard to submission route in `src/lib/review_submission_routes.js`
- [ ] T013 [US2] Implement login redirect flow for unauthenticated access in `src/lib/auth_guard.js`

**Checkpoint**: User Story 2 is functional and independently testable

---

## Phase 5: User Story 3 - Block Unassigned Review Submission (Priority: P3)

**Goal**: Reviewers cannot submit reviews for unassigned papers; generic authorization error shown.

**Independent Test**: Attempt submission for unassigned paper → blocked with generic authorization error and no review stored.

### Implementation for User Story 3

- [ ] T014 [US3] Implement assignment authorization check in `src/services/review_authorization_service.js`
- [ ] T015 [US3] Return generic authorization error via `src/lib/error_responses.js` when access is denied
- [ ] T016 [US3] Log authorization denial in `src/lib/audit_log.js`

**Checkpoint**: User Story 3 is functional and independently testable

---

## Phase 6: User Story 4 - Validate Required and Valid Fields (Priority: P4)

**Goal**: Missing/invalid fields are rejected with field-specific validation errors.

**Independent Test**: Submit with missing/invalid fields → validation errors identify specific fields; corrected submission succeeds.

### Implementation for User Story 4

- [ ] T017 [US4] Enforce required/allowed field rules in `src/services/review_validation_service.js`
- [ ] T018 [US4] Return field-specific validation errors via `src/lib/error_responses.js`
- [ ] T019 [US4] Log validation failures in `src/lib/audit_log.js`

**Checkpoint**: User Story 4 is functional and independently testable

---

## Phase 7: User Story 5 - Handle Duplicate Submissions (Priority: P5)

**Goal**: Duplicate submissions are blocked with “Review already submitted.”

**Independent Test**: Submit twice for same reviewer-paper pair → second attempt blocked with required message and no duplicate stored.

### Implementation for User Story 5

- [ ] T020 [US5] Detect existing review for reviewer-paper pair in `src/services/review_submission_service.js`
- [ ] T021 [US5] Return duplicate-submission message via `src/lib/error_responses.js`
- [ ] T022 [US5] Log duplicate submission attempt in `src/lib/audit_log.js`

**Checkpoint**: User Story 5 is functional and independently testable

---

## Phase 8: User Story 6 - Handle Storage Failures (Priority: P6)

**Goal**: Storage failures show an error and do not store a review.

**Independent Test**: Simulate storage failure during valid submission → error shown, no review stored.

### Implementation for User Story 6

- [ ] T023 [US6] Handle storage failure path in `src/services/review_submission_service.js`
- [ ] T024 [US6] Return storage-failure error via `src/lib/error_responses.js`
- [ ] T025 [US6] Log storage failure in `src/lib/audit_log.js`

**Checkpoint**: User Story 6 is functional and independently testable

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T026 [P] Update `specs/015-submit-completed-paper-review/quickstart.md` if route names or messages differ from planned behavior
- [ ] T027 [P] Run quickstart validation steps and record results in `specs/015-submit-completed-paper-review/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Foundational - no dependencies on other stories
- **User Story 2 (P2)**: Starts after Foundational - no dependencies on other stories
- **User Story 3 (P3)**: Starts after Foundational - no dependencies on other stories
- **User Story 4 (P4)**: Starts after Foundational - depends on US1 validation helper
- **User Story 5 (P5)**: Starts after Foundational - depends on US1 submission service
- **User Story 6 (P6)**: Starts after Foundational - depends on US1 submission service

### Parallel Opportunities

- T002, T004, T005, T006 can run in parallel
- Within US1: T007 and T008 can run in parallel
- Within US3/US4/US5/US6: service updates and logging can run in parallel if touching different files

---

## Parallel Example: User Story 1

```bash
Task: "Implement review submission service in src/services/review_submission_service.js"
Task: "Implement review form validation helper in src/services/review_validation_service.js"
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

