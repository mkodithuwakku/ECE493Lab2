# Research: UC-19 Make Final Paper Decision

## Decisions

- Decision: Use existing CMS stack and decision-recording workflow for final accept/reject actions.
  Rationale: Project guidelines require the existing CMS stack and UC-19 focuses on recording final decisions within the CMS.
  Alternatives considered: Separate decision service (rejected due to scope/stack constraints).

- Decision: Use existing reviews/submissions data store to verify review completion before decisions.
  Rationale: Review completion is derived from stored reviews; reuse avoids duplication.
  Alternatives considered: Separate decision-eligibility store (rejected as unnecessary complexity).

- Decision: Provide immediate author portal visibility after decision recording, even if notifications fail.
  Rationale: Matches AT-UC19-06 and clarified decision visibility requirement.
  Alternatives considered: Wait for notification success (rejected due to test expectations).

- Decision: Lock final decisions after recording (no edits).
  Rationale: Clarified requirement prevents conflicting outcomes and aligns with UC-19 scope.
  Alternatives considered: Allow edits (rejected to avoid re-notification complexity).
