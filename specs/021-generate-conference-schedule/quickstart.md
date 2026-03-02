# Quickstart: UC-21 Generate Conference Schedule

## Purpose
Validate schedule generation and error handling aligned to AT-UC21.

## Preconditions
- CMS is running and accessible.
- Administrator account exists and is authorized.
- Accepted papers exist (unless testing no-accepted-papers flow).
- Scheduling resources are available and sufficient (unless testing constraint failures).

## Generate Schedule Successfully (AT-UC21-01)
1. Log in as administrator.
2. Navigate to Conference Scheduling.
3. Select Generate Conference Schedule.
4. Verify schedule is generated, stored, and displayed.
5. Refresh and verify schedule persists.

## No Accepted Papers (AT-UC21-02)
1. Ensure no accepted papers exist.
2. Attempt schedule generation.
3. Verify clear error message and no schedule stored.

## Unsatisfiable Constraints (AT-UC21-03)
1. Configure insufficient rooms or time slots.
2. Attempt schedule generation.
3. Verify constraint violation message identifying resource type and no schedule stored.
4. Adjust parameters and retry; verify schedule generated and stored.

## Generation Failure (AT-UC21-04)
1. Simulate generation failure.
2. Attempt schedule generation.
3. Verify error message and no schedule stored.

## Storage Failure (AT-UC21-05)
1. Simulate storage failure during save.
2. Attempt schedule generation.
3. Verify save error and no schedule stored after refresh.
