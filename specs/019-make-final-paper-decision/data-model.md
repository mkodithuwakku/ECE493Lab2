# Data Model: UC-19 Make Final Paper Decision

## Entities

### Editor
- id (unique)
- name
- email
- role (editor)

### Author
- id (unique)
- name
- email
- role (author)

### Paper
- id (unique)
- title
- review_status (complete/incomplete)
- decision_status (undecided/accepted/rejected)

### Review
- id (unique)
- paper_id
- reviewer_id
- submitted_at
- status (submitted)

### Decision
- id (unique)
- paper_id
- decision_value (accept/reject)
- decided_by_editor_id
- decided_at
- locked (true)

### Notification
- id (unique)
- author_id
- paper_id
- type (decision_recorded)
- delivery_status (delivered/failed)
- created_at

## Relationships
- Paper 1..* Review
- Paper 0..1 Decision
- Editor 0..* Decision
- Author 0..* Notification
- Paper 0..* Notification

## Validation Rules
- Final decisions are allowed only when review_status is complete.
- Decision is locked after recording and cannot be edited.
- Decision status updates from undecided to accepted or rejected only once.
- Notification delivery failure does not affect decision recording.
- Authors can view decisions only for their own papers.
