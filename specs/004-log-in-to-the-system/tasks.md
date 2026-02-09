---

description: "Task list for UC-04 login implementation"
---

# Tasks: Log In to the System (UC-04)

**Input**: Design documents from `/Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/004-log-in-to-the-system/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Not requested in the feature specification; no test tasks included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.
**Scope**: Tasks map to UC-04 and acceptance tests AT-UC04-* only.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize shared modules used across login stories

- [ ] T001 Create auth limits configuration in backend/src/config/auth_limits.ts
- [ ] T002 [P] Create auth logging utility in backend/src/services/auth_logger.ts
- [ ] T003 [P] Create login API client wrapper in frontend/src/services/auth_client.ts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core building blocks needed by all user stories

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Create user account repository abstraction in backend/src/services/user_account_repository.ts
- [ ] T005 [P] Create session manager helper in backend/src/services/session_manager.ts
- [ ] T006 [P] Create identifier normalization helper in backend/src/services/identifier_normalizer.ts
- [ ] T007 Create lockout policy helper in backend/src/services/lockout_policy.ts
- [ ] T008 Create error-to-response mapper in backend/src/api/login/login_error_mapper.ts

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Log In Successfully (Priority: P1) 🎯 MVP

**Goal**: Authenticate active users with valid credentials and redirect to the personalized homepage

**Independent Test**: AT-UC04-01

### Implementation for User Story 1

- [ ] T009 [US1] Implement success-path authentication in backend/src/services/auth_service.ts
- [ ] T010 [US1] Implement login controller success response in backend/src/api/login/login_controller.ts
- [ ] T011 [P] [US1] Implement login form submit + redirect flow in frontend/src/pages/LoginPage.tsx
- [ ] T012 [P] [US1] Register login route and redirect target in frontend/src/routes.tsx
- [ ] T013 [US1] Wire login API call in frontend/src/services/auth_client.ts

**Checkpoint**: User Story 1 is independently functional

---

## Phase 4: User Story 2 - Handle Missing Login Information (Priority: P2)

**Goal**: Reject missing identifier/password with required-fields message

**Independent Test**: AT-UC04-02

### Implementation for User Story 2

- [ ] T014 [US2] Add required-field validation in backend/src/api/login/login_controller.ts
- [ ] T015 [P] [US2] Add required-field messaging in frontend/src/pages/LoginPage.tsx

**Checkpoint**: User Story 2 is independently functional

---

## Phase 5: User Story 3 - Handle Incorrect Credentials (Priority: P2)

**Goal**: Reject invalid credentials and show remaining attempts count

**Independent Test**: AT-UC04-03

### Implementation for User Story 3

- [ ] T016 [US3] Add failed-attempt tracking + remaining attempts in backend/src/services/auth_service.ts
- [ ] T017 [US3] Return 401 InvalidCredentials with remaining_attempts in backend/src/api/login/login_controller.ts
- [ ] T018 [P] [US3] Display remaining-attempts messaging in frontend/src/pages/LoginPage.tsx

**Checkpoint**: User Story 3 is independently functional

---

## Phase 6: User Story 4 - Block Locked or Disabled Accounts (Priority: P3)

**Goal**: Prevent login for locked/disabled accounts with account inactive message

**Independent Test**: AT-UC04-04

### Implementation for User Story 4

- [ ] T019 [US4] Enforce locked/disabled checks in backend/src/services/auth_service.ts
- [ ] T020 [US4] Return 403 AccountStatusError in backend/src/api/login/login_controller.ts
- [ ] T021 [P] [US4] Display account inactive message in frontend/src/pages/LoginPage.tsx

**Checkpoint**: User Story 4 is independently functional

---

## Phase 7: User Story 5 - Handle Authentication Service Unavailability (Priority: P3)

**Goal**: Surface temporary system issue message when auth services are unavailable

**Independent Test**: AT-UC04-05

### Implementation for User Story 5

- [ ] T022 [US5] Map service/database outage to service_unavailable in backend/src/services/auth_service.ts
- [ ] T023 [US5] Return 503 MessageResponse in backend/src/api/login/login_controller.ts
- [ ] T024 [P] [US5] Display temporary system issue message in frontend/src/pages/LoginPage.tsx

**Checkpoint**: User Story 5 is independently functional

---

## Phase 8: User Story 6 - Handle Critical Authentication Failure (Priority: P3)

**Goal**: Surface critical authentication failure message and ensure no session is created

**Independent Test**: AT-UC04-06

### Implementation for User Story 6

- [ ] T025 [US6] Add critical error handling path in backend/src/services/auth_service.ts
- [ ] T026 [US6] Return 500 MessageResponse in backend/src/api/login/login_controller.ts
- [ ] T027 [P] [US6] Display "authentication cannot be completed" message in frontend/src/pages/LoginPage.tsx

**Checkpoint**: User Story 6 is independently functional

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Finish cross-cutting updates and documentation alignment

- [ ] T028 [P] Align API contract if needed in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/004-log-in-to-the-system/contracts/uc-04-login.openapi.yaml
- [ ] T029 [P] Update quickstart notes for lockout auto-unlock in /Users/mkodi/Documents/University/Year 5/ECE 493/Lab 2/ECE493Lab2/specs/004-log-in-to-the-system/quickstart.md
- [ ] T030 Add credential redaction guidance in backend/src/services/auth_logger.ts

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup completion; blocks all user stories
- **User Stories (Phase 3+)**: Depend on Foundational completion; can proceed in priority order or parallel
- **Polish (Phase 9)**: Depends on all selected user stories

### User Story Dependencies

- **US1 (P1)**: Starts after Foundational; no dependencies on other stories
- **US2 (P2)**: Starts after Foundational; independent of US1
- **US3 (P2)**: Starts after Foundational; independent of US1/US2
- **US4 (P3)**: Starts after Foundational; independent of US1/US2/US3
- **US5 (P3)**: Starts after Foundational; independent of other stories
- **US6 (P3)**: Starts after Foundational; independent of other stories

### Parallel Opportunities

- Within Phase 1: T002 and T003 can run in parallel
- Within Phase 2: T005 and T006 can run in parallel
- Within each story: frontend and backend tasks marked [P] can run in parallel
- Across stories: any story can run in parallel after Phase 2 if staffing allows

---

## Parallel Example: User Story 1

```bash
Task: "Implement login form submit + redirect flow in frontend/src/pages/LoginPage.tsx"
Task: "Register login route and redirect target in frontend/src/routes.tsx"
```

## Parallel Example: User Story 2

```bash
Task: "Add required-field validation in backend/src/api/login/login_controller.ts"
Task: "Add required-field messaging in frontend/src/pages/LoginPage.tsx"
```

## Parallel Example: User Story 3

```bash
Task: "Add failed-attempt tracking + remaining attempts in backend/src/services/auth_service.ts"
Task: "Display remaining-attempts messaging in frontend/src/pages/LoginPage.tsx"
```

## Parallel Example: User Story 4

```bash
Task: "Enforce locked/disabled checks in backend/src/services/auth_service.ts"
Task: "Display account inactive message in frontend/src/pages/LoginPage.tsx"
```

## Parallel Example: User Story 5

```bash
Task: "Map service/database outage to service_unavailable in backend/src/services/auth_service.ts"
Task: "Display temporary system issue message in frontend/src/pages/LoginPage.tsx"
```

## Parallel Example: User Story 6

```bash
Task: "Add critical error handling path in backend/src/services/auth_service.ts"
Task: "Display \"authentication cannot be completed\" message in frontend/src/pages/LoginPage.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Validate AT-UC04-01 independently

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. US1 → Validate independently → Demo
3. US2 → Validate independently → Demo
4. US3 → Validate independently → Demo
5. US4 → Validate independently → Demo
6. US5 → Validate independently → Demo
7. US6 → Validate independently → Demo

### Parallel Team Strategy

1. Team completes Setup + Foundational
2. After Foundation:
   - Dev A: US1
   - Dev B: US2/US3
   - Dev C: US4/US5/US6
3. Merge stories after independent validation
