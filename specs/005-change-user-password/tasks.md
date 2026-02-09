---

description: "Task list for UC-05 change password implementation"
---

# Tasks: Change User Password (UC-05)

**Input**: Design documents from `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/005-change-user-password/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Not requested in the feature specification; no test tasks included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.
**Scope**: Tasks map to UC-05 and acceptance tests AT-UC05-* only.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize shared modules used across password change stories

- [ ] T001 Create auth logging utility for password changes in backend/src/services/auth_logger.ts
- [ ] T002 [P] Create password policy helper in backend/src/services/password_policy.ts
- [ ] T003 [P] Create change-password API client wrapper in frontend/src/services/password_client.ts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core building blocks needed by all user stories

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Create user account repository abstraction in backend/src/services/user_account_repository.ts
- [ ] T005 [P] Create session invalidation helper in backend/src/services/session_manager.ts
- [ ] T006 [P] Create credential redaction helper in backend/src/services/log_redactor.ts
- [ ] T007 Create password hashing helper in backend/src/services/password_hasher.ts
- [ ] T008 Create change-password error mapper in backend/src/api/password/change_password_error_mapper.ts

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Change Password Successfully (Priority: P1) 🎯 MVP

**Goal**: Allow authenticated users to change password successfully and terminate sessions

**Independent Test**: AT-UC05-01

### Implementation for User Story 1

- [ ] T009 [US1] Implement change-password validation and update in backend/src/services/password_change_service.ts
- [ ] T010 [US1] Terminate all sessions after successful change in backend/src/services/session_manager.ts
- [ ] T011 [US1] Implement change-password controller success response in backend/src/api/password/change_password_controller.ts
- [ ] T012 [P] [US1] Implement change-password form submit + success handling in frontend/src/pages/ChangePasswordPage.tsx
- [ ] T013 [US1] Wire change-password API call in frontend/src/services/password_client.ts

**Checkpoint**: User Story 1 is independently functional

---

## Phase 4: User Story 2 - Handle Incorrect Current Password (Priority: P2)

**Goal**: Reject incorrect current password with error message while keeping user logged in

**Independent Test**: AT-UC05-02

### Implementation for User Story 2

- [ ] T014 [US2] Add incorrect-current-password handling in backend/src/services/password_change_service.ts
- [ ] T015 [US2] Return incorrect-password error response in backend/src/api/password/change_password_controller.ts
- [ ] T016 [P] [US2] Display incorrect-password error in frontend/src/pages/ChangePasswordPage.tsx

**Checkpoint**: User Story 2 is independently functional

---

## Phase 5: User Story 3 - Enforce New Password Security Requirements (Priority: P2)

**Goal**: Enforce password policy and show requirement guidelines on failure

**Independent Test**: AT-UC05-03

### Implementation for User Story 3

- [ ] T017 [US3] Enforce password policy in backend/src/services/password_policy.ts
- [ ] T018 [US3] Return requirements guidance error in backend/src/api/password/change_password_controller.ts
- [ ] T019 [P] [US3] Display requirements guidance in frontend/src/pages/ChangePasswordPage.tsx

**Checkpoint**: User Story 3 is independently functional

---

## Phase 6: User Story 4 - Handle Password Confirmation Mismatch (Priority: P2)

**Goal**: Reject mismatched confirmation with mismatch error message

**Independent Test**: AT-UC05-04

### Implementation for User Story 4

- [ ] T020 [US4] Detect confirmation mismatch in backend/src/services/password_change_service.ts
- [ ] T021 [US4] Return mismatch error response in backend/src/api/password/change_password_controller.ts
- [ ] T022 [P] [US4] Display mismatch error in frontend/src/pages/ChangePasswordPage.tsx

**Checkpoint**: User Story 4 is independently functional

---

## Phase 7: User Story 5 - Handle Password Update Failure (Priority: P3)

**Goal**: Report update failure and keep password unchanged

**Independent Test**: AT-UC05-05

### Implementation for User Story 5

- [ ] T023 [US5] Map update failure to error in backend/src/services/password_change_service.ts
- [ ] T024 [US5] Return update failure response in backend/src/api/password/change_password_controller.ts
- [ ] T025 [P] [US5] Display update failure message in frontend/src/pages/ChangePasswordPage.tsx

**Checkpoint**: User Story 5 is independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Finish cross-cutting updates and documentation alignment

- [ ] T026 [P] Align API contract in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/005-change-user-password/contracts/uc-05-change-password.openapi.yaml
- [ ] T027 [P] Update quickstart notes for session termination in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/005-change-user-password/quickstart.md
- [ ] T028 Add credential redaction coverage in backend/src/services/auth_logger.ts

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup completion; blocks all user stories
- **User Stories (Phase 3+)**: Depend on Foundational completion; can proceed in priority order or parallel
- **Polish (Phase 8)**: Depends on all selected user stories

### User Story Dependencies

- **US1 (P1)**: Starts after Foundational; no dependencies on other stories
- **US2 (P2)**: Starts after Foundational; independent of US1
- **US3 (P2)**: Starts after Foundational; independent of US1/US2
- **US4 (P2)**: Starts after Foundational; independent of US1/US2/US3
- **US5 (P3)**: Starts after Foundational; independent of other stories

### Parallel Opportunities

- Within Phase 1: T002 and T003 can run in parallel
- Within Phase 2: T005 and T006 can run in parallel
- Within each story: frontend and backend tasks marked [P] can run in parallel
- Across stories: any story can run in parallel after Phase 2 if staffing allows

---

## Parallel Example: User Story 1

```bash
Task: "Implement change-password form submit + success handling in frontend/src/pages/ChangePasswordPage.tsx"
Task: "Wire change-password API call in frontend/src/services/password_client.ts"
```

## Parallel Example: User Story 2

```bash
Task: "Add incorrect-current-password handling in backend/src/services/password_change_service.ts"
Task: "Display incorrect-password error in frontend/src/pages/ChangePasswordPage.tsx"
```

## Parallel Example: User Story 3

```bash
Task: "Enforce password policy in backend/src/services/password_policy.ts"
Task: "Display requirements guidance in frontend/src/pages/ChangePasswordPage.tsx"
```

## Parallel Example: User Story 4

```bash
Task: "Detect confirmation mismatch in backend/src/services/password_change_service.ts"
Task: "Display mismatch error in frontend/src/pages/ChangePasswordPage.tsx"
```

## Parallel Example: User Story 5

```bash
Task: "Map update failure to error in backend/src/services/password_change_service.ts"
Task: "Display update failure message in frontend/src/pages/ChangePasswordPage.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Validate AT-UC05-01 independently

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. US1 → Validate independently → Demo
3. US2 → Validate independently → Demo
4. US3 → Validate independently → Demo
5. US4 → Validate independently → Demo
6. US5 → Validate independently → Demo

### Parallel Team Strategy

1. Team completes Setup + Foundational
2. After Foundation:
   - Dev A: US1
   - Dev B: US2/US3
   - Dev C: US4/US5
3. Merge stories after independent validation
