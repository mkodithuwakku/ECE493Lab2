# Data Model: UC-14 Access Review Form for Assigned Paper

## Entities

### Reviewer
- id (unique)
- name
- email
- role (reviewer)

### Paper
- id (unique)
- title

### Assignment
- reviewer_id
- paper_id

### ReviewForm
- paper_id
- status (available/unavailable)

### Manuscript
- paper_id
- availability (available/unavailable)

## Relationships
- Reviewer 0..* Assignment
- Paper 0..* Assignment
- Paper 0..1 ReviewForm
- Paper 0..1 Manuscript

## Validation Rules
- Reviewer must be authenticated before accessing any review form.
- Reviewer may access review form and manuscript only for papers they are assigned to.
- If Manuscript is unavailable, review form access is blocked and a clear message is shown.
- If ReviewForm is unavailable due to system error, access fails with a generic user-safe error message.
