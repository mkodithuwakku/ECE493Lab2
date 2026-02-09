# Quickstart: UC-16 Assign Reviewers to Submitted Papers

## Purpose
Validate reviewer assignment behavior and error handling in line with AT-UC16.

## Preconditions
- CMS is running and accessible.
- Editor account exists.
- Submitted papers exist.
- Eligible reviewers exist as needed per test.

## Assign One Reviewer (AT-UC16-01)
1. Log in as editor.
2. Navigate to Paper Management.
3. Select a submitted paper.
4. Assign one eligible reviewer and confirm.
5. Verify assignment recorded, reviewer listed, and confirmation shown.

## Assign Multiple Reviewers (AT-UC16-02)
1. Log in as editor.
2. Select a submitted paper.
3. Assign multiple eligible reviewers and confirm.
4. Verify all assignments recorded and listed; confirmation shown.

## Not Logged In / Not Authorized (AT-UC16-03)
1. Attempt to access assignment while logged out.
2. Verify redirect to login.
3. Log in as non-editor and attempt assignment.
4. Verify authorization error and no assignments created.

## Invalid Reviewer Email/Identifier (AT-UC16-04)
1. Log in as editor.
2. Enter invalid reviewer email/identifier and attempt assignment.
3. Verify error indicates not found or invalid email and no assignment stored.

## Duplicate Assignment (AT-UC16-05)
1. Assign a reviewer to a paper.
2. Attempt to assign the same reviewer again.
3. Verify “Reviewer already assigned.” message and no duplicate stored.

## Assignment Limit Reached (AT-UC16-06)
1. Select a reviewer at assignment limit.
2. Attempt assignment.
3. Verify workload-limit message and no assignment created.

## Notification Failure (AT-UC16-07)
1. Simulate notification failure.
2. Assign eligible reviewer.
3. Verify delivery failure message and assignment recorded.

## Storage Failure (AT-UC16-08)
1. Simulate storage failure.
2. Attempt assignment.
3. Verify error and no assignment stored.
