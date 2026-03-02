# Data Model: UC-18 Receive Notification of Submitted Reviews

## Entities

### Editor
- id (unique)
- name
- email
- role (editor)

### Reviewer
- id (unique)
- name
- email
- role (reviewer)

### Paper
- id (unique)
- title
- assigned_reviewer_ids

### Review
- id (unique)
- reviewer_id
- paper_id
- submitted_at
- status (submitted)
- content_summary (as permitted)

### ReviewStatus
- paper_id
- reviews_received
- reviewers_assigned
- last_updated_at

### Notification
- id (unique)
- editor_id
- paper_id
- type (review_submitted)
- delivery_status (delivered/failed)
- created_at

## Relationships
- Editor 1..* Notification
- Paper 1..* Review
- Paper 1..1 ReviewStatus
- Reviewer 0..* Review

## Validation Rules
- Review submissions update ReviewStatus counts for the associated paper.
- Notifications are generated only for editors authorized for the paper.
- ReviewStatus reflects all submitted reviews for a paper.
- Notification delivery failures do not prevent ReviewStatus updates.
- Retrieval errors return user-safe messages and do not expose internal details.
