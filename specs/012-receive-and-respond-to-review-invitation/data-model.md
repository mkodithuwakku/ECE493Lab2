# Data Model: UC-12 Receive and Respond to Review Invitation

## Entities

### Reviewer
- id (unique)
- name
- email
- assignment_count

### ReviewInvitation
- id (unique)
- reviewer_id
- paper_id
- status (enum: pending | accepted | rejected)

### PaperAssignment
- reviewer_id
- paper_id
- assigned_at

### EditorNotification
- id (unique)
- reviewer_id
- paper_id
- type (enum: rejection | assignment_limit)
- created_at

## Relationships
- Reviewer 1..* ReviewInvitation
- Reviewer 0..* PaperAssignment
- ReviewInvitation 0..1 PaperAssignment (created on acceptance)

## Validation Rules
- Invitations can be accepted only when status is pending.
- Accepting an invitation creates a PaperAssignment.
- Rejecting an invitation does not create a PaperAssignment.
- Assignment limit prevents acceptance when reviewer assignment_count is at max.

## State Transitions
- ReviewInvitation status: pending -> accepted | rejected
