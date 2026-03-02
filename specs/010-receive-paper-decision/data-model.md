# Data Model: UC-10 Receive Paper Acceptance or Rejection Decision

## Entities

### Author
- id (unique)
- name
- email

### PaperSubmission
- id (unique)
- title
- author_ids (one or more Author ids)
- decision_status (enum: not_recorded | recorded)
- decision_value (enum: accepted | rejected, nullable when not recorded)

### Decision
- submission_id (PaperSubmission id)
- value (accepted | rejected)
- recorded_at (timestamp)

## Relationships
- Author 1..* PaperSubmission (a submission has one or more authors)
- PaperSubmission 0..1 Decision (a submission may have no decision until recorded)

## Validation Rules
- decision_value is required only when decision_status is recorded.
- decision_value must be either accepted or rejected.
- Only author_ids associated with the submission may view the decision.

## State Transitions
- decision_status: not_recorded -> recorded when the final decision is stored.
