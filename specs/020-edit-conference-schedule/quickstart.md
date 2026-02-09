# Quickstart: UC-20 Edit Conference Schedule

## Purpose
Validate conference configuration updates and error handling aligned to AT-UC20.

## Preconditions
- CMS is running and accessible.
- Administrator account exists and is authorized.
- Conference configuration page is available.

## Update Parameters Successfully (AT-UC20-01)
1. Log in as administrator.
2. Open Conference Configuration.
3. Modify valid parameters (e.g., submission deadline).
4. Save changes and verify success message.
5. Refresh and verify values persist.
6. Verify relevant CMS behavior reflects updated configuration.

## Administrator Not Logged In / Not Authorized (AT-UC20-02)
1. Attempt to access configuration while logged out and verify redirect to login.
2. Log in as non-admin and attempt access/save.
3. Verify access denied and no changes saved.

## Invalid Parameter Values (AT-UC20-03)
1. Enter invalid values (missing required field, invalid format).
2. Attempt to save.
3. Verify field-level validation errors and no persistence.

## Invalid Date Relationships (AT-UC20-04)
1. Enter invalid date relationships (submission after review, review after conference start).
2. Attempt to save.
3. Verify date-constraint error and no persistence.

## Configuration Retrieval Fails (AT-UC20-05)
1. Simulate retrieval failure.
2. Open configuration page.
3. Verify error message and no partial data displayed.

## Fail to Store Updated Parameters (AT-UC20-06)
1. Simulate save failure.
2. Submit valid changes.
3. Verify error message and no persistence after refresh.
