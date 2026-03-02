# Research: Publish Conference Schedule

## Decision 1: Use Existing CMS Language/Framework
- **Decision**: Use the existing CMS application language/version and framework already in the project.
- **Rationale**: The feature must integrate into the existing CMS stack with no new language or framework introduced.
- **Alternatives considered**: Introducing a new service or framework (rejected due to stack constraint and scope).

## Decision 2: Use Existing CMS Testing Tooling
- **Decision**: Use the existing CMS testing tooling for executing AT-UC23-* acceptance tests.
- **Rationale**: The acceptance tests are the source of truth; using the current tooling ensures consistency with existing test practices.
- **Alternatives considered**: Adding new test tooling (rejected due to stack constraint and unnecessary overhead).

## Decision 3: Use Existing Schedule Data Store and Audit Logging
- **Decision**: Use existing CMS schedule data storage and existing audit logging capabilities for publication status changes.
- **Rationale**: UC-23 requires published status persistence and auditability; the CMS already handles schedules and admin actions.
- **Alternatives considered**: Introducing a separate storage or logging system (rejected due to scope and constraints).

## Decision 4: Performance/Scale Expectations
- **Decision**: No new performance targets beyond current CMS baseline; publication is an infrequent admin action (once per conference).
- **Rationale**: UC-23 does not define additional performance constraints, and the action frequency is low.
- **Alternatives considered**: Establishing new performance SLAs (rejected due to lack of requirement and test coverage).
