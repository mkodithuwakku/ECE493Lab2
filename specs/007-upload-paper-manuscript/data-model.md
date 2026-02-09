# Data Model: UC-07 Upload Paper Manuscript File

## Entities

### PaperSubmission
- **Represents**: The current paper submission in progress.
- **Key fields**: submission_id, author_id, status
- **Relationships**: Has one ManuscriptFile (current upload)

### ManuscriptFile
- **Represents**: A manuscript file uploaded for a submission.
- **Key fields**: file_id, submission_id, filename, format, size, storage_location, created_at
- **Relationships**: Belongs to one PaperSubmission

### UploadAttempt
- **Represents**: A single upload transaction and its outcome.
- **Key fields**: attempt_id, submission_id, status, failure_reason, occurred_at
- **Relationships**: Associated with one PaperSubmission and optionally a ManuscriptFile

## Validation Rules

- File format must be one of: PDF, Word, LaTeX.
- File size must be within the system-defined maximum limit.
- On interruption or storage failure, no ManuscriptFile association is persisted.

## State Transitions

- **UploadAttempt.status**: `started` → `validated` → `stored` → `associated`
- **Failure paths**: `started` → `failed_format` | `failed_size` | `failed_interruption` | `failed_storage`
