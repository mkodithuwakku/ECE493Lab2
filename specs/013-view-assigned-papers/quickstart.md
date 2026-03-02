# Quickstart: UC-13 View Assigned Papers

## Purpose
Validate that reviewers can view their assigned papers and that access/error states match AT-UC13.

## Preconditions
- CMS is running and accessible.
- Reviewer account exists.
- Reviewer may have assigned papers depending on the test.

## View Assigned Papers (AT-UC13-01)
1. Log in as reviewer.
2. Navigate to Assigned Papers.
3. Verify list shows assigned papers with identifying info and that selecting a paper opens its detail/review page (if supported).

## Not Logged In (AT-UC13-02)
1. Attempt to access Assigned Papers while logged out.
2. Verify redirect to login and resume after login.

## No Assigned Papers (AT-UC13-03)
1. Log in as reviewer with no assignments.
2. Navigate to Assigned Papers.
3. Verify clear "no assigned papers" message and no misleading placeholders.

## Retrieval Error (AT-UC13-04)
1. Log in as reviewer.
2. Simulate retrieval error.
3. Verify error message, no partial data, and safe navigation elsewhere.
