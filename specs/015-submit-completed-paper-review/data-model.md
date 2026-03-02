# Data Model: UC-15 Submit Completed Paper Review

## Entities

### Reviewer
- id (unique)
- name
- email
- role (reviewer)

### Paper
- id (unique)
- title

### ReviewForm
- paper_id
- required_fields
- allowed_values

### Review
- reviewer_id
- paper_id
- field_values
- status (submitted/not_submitted)

## Relationships
- Reviewer 0..* Review
- Paper 0..* Review
- Paper 0..1 ReviewForm

## Validation Rules
- Reviewer must be authenticated before submitting a review.
- Reviewer may submit only for papers they are assigned to.
- Required review fields must be present and valid; errors must identify specific fields.
- Duplicate submissions for the same reviewer-paper pair are blocked.
- On storage failure, no review is stored and an error is shown.
