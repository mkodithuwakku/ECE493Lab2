# Data Model: UC-09 Save Paper Submission Progress

## Entities

### PaperSubmissionDraft
- **Represents**: A saved draft state of a submission.
- **Key fields**: draft_id, submission_id, author_id, status, updated_at
- **Relationships**: References SubmissionData

### SubmissionData
- **Represents**: Current submission inputs and uploaded assets.
- **Key fields**: title, abstract, authors, metadata, files
- **Validation**:
  - Minimum draft fields required: title, abstract, at least one author
  - Invalid data must be detected before save

### DraftStatus
- **Represents**: Whether the draft is complete or incomplete.
- **Values**: complete, incomplete

## State Transitions

- **DraftStatus**: `incomplete` → `complete` when minimum fields are present and data validates
- **Save-anyway**: missing minimum fields → draft stored with status `incomplete`
- **Storage failure**: draft not persisted
