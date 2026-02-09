# Data Model: UC-08 Provide Paper Metadata

## Entities

### PaperSubmission
- **Represents**: The current paper submission in progress.
- **Key fields**: submission_id, author_id, status
- **Relationships**: Has one PaperMetadata (current metadata)

### PaperMetadata
- **Represents**: Required metadata for a paper submission.
- **Key fields**:
  - author_names
  - affiliations
  - contact_email
  - abstract
  - keywords
  - paper_source
  - updated_at
- **Validation**:
  - contact_email must be valid format
  - abstract must be non-empty, max 3000 characters
  - keywords max 10 entries
  - reject unsupported characters

### MetadataValidationResult
- **Represents**: Validation outcome for a metadata submission.
- **Key fields**: status (valid, missing_fields, invalid_fields, validation_error), message
- **Relationships**: Associated with a PaperSubmission

## State Transitions

- **MetadataValidationResult.status**: `valid` → `stored` | `missing_fields` | `invalid_fields` | `validation_error`
- **Storage failure**: validation succeeds but persistence fails; no metadata stored
