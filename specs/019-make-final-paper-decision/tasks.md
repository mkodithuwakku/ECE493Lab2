---

description: "Task list for UC-19 Make Final Paper Decision"
---

# Tasks: UC-19 Make Final Paper Decision

**Input**: Design documents from `/specs/019-make-final-paper-decision/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Not requested by spec; no test tasks included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.
**Scope**: Tasks map to UC-19 and AT-UC19-* only.

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

- [ ] T004 Create shared error types for decision storage and retrieval failures in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/errors/decision_errors`
- [ ] T005 [P] Implement audit/logging helper for decision events and failures in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/logging/decision_audit`
- [ ] T006 [P] Add editor-only authorization guard for decision actions in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/middleware/editor_auth`
- [ ] T007 Create base data access interfaces for decisions and review status in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/services/decision_repository` and `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/services/review_status_repository`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Record Final Decision (Priority: P1) 🎯 MVP

**Goal**: Record accept/reject decisions and make them visible to authors.

**Independent Test**: Record a decision for a fully reviewed paper and verify author portal visibility.

### Implementation for User Story 1

- [ ] T008 [P] [US1] Add Decision model fields for value, timestamp, and lock state in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/models/decision`
- [ ] T009 [P] [US1] Add Paper decision status fields in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/models/paper`
- [ ] T010 [P] [US1] Add Notification model fields for decision outcome in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/models/notification`
- [ ] T011 [US1] Implement decision recording service (accept/reject) with lock enforcement in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/services/decision_service`
- [ ] T012 [US1] Enforce decision lock and return conflict on re-decision attempts in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/services/decision_service`
- [ ] T012 [US1] Implement author decision visibility service in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/services/author_decision_service`
- [ ] T013 [US1] Implement decision submission endpoint `/papers/{paperId}/decision` in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/routes/decision`
- [ ] T014 [US1] Implement author decision status endpoint `/papers/{paperId}/decision` in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/routes/author_decision`
- [ ] T015 [US1] Wire decision routes into main router in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/routes/index`

**Checkpoint**: User Story 1 is fully functional and independently testable

---

## Phase 4: User Story 2 - Block Decision When Reviews Incomplete (Priority: P2)

**Goal**: Prevent decisions when required reviews are incomplete.

**Independent Test**: Attempt a decision on an incomplete-review paper and verify block and message.

### Implementation for User Story 2

- [ ] T016 [US2] Add review-completion check in decision service before recording in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/services/decision_service`
- [ ] T017 [US2] Add pending-reviews message handling in decision endpoint responses in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/routes/decision`

**Checkpoint**: User Stories 1 and 2 work independently and together

---

## Phase 5: User Story 3 - Request Additional Reviews Instead of Final Decision (Priority: P2)

**Goal**: Allow editors to request additional reviews and keep papers undecided.

**Independent Test**: Request additional reviews and verify no decision is recorded.

### Implementation for User Story 3

- [ ] T018 [US3] Implement additional review request service using reviewer assignment workflow in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/services/review_request_service`
- [ ] T019 [US3] Implement review request endpoint `/papers/{paperId}/decision/review-requests` in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/routes/review_requests`
- [ ] T020 [US3] Ensure paper remains undecided on review request in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/services/decision_service`

**Checkpoint**: User Stories 1–3 work independently and together

---

## Phase 6: User Story 4 - Authorization Required for Final Decisions (Priority: P3)

**Goal**: Enforce editor-only access to decision actions.

**Independent Test**: Attempt decision access while unauthenticated or non-editor and verify denial.

### Implementation for User Story 4

- [ ] T021 [US4] Apply editor auth guard to decision submission endpoint in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/routes/decision`
- [ ] T022 [US4] Apply author-only guard to decision status endpoint in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/routes/author_decision`
- [ ] T023 [US4] Ensure unauthorized access is denied (redirect/deny) in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/middleware/editor_auth`

**Checkpoint**: User Stories 1–4 work independently and together

---

## Phase 7: User Story 5 - Decision Visible Even If Notification Fails (Priority: P3)

**Goal**: Ensure author portal visibility even when notifications fail.

**Independent Test**: Record a decision during notification failure and verify author visibility.

### Implementation for User Story 5

- [ ] T024 [US5] Add notification failure handling without blocking decision recording in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/services/decision_service`
- [ ] T025 [US5] Log notification delivery failures using audit helper in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/logging/decision_audit`

**Checkpoint**: User Stories 1–5 work independently and together

---

## Phase 8: User Story 6 - Error on Decision Storage Failure (Priority: P3)

**Goal**: Show error and avoid recording decisions when storage fails.

**Independent Test**: Simulate storage failure and verify error and no decision recorded.

### Implementation for User Story 6

- [ ] T026 [US6] Add storage failure handling in decision service with no decision write on error in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/services/decision_service`
- [ ] T027 [US6] Add error response for storage failures in decision endpoint in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/routes/decision`
- [ ] T028 [US6] Ensure error responses do not leak internal details in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/src/lib/errors/decision_errors`

**Checkpoint**: All user stories are independently functional

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T029 [P] Update contracts to reflect clarified decision locking and author visibility in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/019-make-final-paper-decision/contracts/final-decision-api.yaml`
- [ ] T030 [P] Update quickstart steps to reflect final decision locking behavior in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/019-make-final-paper-decision/quickstart.md`
- [ ] T031 Run quickstart validation and document findings in `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/019-make-final-paper-decision/quickstart.md`

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - builds on US1 decision service
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - uses reviewer assignment workflow
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - applies auth guard to US1 endpoints
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - adds notification-failure handling to US1
- **User Story 6 (P3)**: Can start after Foundational (Phase 2) - adds storage-failure handling to US1

### Parallel Opportunities (Examples)

- US1: T008, T009, T010 can run in parallel
- US1: T011 and T012 can proceed after models are in place, in parallel
- US3: T018 and T019 can run in parallel after foundational setup
- US4: T021 and T022 can run in parallel
- US6: T026 and T027 can run in parallel

## Implementation Strategy

- Deliver MVP as User Story 1 first (record decision + author visibility).
- Add decision blocking (US2) and additional review requests (US3).
- Add access control enforcement (US4) and notification-failure resilience (US5).
- Add storage failure handling (US6).
- Finish with documentation alignment and quickstart validation.
