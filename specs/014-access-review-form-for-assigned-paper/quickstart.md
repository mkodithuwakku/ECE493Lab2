# Quickstart: UC-14 Access Review Form for Assigned Paper

## Purpose
Validate reviewer access to assigned paper review forms and error handling in line with AT-UC14.

## Preconditions
- CMS is running and accessible.
- Reviewer account exists.
- Reviewer has at least one assigned paper unless testing unassigned access.

## Access Review Form Successfully (AT-UC14-01)
1. Log in as reviewer.
2. Navigate to Assigned Papers.
3. Select an assigned paper.
4. Open Review Form.
5. Verify the review form loads, paper details match, and manuscript access is available.

## Reviewer Not Logged In (AT-UC14-02)
1. Attempt to access a review form URL while logged out.
2. Verify redirect to login and no review content displayed.
3. Log in and retry; verify normal access to assigned paper review form.

## Paper Not Assigned to Reviewer (AT-UC14-03)
1. Log in as reviewer.
2. Attempt to access a review form for an unassigned paper (direct URL or other means).
3. Verify access is denied with a generic authorization error and no content displayed.

## Manuscript File Not Available (AT-UC14-04)
1. Log in as reviewer.
2. Select an assigned paper whose manuscript is unavailable.
3. Attempt to open the review form.
4. Verify access is blocked and a clear manuscript-unavailable message is shown.

## System Error Retrieving Review Form (AT-UC14-05)
1. Log in as reviewer.
2. Select an assigned paper.
3. Simulate review form retrieval failure.
4. Verify a generic user-safe error message is shown and no partial data is displayed.
