# Research: View Public Conference Information (UC-01)

**Date**: 2026-02-08

## Decision: Reuse existing CMS stack

**Rationale**: The feature is a read-only public homepage flow and does not
require new languages or frameworks beyond the existing CMS baseline.

**Alternatives considered**:
- Introduce a new standalone service for public info (rejected: unnecessary for
  UC-01 scope).

## Decision: Web application architecture (frontend + backend)

**Rationale**: UC-01 is explicitly web-based and accessed via a browser; a
frontend page and backend data retrieval align with standard CMS patterns.

**Alternatives considered**:
- Single-process monolith without separation (rejected: reduces clarity between
  data retrieval and UI rendering).

## Decision: Use existing test framework for AT-UC01-* cases

**Rationale**: Acceptance tests define observable outcomes; using the existing
framework avoids introducing new tooling and keeps focus on UC-01 behaviors.

**Alternatives considered**:
- New acceptance test tooling (rejected: unnecessary for a single use case).
