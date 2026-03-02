# Data Model: Submit a Paper Manuscript (UC-06)

**Date**: 2026-02-08

## Entities

### PaperSubmission

- **Purpose**: Represents an in-progress or submitted paper by an author.
- **Fields**:
  - `id` (identifier)
  - `author_id` (identifier)
  - `status` (enum: draft, submitted)
  - `created_at` (timestamp)

### ManuscriptFile

- **Purpose**: Uploaded manuscript associated with a submission.
- **Fields**:
  - `id` (identifier)
  - `submission_id` (identifier)
  - `filename` (text)
  - `format` (text: pdf, docx, tex)
  - `size_bytes` (integer)
  - `storage_uri` (text)
  - `uploaded_at` (timestamp)

### UploadAttempt

- **Purpose**: Represents a single upload transaction.
- **Fields**:
  - `id` (identifier)
  - `submission_id` (identifier)
  - `status` (enum: success, invalid_format, size_exceeded, interrupted, storage_failed)
  - `created_at` (timestamp)

## Relationships

- PaperSubmission has one ManuscriptFile per submission.
- UploadAttempt is associated with PaperSubmission.

## Validation Rules

- `format` must be PDF, Word, or LaTeX.
- `size_bytes` must be within configured max size.
- Only authenticated authors with active submission may upload.

## State Transitions

- PaperSubmission `status`: draft -> submitted when upload succeeds and submission completes (outside UC-06).
- UploadAttempt `status`: set based on validation/storage outcome.
