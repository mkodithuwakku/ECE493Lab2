# Research: Pay Conference Registration Fee

## Decision 1: Use Existing CMS Language/Framework
- **Decision**: Use the existing CMS application language/version and framework already in the project.
- **Rationale**: The feature must integrate into the existing CMS stack with no new language or framework introduced.
- **Alternatives considered**: Introducing a new service or framework (rejected due to stack constraint and scope).

## Decision 2: Use Existing CMS Testing Tooling
- **Decision**: Use the existing CMS testing tooling for executing AT-UC25-* acceptance tests.
- **Rationale**: The acceptance tests are the source of truth; using the current tooling ensures consistency with existing test practices.
- **Alternatives considered**: Adding new test tooling (rejected due to stack constraint and unnecessary overhead).

## Decision 3: Use Existing Payment Gateway and Data Stores
- **Decision**: Use existing CMS payment gateway configuration and payment/registration data stores.
- **Rationale**: UC-25 requires payment processing and recording; the CMS already integrates with a gateway and stores registration status.
- **Alternatives considered**: Introducing a new gateway or separate payment store (rejected due to scope and constraints).

## Decision 4: Performance/Scale Expectations
- **Decision**: No new performance targets beyond current CMS baseline; payment is user-facing but within standard user load expectations.
- **Rationale**: UC-25 does not define additional performance constraints and acceptance tests do not require them.
- **Alternatives considered**: Establishing new performance SLAs (rejected due to lack of requirement and test coverage).
