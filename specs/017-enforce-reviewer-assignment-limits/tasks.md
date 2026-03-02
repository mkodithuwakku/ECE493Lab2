---

description: "Task list for UC-17 Enforce Reviewer Assignment Limits"
---

# Tasks: UC-17 Enforce Reviewer Assignment Limits

**Input**: Design documents from `/specs/017-enforce-reviewer-assignment-limits/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Not requested in spec; no test tasks included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.
**Scope**: Tasks map to UC-17 and AT-UC17-* only.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create/confirm base directories `src/models/`, `src/services/`, `src/lib/`, `tests/contract/`, `tests/integration/`, `tests/unit/`
- [ ] T002 [P] Create assignment-limit route module placeholder in `src/lib/reviewer_limit_routes.js` and register in app router

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [ ] T003 Implement/confirm authentication guard for editor-only access in `src/lib/auth_guard.js`
- [ ] T004 [P] Implement/confirm standardized error response helper in `src/lib/error_responses.js`
- [ ] T005 [P] Implement/confirm audit logging hook in `src/lib/audit_log.js`
- [ ] T006 [P] Define data-access interface for reviewer counts and limits in `src/services/reviewer_limit_repository.js`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Allow Assignment Below Limit (Priority: P1) 🎯 MVP

**Goal**: Assignment allowed when reviewer is below limit and count updated.

**Independent Test**: Assign reviewer below limit and verify assignment created, count updated, and confirmation shown.

### Implementation for User Story 1

- [ ] T007 [P] [US1] Implement limit-check service for allow path in `src/services/reviewer_limit_service.js`
- [ ] T008 [US1] Implement limit-check controller for request/response in `src/lib/reviewer_limit_controller.js`
- [ ] T009 [US1] Wire POST `/papers/{paperId}/reviewers/limit-check` route in `src/lib/reviewer_limit_routes.js`
- [ ] T010 [US1] Add confirmation response mapping in `src/lib/reviewer_limit_view.js`

**Checkpoint**: User Story 1 is functional and independently testable

---

## Phase 4: User Story 2 - Block Assignment At Limit (Priority: P2)

**Goal**: Block assignment when reviewer is at limit with “Reviewer at assignment limit.”

**Independent Test**: Attempt assignment at limit and verify block and message.

### Implementation for User Story 2

- [ ] T011 [US2] Detect at-limit condition in `src/services/reviewer_limit_service.js`
- [ ] T012 [US2] Return workload-limit message via `src/lib/error_responses.js`
- [ ] T013 [US2] Log limit block in `src/lib/audit_log.js`

**Checkpoint**: User Story 2 is functional and independently testable

---

## Phase 5: User Story 3 - Block Assignment That Would Exceed Limit (Priority: P3)

**Goal**: Block assignment that would exceed limit with “Reviewer at assignment limit.”

**Independent Test**: Simulate assignments that would exceed limit and verify block.

### Implementation for User Story 3

- [ ] T014 [US3] Detect would-exceed condition in `src/services/reviewer_limit_service.js`
- [ ] T015 [US3] Return workload-limit message via `src/lib/error_responses.js`
- [ ] T016 [US3] Log would-exceed block in `src/lib/audit_log.js`

**Checkpoint**: User Story 3 is functional and independently testable

---

## Phase 6: User Story 4 - Handle Count Retrieval Failure (Priority: P4)

**Goal**: Retrieval failure blocks assignment with “Assignment cannot be completed at this time.”

**Independent Test**: Simulate retrieval failure and verify error and no assignment created.

### Implementation for User Story 4

- [ ] T017 [US4] Handle count-retrieval failure in `src/services/reviewer_limit_service.js`
- [ ] T018 [US4] Return retrieval-failure error via `src/lib/error_responses.js`
- [ ] T019 [US4] Log retrieval failure in `src/lib/audit_log.js`

**Checkpoint**: User Story 4 is functional and independently testable

---

## Phase 7: User Story 5 - Handle Update Failure After Allowing Assignment (Priority: P5)

**Goal**: Update failure triggers rollback and shows “Assignment could not be completed.”

**Independent Test**: Simulate update failure after allow and verify rollback and error.

### Implementation for User Story 5

- [ ] T020 [US5] Handle update/storage failure with rollback in `src/services/reviewer_limit_service.js`
- [ ] T021 [US5] Verify rollback cleanup removes partial/duplicate assignments in `src/services/reviewer_limit_service.js`
- [ ] T022 [US5] Return update-failure error via `src/lib/error_responses.js`
- [ ] T023 [US5] Log rollback event in `src/lib/audit_log.js`

**Checkpoint**: User Story 5 is functional and independently testable

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T024 [P] Update `specs/017-enforce-reviewer-assignment-limits/quickstart.md` if route names or messages differ from planned behavior
- [ ] T025 [P] Run quickstart validation steps and record results in `specs/017-enforce-reviewer-assignment-limits/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Foundational - no dependencies on other stories
- **User Story 2 (P2)**: Starts after Foundational - depends on US1 service
- **User Story 3 (P3)**: Starts after Foundational - depends on US1 service
- **User Story 4 (P4)**: Starts after Foundational - depends on US1 service
- **User Story 5 (P5)**: Starts after Foundational - depends on US1 service

### Parallel Opportunities

- T002, T004, T005, T006 can run in parallel
- Within US1: T007 can run in parallel with T008
- Within US2–US5: service updates and logging can run in parallel if touching different files

---

## Parallel Example: User Story 1

```bash
Task: "Implement limit-check service for allow path in src/services/reviewer_limit_service.js"
Task: "Implement limit-check controller for request/response in src/lib/reviewer_limit_controller.js"
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
