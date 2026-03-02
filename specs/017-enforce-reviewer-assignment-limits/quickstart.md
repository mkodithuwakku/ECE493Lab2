# Quickstart: UC-17 Enforce Reviewer Assignment Limits

## Purpose
Validate reviewer assignment limit enforcement and failure handling in line with AT-UC17.

## Preconditions
- CMS is running and accessible.
- Editor account exists.
- Submitted paper exists.
- Reviewers with various assignment counts exist.

## Below Limit (AT-UC17-01)
1. Log in as editor.
2. Select a submitted paper.
3. Assign a reviewer below the limit.
4. Verify assignment created, count updated, and confirmation shown.

## At Limit (AT-UC17-02)
1. Select a reviewer at the limit.
2. Attempt assignment.
3. Verify “Reviewer at assignment limit.” message and no assignment created.

## Would Exceed Limit (AT-UC17-03)
1. Select a reviewer one below the limit.
2. Attempt assignments that would exceed the limit.
3. Verify the exceeding assignment is blocked with “Reviewer at assignment limit.”

## Count Retrieval Failure (AT-UC17-04)
1. Simulate count retrieval failure.
2. Attempt assignment.
3. Verify “Assignment cannot be completed at this time.” and no assignment created.

## Update Failure After Allowing (AT-UC17-05)
1. Select reviewer below limit.
2. Simulate update failure during assignment.
3. Verify “Assignment could not be completed.” and rollback to consistent state.
