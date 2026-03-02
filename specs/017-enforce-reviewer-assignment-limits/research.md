# Research: UC-17 Enforce Reviewer Assignment Limits

## Decisions

- Decision: Use existing CMS stack and reviewer assignment workflow to enforce limits.
  Rationale: Project guidelines require existing CMS stack and the limit check is part of assignment flow.
  Alternatives considered: Separate limit-check microservice (rejected due to scope/stack constraints).

- Decision: Use existing reviewer assignment data store to retrieve and update assignment counts.
  Rationale: Existing store already tracks reviewer assignments; reuse avoids duplication.
  Alternatives considered: Maintain a separate limit-tracking store (rejected as unnecessary complexity).

- Decision: Use explicit, user-safe error messages for limit reached and failure conditions.
  Rationale: Aligns with UC-17 clarification and acceptance tests.
  Alternatives considered: Generic error messages (rejected due to ambiguity).
