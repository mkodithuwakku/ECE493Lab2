# Research: Register for Conference Attendance

## Decision 1: Use Existing CMS Language/Framework
- **Decision**: Use the existing CMS application language/version and framework already in the project.
- **Rationale**: The feature must integrate into the existing CMS stack with no new language or framework introduced.
- **Alternatives considered**: Introducing a new service or framework (rejected due to stack constraint and scope).

## Decision 2: Use Existing CMS Testing Tooling
- **Decision**: Use the existing CMS testing tooling for executing AT-UC24-* acceptance tests.
- **Rationale**: The acceptance tests are the source of truth; using the current tooling ensures consistency with existing test practices.
- **Alternatives considered**: Adding new test tooling (rejected due to stack constraint and unnecessary overhead).

## Decision 3: Use Existing Registration and Attendance Data Stores
- **Decision**: Use existing CMS data stores for attendee registrations, attendance types, and audit logging.
- **Rationale**: UC-24 requires registration persistence and validation of attendance types; the CMS already manages these entities.
- **Alternatives considered**: Introducing a separate storage or logging system (rejected due to scope and constraints).

## Decision 4: Performance/Scale Expectations
- **Decision**: No new performance targets beyond current CMS baseline; registration is frequent but within standard user load expectations.
- **Rationale**: UC-24 does not define additional performance constraints and acceptance tests do not require them.
- **Alternatives considered**: Establishing new performance SLAs (rejected due to lack of requirement and test coverage).
