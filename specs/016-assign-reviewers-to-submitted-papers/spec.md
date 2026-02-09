# Feature Specification: Assign Reviewers to Submitted Papers

**Feature Branch**: `016-assign-reviewers-to-submitted-papers`  
**Created**: 2026-02-09  
**Status**: Draft  
**Input**: User description: "Generate the specification for UC-16 only. Use UC-16 from GeneratedUseCases.md and ONLY acceptance tests AT-UC16-* from GeneratedTestSuites.md. Ignore all other use cases and tests. Do not invent requirements or flows; derive functional requirements directly from UC-16 main and extension flows and ensure each requirement is verifiable by the provided acceptance tests. Fill the “Use Case Scope” section with UC-16 and list the AT-UC16 tests used."

## Use Case Scope *(mandatory)*

- **Use Case**: UC-16 - Assign Reviewers to Submitted Papers
- **Acceptance Tests**: AT-UC16-01, AT-UC16-02, AT-UC16-03, AT-UC16-04, AT-UC16-05, AT-UC16-06, AT-UC16-07, AT-UC16-08


## Clarifications

### Session 2026-02-09

- Q: How specific should invalid reviewer error messages be? → A: Message must state not found vs invalid email.


- Q: What should the duplicate assignment message say? → A: Explicit 'Reviewer already assigned.' message.


- Q: When notification delivery fails, should the assignment still be recorded? → A: Yes, record assignment and notify editor of delivery failure.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Assign Reviewer to Paper (Priority: P1)

An editor assigns one eligible reviewer to a submitted paper and sees confirmation.

**Why this priority**: This is the core assignment flow and enables the review process to start.

**Independent Test**: Can be fully tested by assigning one eligible reviewer to a submitted paper and verifying the assignment appears on the paper.

**Acceptance Scenarios**:

1. **Given** a logged-in editor with a submitted paper and an eligible reviewer, **When** the editor assigns the reviewer, **Then** the assignment is stored, the reviewer appears in the paper’s reviewer list, and a confirmation is shown.

---

### User Story 2 - Assign Multiple Reviewers (Priority: P2)

An editor assigns multiple eligible reviewers to the same submitted paper and sees confirmation.

**Why this priority**: Many papers require multiple reviewers and assignments must scale beyond a single reviewer.

**Independent Test**: Can be fully tested by assigning two or more eligible reviewers to the same paper and verifying each appears on the paper.

**Acceptance Scenarios**:

1. **Given** a logged-in editor with a submitted paper and multiple eligible reviewers, **When** the editor assigns them, **Then** all assignments are stored and listed with confirmation.

---

### User Story 3 - Require Authorization (Priority: P3)

Only authenticated, authorized editors can assign reviewers; unauthenticated or unauthorized users are blocked.

**Why this priority**: Prevents unauthorized assignment changes.

**Independent Test**: Can be fully tested by attempting assignment while logged out or as a non-editor and confirming access is blocked.

**Acceptance Scenarios**:

1. **Given** a user is not logged in, **When** they attempt to access reviewer assignment, **Then** they are redirected to login and cannot assign reviewers.
2. **Given** a logged-in non-editor, **When** they attempt to assign a reviewer, **Then** access is denied and no assignment is created.

---

### User Story 4 - Reject Invalid Reviewer (Priority: P4)

Assignments fail when the reviewer identifier/email is invalid or not registered.

**Why this priority**: Prevents assignments to non-existent reviewers.

**Independent Test**: Can be fully tested by entering an invalid reviewer identifier/email and confirming rejection with an error message.

**Acceptance Scenarios**:

1. **Given** a logged-in editor and a submitted paper, **When** the editor enters an invalid reviewer identifier/email, **Then** the system rejects the assignment and displays an error indicating reviewer not found or invalid email.

---

### User Story 5 - Prevent Duplicate Assignment (Priority: P5)

The system prevents assigning the same reviewer to the same paper more than once.

**Why this priority**: Avoids duplicate assignments and inconsistent reviewer lists.

**Independent Test**: Can be fully tested by re-assigning an already assigned reviewer and confirming the system blocks it.

**Acceptance Scenarios**:

1. **Given** a reviewer already assigned to a paper, **When** the editor attempts to assign the same reviewer again, **Then** the system blocks the assignment and shows “Reviewer already assigned.”

---

### User Story 6 - Enforce Assignment Limits (Priority: P6)

Assignments are blocked when the reviewer’s workload limit has been reached.

**Why this priority**: Ensures workload limits are enforced during assignment.

**Independent Test**: Can be fully tested by attempting to assign a reviewer who is at the assignment limit and confirming the system blocks it.

**Acceptance Scenarios**:

1. **Given** a reviewer at their assignment limit, **When** the editor attempts to assign them, **Then** the system blocks the assignment and shows a workload-limit message.

---

### User Story 7 - Handle Notification Failure (Priority: P7)

If invitation/notification delivery fails, the editor is informed and the system either records or rolls back the assignment, but does so explicitly.

**Why this priority**: Notification failures must be visible and consistent with assignment state.

**Independent Test**: Can be fully tested by simulating notification failure and verifying editor messaging and assignment state.

**Acceptance Scenarios**:

1. **Given** an assignment attempt during notification failure, **When** the editor assigns a reviewer, **Then** the editor is informed of the failure and the system records the assignment, explicitly indicating that invitation delivery failed.

---

### User Story 8 - Handle Storage Failure (Priority: P8)

If the system fails to store an assignment, the editor sees an error and no assignment is stored.

**Why this priority**: Prevents false success and ensures consistency.

**Independent Test**: Can be fully tested by simulating a storage failure and verifying no assignment is stored.

**Acceptance Scenarios**:

1. **Given** a storage failure during assignment, **When** the editor confirms an assignment, **Then** the system shows an error and no assignment is stored.

---

### Edge Cases

- What happens when an unauthenticated or unauthorized user attempts assignment?
- What happens when an invalid reviewer identifier/email is provided?
- How does the system handle duplicate assignment attempts?
- How does the system handle reviewer workload limit violations?
- How does the system behave when notification delivery fails?
- How does the system behave when storage fails to persist the assignment?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow an authenticated editor to assign one eligible reviewer to a submitted paper and show a confirmation message that states the assignment succeeded and identifies the paper and reviewer.
- **FR-002**: System MUST allow an authenticated editor to assign multiple eligible reviewers to the same submitted paper and show a confirmation message that states the assignment succeeded and identifies the paper and the list/count of reviewers.
- **FR-003**: System MUST redirect unauthenticated users to login and MUST prevent non-editors from assigning reviewers.
- **FR-004**: System MUST reject assignments for invalid or unregistered reviewer identifiers/emails and display an error indicating reviewer not found or invalid email.
- **FR-005**: System MUST prevent duplicate reviewer assignments for the same paper and display “Reviewer already assigned.”
- **FR-006**: System MUST block assignments when reviewer workload limits are reached and display a workload-limit message stating the reviewer cannot be assigned due to workload limits.
- **FR-007**: System MUST record reviewer assignments in the database and show assigned reviewers in the paper’s reviewer list.
- **FR-008**: When notification delivery fails, System MUST inform the editor and MUST record the assignment, explicitly indicating that invitation delivery failed.
- **FR-009**: When storage fails to persist the assignment, System MUST display an error and MUST NOT store the assignment.
- **FR-010**: If notifications are enabled, System MUST initiate an invitation/notification for each assigned reviewer.

### Key Entities *(include if feature involves data)*

- **Editor**: Authorized user who assigns reviewers to papers.
- **Reviewer**: Eligible user who can be assigned to review papers.
- **Paper**: Submitted paper requiring reviewer assignments.
- **Assignment**: Link between a reviewer and a paper.
- **Notification/Invitation**: Message sent to reviewers upon assignment.

## Assumptions

- Notification delivery is enabled by system configuration unless explicitly disabled.
- Reviewer recommendation or expertise matching is out of scope unless covered by AT-UC16 tests.
- Editor overrides for assignment limits are out of scope unless covered by AT-UC16 tests.

## Interfaces & Contracts *(mandatory)*

- **Reviewer Assignment Flow**: Editor assigns reviewer(s) to a submitted paper; system validates eligibility, stores assignments, and confirms success or error.
- **Authentication/Authorization Gate**: Only authenticated editors can assign reviewers; unauthenticated users are redirected to login, non-editors receive an authorization error.
- **Duplicate Assignment Handling**: Duplicate reviewer assignment attempts are blocked with “Reviewer already assigned.”
- **Notification Delivery**: On assignment, invitation/notification is initiated; if delivery fails, editor is informed and the assignment is recorded with delivery failure indicated.

## Security & Privacy Considerations *(mandatory)*

- **AuthN/AuthZ**: Only authenticated editors can assign reviewers to papers.
- **Sensitive Data**: Reviewer contact identifiers/emails must not be exposed to unauthorized users.
- **Auditability**: Assignment attempts, authorization denials, duplicate assignments, workload-limit violations, notification failures, and storage failures should be observable for support and troubleshooting.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of unauthenticated assignment attempts are redirected to login and do not create assignments.
- **SC-002**: 100% of non-editor assignment attempts are blocked with an authorization error.
- **SC-003**: 100% of invalid reviewer identifiers/emails are rejected with a clear error and no assignment stored.
- **SC-004**: 100% of duplicate assignment attempts do not create duplicate assignments.
- **SC-005**: 100% of workload-limit violations are blocked with a workload-limit message.
- **SC-006**: 100% of storage failures show an error and do not store assignments.
- **SC-007**: At least 95% of eligible assignments complete with confirmation and correct reviewer list update under normal conditions.
