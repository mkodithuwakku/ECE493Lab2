# Data Model: UC-13 View Assigned Papers

## Entities

### Reviewer
- id (unique)
- name
- email

### AssignedPaper
- paper_id
- title
- reviewer_id

## Relationships
- Reviewer 0..* AssignedPaper

## Validation Rules
- Only assigned papers linked to the reviewer are shown.
- AssignedPaper must include paper_id and title (or other identifying info).
