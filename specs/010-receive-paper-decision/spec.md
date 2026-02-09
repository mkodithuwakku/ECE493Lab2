# UC-10: Receive Paper Acceptance or Rejection Decision

## Summary
Authors need to view the final acceptance or rejection decision for their submitted papers. The system must present the decision on the author’s submissions page, handle unauthenticated access, and communicate when the decision is unavailable or cannot be retrieved.

## Use Case Scope
- UC-10: Receive Paper Acceptance or Rejection Decision
- Acceptance tests used: AT-UC10-01, AT-UC10-02, AT-UC10-03, AT-UC10-04, AT-UC10-05
- Branch mapping: `010-receive-paper-acceptance-or-rejection-decision` → UC-10

## Assumptions
- A final decision (accept/reject) exists only after the review process is complete.
- Decision information is visible only to the author(s) of the paper.
- Email notification behavior and decision explanation guidance are out of scope because they are not covered by AT-UC10 tests.

## User Stories (Prioritized)
- **P1 / US1**: As an Author, I want to view the final decision (Accepted/Rejected) for my submission so I can learn the outcome. (AT-UC10-01)
- **P1 / US2**: As an Author, I want to be told when a decision is not yet available so I know to check back later. (AT-UC10-02)
- **P1 / US3**: As a Visitor, I must be redirected to login when accessing decision details so decision data stays protected. (AT-UC10-03)
- **P1 / US4**: As an Author, I want a clear error message if the decision cannot be retrieved so I know the system failed. (AT-UC10-04)
- **P1 / US5**: As an Author, I want a clear “data unavailable” message during critical failures so I understand the decision is inaccessible. (AT-UC10-05)

## User Scenarios & Testing
- View decision successfully for a submitted paper. (AT-UC10-01)
- Attempt to view a decision that is not yet available. (AT-UC10-02)
- Attempt to access decision information while not logged in. (AT-UC10-03)
- Encounter an error while retrieving the decision. (AT-UC10-04)
- Encounter a critical system failure that makes decision data unavailable. (AT-UC10-05)

## Functional Requirements
- FR-1: The system shall display the final decision (Accepted or Rejected) for a selected submitted paper to a logged-in author when a decision exists. (AT-UC10-01)
- FR-2: The system shall ensure the displayed decision corresponds to the selected paper. (AT-UC10-01)
- FR-3: The system shall restrict decision visibility to the paper’s author(s). (AT-UC10-01)
- FR-4: When no final decision is recorded, the system shall indicate that the decision is not yet available and shall not display an acceptance or rejection result. (AT-UC10-02)
- FR-5: Unauthenticated users attempting to access decision information shall be redirected to the login page and denied access to the decision until authenticated. (AT-UC10-03)
- FR-6: If an error occurs during decision retrieval, the system shall display an error message and shall not show incorrect or partial decision information. (AT-UC10-04)
- FR-7: If a critical system failure prevents decision access, the system shall report that decision data is unavailable and shall not show any acceptance or rejection result. (AT-UC10-05)

## Non-Functional Requirements
- NFR-1: Decision access and failure events shall be logged with a request/trace identifier and without sensitive data. (Critical flow)

## Success Criteria
- 100% of logged-in authors with recorded decisions can view the correct decision for their selected paper without error. (AT-UC10-01)
- 100% of attempts to view decisions that are not yet recorded show a clear “not yet available” status and no acceptance/rejection result. (AT-UC10-02)
- 100% of unauthenticated access attempts are redirected to login and do not reveal decision data. (AT-UC10-03)
- 100% of simulated retrieval errors present an explicit error message and no partial/incorrect decision details. (AT-UC10-04)
- 100% of simulated critical failures report decision data as unavailable and show no decision result. (AT-UC10-05)

## Key Entities
- Author
- Paper Submission
- Decision (Accepted/Rejected)
- Decision Status
