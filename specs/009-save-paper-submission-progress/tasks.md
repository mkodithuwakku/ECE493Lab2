---

description: "Task list for UC-09 save submission progress implementation"
---

# Tasks: Save Paper Submission Progress (UC-09)

**Input**: Design documents from `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/009-save-paper-submission-progress/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Not requested in the feature specification; no test tasks included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.
**Scope**: Tasks map to UC-09 and acceptance tests AT-UC09-* only.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize shared modules used across draft save stories

- [ ] T001 Create draft validation helper in backend/src/services/draft_validation.ts
- [ ] T002 [P] Create save-draft API client wrapper in frontend/src/services/draft_client.ts
- [ ] T003 [P] Create draft logging utility in backend/src/services/draft_logger.ts
- [ ] T004 [P] Create log redaction helper in backend/src/services/log_redactor.ts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core building blocks needed by all user stories

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Create submission repository abstraction in backend/src/services/submission_repository.ts
- [ ] T006 [P] Create draft repository abstraction in backend/src/services/draft_repository.ts
- [ ] T007 [P] Create draft error mapper in backend/src/api/submissions/draft_error_mapper.ts
- [ ] T008 Register save-draft route/controller in backend/src/api/submissions/save_draft_controller.ts
- [ ] T009 Ensure auth/authorization middleware protects save-draft endpoint in backend/src/api/submissions/save_draft_controller.ts

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Save Submission Progress Successfully (Priority: P1) 🎯 MVP

**Goal**: Validate and store submission data as a draft with confirmation

**Independent Test**: AT-UC09-01

### Implementation for User Story 1

- [ ] T010 [US1] Implement validation + storage + update in backend/src/services/draft_service.ts
- [ ] T011 [US1] Integrate structured logging + redaction in backend/src/services/draft_service.ts
- [ ] T012 [US1] Implement success response in backend/src/api/submissions/save_draft_controller.ts
- [ ] T013 [P] [US1] Implement save-draft UI action + success handling in frontend/src/pages/SubmissionProgressPage.tsx
- [ ] T014 [US1] Wire save-draft API call in frontend/src/services/draft_client.ts

**Checkpoint**: User Story 1 is independently functional

---

## Phase 4: User Story 2 - Invalid Submission Data Prevents Save (Priority: P2)

**Goal**: Return validation errors for invalid data

**Independent Test**: AT-UC09-02

### Implementation for User Story 2

- [ ] T015 [US2] Add invalid-data detection in backend/src/services/draft_validation.ts
- [ ] T016 [US2] Return validation errors in backend/src/api/submissions/save_draft_controller.ts
- [ ] T017 [P] [US2] Display validation error messages in frontend/src/pages/SubmissionProgressPage.tsx

**Checkpoint**: User Story 2 is independently functional

---

## Phase 5: User Story 3 - Minimum Draft Information Missing (Priority: P2)

**Goal**: Warn on missing minimum fields and allow save-anyway or cancel

**Independent Test**: AT-UC09-03

### Implementation for User Story 3

- [ ] T018 [US3] Add minimum-field detection in backend/src/services/draft_validation.ts
- [ ] T019 [US3] Return incomplete-data warning in backend/src/api/submissions/save_draft_controller.ts
- [ ] T020 [US3] Save draft as incomplete when save-anyway chosen in backend/src/services/draft_service.ts
- [ ] T021 [P] [US3] Display warning with save/cancel choice in frontend/src/pages/SubmissionProgressPage.tsx

**Checkpoint**: User Story 3 is independently functional

---

## Phase 6: User Story 4 - System Fails to Store Draft (Priority: P3)

**Goal**: Report storage failure and do not store draft

**Independent Test**: AT-UC09-04

### Implementation for User Story 4

- [ ] T022 [US4] Map storage failure in backend/src/services/draft_service.ts
- [ ] T023 [US4] Return storage failure response in backend/src/api/submissions/save_draft_controller.ts
- [ ] T024 [P] [US4] Display save failure message in frontend/src/pages/SubmissionProgressPage.tsx

**Checkpoint**: User Story 4 is independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Finish cross-cutting updates and documentation alignment

- [ ] T025 [P] Align API contract in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/009-save-paper-submission-progress/contracts/uc-09-save-draft.openapi.yaml
- [ ] T026 [P] Update quickstart notes for save-draft error handling in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/009-save-paper-submission-progress/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup completion; blocks all user stories
- **User Stories (Phase 3+)**: Depend on Foundational completion; can proceed in priority order or parallel
- **Polish (Phase 7)**: Depends on all selected user stories

### User Story Dependencies

- **US1 (P1)**: Starts after Foundational; no dependencies on other stories
- **US2 (P2)**: Starts after Foundational; independent of US1
- **US3 (P2)**: Starts after Foundational; independent of US1/US2
- **US4 (P3)**: Starts after Foundational; independent of other stories

### Parallel Opportunities

- Within Phase 1: T002, T003, and T004 can run in parallel
- Within Phase 2: T006 and T007 can run in parallel
- Within each story: frontend and backend tasks marked [P] can run in parallel
- Across stories: any story can run in parallel after Phase 2 if staffing allows

---

## Parallel Example: User Story 1

```bash
Task: "Implement save-draft UI action + success handling in frontend/src/pages/SubmissionProgressPage.tsx"
Task: "Wire save-draft API call in frontend/src/services/draft_client.ts"
```

## Parallel Example: User Story 2

```bash
Task: "Add invalid-data detection in backend/src/services/draft_validation.ts"
Task: "Display validation error messages in frontend/src/pages/SubmissionProgressPage.tsx"
```

## Parallel Example: User Story 3

```bash
Task: "Add minimum-field detection in backend/src/services/draft_validation.ts"
Task: "Display warning with save/cancel choice in frontend/src/pages/SubmissionProgressPage.tsx"
```

## Parallel Example: User Story 4

```bash
Task: "Map storage failure in backend/src/services/draft_service.ts"
Task: "Display save failure message in frontend/src/pages/SubmissionProgressPage.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Validate AT-UC09-01 independently

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. US1 → Validate independently → Demo
3. US2 → Validate independently → Demo
4. US3 → Validate independently → Demo
5. US4 → Validate independently → Demo

### Parallel Team Strategy

1. Team completes Setup + Foundational
2. After Foundation:
   - Dev A: US1
   - Dev B: US2/US3
   - Dev C: US4
3. Merge stories after independent validation
