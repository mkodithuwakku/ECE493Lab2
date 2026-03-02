# Research: UC-18 Receive Notification of Submitted Reviews

## Decisions

- Decision: Use existing CMS stack and notification workflow for review-submission alerts.
  Rationale: Project guidelines require the existing CMS stack and UC-18 focuses on notification delivery and status visibility.
  Alternatives considered: Separate notification subsystem (rejected due to scope/stack constraints).

- Decision: Use existing reviews/submissions data store for review status updates and retrieval.
  Rationale: Review status already derives from stored reviews; reuse avoids duplication.
  Alternatives considered: Dedicated review-status store (rejected as unnecessary complexity).

- Decision: Provide editor access via authenticated notification and paper management views, with clear errors on retrieval failures.
  Rationale: Matches AT-UC18 expected results and failure handling requirements.
  Alternatives considered: Silent failure or generic error messaging (rejected due to test expectations).
