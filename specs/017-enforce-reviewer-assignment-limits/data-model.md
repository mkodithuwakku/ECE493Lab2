# Data Model: UC-17 Enforce Reviewer Assignment Limits

## Entities

### Reviewer
- id (unique)
- name
- email
- assignment_count
- assignment_limit

### Paper
- id (unique)
- title

### Assignment
- reviewer_id
- paper_id
- status (assigned)

## Relationships
- Reviewer 0..* Assignment
- Paper 0..* Assignment

## Validation Rules
- Reviewer assignment count must be retrieved before assignment decision.
- Assignments are allowed only when assignment_count < assignment_limit.
- Assignment count is updated on successful assignment.
- If count retrieval fails, no assignment is created.
- If update fails, assignment is rolled back to a consistent state.
