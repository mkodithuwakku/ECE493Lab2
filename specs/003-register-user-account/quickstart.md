# Quickstart: Register a New User Account (UC-03)

**Date**: 2026-02-08

## Purpose

Validate the UC-03 registration flow for new users.

## Steps

1. Start the existing CMS application using the project’s standard run steps.
2. Open a web browser and navigate to the CMS website.
3. Select the option to register a new account.
4. Verify the registration form displays and accepts valid inputs.
5. Submit valid registration information and confirm redirect to login without
   authentication. (AT-UC03-01)
6. Validate alternate/error states by preparing the system state and resubmitting:
   - Invalid or incomplete fields show validation errors and allow correction.
     (AT-UC03-02)
   - Duplicate email shows "Email is already registered." and no account is created.
     (AT-UC03-03)
   - Invalid password shows "Password must be at least 8 characters and include a non-letter character."
     and allows correction.
     (AT-UC03-04)
   - Storage failure shows "Registration failed. Please try again." and no account is created.
     (AT-UC03-05)
