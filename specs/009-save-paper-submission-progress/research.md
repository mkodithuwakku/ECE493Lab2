# Research: UC-09 Save Paper Submission Progress

## Decisions

### 1. Use existing CMS save-draft flow and storage services
- **Decision**: Reuse the current CMS draft save mechanism and storage service.
- **Rationale**: Minimizes change while meeting UC-09 validation and persistence requirements.
- **Alternatives considered**: Introduce a new draft subsystem specific to submissions.

### 2. Fixed minimum draft fields with save-anyway
- **Decision**: Require minimum draft fields (title, abstract, at least one author) and allow save-anyway to create an incomplete draft.
- **Rationale**: Matches UC-09 extension flow and clarifications.
- **Alternatives considered**: Block all saves without minimum fields.

### 3. Structured logging with redaction
- **Decision**: Add structured logging with trace IDs and redact submission content.
- **Rationale**: Required by constitution for critical flows.
- **Alternatives considered**: Rely on existing logging defaults.
