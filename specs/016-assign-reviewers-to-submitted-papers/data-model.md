# Data Model: UC-16 Assign Reviewers to Submitted Papers

## Entities

### Editor
- id (unique)
- name
- email

### Reviewer
- id (unique)
- name
- email
- assignment_count
- assignment_limit

### Paper
- id (unique)
- title
- status (submitted)

### Assignment
- reviewer_id
- paper_id
- status (assigned)

### Notification
- reviewer_id
- paper_id
- delivery_status (sent/failed)

## Relationships
- Paper 0..* Assignment
- Reviewer 0..* Assignment
- Editor 0..* Assignment (created_by)
- Assignment 0..1 Notification

## Validation Rules
- Only authenticated editors can create assignments.
- Reviewer must exist and be eligible before assignment.
- Duplicate reviewer-paper assignments are blocked.
- Reviewer assignment limit is enforced.
- If notification delivery fails, assignment is still stored and failure is reported.
- If storage fails, assignment is not stored and error is shown.
