---

description: "Task list for UC-12 review invitations"
---

# Tasks: UC-12 Receive and Respond to Review Invitation

**Input**: Design documents from `/specs/012-receive-and-respond-to-review-invitation/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/invitations-api.yaml

**Tests**: Not requested by the spec; no test tasks included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.
**Scope**: Tasks map only to UC-12 and AT-UC12-*.

## Format: `[ID] [P?] [Story] Description`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Minimal setup for UC-12 documentation and structure alignment

- [ ] T001 Confirm feature docs and paths under `specs/012-receive-and-respond-to-review-invitation/`
- [ ] T002 [P] Align invitations endpoints with contract in `specs/012-receive-and-respond-to-review-invitation/contracts/invitations-api.yaml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared logic required before user story work

- [ ] T003 [P] Define review invitation model in `src/models/review_invitation.py`
- [ ] T004 [P] Define paper assignment model in `src/models/paper_assignment.py`
- [ ] T005 [P] Define reviewer model updates (assignment_count) in `src/models/reviewer.py`
- [ ] T006 Implement invitation authorization utility in `src/lib/authorization.py`
- [ ] T007 Implement response recording error mapping in `src/lib/invitation_errors.py`
- [ ] T008 [P] Add structured logging with request/trace IDs for invitation access, responses, and failures in `src/lib/audit_log.py`

**Checkpoint**: Foundation ready

---

## Phase 3: User Story 1 - Accept Review Invitation (Priority: P1) 🎯 MVP

**Goal**: Reviewer can accept a pending invitation and the assignment is recorded with confirmation.

**Independent Test**: Accepting a pending invitation records acceptance, assigns the paper, and shows confirmation.

### Implementation for User Story 1

- [ ] T009 [P] [US1] Implement invitation service to accept invitations in `src/services/invitation_service.py`
- [ ] T010 [US1] Create assignment on acceptance in `src/services/invitation_service.py`
- [ ] T011 [US1] Implement accept handler in `src/lib/invitations_controller.py`
- [ ] T012 [US1] Wire accept route in `src/lib/routes.py`
- [ ] T013 [US1] Add acceptance confirmation messaging in `src/lib/invitations_presenter.py`

**Checkpoint**: User Story 1 independently complete

---

## Phase 4: User Story 2 - Reject Review Invitation (Priority: P1)

**Goal**: Reviewer can reject a pending invitation and the editor is notified.

**Independent Test**: Rejecting a pending invitation records rejection, does not assign the paper, notifies editor, and shows confirmation.

### Implementation for User Story 2

- [ ] T014 [P] [US2] Implement invitation service to reject invitations in `src/services/invitation_service.py`
- [ ] T015 [US2] Trigger editor notification on rejection in `src/services/invitation_service.py`
- [ ] T016 [US2] Implement reject handler in `src/lib/invitations_controller.py`
- [ ] T017 [US2] Wire reject route in `src/lib/routes.py`
- [ ] T018 [US2] Add rejection confirmation messaging in `src/lib/invitations_presenter.py`

**Checkpoint**: User Story 2 independently complete

---

## Phase 5: User Story 3 - Respond Without Email Delivery (Priority: P2)

**Goal**: Reviewer can respond in the CMS even when email delivery fails.

**Independent Test**: Invitation is visible in CMS and response is recorded despite email failure.

### Implementation for User Story 3

- [ ] T019 [US3] Ensure pending invitations list is available without email link in `src/services/invitation_service.py`
- [ ] T020 [US3] Log email delivery failure in `src/lib/audit_log.py`

**Checkpoint**: User Story 3 independently complete

---

## Phase 6: User Story 4 - Require Login to Respond (Priority: P2)

**Goal**: Unauthenticated reviewers are redirected to login and resume invitation flow.

**Independent Test**: Accessing invitations while logged out redirects to login and resumes after login.

### Implementation for User Story 4

- [ ] T021 [US4] Enforce unauthenticated redirect to login for invitations in `src/lib/routes.py`

**Checkpoint**: User Story 4 independently complete

---

## Phase 7: User Story 5 - Assignment Limit Reached (Priority: P2)

**Goal**: Acceptance is blocked when assignment limit is reached and editor is notified.

**Independent Test**: Acceptance at limit is blocked with error and notification.

### Implementation for User Story 5

- [ ] T022 [US5] Enforce assignment limit check before acceptance in `src/services/invitation_service.py`
- [ ] T023 [US5] Map assignment-limit error to user-facing message in `src/lib/invitations_presenter.py`
- [ ] T024 [US5] Trigger editor notification on assignment limit in `src/services/invitation_service.py`

**Checkpoint**: User Story 5 independently complete

---

## Phase 8: User Story 6 - Error While Recording Response (Priority: P2)

**Goal**: Recording errors show a failure message and keep the invitation pending.

**Independent Test**: When recording fails, response is not saved and invitation remains pending.

### Implementation for User Story 6

- [ ] T025 [US6] Map recording error to user-facing message in `src/lib/invitations_presenter.py`
- [ ] T026 [US6] Ensure invitation remains pending on failure in `src/services/invitation_service.py`
- [ ] T027 [US6] Ensure sensitive error details are not exposed in `src/lib/invitations_presenter.py`

**Checkpoint**: User Story 6 independently complete

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Cross-cutting concerns for UC-12

- [ ] T028 [P] Update quickstart validation notes in `specs/012-receive-and-respond-to-review-invitation/quickstart.md`
- [ ] T029 [P] Update invitation access documentation in `specs/012-receive-and-respond-to-review-invitation/spec.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Stories (Phases 3-8)**: Depend on Foundational completion
- **Polish (Phase 9)**: Depends on all user stories completion

### User Story Dependencies

- **US1 (P1)**: Depends on Foundational tasks T003–T008
- **US2 (P1)**: Depends on Foundational tasks T003–T008
- **US3 (P2)**: Depends on Foundational tasks T003–T008
- **US4 (P2)**: Depends on Foundational tasks T003–T008
- **US5 (P2)**: Depends on Foundational tasks T003–T008
- **US6 (P2)**: Depends on Foundational tasks T003–T008

### Parallel Opportunities

- Phase 1: T002 can run in parallel with T001
- Phase 2: T003, T004, T005 can run in parallel; T006, T007, T008 can run in parallel after models are defined
- Phase 3: T009 can run in parallel with T013 once foundational utilities exist

---

## Parallel Example: User Story 1

```text
Task: "Implement invitation service to accept invitations in src/services/invitation_service.py"
Task: "Add acceptance confirmation messaging in src/lib/invitations_presenter.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1
2. Complete Phase 2
3. Complete Phase 3 (US1)
4. Validate against AT-UC12 scenarios

### Incremental Delivery

- Deliver US1 first, then add US2–US6 in priority order.
