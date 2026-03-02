# Quickstart: UC-07 Upload Paper Manuscript File

## Goal
Validate the manuscript upload flow against AT-UC07-01 through AT-UC07-05.

## Prerequisites
- CMS is running and accessible
- Author account exists and is authenticated
- Author has started a paper submission

## Scenarios

### AT-UC07-01 Upload Manuscript Successfully
1. Navigate to the manuscript upload step in the submission flow.
2. Select a supported file (PDF/Word/LaTeX) within the size limit.
3. Confirm upload.
4. Expect validation success, storage, association, and confirmation message.

### AT-UC07-02 Unsupported File Format
1. Attempt upload with an unsupported format file.
2. Expect an error listing acceptable formats and no stored file.
3. Retry with a supported file to confirm success path.

### AT-UC07-03 File Exceeds Maximum Allowed Size
1. Attempt upload with a supported file exceeding the size limit.
2. Expect an error indicating the maximum file size and no stored file.
3. Retry with a smaller supported file to confirm success path.

### AT-UC07-04 Upload Interrupted
1. Start uploading a valid file.
2. Interrupt the upload (e.g., network interruption).
3. Expect an upload failure message and the ability to retry.

### AT-UC07-05 Storage Failure
1. Simulate storage or server error during upload.
2. Expect a storage failure message and no association with the submission.
