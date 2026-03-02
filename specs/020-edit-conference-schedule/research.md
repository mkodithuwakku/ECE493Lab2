# Research: UC-20 Edit Conference Schedule

## Decisions

- Decision: Use existing CMS stack and configuration update workflow for conference parameters.
  Rationale: Project guidelines require the existing CMS stack and UC-20 focuses on parameter updates.
  Alternatives considered: Separate configuration service (rejected due to scope/stack constraints).

- Decision: Scope strictly to configuration parameters (deadlines/dates), not published schedule grid editing.
  Rationale: AT-UC20 tests address configuration updates and validation, not schedule grid edits.
  Alternatives considered: Include grid editing (rejected due to test misalignment).

- Decision: Validate and display all applicable errors together for invalid values and date relationships.
  Rationale: Clarified requirement reduces back-and-forth and improves admin usability.
  Alternatives considered: First-error-only validation (rejected).
