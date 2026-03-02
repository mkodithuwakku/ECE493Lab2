# Research: UC-21 Generate Conference Schedule

## Decisions

- Decision: Use existing CMS stack and schedule generation workflow for assigning accepted papers to time slots and rooms.
  Rationale: Project guidelines require the existing CMS stack and UC-21 focuses on initial schedule generation.
  Alternatives considered: Separate scheduling service (rejected due to scope/stack constraints).

- Decision: Do not persist any schedule when constraints are unsatisfiable.
  Rationale: AT-UC21-03 expects no schedule stored on constraint failure.
  Alternatives considered: Persist partial schedules (rejected due to test mismatch).

- Decision: Constraint errors identify insufficient resource type (e.g., rooms/time slots).
  Rationale: Clarified requirement helps administrators adjust parameters and retry.
  Alternatives considered: Generic constraint error (rejected for lower usability).
