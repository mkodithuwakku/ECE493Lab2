# Quickstart: UC-08 Provide Paper Metadata

## Goal
Validate the metadata entry flow against AT-UC08-01 through AT-UC08-05.

## Prerequisites
- CMS is running and accessible
- Author account exists and is authenticated
- Author has started a paper submission

## Scenarios

### AT-UC08-01 Save Paper Metadata Successfully
1. Navigate to the metadata entry step in the submission flow.
2. Enter all required metadata fields (valid email, abstract <= 3000 chars, <= 10 keywords).
3. Submit the metadata form.
4. Expect validation success, storage, and confirmation message.

### AT-UC08-02 Missing Required Metadata Fields
1. Submit metadata with required fields missing.
2. Expect a summary error message and no stored metadata.

### AT-UC08-03 Invalid Metadata Information
1. Submit metadata with invalid values (e.g., invalid email, unsupported characters).
2. Expect a summary validation error message and no stored metadata.

### AT-UC08-04 System Fails to Validate Metadata
1. Submit valid metadata while simulating a validation subsystem failure.
2. Expect a validation failure message and no stored metadata.

### AT-UC08-05 System Fails to Store Metadata
1. Submit valid metadata while simulating a storage failure.
2. Expect a storage failure message and no stored metadata.
