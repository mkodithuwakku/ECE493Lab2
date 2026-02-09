# Acceptance Test Suites
Prompt:
Attached are the lab assignment pdf, the srs document pdf, and the generated use cases in markdown format. Please generate an acceptance test suite for use case 1 that adheres to the lab assignment description. Please generate the output in markdown format that I can copy and paste into a markdown file.

## Acceptance Test Suite — UC-01: View Public Conference Information

---

### Use Case Under Test

**Use Case ID:** UC-01  
**Use Case Name:** View Public Conference Information  
**Primary Actor:** Guest (Unregistered User)  
**Goal:** Allow a public user to view conference announcements and general information without logging in.

---

### Acceptance Criteria

The system satisfies UC-01 if:

- A guest user can access the CMS homepage without authentication.
- Public conference announcements and information are displayed when available.
- The system provides appropriate feedback for all defined alternate and failure flows.
- All main and alternate flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- User accesses the system using a modern web browser.
- User is not logged in and has no registered account.
- Public conference information is marked as visible to guests.

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC01-01  | Main Success Scenario |
| AT-UC01-02  | Extension 3a – Website Unavailable |
| AT-UC01-03  | Extension 4a – No Public Information Available |
| AT-UC01-04  | Extension 4b – Partial Content Load Failure |
| AT-UC01-05  | Failure End Scenario – Content Retrieval Error |

---

### Acceptance Test Cases

---

#### AT-UC01-01 — View Public Conference Information (Main Success Scenario)

**Purpose:**  
Verify that a guest user can successfully view public conference announcements and information.

**Preconditions:**
- CMS is running and accessible.
- Public conference announcements exist.
- User is not logged in.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS homepage URL.
3. Observe that the homepage loads successfully.
4. Locate the public announcements or conference information section.

**Expected Results:**
- Homepage loads without errors.
- Public announcements and conference information are displayed.
- No login or registration is required to view the information.

---

#### AT-UC01-02 — Website Unavailable (Extension 3a)

**Purpose:**  
Verify system behavior when the CMS website is unavailable.

**Preconditions:**
- CMS server is offline or unreachable.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS homepage URL.

**Expected Results:**
- Homepage does not load.
- User is shown a clear error message indicating the website is unavailable.
- No conference information is displayed.

---

#### AT-UC01-03 — No Public Conference Information Available (Extension 4a)

**Purpose:**  
Verify system behavior when no public announcements or conference information exist.

**Preconditions:**
- CMS is accessible.
- No public announcements or conference information are stored in the system.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS homepage URL.
3. Observe the public announcements section.

**Expected Results:**
- Homepage loads successfully.
- System displays a message indicating that no public conference information is currently available.
- User is not shown empty or misleading content.

---

#### AT-UC01-04 — Partial Content Load Failure (Extension 4b)

**Purpose:**  
Verify system behavior when only part of the public information can be loaded.

**Preconditions:**
- CMS is accessible.
- Some public conference information exists.
- A partial system failure occurs during content loading.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS homepage URL.
3. Observe the public information section during loading.

**Expected Results:**
- Available conference information is displayed.
- System displays a warning indicating that some information could not be loaded.
- User is informed that the displayed information may be incomplete.

---

#### AT-UC01-05 — System Error During Content Retrieval (Failure End Scenario)

**Purpose:**  
Verify system behavior when a complete error occurs during content retrieval.

**Preconditions:**
- CMS homepage is reachable.
- Backend content retrieval fails due to a system error.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS homepage URL.
3. Allow the system to attempt loading public conference information.

**Expected Results:**
- System displays an error message indicating that information cannot be retrieved.
- No public conference information is displayed.
- Use case ends in failure due to system error.

### Completion Criteria

UC-01 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-02: View Conference Registration Prices

---

### Use Case Under Test

**Use Case ID:** UC-02  
**Use Case Name:** View Conference Registration Prices  
**Primary Actor:** Guest (Unregistered User)  
**Goal:** Allow a guest or unregistered visitor to view conference registration prices in order to decide whether to attend the conference.

---

### Acceptance Criteria

The system satisfies UC-02 if:

- A guest user can access the registration pricing information without authentication.
- The system displays registration prices based on attendance types.
- The system provides appropriate feedback for all defined alternate and failure flows.
- All main and alternate flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- User accesses the system using a modern web browser.
- User is not logged in and has no registered account.
- Conference registration pricing information may be complete, missing, partially available, or unavailable due to system error (depending on the test).
- Pricing is expected to be presented in a readable format (e.g., list/table) to support decision-making.

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC02-01  | Main Success Scenario |
| AT-UC02-02  | Extension 3a – Pricing Information Not Available |
| AT-UC02-03  | Extension 4a – Error Retrieving Pricing Data |
| AT-UC02-04  | Extension 5a – Partial Pricing Information Available |

---

### Acceptance Test Cases

---

#### AT-UC02-01 — View Conference Registration Prices (Main Success Scenario)

**Purpose:**  
Verify that a guest user can successfully view the complete conference registration price list.

**Preconditions:**
- CMS is running and accessible.
- Conference registration pricing information exists in the system.
- User is not logged in.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS website URL.
3. Select the option/link to view conference registration information (pricing).
4. Allow the system to retrieve the registration price list.
5. Review the displayed registration prices.

**Expected Results:**
- The registration pricing page/section loads without errors.
- The system displays the complete registration price list.
- Prices are displayed based on attendance types (e.g., categories of attendees).
- No login or registration is required to view the pricing information.

---

#### AT-UC02-02 — Pricing Information Not Available (Extension 3a)

**Purpose:**  
Verify system behavior when no registration pricing data exists.

**Preconditions:**
- CMS is running and accessible.
- No pricing data exists in the system (empty or not configured).
- User is not logged in.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS website URL.
3. Select the option/link to view conference registration prices.

**Expected Results:**
- The pricing page/section loads (or attempts to load).
- The system displays a message indicating that registration prices are not currently available.
- No incorrect, placeholder, or misleading pricing is displayed.

---

#### AT-UC02-03 — Error Retrieving Pricing Data (Extension 4a)

**Purpose:**  
Verify system behavior when the system encounters an error retrieving registration pricing information.

**Preconditions:**
- CMS is running and accessible.
- Pricing data exists, but the system fails during retrieval (e.g., database/service failure).
- User is not logged in.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS website URL.
3. Select the option/link to view conference registration prices.
4. Allow the system to attempt retrieval of pricing data (with retrieval failure simulated/observed).

**Expected Results:**
- The system displays an error message indicating a temporary system issue.
- Registration prices are not displayed (or are clearly indicated as unavailable due to error).
- The error feedback is user-friendly (no internal stack traces or sensitive details shown).

---

#### AT-UC02-04 — Partial Pricing Information Available (Extension 5a)

**Purpose:**  
Verify system behavior when only some pricing information is available.

**Preconditions:**
- CMS is running and accessible.
- Some pricing data exists, but some required pricing fields/categories are missing or cannot be retrieved.
- User is not logged in.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS website URL.
3. Select the option/link to view conference registration prices.
4. Allow the system to retrieve whatever pricing data is available.
5. Review the displayed pricing information.

**Expected Results:**
- The system displays the pricing information that is available.
- The system displays a warning indicating that some pricing details may be incomplete.
- The warning is clear and visible near the pricing information.

---

### Completion Criteria

UC-02 is considered accepted when all test cases pass and all defined flows (main and alternate) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-03: Register a New User Account

---

### Use Case Under Test

**Use Case ID:** UC-03  
**Use Case Name:** Register a New User Account  
**Primary Actor:** User (Unregistered Visitor)  
**Secondary Actor(s):** Email Service  
**Goal:** Allow a new user to create an account in the CMS so they can access authorized system functionalities.

---

### Acceptance Criteria

The system satisfies UC-03 if:

- An unregistered user can access the registration workflow from the CMS website.
- The system displays a registration form and accepts valid registration data.
- The system validates input and provides clear, actionable error messages for invalid data.
- The system prevents registration with an email address that already exists.
- The system enforces password security requirements and explains those requirements when violated.
- The system creates and stores a new user account when all validation passes.
- After successful registration, the user is redirected to the login page.
- The system provides appropriate feedback when account creation/storage fails.
- All main and alternate flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- User accesses the system using a modern web browser.
- User is not logged in and has no registered account (unless specified by a test’s preconditions).
- The CMS has a registration page/form accessible from the website.
- The system performs server-side validation on required fields (e.g., email format, required fields, password rules).
- The system uses a database to store users.
- The system may interact with an Email Service (even if no verification is required, the actor exists in the use case).

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC03-01  | Main Success Scenario |
| AT-UC03-02  | Extension 5a – Invalid or Incomplete Registration Information |
| AT-UC03-03  | Extension 7a – Email Address Already Exists |
| AT-UC03-04  | Extension 7b – Password Does Not Meet Security Requirements |
| AT-UC03-05  | Extension 8a – System Fails to Store User Information |

---

### Acceptance Test Cases

---

#### AT-UC03-01 — Register a New User Account (Main Success Scenario)

**Purpose:**  
Verify that an unregistered user can successfully register a new account and is redirected to the login page.

**Preconditions:**
- CMS is running and accessible.
- The test email address is not already registered.
- User is not logged in.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS website.
3. Select the option to register a new account.
4. Confirm the system displays the registration form.
5. Enter valid required information (including a unique email address and a valid password).
6. Submit the registration form.
7. Observe the system response after submission.

**Expected Results:**
- The system validates the entered information successfully.
- A new user account is created and stored in the database.
- The system redirects the user to the login page.
- The user remains unlogged-in (registration does not automatically authenticate unless explicitly designed to do so).

---

#### AT-UC03-02 — Invalid or Incomplete Registration Information (Extension 5a)

**Purpose:**  
Verify that the system detects missing/invalid fields, shows validation errors, and allows resubmission after correction.

**Preconditions:**
- CMS is running and accessible.
- User is not logged in.
- The test email address used (if any) is not already registered.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS website.
3. Select the option to register a new account.
4. Confirm the registration form is displayed.
5. Enter invalid or incomplete information (e.g., omit required fields, malformed email format, empty password).
6. Submit the registration form.
7. Observe validation feedback.
8. Correct the invalid/incomplete fields with valid values.
9. Resubmit the registration form.

**Expected Results:**
- The system detects missing or invalid form fields.
- The system displays clear validation error messages indicating what must be fixed.
- The account is not created while inputs are invalid.
- After correction and resubmission, the use case proceeds to validation and (if valid) continues toward account creation.

---

#### AT-UC03-03 — Email Address Already Exists (Extension 7a)

**Purpose:**  
Verify that the system prevents duplicate account creation when the email address is already registered.

**Preconditions:**
- CMS is running and accessible.
- A user account already exists with the test email address.
- User is not logged in.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS website.
3. Select the option to register a new account.
4. Confirm the registration form is displayed.
5. Enter required information using an email address that is already registered.
6. Enter a valid password meeting security requirements.
7. Submit the registration form.

**Expected Results:**
- The system detects the duplicate email address.
- The system displays an error message indicating the email is already registered.
- The system does not create a new user account.
- The user is not redirected to the login page due to successful registration.
- The user remains on the registration form (or an appropriate error state) and can choose to update the email or abandon registration.

---

#### AT-UC03-04 — Password Does Not Meet Security Requirements (Extension 7b)

**Purpose:**  
Verify that the system enforces password security requirements and provides guidance when the password is weak/non-compliant.

**Preconditions:**
- CMS is running and accessible.
- The test email address is not already registered.
- User is not logged in.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS website.
3. Select the option to register a new account.
4. Confirm the registration form is displayed.
5. Enter a unique, valid email address.
6. Enter a password that violates security requirements (e.g., too short, missing required character types, etc.).
7. Submit the registration form.
8. Observe password validation feedback.
9. Enter a new password that meets the security requirements.
10. Resubmit the registration form.

**Expected Results:**
- The system detects that the password violates security standards.
- The system displays password requirement guidelines (or a clear message describing what is required).
- The account is not created while the password is invalid.
- After entering a compliant password and resubmitting, the use case proceeds to validation and (if valid) continues toward account creation.

---

#### AT-UC03-05 — System Fails to Store User Information (Extension 8a)

**Purpose:**  
Verify system behavior when account creation/storage fails due to a database or server error.

**Preconditions:**
- CMS is running and accessible.
- The test email address is not already registered.
- User is not logged in.
- A database/server failure is simulated during account creation/storage.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS website.
3. Select the option to register a new account.
4. Confirm the registration form is displayed.
5. Enter valid required information (unique email + valid password).
6. Submit the registration form.
7. Simulate/observe a failure during account storage (e.g., database down, server error).

**Expected Results:**
- The system encounters a database or server error during storage.
- The system displays an error message indicating registration failure.
- The user account is not created (no partial/invalid user record is stored).
- The user is not redirected to the login page due to success.
- The user remains unregistered and may abandon the registration attempt.

---

### Completion Criteria

UC-03 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.


## Acceptance Test Suite — UC-04: Log In to the System

---

### Use Case Under Test

**Use Case ID:** UC-04  
**Use Case Name:** Log In to the System  
**Primary Actor:** Registered User  
**Goal:** Allow a registered user to authenticate with the CMS in order to access authorized system functionalities and their personalized homepage.

---

### Acceptance Criteria

The system satisfies UC-04 if:

- A registered user can log in using valid credentials.
- The user is redirected to their personalized homepage upon successful login.
- The system validates login input and provides clear feedback for missing or invalid credentials.
- The system prevents access for locked or disabled accounts.
- The system provides appropriate error messages when authentication services are unavailable.
- All main and alternate flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- User accesses the system using a modern web browser.
- A registered user account exists in the system.
- The user account may be active, locked, or disabled depending on the test case.
- Login requires a username (or email) and password.

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC04-01  | Main Success Scenario |
| AT-UC04-02  | Extension 5a – Incomplete Login Information |
| AT-UC04-03  | Extension 7a – Incorrect Username or Password |
| AT-UC04-04  | Extension 7b – Account Locked or Disabled |
| AT-UC04-05  | Extension 7c – Authentication Service Unavailable |
| AT-UC04-06  | Failure End Scenario – Authentication Cannot Be Completed |

---

### Acceptance Test Cases

---

#### AT-UC04-01 — Log In Successfully (Main Success Scenario)

**Purpose:**  
Verify that a registered user can log in with valid credentials and is redirected to their personalized homepage.

**Preconditions:**
- CMS is running and accessible.
- A registered user account exists with valid credentials.
- The user account is active.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS website.
3. Select the option to log in.
4. Enter a valid username and valid password.
5. Submit the login form.

**Expected Results:**
- The system validates the credentials.
- The system authenticates the user.
- The user is redirected to their personalized homepage.
- No authentication error messages are displayed.

---

#### AT-UC04-02 — Missing Username or Password (Extension 5a)

**Purpose:**  
Verify system behavior when the user submits incomplete login information.

**Preconditions:**
- CMS is running and accessible.
- Login page is reachable.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS login page.
3. Leave the username field blank and enter any password.
4. Submit the login form.
5. Repeat the test leaving the password field blank and entering any username.

**Expected Results:**
- The system detects missing required fields.
- The system displays an error message requesting completion of required fields.
- The user remains on the login page and is not authenticated.

---

#### AT-UC04-03 — Incorrect Username or Password (Extension 7a)

**Purpose:**  
Verify system behavior when the user enters invalid login credentials.

**Preconditions:**
- CMS is running and accessible.
- A registered user account exists.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS login page.
3. Enter an incorrect username or an incorrect password.
4. Submit the login form.

**Expected Results:**
- The system detects invalid credentials.
- The system displays an authentication failure message.
- The user is not logged in and remains on the login page.
- The user may retry or abandon the login attempt.

---

#### AT-UC04-04 — Account Locked or Disabled (Extension 7b)

**Purpose:**  
Verify system behavior when the user account is locked or disabled.

**Preconditions:**
- CMS is running and accessible.
- A registered user account exists and is marked as locked or disabled.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS login page.
3. Enter the locked or disabled account’s valid username and valid password.
4. Submit the login form.

**Expected Results:**
- The system detects that the account is locked or disabled.
- The system displays a message indicating the account is inactive.
- The user is not authenticated and cannot access authorized features.

---

#### AT-UC04-05 — Authentication Service Unavailable (Extension 7c)

**Purpose:**  
Verify system behavior when the authentication service or supporting database is unavailable.

**Preconditions:**
- CMS login page is reachable.
- Authentication service or database is unavailable.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS login page.
3. Enter valid credentials for an active account.
4. Submit the login form.

**Expected Results:**
- The system fails to authenticate due to a service error.
- The system displays an error message indicating a temporary system issue.
- The user is not logged in and remains on the login page.

---

#### AT-UC04-06 — Authentication Cannot Be Completed (Failure End Scenario)

**Purpose:**  
Verify system behavior when a critical error prevents authentication from completing.

**Preconditions:**
- CMS login page is reachable.
- A critical server or database error occurs during authentication.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS login page.
3. Enter valid credentials for an active account.
4. Submit the login form.

**Expected Results:**
- The system displays an error message indicating authentication cannot be completed at this time.
- The user is not logged in and no session is created.
- The user is not redirected to the personalized homepage.
- The use case ends in failure.

---

### Completion Criteria

UC-04 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-05: Change User Password

---

### Use Case Under Test

**Use Case ID:** UC-05  
**Use Case Name:** Change User Password  
**Primary Actor:** Registered User  
**Goal:** Allow a logged-in registered user to change their account password to maintain account security.

---

### Acceptance Criteria

The system satisfies UC-05 if:

- A logged-in user can access account settings and initiate a password change.
- The system verifies the user’s current password before allowing a change.
- The system enforces password security requirements for the new password.
- The system prevents password changes when the new password and confirmation do not match.
- The system provides clear error or success feedback for all defined alternate and failure flows.
- All main and alternate flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- User accesses the system using a modern web browser.
- User is authenticated (logged in) unless otherwise specified.
- Password security requirements are defined by the system (e.g., minimum length, complexity).
- The CMS provides an **Account Settings** or **Profile** page with a **Change Password** option.

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC05-01  | Main Success Scenario |
| AT-UC05-02  | Extension 5a – Current Password Incorrect |
| AT-UC05-03  | Extension 6a – New Password Does Not Meet Security Requirements |
| AT-UC05-04  | Extension 6b – New Password and Confirmation Do Not Match |
| AT-UC05-05  | Extension 9a / Failure End Scenario – System Fails to Update Password |

---

### Acceptance Test Cases

---

#### AT-UC05-01 — Change User Password Successfully (Main Success Scenario)

**Purpose:**  
Verify that a logged-in user can successfully change their password when all inputs are valid.

**Preconditions:**
- CMS is running and accessible.
- User has a valid registered account.
- User is logged in.
- User knows their current password.

**Test Steps:**
1. Ensure the user is logged in to the CMS.
2. Navigate to **Account Settings** or **Profile**.
3. Select the **Change Password** option.
4. Enter the correct current password.
5. Enter a new password that meets security requirements.
6. Re-enter the new password in the confirmation field.
7. Submit the password change request.
8. Log out of the system.
9. Log in again using the new password.

**Expected Results:**
- The system validates the current password.
- The system accepts the new password and updates the account.
- A success message is displayed.
- The user can log in using the new password.
- The old password no longer works.

---

#### AT-UC05-02 — Incorrect Current Password (Extension 5a)

**Purpose:**  
Verify that the system rejects a password change when the current password is incorrect.

**Preconditions:**
- CMS is running and accessible.
- User is logged in.
- User account exists.

**Test Steps:**
1. Navigate to **Account Settings** → **Change Password**.
2. Enter an incorrect current password.
3. Enter a valid new password.
4. Confirm the same new password.
5. Submit the password change request.

**Expected Results:**
- The system detects the incorrect current password.
- An error message indicating the current password is incorrect is displayed.
- The password is not changed.
- The user remains logged in.

---

#### AT-UC05-03 — New Password Does Not Meet Security Requirements (Extension 6a)

**Purpose:**  
Verify that the system enforces password security rules for the new password.

**Preconditions:**
- CMS is running and accessible.
- User is logged in.
- User knows their current password.

**Test Steps:**
1. Navigate to **Account Settings** → **Change Password**.
2. Enter the correct current password.
3. Enter a new password that violates security requirements (e.g., too short or too weak).
4. Enter the same invalid password in the confirmation field.
5. Submit the password change request.

**Expected Results:**
- The system rejects the new password.
- An error message describing password requirements is displayed.
- The password is not changed.
- The user is prompted to enter a compliant password.

---

#### AT-UC05-04 — New Password and Confirmation Do Not Match (Extension 6b)

**Purpose:**  
Verify that the system prevents password changes when the confirmation does not match the new password.

**Preconditions:**
- CMS is running and accessible.
- User is logged in.
- User knows their current password.

**Test Steps:**
1. Navigate to **Account Settings** → **Change Password**.
2. Enter the correct current password.
3. Enter a valid new password.
4. Enter a different password in the confirmation field.
5. Submit the password change request.

**Expected Results:**
- The system detects the mismatch between the new password and confirmation.
- An error message indicating the mismatch is displayed.
- The password is not changed.
- The user is prompted to re-enter matching values.

---

#### AT-UC05-05 — System Fails to Update Password (Extension 9a / Failure End Scenario)

**Purpose:**  
Verify system behavior when a backend or database error prevents the password from being updated.

**Preconditions:**
- CMS is running and accessible.
- User is logged in.
- A backend or database failure is simulated during password update.

**Test Steps:**
1. Navigate to **Account Settings** → **Change Password**.
2. Enter the correct current password.
3. Enter a valid new password and confirm it correctly.
4. Submit the password change request while the failure condition exists.
5. Attempt to log out and log in using the new password.
6. Attempt to log in using the old password.

**Expected Results:**
- The system displays an error message indicating the password could not be updated.
- The password remains unchanged.
- The old password still allows login.
- The new password does not allow login.

---

### Completion Criteria

UC-05 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-06: Log Out of the System

---

### Use Case Under Test

**Use Case ID:** UC-06  
**Use Case Name:** Log Out of the System  
**Primary Actor:** Logged-in User  
**Goal:** Allow an authenticated user to securely log out of the CMS and terminate their session.

---

### Acceptance Criteria

The system satisfies UC-06 if:

- A logged-in user can initiate the logout action from the system.
- The system terminates the user’s authenticated session.
- The user is redirected to a public or login page after logout.
- The system prevents access to authenticated-only features after logout.
- The system handles logout-related system errors gracefully.
- All main and alternate flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- User accesses the system using a modern web browser.
- User is authenticated (logged in) before starting the use case.
- The CMS provides a visible **Log Out** option (e.g., button or menu item).
- Session management is handled by the backend (e.g., cookies, tokens).

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC06-01  | Main Success Scenario |
| AT-UC06-02  | Extension 4a – User Attempts Logout When Not Logged In |
| AT-UC06-03  | Extension 5a – Session Already Expired |
| AT-UC06-04  | Failure End Scenario – Logout Process Fails Due to System Error |

---

### Acceptance Test Cases

---

#### AT-UC06-01 — Log Out Successfully (Main Success Scenario)

**Purpose:**  
Verify that a logged-in user can successfully log out and that their session is terminated.

**Preconditions:**
- CMS is running and accessible.
- User is logged in with an active session.

**Test Steps:**
1. Ensure the user is logged in to the CMS.
2. Navigate to any authenticated page.
3. Select the **Log Out** option.
4. Observe the system response after logout.
5. Attempt to access a restricted (authenticated-only) page using the browser back button or direct URL.

**Expected Results:**
- The system terminates the user’s session.
- The user is redirected to the login page or a public homepage.
- Access to authenticated-only pages is denied after logout.
- The user is treated as a guest after logout.

---

#### AT-UC06-02 — Logout Attempt When Not Logged In (Extension 4a)

**Purpose:**  
Verify system behavior when a logout action is attempted without an active session.

**Preconditions:**
- CMS is running and accessible.
- User is not logged in.

**Test Steps:**
1. Open a web browser.
2. Navigate to the CMS website.
3. Attempt to access the logout URL directly or select **Log Out** if visible.

**Expected Results:**
- The system does not crash or throw an unhandled error.
- The system redirects the user to the login page or public homepage.
- The user remains unauthenticated.

---

#### AT-UC06-03 — Session Already Expired (Extension 5a)

**Purpose:**  
Verify system behavior when the user’s session has already expired before logout.

**Preconditions:**
- CMS is running and accessible.
- User was previously logged in.
- User session has expired due to timeout.

**Test Steps:**
1. Open a web browser with an expired session.
2. Attempt to select the **Log Out** option or navigate to the logout URL.

**Expected Results:**
- The system detects that the session is no longer valid.
- The system redirects the user to the login page or public homepage.
- The user is informed (optionally) that their session has expired.
- No authenticated session remains active.

---

#### AT-UC06-04 — Logout Fails Due to System Error (Failure End Scenario)

**Purpose:**  
Verify system behavior when a backend or server error occurs during logout.

**Preconditions:**
- CMS is running and accessible.
- User is logged in.
- A backend or session-handling failure is simulated during logout.

**Test Steps:**
1. Ensure the user is logged in.
2. Navigate to any authenticated page.
3. Select the **Log Out** option while the failure condition exists.

**Expected Results:**
- The system displays an error message indicating logout could not be completed.
- The user session may remain active or be partially terminated, but access control remains enforced.
- The system does not expose sensitive session information.
- The user is prompted to retry logout or close the session safely.

---

### Completion Criteria

UC-06 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-07: Upload Paper Manuscript File

---

### Use Case Under Test

**Use Case ID:** UC-07  
**Use Case Name:** Upload Paper Manuscript File  
**Primary Actor:** Author (Registered User)  
**Goal:** Allow an author to upload a paper manuscript file in an approved format so that it can be processed as part of a paper submission.

---

### Acceptance Criteria

The system satisfies UC-07 if:

- A logged-in author who has started a paper submission can access the manuscript upload workflow.
- The system accepts manuscript uploads only in supported formats (PDF, Word, LaTeX).
- The system enforces a maximum file size limit and provides a clear message when exceeded.
- The system validates the selected file before upload completion (format + size).
- The system stores the uploaded file and associates it with the correct (current) paper submission.
- The system displays a confirmation message on successful upload.
- The system provides clear error feedback and allows recovery (retry or re-select file) for all defined alternate/failure flows.
- All main and alternate flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- Author accesses the system using a modern web browser.
- Author is registered and logged in.
- Author has started a paper submission and is in the submission process when uploading.
- Supported file formats include: **PDF, Word, LaTeX**.
- The system has a defined maximum upload size (exact value is system-configured).
- The system uses a storage mechanism (e.g., file storage service) to store manuscript files.

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC07-01  | Main Success Scenario |
| AT-UC07-02  | Extension 4a – Selected File Format Not Supported |
| AT-UC07-03  | Extension 4b – Selected File Exceeds Maximum Allowed Size |
| AT-UC07-04  | Extension 6a – File Upload Is Interrupted |
| AT-UC07-05  | Extension 7a / Failure End Scenario – System Fails to Store Uploaded File |

---

### Acceptance Test Cases

---

#### AT-UC07-01 — Upload Manuscript Successfully (Main Success Scenario)

**Purpose:**  
Verify that a logged-in author can upload a valid manuscript file and that it is stored and associated with the current paper submission.

**Preconditions:**
- CMS is running and accessible.
- Author is registered and logged in.
- Author has started a paper submission and is in the submission process.
- A valid manuscript file exists on the author’s device:
  - Format: PDF/Word/LaTeX
  - Size: within the maximum allowed limit

**Test Steps:**
1. Ensure the author is logged in and currently in the paper submission process.
2. Select the option to **Upload Manuscript File**.
3. When prompted, choose a valid manuscript file in a supported format.
4. Confirm the file upload.
5. Wait for the system to process the upload.

**Expected Results:**
- The system validates file format and file size successfully.
- The system uploads and stores the manuscript file.
- The system associates the uploaded file with the current paper submission.
- The system displays a confirmation message indicating successful upload.

---

#### AT-UC07-02 — Unsupported File Format Selected (Extension 4a)

**Purpose:**  
Verify that the system rejects unsupported file formats and allows the author to select a supported file and continue.

**Preconditions:**
- CMS is running and accessible.
- Author is logged in.
- Author has started a paper submission and is in the submission process.
- An unsupported-format file exists on the author’s device (e.g., .txt, .png, .zip).

**Test Steps:**
1. Navigate to the manuscript upload step in the paper submission process.
2. Select **Upload Manuscript File**.
3. Choose a file with an unsupported format.
4. Confirm the file upload.
5. Observe the system feedback.
6. Choose a new file in a supported format (PDF/Word/LaTeX).
7. Confirm the upload again.

**Expected Results:**
- The system detects the unsupported file format.
- The system displays an error message listing acceptable formats (PDF, Word, LaTeX).
- The system does not upload/store the unsupported file.
- After selecting a supported file, the upload proceeds successfully (validation, storage, association, confirmation).

---

#### AT-UC07-03 — File Exceeds Maximum Allowed Size (Extension 4b)

**Purpose:**  
Verify that the system rejects files exceeding the maximum allowed size and allows the author to select a smaller file and continue.

**Preconditions:**
- CMS is running and accessible.
- Author is logged in.
- Author has started a paper submission and is in the submission process.
- A supported-format file exists that exceeds the maximum allowed size.

**Test Steps:**
1. Navigate to the manuscript upload step in the paper submission process.
2. Select **Upload Manuscript File**.
3. Choose a supported-format file that exceeds the maximum allowed size.
4. Confirm the file upload.
5. Observe the system feedback.
6. Choose a smaller supported-format file that is within the size limit.
7. Confirm the upload again.

**Expected Results:**
- The system detects that the file exceeds the size limit.
- The system displays an error message indicating the maximum file size.
- The system does not upload/store the oversized file.
- After selecting a smaller valid file, the upload proceeds successfully (validation, storage, association, confirmation).

---

#### AT-UC07-04 — Upload Interrupted During Transfer (Extension 6a)

**Purpose:**  
Verify that the system handles interrupted uploads gracefully and allows the author to retry.

**Preconditions:**
- CMS is running and accessible.
- Author is logged in.
- Author has started a paper submission and is in the submission process.
- A valid manuscript file exists (supported format, within size limit).
- A network interruption condition can be simulated (e.g., disable network during upload).

**Test Steps:**
1. Navigate to the manuscript upload step in the paper submission process.
2. Select **Upload Manuscript File**.
3. Choose a valid manuscript file and confirm the upload.
4. During the upload, simulate a network interruption.
5. Observe the system response.
6. Restore connectivity (if simulated).
7. Retry the upload (either by retry button or repeating the upload action).

**Expected Results:**
- The system detects the interruption during upload.
- The system displays an error message indicating the upload failed.
- The system does not confirm a successful upload and does not associate a partially uploaded file to the submission.
- The author can retry the upload.
- On a successful retry, the system stores the file, associates it with the submission, and displays a success confirmation.

---

#### AT-UC07-05 — System Fails to Store Uploaded File (Extension 7a / Failure End Scenario)

**Purpose:**  
Verify that the system provides appropriate feedback when storage fails and that the manuscript file is not associated with the submission.

**Preconditions:**
- CMS is running and accessible.
- Author is logged in.
- Author has started a paper submission and is in the submission process.
- A valid manuscript file exists (supported format, within size limit).
- A storage/server failure can be simulated during the “store file” step (e.g., storage service unavailable).

**Test Steps:**
1. Navigate to the manuscript upload step in the paper submission process.
2. Select **Upload Manuscript File**.
3. Choose a valid manuscript file and confirm the upload.
4. Simulate a storage/server error during the file storage step.
5. Observe the system response.
6. Check the paper submission state (e.g., uploaded file list/attachment section).

**Expected Results:**
- The system encounters a storage/server error while attempting to save the file.
- The system displays an error message indicating the file could not be saved/stored.
- The manuscript file is not associated with the paper submission.
- No success confirmation is displayed.
- The author may retry later; if the author abandons the attempt, the use case ends in failure (no file uploaded/associated).

---

### Completion Criteria

UC-07 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-08: Provide Paper Metadata

---

### Use Case Under Test

**Use Case ID:** UC-08  
**Use Case Name:** Provide Paper Metadata  
**Primary Actor:** Author (Registered User)  
**Goal:** Allow an author to enter complete and valid paper metadata so that the submission can be properly reviewed and managed.

---

### Acceptance Criteria

The system satisfies UC-08 if:

- A logged-in author who has started a paper submission can access the paper metadata entry/edit workflow.
- The system displays a metadata form containing required fields (e.g., author names, affiliations, contact info, abstract, keywords, paper source).
- The system validates required fields and rejects submissions with missing required data.
- The system validates field formats/content (e.g., email format, non-empty abstract, supported characters) and rejects invalid entries with clear feedback.
- On valid submission, the system stores the metadata and associates it with the correct paper submission.
- The system displays a confirmation message when metadata is saved successfully.
- The system handles validation and storage failures gracefully with a clear error message.
- All main and alternate flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- Author accesses the system using a modern web browser.
- Author is registered and logged in.
- Author has started a paper submission and is in the submission process.
- Required paper metadata fields are defined by the system and enforced server-side.
- Metadata is stored in a database and linked to the author’s current paper submission.

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC08-01  | Main Success Scenario |
| AT-UC08-02  | Extension 4a – Required Metadata Fields Missing |
| AT-UC08-03  | Extension 4b – Metadata Contains Invalid Information |
| AT-UC08-04  | Extension 6a – System Fails to Validate Metadata |
| AT-UC08-05  | Extension 7a / Failure End Scenario – System Fails to Store Metadata |

---

### Acceptance Test Cases

---

#### AT-UC08-01 — Save Paper Metadata Successfully (Main Success Scenario)

**Purpose:**  
Verify that a logged-in author can enter valid paper metadata and save it successfully for the current paper submission.

**Preconditions:**
- CMS is running and accessible.
- Author is logged in.
- Author has started a paper submission and is in the submission process.
- Valid metadata values are available (authors, affiliations, contact info, abstract, keywords, paper source).

**Test Steps:**
1. Ensure the author is logged in and currently in the paper submission process.
2. Select the option to **Enter/Edit Paper Metadata**.
3. Confirm the system displays the paper metadata form.
4. Enter valid values in all required fields (e.g., author names, affiliations, contact info, abstract, keywords, paper source).
5. Submit the metadata form.
6. Observe the system response after submission.
7. Navigate away and return to the metadata page (or reload) to verify persistence.

**Expected Results:**
- The system validates the metadata successfully.
- The system stores the metadata and associates it with the current paper submission.
- The system displays a confirmation message indicating the metadata was saved successfully.
- Previously entered metadata remains available on revisit/reload.

---

#### AT-UC08-02 — Missing Required Metadata Fields (Extension 4a)

**Purpose:**  
Verify that the system detects missing required metadata fields, provides clear feedback, and allows correction and resubmission.

**Preconditions:**
- CMS is running and accessible.
- Author is logged in.
- Author has started a paper submission.

**Test Steps:**
1. Navigate to **Enter/Edit Paper Metadata**.
2. Leave one or more required fields blank (e.g., abstract, author name, contact email, keywords).
3. Submit the metadata form.
4. Observe system feedback.
5. Fill in the previously missing required fields with valid values.
6. Resubmit the metadata form.

**Expected Results:**
- The system detects missing required fields.
- The system highlights missing fields and displays an error message indicating what is required.
- The system does not store incomplete metadata.
- After correcting missing fields and resubmitting, the system stores the metadata and shows a success confirmation.

---

#### AT-UC08-03 — Invalid Metadata Information (Extension 4b)

**Purpose:**  
Verify that the system detects invalid metadata entries, shows validation messages, and allows correction and resubmission.

**Preconditions:**
- CMS is running and accessible.
- Author is logged in.
- Author has started a paper submission.

**Test Steps:**
1. Navigate to **Enter/Edit Paper Metadata**.
2. Enter invalid values (examples):
   - Invalid email format in contact information (e.g., missing `@`).
   - Empty or whitespace-only abstract.
   - Unsupported characters (if the system restricts them).
3. Submit the metadata form.
4. Observe system feedback.
5. Correct the invalid values using valid inputs.
6. Resubmit the metadata form.

**Expected Results:**
- The system detects invalid entries and rejects the submission.
- The system displays clear validation error messages describing what is wrong.
- The system does not store invalid metadata.
- After correction and resubmission, the system stores the metadata and shows a success confirmation.

---

#### AT-UC08-04 — System Fails to Validate Metadata (Extension 6a)

**Purpose:**  
Verify system behavior when an internal error prevents validation from completing.

**Preconditions:**
- CMS is running and accessible.
- Author is logged in.
- Author has started a paper submission.
- An internal validation error can be simulated (e.g., validation service failure, server error during validation).

**Test Steps:**
1. Navigate to **Enter/Edit Paper Metadata**.
2. Enter valid metadata in all required fields.
3. Submit the metadata form while the validation failure condition exists.
4. Observe system feedback.
5. (Optional) Retry submission after removing the failure condition.

**Expected Results:**
- The system reports that validation failed due to a system issue.
- The system does not claim the metadata was saved.
- The system does not store partially validated data.
- The author can abandon or retry; if retried after recovery, the submission can proceed normally.

---

#### AT-UC08-05 — System Fails to Store Metadata (Extension 7a / Failure End Scenario)

**Purpose:**  
Verify system behavior when storage fails after successful validation.

**Preconditions:**
- CMS is running and accessible.
- Author is logged in.
- Author has started a paper submission.
- A database/server failure can be simulated during the metadata storage step.

**Test Steps:**
1. Navigate to **Enter/Edit Paper Metadata**.
2. Enter valid metadata in all required fields.
3. Submit the metadata form while the storage failure condition exists.
4. Observe system feedback.
5. Navigate away and return to the metadata page (or reload) to verify whether data persisted.

**Expected Results:**
- The system displays an error message indicating the metadata could not be saved.
- The system does not display a success confirmation.
- The metadata is not stored (or is not reliably persisted/associated with the submission).
- The author may retry later; if the author abandons the attempt, the use case ends in failure (metadata not stored).

---

### Completion Criteria

UC-08 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-09: Save Paper Submission Progress

---

### Use Case Under Test

**Use Case ID:** UC-09  
**Use Case Name:** Save Paper Submission Progress  
**Primary Actor:** Author (Registered User)  
**Goal:** Allow an author to save a paper submission at any stage so that work can be continued later without losing entered information.

---

### Acceptance Criteria

The system satisfies UC-09 if:

- A logged-in author who has started a paper submission can save their current progress as a draft.
- The system validates submission data during save and provides clear validation feedback when data is invalid.
- The system detects when required draft-level information is missing and warns the author appropriately.
- The system stores draft submission data in the database when the save operation succeeds.
- The system displays a confirmation message when the draft is saved successfully.
- The saved draft can be retrieved later and reflects the most recently saved changes.
- The system provides clear error feedback if the save operation fails due to a system/database error.
- All main and alternate flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- Author accesses the system using a modern web browser.
- Author is registered and logged in.
- Author has started a paper submission and is in the submission process.
- The system supports saving a submission as a **draft** in the database.
- “Required draft-level fields” represent the minimum data needed for a draft save (as defined by the system).

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC09-01  | Main Success Scenario |
| AT-UC09-02  | Extension 4a – Submission Data Contains Invalid Information |
| AT-UC09-03  | Extension 4b – Required Minimum Information Is Missing |
| AT-UC09-04  | Extension 5a / Failure End Scenario – System Fails to Store Submission Data |

---

### Acceptance Test Cases

---

#### AT-UC09-01 — Save Submission Progress Successfully (Main Success Scenario)

**Purpose:**  
Verify that an author can save the current submission progress as a draft and retrieve it later with the saved changes intact.

**Preconditions:**
- CMS is running and accessible.
- Author is logged in.
- Author has started a paper submission and is in the submission workflow.
- The current submission state contains valid data for saving.

**Test Steps:**
1. Ensure the author is logged in and in an active paper submission workflow.
2. Enter or update paper information and/or upload files (make at least one identifiable change).
3. Select the option to **Save** the submission.
4. Observe the system response.
5. Navigate away from the submission (e.g., dashboard/home).
6. Re-open the draft submission for editing.

**Expected Results:**
- The system validates the entered submission information.
- The system stores the submission data as a draft in the database.
- The system displays a confirmation message indicating the submission has been saved.
- When the draft is reopened, the previously saved changes are present.

---

#### AT-UC09-02 — Invalid Submission Data Prevents Save (Extension 4a)

**Purpose:**  
Verify that the system detects invalid or incomplete submission data, shows validation errors, and allows the author to correct issues and successfully save.

**Preconditions:**
- CMS is running and accessible.
- Author is logged in.
- Author has started a paper submission and is in the submission workflow.

**Test Steps:**
1. Navigate to an active paper submission draft.
2. Enter invalid or incomplete information in one or more fields (e.g., malformed email if present, missing required value, invalid format).
3. Select **Save**.
4. Observe the validation feedback.
5. Correct the invalid/incomplete information with valid values.
6. Select **Save** again.

**Expected Results:**
- The system detects invalid or incomplete submission data.
- The system displays validation error messages identifying the issues.
- The system does not save the draft while invalid data remains.
- After correction, the system saves the submission data as a draft and displays a confirmation message.

---

#### AT-UC09-03 — Required Minimum Draft Information Missing (Extension 4b)

**Purpose:**  
Verify that the system warns the author when required minimum draft-level information is missing, and supports the author’s choice to save anyway or cancel.

**Preconditions:**
- CMS is running and accessible.
- Author is logged in.
- Author has started a paper submission and is in the submission workflow.
- The submission is missing one or more required draft-level fields (as defined by the system).

**Test Steps (Save Anyway Path):**
1. Navigate to an active paper submission draft.
2. Ensure one or more required draft-level fields are missing.
3. Select **Save**.
4. Observe the system warning about incomplete data.
5. Choose the option to **Save Draft Anyway** (or equivalent).

**Expected Results (Save Anyway Path):**
- The system detects missing required draft-level information.
- The system displays a warning indicating incomplete data.
- When the author chooses to save anyway, the system stores the draft and displays a confirmation message.

**Test Steps (Cancel Save Path):**
1. Repeat steps 1–4 above.
2. Choose **Cancel** (or equivalent) when warned about incomplete data.
3. Navigate away and re-open the submission.

**Expected Results (Cancel Save Path):**
- The system does not save changes when the author cancels the save operation.
- When the submission is reopened, the unsaved changes are not persisted.

---

#### AT-UC09-04 — System Fails to Store Draft (Extension 5a / Failure End Scenario)

**Purpose:**  
Verify system behavior when the save operation fails due to a database/server error and the draft is not saved.

**Preconditions:**
- CMS is running and accessible.
- Author is logged in.
- Author has started a paper submission and is in the submission workflow.
- A database/server/storage failure can be simulated during the save operation.

**Test Steps:**
1. Navigate to an active paper submission draft.
2. Make a clear identifiable change (e.g., edit a field value).
3. Select **Save** while the failure condition exists.
4. Observe the system response.
5. Navigate away and re-open the submission.

**Expected Results:**
- The system encounters a database/server error during storage.
- The system displays an error message indicating the save operation failed.
- The system does not display a success confirmation.
- The submission progress is not saved (recent changes are not present when reopened).
- The author may abandon the save attempt (use case ends in failure).

---

### Completion Criteria

UC-09 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-10: Receive Paper Acceptance or Rejection Decision

---

### Use Case Under Test

**Use Case ID:** UC-10  
**Use Case Name:** Receive Paper Acceptance or Rejection Decision  
**Primary Actor:** Author (Registered User)  
**Goal:** Allow an author to receive and view the final acceptance or rejection decision for a submitted paper.

---

### Acceptance Criteria

The system satisfies UC-10 if:

- The final decision (accept or reject) for a paper is recorded in the system.
- The correct author can view the decision after logging in.
- The decision displayed corresponds to the correct paper submission.
- The system provides appropriate feedback when the decision is not yet available.
- The system handles notification or retrieval failures gracefully.
- All main, alternate, and failure flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- Author accesses the system using a modern web browser.
- Author is registered and logged in unless otherwise specified.
- Author has submitted at least one paper.
- A final decision (accept/reject) is recorded by the system once the review process is complete.
- Decision information is restricted to the author(s) of the paper.

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC10-01  | Main Success Scenario |
| AT-UC10-02  | Extension 4a – Decision Not Yet Available |
| AT-UC10-03  | Extension 5a – Author Not Logged In |
| AT-UC10-04  | Extension 6a – Error Retrieving Decision |
| AT-UC10-05  | Failure End Scenario – Decision Data Unavailable Due to System Error |

---

### Acceptance Test Cases

---

#### AT-UC10-01 — View Acceptance or Rejection Decision Successfully (Main Success Scenario)

**Purpose:**  
Verify that an author can view the final acceptance or rejection decision for a submitted paper.

**Preconditions:**
- CMS is running and accessible.
- Author is logged in.
- Author has submitted a paper.
- The final decision (accept or reject) has been recorded for the paper.

**Test Steps:**
1. Log in to the CMS as the author.
2. Navigate to **My Submissions** or an equivalent page.
3. Select the submitted paper.
4. View the decision section for the paper.

**Expected Results:**
- The system displays the final decision (Accepted or Rejected).
- The decision shown corresponds to the selected paper.
- No error messages are displayed.
- The decision is visible only to the paper’s author(s).

---

#### AT-UC10-02 — Decision Not Yet Available (Extension 4a)

**Purpose:**  
Verify system behavior when the author attempts to view a decision that has not yet been finalized.

**Preconditions:**
- CMS is running and accessible.
- Author is logged in.
- Author has submitted a paper.
- No final decision has been recorded for the paper.

**Test Steps:**
1. Log in to the CMS as the author.
2. Navigate to **My Submissions**.
3. Select the submitted paper.
4. Attempt to view the decision.

**Expected Results:**
- The system indicates that the decision is not yet available.
- The system does not display an acceptance or rejection result.
- The author remains able to access other submission information.

---

#### AT-UC10-03 — Author Not Logged In (Extension 5a)

**Purpose:**  
Verify that the system prevents unauthenticated users from viewing paper decisions.

**Preconditions:**
- CMS is running and accessible.
- Author is not logged in.
- A paper submission with a recorded decision exists.

**Test Steps:**
1. Open a web browser.
2. Navigate directly to the submissions or decision page URL.

**Expected Results:**
- The system redirects the user to the login page.
- The decision information is not displayed.
- Access to decision data is denied until authentication occurs.

---

#### AT-UC10-04 — Error Retrieving Decision (Extension 6a)

**Purpose:**  
Verify system behavior when an error occurs while retrieving the decision information.

**Preconditions:**
- CMS is running and accessible.
- Author is logged in.
- Author has submitted a paper.
- A system or database error can be simulated during decision retrieval.

**Test Steps:**
1. Log in to the CMS as the author.
2. Navigate to **My Submissions**.
3. Select the submitted paper.
4. Attempt to view the decision while the error condition exists.

**Expected Results:**
- The system displays an error message indicating the decision could not be retrieved.
- The system does not display incorrect or partial decision information.
- The author may retry later or navigate away safely.

---

#### AT-UC10-05 — Decision Data Unavailable Due to System Error (Failure End Scenario)

**Purpose:**  
Verify system behavior when a critical failure prevents decision data from being accessed.

**Preconditions:**
- CMS is running and accessible.
- Author is logged in.
- Author has submitted a paper.
- A critical backend or database failure occurs.

**Test Steps:**
1. Log in to the CMS as the author.
2. Navigate to **My Submissions**.
3. Select the submitted paper.
4. Attempt to view the decision.

**Expected Results:**
- The system reports that decision data is unavailable.
- No acceptance or rejection result is shown.
- The use case ends in failure due to system error.
- The system does not expose sensitive or internal error details.

---

### Completion Criteria

UC-10 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-11: View Conference Schedule for Accepted Paper

---

### Use Case Under Test

**Use Case ID:** UC-11  
**Use Case Name:** View Conference Schedule for Accepted Paper  
**Primary Actor:** Author (Registered User)  
**Secondary Actor(s):** Administrator, Editor  
**Goal:** Allow an author of an accepted paper to view the published conference schedule so they know the assigned presentation time and location.

---

### Acceptance Criteria

The system satisfies UC-11 if:

- An author with an accepted paper can access the conference schedule view from the CMS.
- The system displays the schedule entry for the author’s accepted paper, including presentation time and room/location.
- The system prevents unauthenticated access and redirects to login when necessary.
- The system provides clear feedback when the schedule is not published, cannot be retrieved, or does not contain the author’s paper.
- All main and alternate flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- Author accesses the system using a modern web browser.
- Author is registered and logged in unless otherwise specified.
- The author has at least one **accepted** paper in the system.
- The conference schedule may be **published** or **unpublished** depending on the test.
- The schedule includes at minimum: paper identifier/title, presentation time slot, and room/location.

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC11-01  | Main Success Scenario |
| AT-UC11-02  | Extension 1a – Author Not Logged In |
| AT-UC11-03  | Extension 3a – Conference Schedule Not Yet Published |
| AT-UC11-04  | Extension 4a – System Fails to Retrieve Schedule |
| AT-UC11-05  | Extension 5a – Author’s Paper Missing From Schedule |

---

### Acceptance Test Cases

---

#### AT-UC11-01 — View Schedule for Accepted Paper Successfully (Main Success Scenario)

**Purpose:**  
Verify that an author can view the published conference schedule entry for their accepted paper (time and room/location).

**Preconditions:**
- CMS is running and accessible.
- Author is logged in.
- Author has an accepted paper.
- Conference schedule has been generated and published.
- The published schedule contains an entry for the author’s accepted paper.

**Test Steps:**
1. Log in to the CMS as the author.
2. Navigate to **My Submissions** or **Schedule** section.
3. Select the option to **View Conference Schedule**.
4. Allow the system to retrieve the published conference schedule.
5. Locate the schedule entry for the author’s accepted paper.

**Expected Results:**
- The system displays the published conference schedule.
- The schedule includes the author’s accepted paper entry.
- The schedule entry includes the assigned presentation time and room/location.
- No error or warning messages are displayed.

---

#### AT-UC11-02 — Author Not Logged In (Extension 1a)

**Purpose:**  
Verify that an unauthenticated author is redirected to login and can resume viewing the schedule after logging in.

**Preconditions:**
- CMS is running and accessible.
- Author is not logged in.
- Author has an accepted paper.
- Conference schedule is published.

**Test Steps:**
1. Open a web browser.
2. Attempt to access the schedule page directly (or select **View Conference Schedule** from a public route if present).
3. Observe that the system requires authentication.
4. Log in successfully as the author.
5. Navigate (or be redirected) to the schedule view.

**Expected Results:**
- The system redirects the user to the login page when not authenticated.
- After successful login, the user can access the schedule view.
- The use case continues from the schedule navigation step without requiring the user to restart completely.

---

#### AT-UC11-03 — Conference Schedule Not Yet Published (Extension 3a)

**Purpose:**  
Verify that the system informs the author when the schedule is not published.

**Preconditions:**
- CMS is running and accessible.
- Author is logged in.
- Author has an accepted paper.
- Conference schedule has not been published (unavailable).

**Test Steps:**
1. Log in to the CMS as the author.
2. Navigate to **My Submissions** or **Schedule** section.
3. Select **View Conference Schedule**.

**Expected Results:**
- The system detects the schedule is unavailable/unpublished.
- The system displays a message indicating the schedule has not yet been published.
- The system does not display an empty schedule as if it were valid.
- The author can return later to try again.

---

#### AT-UC11-04 — System Fails to Retrieve Schedule (Extension 4a)

**Purpose:**  
Verify system behavior when a server/database error prevents schedule retrieval.

**Preconditions:**
- CMS is running and accessible (UI reachable).
- Author is logged in.
- Author has an accepted paper.
- Conference schedule is published (expected to exist).
- A server/database error can be simulated during schedule retrieval.

**Test Steps:**
1. Log in to the CMS as the author.
2. Navigate to **My Submissions** or **Schedule** section.
3. Select **View Conference Schedule** while the retrieval failure condition exists.
4. Observe the system response.

**Expected Results:**
- The system displays an error message indicating temporary unavailability (schedule cannot be retrieved).
- The system does not display incorrect or partial schedule data as if complete.
- The author can retry later or abandon the attempt safely.

---

#### AT-UC11-05 — Author’s Paper Missing From Schedule (Extension 5a)

**Purpose:**  
Verify that the system warns the author when their accepted paper does not appear in the schedule.

**Preconditions:**
- CMS is running and accessible.
- Author is logged in.
- Author has an accepted paper.
- Conference schedule is published.
- The published schedule does not include an entry for the author’s accepted paper.

**Test Steps:**
1. Log in to the CMS as the author.
2. Navigate to **My Submissions** or **Schedule** section.
3. Select **View Conference Schedule**.
4. Review the displayed schedule and attempt to locate the author’s accepted paper.

**Expected Results:**
- The system displays the published conference schedule.
- The author’s accepted paper is not listed in the schedule.
- The system displays a warning indicating the paper is not yet scheduled (or cannot be found in the schedule).
- The author can take follow-up action outside the system (e.g., contact organizer/editor), and the system remains stable.

---

### Completion Criteria

UC-11 is considered accepted when all test cases pass and all defined flows (main and alternate) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-12: Receive and Respond to Review Invitation

---

### Use Case Under Test

**Use Case ID:** UC-12  
**Use Case Name:** Receive and Respond to Review Invitation  
**Primary Actor:** Referee / Reviewer  
**Secondary Actor(s):** Editor, Email Notification Service  
**Goal:** Allow a reviewer to receive a review invitation and accept or reject it so that the review assignment process can proceed correctly.

---

### Acceptance Criteria

The system satisfies UC-12 if:

- When an editor assigns a reviewer, the system generates a review invitation.
- The invitation is delivered via email when the email service is available.
- The reviewer can view pending invitations in the CMS and respond (accept or reject).
- On acceptance, the system records the acceptance and adds the paper to the reviewer’s assigned papers list.
- On rejection, the system records the rejection and notifies the editor.
- If email delivery fails, the reviewer can still view the invitation within the CMS after logging in.
- If the reviewer is not logged in, the system redirects to login and resumes the use case after successful login.
- If the reviewer has reached the maximum assignment limit, the system prevents acceptance and notifies the editor.
- If a system error occurs while recording the response, the system reports the failure and does not save the response.
- All main, alternate, and failure flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- Reviewer accesses the system using a modern web browser and has access to email.
- Reviewer is registered in the CMS and has a valid email address in the system.
- Editor can assign reviewers to submitted papers.
- The CMS includes a **Review Invitations** section where pending invitations are displayed.
- The system enforces a maximum number of assigned papers per reviewer (assignment limit).

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC12-01  | Main Success Scenario (Reviewer Accepts Invitation) |
| AT-UC12-02  | Extension 8a – Reviewer Rejects the Review Invitation |
| AT-UC12-03  | Extension 3a – Email Notification Fails to Send |
| AT-UC12-04  | Extension 5a – Reviewer Is Not Logged In |
| AT-UC12-05  | Extension 9a – Reviewer Exceeded Maximum Assigned Papers |
| AT-UC12-06  | Failure End Scenario – System Error During Invitation Processing |

---

### Acceptance Test Cases

---

#### AT-UC12-01 — Accept Review Invitation Successfully (Main Success Scenario)

**Purpose:**  
Verify that a reviewer can accept a pending review invitation and the system records the acceptance and assigns the paper.

**Preconditions:**
- CMS is running and accessible.
- Reviewer is registered with a valid email address.
- Editor has assigned the reviewer to a paper (a pending invitation exists).
- Email notification service is available (invitation email is delivered).
- Reviewer has not exceeded the maximum assignment limit.

**Test Steps:**
1. Editor assigns the reviewer to a submitted paper.
2. Reviewer opens the invitation email.
3. Reviewer logs in to the CMS.
4. Reviewer navigates to the **Review Invitations** section.
5. Reviewer selects the pending invitation.
6. Reviewer selects **Accept**.
7. Observe the system response.

**Expected Results:**
- The system displays the pending review invitation.
- The system records the reviewer’s acceptance.
- The paper is added to the reviewer’s list of assigned papers.
- The system displays a confirmation message indicating successful assignment.

---

#### AT-UC12-02 — Reject Review Invitation (Extension 8a)

**Purpose:**  
Verify that a reviewer can reject a review invitation and that the system records the rejection and notifies the editor.

**Preconditions:**
- CMS is running and accessible.
- Reviewer is registered and logged in.
- A pending review invitation exists for the reviewer.

**Test Steps:**
1. Log in to the CMS as the reviewer.
2. Navigate to the **Review Invitations** section.
3. Select the pending invitation.
4. Select **Reject**.
5. Observe the system response.

**Expected Results:**
- The system records the reviewer’s rejection.
- The paper is not added to the reviewer’s assigned papers list.
- The system notifies the editor of the rejection (or records a notification action).
- The system displays confirmation that the rejection was recorded.

---

#### AT-UC12-03 — Email Notification Fails to Send (Extension 3a)

**Purpose:**  
Verify that if the email invitation fails to send, the reviewer can still see and respond to the invitation by logging into the CMS.

**Preconditions:**
- CMS is running and accessible.
- Reviewer is registered with a valid email address.
- Editor has assigned the reviewer to a paper (invitation exists in the CMS).
- Email notification service is unavailable (email delivery fails).

**Test Steps:**
1. Editor assigns the reviewer to a paper while email service is unavailable.
2. Confirm the reviewer does not receive an invitation email.
3. Reviewer logs in to the CMS manually (without using an email link).
4. Reviewer navigates to the **Review Invitations** section.
5. Reviewer selects the pending invitation.
6. Reviewer responds (Accept or Reject).

**Expected Results:**
- The system detects and logs the email notification failure (system-side behavior).
- The pending invitation is still visible in the CMS.
- The reviewer can respond to the invitation within the CMS.
- The system records the response and displays appropriate confirmation.

---

#### AT-UC12-04 — Reviewer Not Logged In (Extension 5a)

**Purpose:**  
Verify that if the reviewer is not logged in, the system redirects to login and resumes the use case after successful login.

**Preconditions:**
- CMS is running and accessible.
- A pending review invitation exists for the reviewer.
- Reviewer is not logged in.

**Test Steps:**
1. Reviewer attempts to access the review invitation (e.g., via email link or direct URL to invitations).
2. Observe the system redirect behavior.
3. Reviewer logs in successfully.
4. Reviewer navigates to the **Review Invitations** section (or is redirected there).
5. Reviewer selects the pending invitation and responds.

**Expected Results:**
- The system redirects the reviewer to the login page.
- After successful login, the reviewer can access the review invitations section.
- The use case resumes at the invitation viewing step (reviewer can respond normally).

---

#### AT-UC12-05 — Reviewer Exceeded Maximum Assigned Papers (Extension 9a)

**Purpose:**  
Verify that the system prevents invitation acceptance when the reviewer has reached the maximum assignment limit and notifies the editor.

**Preconditions:**
- CMS is running and accessible.
- Reviewer is registered and logged in.
- A pending review invitation exists for the reviewer.
- Reviewer has already reached the maximum allowed number of assigned papers.

**Test Steps:**
1. Log in to the CMS as the reviewer.
2. Navigate to the **Review Invitations** section.
3. Select the pending invitation.
4. Select **Accept**.
5. Observe the system response.

**Expected Results:**
- The system detects the assignment limit has been reached.
- The system prevents acceptance of the invitation.
- The system displays an error message indicating the workload/assignment limit has been reached.
- The system notifies the editor of the assignment constraint (or records a notification action).
- The paper is not added to the reviewer’s assigned papers list.

---

#### AT-UC12-06 — System Error While Recording Invitation Response (Failure End Scenario)

**Purpose:**  
Verify system behavior when an error occurs while recording the reviewer’s acceptance/rejection response.

**Preconditions:**
- CMS is running and accessible (UI reachable).
- Reviewer is registered and logged in.
- A pending review invitation exists for the reviewer.
- A database/server failure can be simulated during response recording.

**Test Steps:**
1. Log in to the CMS as the reviewer.
2. Navigate to the **Review Invitations** section.
3. Select the pending invitation.
4. Select **Accept** (or **Reject**) while the failure condition exists.
5. Observe the system response.
6. Refresh the invitations page and/or check the reviewer’s assigned papers list.

**Expected Results:**
- The system displays an error message indicating the invitation response could not be processed.
- The reviewer’s response is not saved (invitation remains unresolved/pending).
- The paper is not added to the reviewer’s assigned papers list (if acceptance was attempted).
- The system does not expose sensitive internal error details.
- The reviewer may retry later; if they abandon the attempt, the use case ends in failure.

---

### Completion Criteria

UC-12 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-13: View Assigned Papers

---

### Use Case Under Test

**Use Case ID:** UC-13  
**Use Case Name:** View Assigned Papers  
**Primary Actor:** Referee / Reviewer  
**Goal:** Allow a reviewer to view the list of papers assigned to them so they can manage and complete their reviews.

---

### Acceptance Criteria

The system satisfies UC-13 if:

- A logged-in reviewer can access the **Assigned Papers** view from the reviewer interface/dashboard.
- The system displays an accurate, up-to-date list of papers assigned to the reviewer.
- Each listed assigned paper provides enough identifying information (e.g., title, paper ID, authors) to distinguish it from others.
- If no papers are assigned, the system clearly indicates that there are no assigned papers.
- If the reviewer is not logged in, the system redirects to login and allows the reviewer to continue after authentication.
- The system handles retrieval failures gracefully with clear error feedback.
- All main and alternate flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- Reviewer accesses the system using a modern web browser.
- Reviewer is registered in the CMS.
- Reviewer is logged in unless otherwise specified.
- Reviewer has either:
  - one or more assigned papers, or
  - zero assigned papers (depending on the test case).
- The CMS provides a navigation option such as **Assigned Papers**, **My Reviews**, or similar.

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC13-01  | Main Success Scenario |
| AT-UC13-02  | Extension 1a – Reviewer Not Logged In |
| AT-UC13-03  | Extension 3a – No Assigned Papers |
| AT-UC13-04  | Failure End Scenario – System Error Retrieving Assigned Papers |

---

### Acceptance Test Cases

---

#### AT-UC13-01 — View Assigned Papers Successfully (Main Success Scenario)

**Purpose:**  
Verify that a logged-in reviewer can view the list of papers assigned to them.

**Preconditions:**
- CMS is running and accessible.
- Reviewer is logged in.
- Reviewer has one or more assigned papers.

**Test Steps:**
1. Log in to the CMS as a reviewer.
2. Navigate to the reviewer dashboard/home page.
3. Select **Assigned Papers** (or equivalent).
4. Observe the assigned papers list.
5. Select one assigned paper (if selectable) to ensure it opens the expected paper detail/review page.

**Expected Results:**
- The assigned papers page loads successfully.
- The system displays a list of assigned papers for the reviewer.
- Each entry includes identifying information (e.g., title and/or paper ID).
- Selecting a paper opens the correct corresponding paper detail/review page (if supported).
- No errors or warnings are displayed.

---

#### AT-UC13-02 — Reviewer Not Logged In (Extension 1a)

**Purpose:**  
Verify that an unauthenticated reviewer cannot access assigned papers and is redirected to login.

**Preconditions:**
- CMS is running and accessible.
- Reviewer is not logged in.
- Reviewer has an existing account and may have assigned papers.

**Test Steps:**
1. Open a web browser.
2. Attempt to access the **Assigned Papers** page directly (via URL) or by navigating from a public page.
3. Observe the system response.
4. Log in using valid reviewer credentials.
5. Navigate (or be redirected) to **Assigned Papers**.

**Expected Results:**
- The system redirects the reviewer to the login page when not authenticated.
- After successful login, the reviewer can access the assigned papers list.
- The reviewer is not shown assigned paper details before authentication.

---

#### AT-UC13-03 — No Assigned Papers (Extension 3a)

**Purpose:**  
Verify that the system clearly indicates when the reviewer has no assigned papers.

**Preconditions:**
- CMS is running and accessible.
- Reviewer is logged in.
- Reviewer has zero assigned papers.

**Test Steps:**
1. Log in to the CMS as the reviewer with no assignments.
2. Navigate to **Assigned Papers** (or equivalent).
3. Observe the assigned papers page content.

**Expected Results:**
- The assigned papers page loads successfully.
- The system displays a clear message indicating there are no assigned papers.
- The system does not display misleading empty rows or placeholders as if they were real assignments.

---

#### AT-UC13-04 — Error Retrieving Assigned Papers (Failure End Scenario)

**Purpose:**  
Verify system behavior when a backend/database error prevents retrieval of assigned papers.

**Preconditions:**
- CMS is running and accessible (UI reachable).
- Reviewer is logged in.
- A backend/database/service failure can be simulated during retrieval of assigned papers.

**Test Steps:**
1. Log in to the CMS as a reviewer.
2. Navigate to **Assigned Papers** while the failure condition exists.
3. Observe the system response.
4. Refresh the page or retry navigation after a short interval (optional).

**Expected Results:**
- The system displays an error message indicating assigned papers could not be retrieved.
- The system does not display incorrect or partial data as if it were complete.
- The reviewer remains authenticated and can safely navigate to other parts of the system.
- If the reviewer abandons the attempt, the use case ends in failure (assigned papers not viewable).

---

### Completion Criteria

UC-13 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-14: Access Review Form for Assigned Paper

---

### Use Case Under Test

**Use Case ID:** UC-14  
**Use Case Name:** Access Review Form for Assigned Paper  
**Primary Actor:** Referee / Reviewer  
**Goal:** Allow a reviewer to access the review form and relevant paper materials for an assigned paper so they can begin the review process.

---

### Acceptance Criteria

The system satisfies UC-14 if:

- A logged-in reviewer can access the review form for a paper assigned to them.
- The system displays the correct paper details and manuscript access for the selected assigned paper.
- The system prevents access to the review form for papers not assigned to the reviewer.
- If the reviewer is not logged in, the system redirects to login and allows continuation after authentication.
- The system provides clear feedback when paper content or the review form cannot be retrieved.
- All main, alternate, and failure flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- Reviewer accesses the system using a modern web browser.
- Reviewer is registered in the CMS.
- Reviewer is logged in unless otherwise specified.
- At least one paper is assigned to the reviewer for main-flow testing.
- The CMS provides an **Assigned Papers** list and an option to **Review** or **Open Review Form** for assigned papers.
- Manuscript files are stored and retrievable through the CMS for assigned papers.

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC14-01  | Main Success Scenario |
| AT-UC14-02  | Extension 1a – Reviewer Not Logged In |
| AT-UC14-03  | Extension 4a – Paper Not Assigned to Reviewer |
| AT-UC14-04  | Extension 5a – Manuscript File Not Available |
| AT-UC14-05  | Failure End Scenario – System Error Retrieving Review Form |

---

### Acceptance Test Cases

---

#### AT-UC14-01 — Access Review Form Successfully (Main Success Scenario)

**Purpose:**  
Verify that a logged-in reviewer can open the review form for an assigned paper and access the necessary paper materials.

**Preconditions:**
- CMS is running and accessible.
- Reviewer is logged in.
- Reviewer has at least one assigned paper.
- The assigned paper has an uploaded manuscript file available.

**Test Steps:**
1. Log in to the CMS as a reviewer.
2. Navigate to **Assigned Papers** (or equivalent).
3. Select an assigned paper.
4. Select **Review** / **Open Review Form** (or equivalent).
5. Observe the review form page.
6. Attempt to open or download the manuscript file from the review page (if available as a link/button).

**Expected Results:**
- The review form loads successfully for the selected assigned paper.
- The paper details displayed match the selected assigned paper.
- The reviewer can access the manuscript file (view/download).
- No authorization errors are displayed.

---

#### AT-UC14-02 — Reviewer Not Logged In (Extension 1a)

**Purpose:**  
Verify that an unauthenticated user is redirected to login and cannot access review forms without authentication.

**Preconditions:**
- CMS is running and accessible.
- Reviewer is not logged in.
- An assigned paper exists for the reviewer account.

**Test Steps:**
1. Open a web browser.
2. Attempt to access the review form URL directly (or access via an assigned paper link if visible).
3. Observe the system response.
4. Log in using valid reviewer credentials.
5. Navigate to **Assigned Papers** and attempt to open the review form again.

**Expected Results:**
- The system redirects the user to the login page when not authenticated.
- No review form or manuscript content is displayed before login.
- After login, the reviewer can access the review form normally for assigned papers.

---

#### AT-UC14-03 — Paper Not Assigned to Reviewer (Extension 4a)

**Purpose:**  
Verify that the system prevents access to the review form for papers not assigned to the reviewer.

**Preconditions:**
- CMS is running and accessible.
- Reviewer is logged in.
- A paper exists in the system that is not assigned to the reviewer.

**Test Steps:**
1. Log in to the CMS as a reviewer.
2. Attempt to access the review form for an unassigned paper (e.g., via direct URL manipulation or attempting to open a paper not in the reviewer’s assignment list).
3. Observe the system response.

**Expected Results:**
- The system denies access to the review form for the unassigned paper.
- The system displays an authorization error message (e.g., “You are not assigned to this paper”).
- The reviewer cannot view the unassigned paper’s manuscript or review form.

---

#### AT-UC14-04 — Manuscript File Not Available (Extension 5a)

**Purpose:**  
Verify system behavior when the review form is accessible but the manuscript file cannot be retrieved.

**Preconditions:**
- CMS is running and accessible.
- Reviewer is logged in.
- A paper is assigned to the reviewer.
- The manuscript file is missing or inaccessible (e.g., deleted, storage unavailable, broken link).

**Test Steps:**
1. Log in to the CMS as the reviewer.
2. Navigate to **Assigned Papers**.
3. Select the assigned paper with missing/unavailable manuscript.
4. Open the review form.
5. Attempt to open or download the manuscript file.

**Expected Results:**
- The review form loads successfully (if form retrieval is not dependent on manuscript retrieval).
- The system indicates the manuscript is unavailable and provides a clear error/warning message.
- The system does not crash or expose internal storage details.
- The reviewer can still view the review form fields (if permitted by design), or is clearly informed if reviewing cannot proceed.

---

#### AT-UC14-05 — System Error Retrieving Review Form (Failure End Scenario)

**Purpose:**  
Verify system behavior when a system error prevents the review form from loading.

**Preconditions:**
- CMS is running and accessible (UI reachable).
- Reviewer is logged in.
- A paper is assigned to the reviewer.
- A backend/database/service failure can be simulated during review form retrieval.

**Test Steps:**
1. Log in to the CMS as the reviewer.
2. Navigate to **Assigned Papers**.
3. Select an assigned paper.
4. Select **Open Review Form** while the failure condition exists.
5. Observe the system response.
6. Refresh the page or retry opening the form (optional).

**Expected Results:**
- The system displays an error message indicating the review form could not be loaded.
- The system does not display incomplete/incorrect form data as if valid.
- The reviewer remains authenticated and can navigate away safely.
- If the reviewer abandons the attempt, the use case ends in failure (review form not accessible).

---

### Completion Criteria

UC-14 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-15: Submit Review for Assigned Paper

---

### Use Case Under Test

**Use Case ID:** UC-15  
**Use Case Name:** Submit Review for Assigned Paper  
**Primary Actor:** Referee / Reviewer  
**Goal:** Allow a reviewer to complete and submit a review for a paper assigned to them so the editor can use it in the decision process.

---

### Acceptance Criteria

The system satisfies UC-15 if:

- A logged-in reviewer can submit a review only for a paper assigned to them.
- The system validates required review fields (e.g., ratings, written comments) before submission.
- The system saves the submitted review and associates it with the correct paper and reviewer.
- The system confirms successful submission and prevents accidental duplicate submissions (or clearly handles resubmission).
- The system prevents submission if the reviewer is not logged in or not assigned to the paper.
- The system provides clear feedback for validation errors and system/storage failures.
- All main, alternate, and failure flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- Reviewer accesses the system using a modern web browser.
- Reviewer is registered in the CMS and logged in unless otherwise specified.
- Reviewer has at least one assigned paper for main-flow testing.
- The CMS provides a review form for assigned papers (accessible via **Assigned Papers** → **Open Review Form**).
- The review form includes required fields (as defined by the system), such as:
  - Overall score/rating
  - Confidence score (if applicable)
  - Written comments (to authors and/or to committee)

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC15-01  | Main Success Scenario |
| AT-UC15-02  | Extension 1a – Reviewer Not Logged In |
| AT-UC15-03  | Extension 3a – Paper Not Assigned to Reviewer |
| AT-UC15-04  | Extension 4a – Missing Required Review Fields |
| AT-UC15-05  | Extension 4b – Invalid Review Field Values |
| AT-UC15-06  | Extension 6a – Duplicate Submission / Review Already Submitted |
| AT-UC15-07  | Failure End Scenario – System Fails to Store Submitted Review |

---

### Acceptance Test Cases

---

#### AT-UC15-01 — Submit Review Successfully (Main Success Scenario)

**Purpose:**  
Verify that a reviewer can submit a complete and valid review for an assigned paper and that it is saved correctly.

**Preconditions:**
- CMS is running and accessible.
- Reviewer is logged in.
- Reviewer is assigned to the target paper.
- Review form is accessible for the assigned paper.
- Review has not yet been submitted for this paper by this reviewer.

**Test Steps:**
1. Log in to the CMS as a reviewer.
2. Navigate to **Assigned Papers**.
3. Select an assigned paper.
4. Open the review form.
5. Enter valid values into all required fields (e.g., ratings and required comments).
6. Submit the review.
7. Navigate back to **Assigned Papers** (or review history page) and reopen the paper’s review status (if available).

**Expected Results:**
- The system validates the review input successfully.
- The system stores the review and associates it with the correct paper and reviewer.
- The system displays a confirmation message indicating the review was submitted.
- The review status reflects submission (e.g., “Submitted”).
- The submitted review content is retrievable for viewing (if the system supports it).

---

#### AT-UC15-02 — Reviewer Not Logged In (Extension 1a)

**Purpose:**  
Verify that an unauthenticated user cannot submit a review and is redirected to login.

**Preconditions:**
- CMS is running and accessible.
- Reviewer is not logged in.
- A review form URL exists for an assigned paper.

**Test Steps:**
1. Open a web browser.
2. Attempt to access the review form submission page directly (via URL) or attempt to submit the review form without logging in.
3. Observe the system response.
4. Log in using valid reviewer credentials.
5. Navigate to the assigned paper and open the review form.

**Expected Results:**
- The system redirects the user to the login page when not authenticated.
- No review form submission is accepted without login.
- After logging in, the reviewer can access the review form normally for assigned papers.

---

#### AT-UC15-03 — Paper Not Assigned to Reviewer (Extension 3a)

**Purpose:**  
Verify that a reviewer cannot submit a review for a paper they are not assigned to.

**Preconditions:**
- CMS is running and accessible.
- Reviewer is logged in.
- A target paper exists that is not assigned to the reviewer.

**Test Steps:**
1. Log in to the CMS as the reviewer.
2. Attempt to access the review form for an unassigned paper (e.g., by URL manipulation).
3. Attempt to submit the review (if the form is visible).

**Expected Results:**
- The system blocks access to the review form and/or prevents submission.
- The system displays an authorization error (e.g., “You are not assigned to this paper”).
- No review is stored for the unassigned paper.

---

#### AT-UC15-04 — Missing Required Review Fields (Extension 4a)

**Purpose:**  
Verify that the system rejects review submissions with missing required fields and provides clear feedback.

**Preconditions:**
- CMS is running and accessible.
- Reviewer is logged in.
- Reviewer is assigned to the target paper.
- Review form is accessible and review has not yet been submitted.

**Test Steps:**
1. Navigate to the assigned paper’s review form.
2. Leave one or more required fields blank (e.g., omit overall rating or required comments).
3. Submit the review.
4. Observe validation feedback.
5. Fill in the missing required fields with valid values.
6. Submit the review again.

**Expected Results:**
- The system detects missing required fields.
- The system displays clear validation errors indicating what must be completed.
- The review is not stored while required fields are missing.
- After completion, the review submits successfully and a confirmation message is shown.

---

#### AT-UC15-05 — Invalid Review Field Values (Extension 4b)

**Purpose:**  
Verify that the system rejects invalid field values (e.g., out-of-range ratings) and provides clear feedback.

**Preconditions:**
- CMS is running and accessible.
- Reviewer is logged in.
- Reviewer is assigned to the target paper.
- Review form is accessible and review has not yet been submitted.

**Test Steps:**
1. Navigate to the assigned paper’s review form.
2. Enter invalid values (examples):
   - Rating outside allowed range (e.g., 99 when allowed range is 1–5/1–10).
   - Non-numeric input in numeric rating field (if possible).
3. Submit the review.
4. Observe validation feedback.
5. Correct the invalid values to valid ones.
6. Submit the review again.

**Expected Results:**
- The system detects invalid values and rejects submission.
- The system displays clear validation messages describing the invalid fields.
- The review is not stored while invalid values remain.
- After correction, the review submits successfully.

---

#### AT-UC15-06 — Duplicate Submission / Review Already Submitted (Extension 6a)

**Purpose:**  
Verify that the system handles attempts to submit a review when one has already been submitted.

**Preconditions:**
- CMS is running and accessible.
- Reviewer is logged in.
- Reviewer is assigned to the target paper.
- A review has already been successfully submitted by this reviewer for this paper.

**Test Steps:**
1. Navigate to the assigned paper.
2. Attempt to open the review form and submit again (or refresh and resubmit the last POST action if feasible).
3. Observe the system response.

**Expected Results:**
- The system prevents accidental duplicate submissions OR clearly treats the action as an update (depending on system design).
- The system displays an appropriate message (e.g., “Review already submitted” or “Review updated successfully”).
- No duplicate review records are created for the same reviewer-paper pair.

---

#### AT-UC15-07 — System Fails to Store Submitted Review (Failure End Scenario)

**Purpose:**  
Verify system behavior when a backend/storage error occurs during review submission.

**Preconditions:**
- CMS is running and accessible (UI reachable).
- Reviewer is logged in.
- Reviewer is assigned to the target paper.
- Review form is accessible.
- A backend/database failure can be simulated during review storage.

**Test Steps:**
1. Navigate to the assigned paper’s review form.
2. Enter valid values in all required fields.
3. Submit the review while the failure condition exists.
4. Observe the system response.
5. Refresh the page and check the review status/history (if available).

**Expected Results:**
- The system displays an error message indicating the review could not be submitted/saved.
- The system does not display a success confirmation.
- The review is not stored (status remains unsubmitted).
- The system does not expose sensitive internal error details.
- The reviewer may retry later; if they abandon the attempt, the use case ends in failure.

---

### Completion Criteria

UC-15 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-16: Assign Reviewers to Submitted Papers

---

### Use Case Under Test

**Use Case ID:** UC-16  
**Use Case Name:** Assign Reviewers to Submitted Papers  
**Primary Actor:** Editor  
**Goal:** Allow an editor to assign one or more reviewers to a submitted paper so that the review process can proceed.

---

### Acceptance Criteria

The system satisfies UC-16 if:

- A logged-in editor can access paper management and select a submitted paper for reviewer assignment.
- The system displays paper details and a list/search of available reviewers.
- The editor can assign one or more reviewers to the selected paper.
- The system validates reviewer identity (e.g., reviewer exists / valid email) and prevents invalid assignments.
- The system prevents duplicate assignments of the same reviewer to the same paper.
- The system prevents assignment when the reviewer has exceeded their assignment limit (if enforced) and provides clear feedback.
- The system records assignments and (if applicable) generates review invitations/notifications.
- The system provides clear feedback for all alternate and failure flows (invalid inputs, permission issues, notification failures, storage errors).
- All main, alternate, and failure flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- Editor accesses the system using a modern web browser.
- Editor is registered and logged in unless otherwise specified.
- At least one paper has been submitted and is visible in the editor’s paper management interface.
- A reviewer directory/list exists in the CMS.
- The CMS may enforce reviewer workload limits (maximum assigned papers).
- The CMS may send notifications (e.g., email/in-app) when a reviewer is assigned.
- Assignments are stored in a database and should be visible in the paper’s reviewer/assignment view.

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC16-01  | Main Success Scenario (Assign One Reviewer) |
| AT-UC16-02  | Main Success Scenario Variant (Assign Multiple Reviewers) |
| AT-UC16-03  | Extension – Editor Not Logged In / Not Authorized |
| AT-UC16-04  | Extension – Reviewer Not Found / Invalid Reviewer Email |
| AT-UC16-05  | Extension – Reviewer Already Assigned (Duplicate Assignment) |
| AT-UC16-06  | Extension – Reviewer Assignment Limit Reached |
| AT-UC16-07  | Extension – Notification/Invitation Delivery Fails |
| AT-UC16-08  | Failure End Scenario – System Fails to Store Assignment |

---

### Acceptance Test Cases

---

#### AT-UC16-01 — Assign One Reviewer Successfully (Main Success Scenario)

**Purpose:**  
Verify that an editor can assign a single valid reviewer to a submitted paper and the assignment is recorded.

**Preconditions:**
- CMS is running and accessible.
- Editor is logged in.
- At least one submitted paper exists.
- At least one valid reviewer exists and is eligible (not already assigned; within workload limit).

**Test Steps:**
1. Log in to the CMS as an editor.
2. Navigate to the **Paper Management** (or equivalent) section.
3. Select a submitted paper.
4. Choose the option to **Assign Reviewer(s)**.
5. Select a valid reviewer (or enter/select the reviewer’s email/identifier).
6. Confirm the assignment.

**Expected Results:**
- The system records the reviewer assignment for the selected paper.
- The assigned reviewer appears in the paper’s reviewer/assignment list.
- The system displays a success confirmation message.
- If notifications are enabled, the system initiates an invitation/notification to the reviewer.

---

#### AT-UC16-02 — Assign Multiple Reviewers Successfully (Main Success Scenario Variant)

**Purpose:**  
Verify that an editor can assign multiple reviewers to the same submitted paper and all assignments are recorded.

**Preconditions:**
- CMS is running and accessible.
- Editor is logged in.
- A submitted paper exists.
- Two or more eligible reviewers exist (not already assigned; within workload limits).

**Test Steps:**
1. Log in to the CMS as an editor.
2. Navigate to **Paper Management**.
3. Select a submitted paper.
4. Open **Assign Reviewer(s)**.
5. Select multiple eligible reviewers.
6. Confirm the assignment(s).

**Expected Results:**
- The system records all selected reviewer assignments for the paper.
- Each assigned reviewer is listed under the paper’s reviewer/assignment list.
- The system displays a success confirmation message (single combined confirmation or per-assignment confirmations).
- If notifications are enabled, invitations/notifications are initiated for each assigned reviewer.

---

#### AT-UC16-03 — Editor Not Logged In or Not Authorized (Extension)

**Purpose:**  
Verify that only authorized editors can assign reviewers and unauthenticated/unauthorized users are blocked.

**Preconditions:**
- CMS is running and accessible.
- User is not logged in OR user is logged in with a non-editor role.

**Test Steps:**
1. Attempt to access paper management or the reviewer assignment page directly (via navigation or URL).
2. If redirected to login, log in as a non-editor user (optional).
3. Attempt to assign a reviewer to a submitted paper.

**Expected Results:**
- If not logged in: the system redirects to the login page and does not allow assignment actions.
- If logged in but not authorized: the system denies access and displays an authorization error.
- No reviewer assignments are created.

---

#### AT-UC16-04 — Reviewer Not Found / Invalid Reviewer Email (Extension)

**Purpose:**  
Verify that the system prevents assignments when the selected reviewer does not exist or the reviewer identifier/email is invalid.

**Preconditions:**
- CMS is running and accessible.
- Editor is logged in.
- A submitted paper exists.

**Test Steps:**
1. Navigate to **Paper Management** and select a submitted paper.
2. Open **Assign Reviewer(s)**.
3. Enter an invalid reviewer identifier/email (or select a reviewer entry that does not exist, if possible).
4. Confirm the assignment attempt.

**Expected Results:**
- The system rejects the assignment attempt.
- The system displays a clear error message (e.g., reviewer not found / invalid email).
- No assignment is stored for the invalid reviewer.

---

#### AT-UC16-05 — Reviewer Already Assigned (Duplicate Assignment) (Extension)

**Purpose:**  
Verify that the system prevents assigning the same reviewer to the same paper more than once.

**Preconditions:**
- CMS is running and accessible.
- Editor is logged in.
- A submitted paper exists.
- A reviewer is already assigned to the selected paper.

**Test Steps:**
1. Navigate to the selected paper’s reviewer assignment page.
2. Attempt to assign the same reviewer again.
3. Confirm the assignment attempt.

**Expected Results:**
- The system prevents duplicate assignment.
- The system displays a message indicating the reviewer is already assigned.
- The paper’s reviewer list remains unchanged (no duplicate entry).

---

#### AT-UC16-06 — Reviewer Assignment Limit Reached (Extension)

**Purpose:**  
Verify that the system prevents assignment when the reviewer has reached the maximum workload/assignment limit (if enforced).

**Preconditions:**
- CMS is running and accessible.
- Editor is logged in.
- A submitted paper exists.
- A reviewer exists who has reached the system’s assignment limit.

**Test Steps:**
1. Navigate to the selected paper’s reviewer assignment page.
2. Select the reviewer who is at the assignment limit.
3. Attempt to confirm the assignment.

**Expected Results:**
- The system prevents assignment for that reviewer.
- The system displays a clear message indicating the reviewer cannot be assigned due to workload/limit.
- The reviewer is not added to the paper’s reviewer list.
- (Optional, if supported) The system logs or notifies the editor that the reviewer is unavailable due to workload.

---

#### AT-UC16-07 — Notification/Invitation Delivery Fails (Extension)

**Purpose:**  
Verify that if reviewer notification/invitation delivery fails (e.g., email service down), the assignment is still recorded (or the system clearly reports whether it was recorded), and the editor is informed.

**Preconditions:**
- CMS is running and accessible.
- Editor is logged in.
- A submitted paper exists.
- A valid eligible reviewer exists.
- Notification service is unavailable (simulated).

**Test Steps:**
1. Navigate to the selected paper’s reviewer assignment page.
2. Assign an eligible reviewer.
3. Confirm the assignment while the notification failure condition exists.
4. View the paper’s reviewer list/assignment status.

**Expected Results:**
- The system informs the editor that notification/invitation delivery failed.
- The system either:
  - records the assignment successfully and shows the reviewer as assigned, OR
  - rolls back the assignment and clearly indicates the assignment was not completed.
- The system does not crash or expose sensitive internal error details.
- The editor can retry notification (if supported) or proceed with alternate communication.

---

#### AT-UC16-08 — System Fails to Store Assignment (Failure End Scenario)

**Purpose:**  
Verify system behavior when a backend/database error prevents saving reviewer assignments.

**Preconditions:**
- CMS is running and accessible (UI reachable).
- Editor is logged in.
- A submitted paper exists.
- A valid eligible reviewer exists.
- A database/server failure can be simulated during assignment storage.

**Test Steps:**
1. Navigate to the selected paper’s reviewer assignment page.
2. Select an eligible reviewer.
3. Confirm the assignment while the storage failure condition exists.
4. Refresh the page and re-check the paper’s reviewer list.

**Expected Results:**
- The system displays an error message indicating the assignment could not be saved.
- No reviewer assignment is stored (reviewer does not appear in the paper’s reviewer list).
- No invitations/notifications are treated as successfully sent for a non-stored assignment.
- The editor may retry later; if they abandon the attempt, the use case ends in failure.

---

### Completion Criteria

UC-16 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.


# Acceptance Test Suites

## Acceptance Test Suite — UC-17: Enforce Reviewer Assignment Limits

---

### Use Case Under Test

**Use Case ID:** UC-17  
**Use Case Name:** Enforce Reviewer Assignment Limits  
**Primary Actor:** Editor  
**Goal:** Ensure the system enforces a maximum workload limit for reviewers by preventing assignments that would exceed the allowed number of assigned papers.

---

### Acceptance Criteria

The system satisfies UC-17 if:

- When an editor attempts to assign a reviewer to a paper, the system retrieves the reviewer’s current number of assigned papers.
- The system compares the reviewer’s current assignment count to a defined maximum assignment limit.
- If the reviewer is below the limit, the system allows the assignment to proceed and updates the reviewer’s assignment count.
- If the reviewer has reached (or would exceed) the limit, the system blocks the assignment and displays a clear message explaining that the reviewer cannot be assigned due to workload limits.
- The system does not create partial or inconsistent assignment records when blocking an assignment.
- The system handles retrieval or storage failures gracefully with clear error messages.
- All main, alternate, and failure flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- Editor accesses the system using a modern web browser.
- Editor is registered and logged in unless otherwise specified.
- At least one submitted paper exists.
- Reviewers exist in the system and each reviewer has an assignment count.
- A maximum reviewer assignment limit is defined in system configuration.
- Reviewer assignment actions and counts are stored in a database.

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC17-01  | Main Success Scenario – Reviewer Below Limit |
| AT-UC17-02  | Extension – Reviewer At Limit (Assignment Blocked) |
| AT-UC17-03  | Extension – Reviewer Would Exceed Limit (Assignment Blocked) |
| AT-UC17-04  | Extension – Assignment Count Cannot Be Retrieved |
| AT-UC17-05  | Failure End Scenario – System Fails to Update Assignment Count |

---

### Acceptance Test Cases

---

#### AT-UC17-01 — Assign Reviewer When Below Limit (Main Success Scenario)

**Purpose:**  
Verify that the system allows reviewer assignment when the reviewer has not reached the maximum workload limit and updates the assignment count.

**Preconditions:**
- CMS is running and accessible.
- Editor is logged in.
- A submitted paper exists.
- A reviewer exists with assigned-paper count strictly less than the maximum limit.
- The reviewer is not already assigned to the selected paper.

**Test Steps:**
1. Log in to the CMS as an editor.
2. Navigate to **Paper Management** and select a submitted paper.
3. Choose **Assign Reviewer(s)**.
4. Select the reviewer who is below the assignment limit.
5. Confirm the assignment.

**Expected Results:**
- The system retrieves the reviewer’s current assignment count.
- The system determines the reviewer is below the maximum limit.
- The system creates the reviewer assignment for the selected paper.
- The reviewer appears in the paper’s assigned reviewer list.
- The reviewer’s assignment count is incremented/updated appropriately.
- A success confirmation message is displayed.

---

#### AT-UC17-02 — Block Assignment When Reviewer Is At Limit (Extension)

**Purpose:**  
Verify that the system blocks assigning a reviewer who is already at the maximum assignment limit.

**Preconditions:**
- CMS is running and accessible.
- Editor is logged in.
- A submitted paper exists.
- A reviewer exists whose assignment count equals the maximum allowed limit.
- The reviewer is not already assigned to the selected paper.

**Test Steps:**
1. Log in to the CMS as an editor.
2. Navigate to **Paper Management** and select a submitted paper.
3. Choose **Assign Reviewer(s)**.
4. Select the reviewer who is at the assignment limit.
5. Confirm the assignment attempt.

**Expected Results:**
- The system retrieves the reviewer’s current assignment count.
- The system determines the reviewer has reached the maximum limit.
- The system blocks the assignment (no reviewer is added to the paper).
- The system displays a clear workload-limit error message.
- No partial assignment records are created.

---

#### AT-UC17-03 — Block Assignment That Would Exceed Limit (Extension)

**Purpose:**  
Verify that the system blocks reviewer assignment when the assignment would cause the reviewer to exceed the maximum allowed limit (e.g., concurrent assignments or batch assignment).

**Preconditions:**
- CMS is running and accessible.
- Editor is logged in.
- A submitted paper exists.
- A reviewer exists whose assignment count is one less than the maximum limit.
- The system supports actions that could add more than one assignment in a single operation (or a concurrency scenario can be simulated).

**Test Steps (Batch/Concurrent Scenario):**
1. Log in to the CMS as an editor.
2. Navigate to **Paper Management**.
3. Attempt to assign the same reviewer to multiple papers in rapid sequence or in a batch action such that the total would exceed the limit.
4. Observe the system response for the assignment that would exceed the limit.

**Expected Results:**
- The system allows assignments up to the maximum limit.
- The system blocks the assignment that would exceed the limit.
- The system displays a clear workload-limit message for the blocked assignment.
- The reviewer’s assignment count does not exceed the maximum limit.
- No inconsistent or duplicate assignment records are created.

---

#### AT-UC17-04 — Cannot Retrieve Reviewer Assignment Count (Extension)

**Purpose:**  
Verify system behavior when the reviewer’s current assignment count cannot be retrieved due to a system error.

**Preconditions:**
- CMS is running and accessible (UI reachable).
- Editor is logged in.
- A submitted paper exists.
- A backend/database/service failure is simulated for retrieving reviewer assignment counts.

**Test Steps:**
1. Log in to the CMS as an editor.
2. Navigate to **Paper Management** and select a submitted paper.
3. Choose **Assign Reviewer(s)**.
4. Select a reviewer.
5. Confirm the assignment attempt while retrieval failure condition exists.

**Expected Results:**
- The system fails to retrieve the reviewer’s current assignment count.
- The system displays an error message indicating the assignment cannot be completed at this time.
- The system does not create an assignment record.
- The system does not modify any reviewer assignment counts.

---

#### AT-UC17-05 — Fails to Update Assignment Count After Allowing Assignment (Failure End Scenario)

**Purpose:**  
Verify system behavior when the system allows the assignment decision (reviewer below limit) but fails while updating/storing the assignment count or saving the assignment transaction.

**Preconditions:**
- CMS is running and accessible (UI reachable).
- Editor is logged in.
- A submitted paper exists.
- A reviewer exists below the assignment limit.
- A backend/database failure can be simulated during the storage/update step (assignment write or count increment).

**Test Steps:**
1. Log in to the CMS as an editor.
2. Navigate to **Paper Management** and select a submitted paper.
3. Choose **Assign Reviewer(s)**.
4. Select a reviewer below the limit.
5. Confirm the assignment while storage/update failure condition exists.
6. Refresh and re-open the paper’s assigned reviewer list (and reviewer workload count if visible).

**Expected Results:**
- The system reports an error indicating the assignment could not be completed/saved.
- The paper does not show the reviewer as assigned (or, if partial write occurred, the system rolls back to a consistent state).
- The reviewer’s assignment count is not incremented (or is rolled back to its prior value).
- No inconsistent partial assignment records remain.
- The use case ends in failure for this assignment attempt.

---

### Completion Criteria

UC-17 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-18: Receive Notification of Submitted Reviews

---

### Use Case Under Test

**Use Case ID:** UC-18  
**Use Case Name:** Receive Notification of Submitted Reviews  
**Primary Actor:** Editor  
**Goal:** Notify the editor when a reviewer submits a review so the editor can track review progress and access the submitted review information.

---

### Acceptance Criteria

The system satisfies UC-18 if:

- When a reviewer submits a review, the system stores it and updates the paper’s review status.
- The system generates a notification to the editor indicating a review has been submitted.
- The editor can view the notification (in-app and/or email depending on implementation).
- The editor can navigate to the relevant paper and see updated review status and review content (as permitted).
- If notification delivery fails (e.g., email service down), the review is still recorded and visible in the editor’s paper management view.
- The system prevents unauthorized users from viewing editor notifications or submitted review details.
- The system provides clear feedback if review status or notifications cannot be retrieved due to system error.
- All main, alternate, and failure flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- Editor and reviewer accounts exist.
- At least one submitted paper exists with at least one reviewer assigned.
- Notification mechanisms may include:
  - In-app notification panel/dashboard alerts, and/or
  - Email notifications.
- Paper review status is visible to the editor via **Paper Management** or an equivalent interface.
- Review submission is performed through the reviewer workflow (review form submission).

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC18-01  | Main Success Scenario – Notification Delivered and Status Updated |
| AT-UC18-02  | Extension – Multiple Reviews Submitted (Multiple Notifications / Aggregation) |
| AT-UC18-03  | Extension – Notification Delivery Fails (Email/In-App) |
| AT-UC18-04  | Extension – Editor Not Logged In (Access Notification/Status) |
| AT-UC18-05  | Failure End Scenario – System Error Retrieving Notification or Review Status |

---

### Acceptance Test Cases

---

#### AT-UC18-01 — Receive Notification After Review Submission (Main Success Scenario)

**Purpose:**  
Verify that when a reviewer submits a review, the system updates review status and notifies the editor.

**Preconditions:**
- CMS is running and accessible.
- Editor account exists and is associated with the paper (has permission to manage/see reviews).
- Reviewer account exists and is assigned to the paper.
- Reviewer has not yet submitted a review for this paper.
- Notification system is available (in-app and/or email).

**Test Steps:**
1. Log in to the CMS as the reviewer.
2. Navigate to the assigned paper and open the review form.
3. Enter valid values in all required review fields.
4. Submit the review.
5. Log out (optional) and log in to the CMS as the editor.
6. Navigate to the editor’s notifications area (or inbox/email if applicable).
7. Open the notification referring to the submitted review.
8. Navigate to the relevant paper in **Paper Management** and view review status/details.

**Expected Results:**
- The system stores the submitted review successfully.
- The paper’s review status is updated (e.g., review count increases / status reflects new submission).
- The editor receives a notification indicating a review was submitted for the paper.
- The notification references the correct paper.
- The editor can access the paper and see updated status and submitted review content (as permitted).

---

#### AT-UC18-02 — Multiple Reviews Submitted (Extension)

**Purpose:**  
Verify that the system handles multiple review submissions by generating appropriate notifications and updating review status accordingly.

**Preconditions:**
- CMS is running and accessible.
- Editor account exists and has permission to view review progress.
- A submitted paper exists with two or more reviewers assigned.
- Notification system is available.

**Test Steps:**
1. Log in as Reviewer A and submit a valid review for the paper.
2. Log in as Reviewer B and submit a valid review for the same paper.
3. Log in as the editor.
4. Check notifications and the paper’s review status.

**Expected Results:**
- Both reviews are stored and associated with the correct reviewers and paper.
- The paper’s review status reflects both submissions (e.g., 2 reviews received).
- The editor receives either:
  - separate notifications for each submitted review, OR
  - a combined/aggregated notification indicating multiple reviews were received,
  depending on implementation.
- Notification(s) reference the correct paper and submission events.

---

#### AT-UC18-03 — Notification Delivery Fails (Extension)

**Purpose:**  
Verify that if notification delivery fails, the review is still recorded and visible to the editor through paper management.

**Preconditions:**
- CMS is running and accessible.
- Editor and reviewer accounts exist.
- Reviewer is assigned to a submitted paper.
- Notification service is unavailable (simulate in-app notification failure and/or email service down).

**Test Steps:**
1. Log in to the CMS as the reviewer.
2. Submit a valid review for the assigned paper while the notification failure condition exists.
3. Log in to the CMS as the editor.
4. Check the notifications area (and/or email if applicable).
5. Navigate to the paper in **Paper Management** and view review status/details.

**Expected Results:**
- The system stores the submitted review successfully.
- The paper’s review status is updated.
- The editor may not receive the expected notification due to delivery failure.
- The editor can still see updated review status and access review content via paper management.
- The system does not crash or expose sensitive internal error details.

---

#### AT-UC18-04 — Editor Not Logged In (Extension)

**Purpose:**  
Verify that an editor must be authenticated to view notifications and review status, and is redirected to login if not logged in.

**Preconditions:**
- CMS is running and accessible.
- A review has been submitted for a paper managed by the editor.
- Editor is not logged in.

**Test Steps:**
1. Attempt to access the editor notifications page directly (via URL) without logging in.
2. Observe system behavior.
3. Log in as the editor.
4. Navigate to notifications and/or paper management to view the update.

**Expected Results:**
- The system redirects the user to the login page when not authenticated.
- Notifications and review status are not visible before login.
- After login, the editor can access notifications and view updated paper review status.

---

#### AT-UC18-05 — System Error Retrieving Notification or Review Status (Failure End Scenario)

**Purpose:**  
Verify system behavior when a system/database error prevents the editor from retrieving notifications or updated review status.

**Preconditions:**
- CMS is running and accessible (UI reachable).
- A review has been submitted and stored.
- Editor is logged in.
- A backend/database failure can be simulated during retrieval of notifications or review status.

**Test Steps:**
1. Log in to the CMS as the editor.
2. Navigate to the notifications area while the retrieval failure condition exists.
3. Attempt to open the notification (if listed) or refresh notifications.
4. Navigate to **Paper Management** and attempt to view review status/details for the relevant paper.
5. Observe the system response.

**Expected Results:**
- The system displays an error message indicating notifications and/or review status cannot be retrieved.
- The system does not display incorrect or partial data as if it were complete.
- The editor remains authenticated and can navigate away safely.
- If the editor abandons the attempt, the use case ends in failure (notification/status not viewable at that time).

---

### Completion Criteria

UC-18 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-19: Make Final Paper Decision

---

### Use Case Under Test

**Use Case ID:** UC-19  
**Use Case Name:** Make Final Paper Decision  
**Primary Actor:** Editor  
**Goal:** Allow an editor to make and record the final acceptance or rejection decision for a submitted paper based on completed reviews.

---

### Acceptance Criteria

The system satisfies UC-19 if:

- A logged-in editor can access the paper decision workflow for a submitted paper.
- The system allows a final decision (Accept/Reject) only when required reviews are complete.
- The system records the final decision and updates the paper’s decision status.
- The system confirms to the editor that the decision was recorded successfully.
- The decision becomes visible to the author through the author portal (and/or via notification depending on implementation).
- The system supports an alternate path where the editor requests additional reviews when reviews are insufficient.
- The system prevents unauthorized users from making final decisions.
- The system provides clear feedback for validation errors, incomplete reviews, and system/storage failures.
- All main, alternate, and failure flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- Editor accesses the system using a modern web browser.
- Editor is registered and logged in unless otherwise specified.
- Papers exist in the system with varying review states:
  - **Paper A:** required reviews complete
  - **Paper B:** one or more required reviews incomplete
- The CMS defines what “required reviews complete” means (e.g., minimum number of reviews).
- The author portal supports viewing final decision status once recorded.
- Notification mechanisms (email/in-app) may exist and may succeed or fail depending on test setup.
- Database/server failures can be simulated for negative testing.

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC19-01  | Main Success Scenario – Record Final Decision (Accept) |
| AT-UC19-02  | Main Success Scenario Variant – Record Final Decision (Reject) |
| AT-UC19-03  | Extension – Reviews Incomplete (Decision Blocked) |
| AT-UC19-04  | Extension – Request Additional Reviews Instead of Final Decision |
| AT-UC19-05  | Extension – Editor Not Logged In / Not Authorized |
| AT-UC19-06  | Extension – Decision Notification Fails (Author Still Sees Decision in Portal) |
| AT-UC19-07  | Failure End Scenario – System Fails to Store Final Decision |

---

### Acceptance Test Cases

---

#### AT-UC19-01 — Record Final Decision: Accept (Main Success Scenario)

**Purpose:**  
Verify that an editor can record an **Accept** decision for a paper with completed required reviews and that the author can view the decision.

**Preconditions:**
- CMS is running and accessible.
- Editor is logged in.
- Paper A exists with required reviews complete.
- Paper A does not already have a recorded final decision.

**Test Steps:**
1. Log in to the CMS as the editor.
2. Navigate to **Paper Management** (or equivalent).
3. Select Paper A.
4. Open the **Final Decision** (or equivalent) interface.
5. Verify review status indicates required reviews are complete.
6. Select decision = **Accept**.
7. Submit/confirm the final decision.
8. Log in as the author of Paper A and navigate to **My Submissions**.
9. Open Paper A and view decision status.

**Expected Results:**
- The system allows the decision submission because required reviews are complete.
- The system records the **Accept** decision and updates paper decision status.
- The editor sees a success confirmation message.
- The author can view the **Accepted** decision status for Paper A in the portal.
- The decision shown corresponds to the correct paper.

---

#### AT-UC19-02 — Record Final Decision: Reject (Main Success Scenario Variant)

**Purpose:**  
Verify that an editor can record a **Reject** decision for a paper with completed required reviews and that the author can view the decision.

**Preconditions:**
- CMS is running and accessible.
- Editor is logged in.
- Paper A (or another test paper) exists with required reviews complete.
- The paper does not already have a recorded final decision.

**Test Steps:**
1. Log in to the CMS as the editor.
2. Navigate to **Paper Management** and select the target paper.
3. Open the **Final Decision** interface.
4. Confirm required reviews are complete.
5. Select decision = **Reject**.
6. Submit/confirm the final decision.
7. Log in as the author and navigate to **My Submissions**.
8. Open the paper and view decision status.

**Expected Results:**
- The system records the **Reject** decision and updates paper decision status.
- The editor receives a success confirmation message.
- The author can view the **Rejected** decision status for the paper in the portal.

---

#### AT-UC19-03 — Reviews Incomplete: Block Final Decision (Extension)

**Purpose:**  
Verify that the system prevents an editor from making a final decision when required reviews are not complete.

**Preconditions:**
- CMS is running and accessible.
- Editor is logged in.
- Paper B exists with one or more required reviews incomplete.
- Paper B does not already have a recorded final decision.

**Test Steps:**
1. Log in to the CMS as the editor.
2. Navigate to **Paper Management** and select Paper B.
3. Open the **Final Decision** interface.
4. Attempt to select **Accept** (or **Reject**) and submit the decision.

**Expected Results:**
- The system detects that required reviews are incomplete.
- The system blocks final decision submission.
- The system displays a clear message indicating the decision cannot be made until required reviews are complete.
- No final decision is recorded for Paper B.

---

#### AT-UC19-04 — Request Additional Reviews (Extension)

**Purpose:**  
Verify that the editor can choose an alternate path to request additional reviews instead of making a final decision.

**Preconditions:**
- CMS is running and accessible.
- Editor is logged in.
- Paper B exists and is eligible for requesting additional reviews (e.g., insufficient reviews or editor chooses to request more).
- Additional reviewers are available.

**Test Steps:**
1. Log in as the editor.
2. Navigate to **Paper Management** and select Paper B.
3. Open the decision/review management interface.
4. Choose the option to **Request Additional Reviews** (or equivalent).
5. Select one or more additional reviewers (or initiate the request workflow).
6. Confirm the request.

**Expected Results:**
- The system records the request for additional reviews (and/or creates new reviewer assignments).
- The paper remains in a non-finalized state (no Accept/Reject recorded).
- The editor receives confirmation that additional reviews were requested.
- (If notifications are implemented) new invitations/notifications are initiated for the assigned reviewers.

---

#### AT-UC19-05 — Editor Not Logged In / Not Authorized (Extension)

**Purpose:**  
Verify that unauthenticated or unauthorized users cannot make final paper decisions.

**Preconditions:**
- CMS is running and accessible.
- A submitted paper exists.

**Test Steps:**
1. Attempt to access the final decision interface without logging in.
2. Observe system behavior (redirect to login).
3. Log in as a non-editor user (optional).
4. Attempt to access the final decision interface and submit a decision.

**Expected Results:**
- If not logged in: the system redirects to login and prevents access to decision actions.
- If logged in as non-editor: the system denies access and displays an authorization error.
- No final decision is recorded by unauthorized users.

---

#### AT-UC19-06 — Decision Notification Fails (Extension)

**Purpose:**  
Verify that if author notification fails (email/in-app), the decision is still recorded and visible in the author portal.

**Preconditions:**
- CMS is running and accessible.
- Editor is logged in.
- Paper A exists with required reviews complete.
- Notification service is unavailable (simulate email/in-app failure).

**Test Steps:**
1. Log in as the editor.
2. Navigate to Paper A and record a final decision (Accept or Reject) while notification failure exists.
3. Observe editor confirmation.
4. Log in as the author and view Paper A decision status in the portal.
5. Check that no notification was received (if applicable to implementation).

**Expected Results:**
- The system records the final decision successfully.
- The editor sees a success confirmation message.
- The author can view the decision in the portal even if notification delivery failed.
- The system may display/log an informational message to the editor that notification delivery failed (optional).

---

#### AT-UC19-07 — Fail to Store Final Decision (Failure End Scenario)

**Purpose:**  
Verify system behavior when a backend/database error prevents storing the final decision.

**Preconditions:**
- CMS is running and accessible (UI reachable).
- Editor is logged in.
- A paper with required reviews complete exists.
- A backend/database failure can be simulated during decision storage.

**Test Steps:**
1. Log in as the editor.
2. Navigate to **Paper Management** and select the target paper.
3. Open the **Final Decision** interface.
4. Select **Accept** or **Reject**.
5. Submit the decision while the storage failure condition exists.
6. Refresh the page and re-open the paper’s decision status.
7. Log in as the author and check whether a decision is visible.

**Expected Results:**
- The system displays an error message indicating the decision could not be saved.
- No final decision is recorded (paper remains undecided).
- The author does not see a new decision status as recorded.
- The system does not expose sensitive internal error details.
- The use case ends in failure for this decision attempt.

---

### Completion Criteria

UC-19 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-20: Configure Conference Parameters

---

### Use Case Under Test

**Use Case ID:** UC-20  
**Use Case Name:** Configure Conference Parameters  
**Primary Actor:** Administrator  
**Goal:** Allow an administrator to configure core conference parameters (e.g., dates, submission deadlines, review deadlines, registration settings) so the CMS behaves according to the conference setup.

---

### Acceptance Criteria

The system satisfies UC-20 if:

- A logged-in administrator can access the conference configuration/settings interface.
- The system displays editable conference parameters (as defined by the CMS) and their current values.
- The system validates parameter inputs (required fields, correct data types, valid date ranges).
- The system prevents saving invalid configurations and provides clear validation feedback.
- On successful save, the system persists configuration changes and confirms success.
- Updated configuration values take effect in the relevant parts of the CMS (e.g., deadlines affect submission availability).
- The system restricts access so only administrators can change conference parameters.
- The system handles storage/retrieval failures gracefully with clear error feedback.
- All main, alternate, and failure flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- Administrator accesses the system using a modern web browser.
- Administrator account exists and can authenticate successfully.
- The CMS includes a configuration/settings page for conference parameters.
- Conference parameters include at minimum:
  - Conference name (optional)
  - Key dates (conference dates)
  - Submission deadlines
  - Review deadlines
  - Registration open/close dates (if applicable)
- The system stores configuration in a database and uses it to control CMS behavior (e.g., feature availability).

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC20-01  | Main Success Scenario – Update Parameters Successfully |
| AT-UC20-02  | Extension – Administrator Not Logged In / Not Authorized |
| AT-UC20-03  | Extension – Invalid Parameter Values (Validation Failure) |
| AT-UC20-04  | Extension – Invalid Date Relationships (e.g., deadline after conference date) |
| AT-UC20-05  | Extension – Configuration Retrieval Fails |
| AT-UC20-06  | Failure End Scenario – System Fails to Store Updated Parameters |

---

### Acceptance Test Cases

---

#### AT-UC20-01 — Update Conference Parameters Successfully (Main Success Scenario)

**Purpose:**  
Verify that an administrator can update conference configuration parameters and that changes persist and take effect.

**Preconditions:**
- CMS is running and accessible.
- Administrator is logged in.
- Conference configuration page is available.

**Test Steps:**
1. Log in to the CMS as an administrator.
2. Navigate to **Admin Settings** / **Conference Configuration** (or equivalent).
3. Verify current configuration values are displayed.
4. Modify one or more parameters with valid values (e.g., update submission deadline, review deadline).
5. Save the configuration changes.
6. Observe confirmation.
7. Refresh the page and verify the updated values persist.
8. Navigate to a relevant user workflow affected by the change (e.g., submission portal) to confirm behavior reflects the new configuration.

**Expected Results:**
- The system accepts valid parameter updates.
- The system saves changes and displays a success message.
- Updated values persist on reload.
- Relevant CMS behavior reflects the new configuration (e.g., deadlines/availability updated as expected).

---

#### AT-UC20-02 — Administrator Not Logged In / Not Authorized (Extension)

**Purpose:**  
Verify that only administrators can access and modify conference parameters.

**Preconditions:**
- CMS is running and accessible.
- User is not logged in OR is logged in as a non-admin role.

**Test Steps:**
1. Attempt to access the conference configuration page without logging in.
2. Observe system behavior.
3. Log in as a non-admin user (optional).
4. Attempt to access the conference configuration page and modify parameters.

**Expected Results:**
- If not logged in: system redirects to login and prevents access.
- If logged in as non-admin: system denies access and displays an authorization error.
- Non-admin users cannot save configuration changes.

---

#### AT-UC20-03 — Invalid Parameter Values (Validation Failure) (Extension)

**Purpose:**  
Verify that the system rejects invalid configuration values and provides clear validation messages.

**Preconditions:**
- CMS is running and accessible.
- Administrator is logged in.
- Conference configuration page is available.

**Test Steps:**
1. Navigate to the conference configuration page.
2. Enter invalid values in one or more fields (examples):
   - Leave a required field blank.
   - Enter letters into a numeric field (if any).
   - Enter an invalid date format (if not using a date picker).
3. Attempt to save the configuration.

**Expected Results:**
- The system detects invalid inputs.
- The system prevents saving.
- The system displays clear validation errors indicating which fields must be corrected.
- No configuration changes are persisted.

---

#### AT-UC20-04 — Invalid Date Relationships (Extension)

**Purpose:**  
Verify that the system enforces valid relationships between key dates (e.g., submission deadline must be before review deadline, deadlines must be before conference dates).

**Preconditions:**
- CMS is running and accessible.
- Administrator is logged in.

**Test Steps:**
1. Navigate to conference configuration.
2. Set an invalid date relationship (examples):
   - Submission deadline after review deadline.
   - Review deadline after conference start date.
3. Attempt to save the configuration.

**Expected Results:**
- The system detects invalid date relationships.
- The system prevents saving.
- The system displays a clear message explaining the date constraint violation.
- No invalid configuration changes are persisted.

---

#### AT-UC20-05 — Configuration Retrieval Fails (Extension)

**Purpose:**  
Verify system behavior when the configuration settings cannot be loaded due to a backend/database error.

**Preconditions:**
- CMS UI is reachable.
- Administrator is logged in.
- A backend/database/service failure can be simulated during configuration retrieval.

**Test Steps:**
1. Log in to the CMS as an administrator.
2. Navigate to the conference configuration page while the failure condition exists.
3. Observe the system response.
4. Retry loading the page (optional).

**Expected Results:**
- The system displays an error message indicating configuration cannot be loaded.
- The system does not display incorrect or partial configuration as if complete.
- The administrator can retry later or navigate away safely.

---

#### AT-UC20-06 — Fail to Store Updated Parameters (Failure End Scenario)

**Purpose:**  
Verify system behavior when the system fails to save configuration changes due to a backend/database error.

**Preconditions:**
- CMS is running and accessible (UI reachable).
- Administrator is logged in.
- A backend/database failure can be simulated during configuration save.

**Test Steps:**
1. Navigate to conference configuration.
2. Modify one or more parameters with valid values.
3. Attempt to save while the storage failure condition exists.
4. Observe the system response.
5. Refresh the configuration page and check whether changes persisted.

**Expected Results:**
- The system displays an error message indicating the configuration could not be saved.
- The system does not show a success confirmation.
- Changes are not persisted after refresh (configuration remains unchanged).
- The system does not expose sensitive internal error details.
- The use case ends in failure for this save attempt.

---

### Completion Criteria

UC-20 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-21: Generate Conference Schedule

---

### Use Case Under Test

**Use Case ID:** UC-21  
**Use Case Name:** Generate Conference Schedule  
**Primary Actor:** Administrator  
**Secondary Actor(s):** Editor, Database  
**Goal:** Allow an administrator to generate an initial conference schedule so that accepted papers are assigned presentation times and rooms.

---

### Acceptance Criteria

The system satisfies UC-21 if:

- A logged-in administrator can access the conference scheduling section and initiate schedule generation.
- The system retrieves accepted papers and available scheduling resources (rooms, time slots, conference dates/parameters).
- The system applies a scheduling algorithm to assign accepted papers to time slots and rooms.
- The system stores the generated schedule in the database and displays it to the administrator.
- If no accepted papers exist, the system blocks generation and displays a clear message.
- If scheduling constraints cannot be satisfied (e.g., insufficient rooms/time slots), the system reports the issue clearly and allows the administrator to adjust parameters and retry.
- If schedule generation fails due to an internal error, the system reports failure and does not store a partial schedule as successful.
- If saving the schedule fails, the system reports the save failure and does not claim generation completed successfully.
- All main, alternate, and failure flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- Administrator accesses the system using a modern web browser.
- Administrator is registered and logged in unless otherwise specified.
- A set of accepted papers may or may not exist depending on the test.
- Scheduling parameters/resources exist in the system (rooms, time slots, conference dates), unless the test intentionally violates constraints.
- The system stores schedules in a database and displays them in a readable format after generation.

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC21-01  | Main Success Scenario |
| AT-UC21-02  | Extension 4a – No Accepted Papers Are Available |
| AT-UC21-03  | Extension 5a – Scheduling Constraints Cannot Be Satisfied (Adjust + Retry) |
| AT-UC21-04  | Extension 6a – System Fails During Schedule Generation |
| AT-UC21-05  | Extension 7a / Failure End Scenario – System Fails to Store Generated Schedule |

---

### Acceptance Test Cases

---

#### AT-UC21-01 — Generate Conference Schedule Successfully (Main Success Scenario)

**Purpose:**  
Verify that an administrator can generate a schedule when accepted papers and valid scheduling resources exist, and that the schedule is stored and displayed.

**Preconditions:**
- CMS is running and accessible.
- Administrator is logged in.
- One or more accepted papers exist in the system.
- Scheduling parameters/resources (rooms, time slots, conference dates) are available and sufficient.

**Test Steps:**
1. Log in to the CMS as an administrator.
2. Navigate to the **Conference Scheduling** section.
3. Select **Generate Conference Schedule** (or equivalent).
4. Allow the system to retrieve accepted papers and scheduling resources.
5. Allow the system to run the scheduling algorithm.
6. Observe the generated schedule display.
7. Refresh the page (or re-open the schedule view) to confirm it was stored.

**Expected Results:**
- The system generates a valid conference schedule.
- The system stores the schedule in the database.
- The system displays the generated schedule to the administrator.
- After refresh/re-open, the schedule remains available and unchanged (persisted).

---

#### AT-UC21-02 — No Accepted Papers Available (Extension 4a)

**Purpose:**  
Verify that schedule generation is blocked when there are no accepted papers, and the system provides clear feedback.

**Preconditions:**
- CMS is running and accessible.
- Administrator is logged in.
- No accepted papers exist in the system.

**Test Steps:**
1. Log in to the CMS as an administrator.
2. Navigate to the **Conference Scheduling** section.
3. Select **Generate Conference Schedule**.
4. Observe the system response.

**Expected Results:**
- The system detects there are no accepted papers.
- The system displays a message indicating schedule generation cannot proceed without accepted papers.
- No schedule is generated or stored.
- The administrator can safely abandon the attempt.

---

#### AT-UC21-03 — Scheduling Constraints Cannot Be Satisfied (Extension 5a)

**Purpose:**  
Verify that the system detects unsatisfiable scheduling constraints, reports the issue clearly, and allows the administrator to adjust parameters and retry.

**Preconditions:**
- CMS is running and accessible.
- Administrator is logged in.
- One or more accepted papers exist.
- Scheduling resources/parameters are intentionally insufficient or conflicting (e.g., too few rooms or too few time slots).

**Test Steps:**
1. Log in to the CMS as an administrator.
2. Navigate to **Conference Scheduling**.
3. Select **Generate Conference Schedule** with the current (insufficient/conflicting) parameters.
4. Observe the error feedback.
5. Adjust scheduling parameters/resources (e.g., add rooms, expand time slots, adjust dates).
6. Retry schedule generation.

**Expected Results:**
- The system detects constraint violations (conflicts/insufficient resources).
- The system displays an error message describing the constraint issue.
- No schedule is stored as successfully generated while constraints are unsatisfied.
- After adjusting parameters, generation can proceed and a schedule is generated, stored, and displayed successfully.

---

#### AT-UC21-04 — System Fails During Schedule Generation (Extension 6a)

**Purpose:**  
Verify that the system handles internal errors during schedule generation and does not store a partial or invalid schedule as successful.

**Preconditions:**
- CMS is running and accessible (UI reachable).
- Administrator is logged in.
- Accepted papers exist.
- Scheduling resources are available.
- An internal error can be simulated during scheduling algorithm execution (e.g., service failure, unhandled exception).

**Test Steps:**
1. Log in to the CMS as an administrator.
2. Navigate to **Conference Scheduling**.
3. Select **Generate Conference Schedule** while the generation failure condition exists.
4. Observe the system response.
5. Check whether any schedule appears as newly generated/stored (e.g., schedule list/history, schedule view).

**Expected Results:**
- The system reports that schedule generation failed (clear error message).
- The system does not display a success confirmation.
- The system does not store a new schedule as successfully generated (no new valid schedule is created/visible as saved).
- The administrator may retry later or abandon the attempt.

---

#### AT-UC21-05 — Fail to Store Generated Schedule (Extension 7a / Failure End Scenario)

**Purpose:**  
Verify that if the system generates a schedule but fails to store it, the system reports the save failure and does not claim the schedule was successfully created.

**Preconditions:**
- CMS is running and accessible (UI reachable).
- Administrator is logged in.
- Accepted papers exist.
- Scheduling resources are available and sufficient.
- A database/server/storage failure can be simulated during the “store schedule” step.

**Test Steps:**
1. Log in to the CMS as an administrator.
2. Navigate to **Conference Scheduling**.
3. Select **Generate Conference Schedule** while the storage failure condition exists.
4. Observe the system response.
5. Refresh the schedule view or check schedule listings to confirm whether a new schedule exists.

**Expected Results:**
- The system displays an error message indicating the generated schedule could not be saved.
- The system does not display a success confirmation for generation completion.
- No new schedule is persisted/available after refresh (or the system rolls back to a consistent state).
- The administrator may retry later; if they abandon the attempt, the use case ends in failure.

---

### Completion Criteria

UC-21 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-22: Publish Conference Schedule

---

### Use Case Under Test

**Use Case ID:** UC-22  
**Use Case Name:** Publish Conference Schedule  
**Primary Actor:** Administrator  
**Goal:** Allow an administrator to publish the conference schedule so that users (especially authors of accepted papers) can view finalized presentation times and locations.

---

### Acceptance Criteria

The system satisfies UC-22 if:

- A logged-in administrator can access the schedule management area and publish a generated schedule.
- The system publishes only a valid, existing schedule (i.e., a schedule must already be generated).
- Publishing makes the schedule visible to intended audiences (e.g., authors/guests depending on system rules).
- The system records the schedule’s published state and persists it across sessions.
- The system provides clear feedback when:
  - no schedule exists to publish,
  - the schedule is invalid/incomplete,
  - publication fails due to system/storage issues,
  - notifications fail (if notifications are part of the use case).
- Access control is enforced so only administrators can publish schedules.
- All main, alternate, and failure flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- Administrator accesses the system using a modern web browser.
- Administrator is logged in unless otherwise specified.
- A conference schedule may exist in either:
  - **Generated but Unpublished** state, or
  - **Published** state.
- Publishing toggles visibility of the schedule for non-admin users.
- Notification mechanisms (email/in-app) may exist to inform authors/users that the schedule has been published (implementation-dependent).
- Database/server failures can be simulated for negative tests.

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC22-01  | Main Success Scenario – Publish Existing Schedule |
| AT-UC22-02  | Extension – No Schedule Exists to Publish |
| AT-UC22-03  | Extension – Schedule Exists but Is Invalid/Incomplete |
| AT-UC22-04  | Extension – Administrator Not Logged In / Not Authorized |
| AT-UC22-05  | Extension – Notification Delivery Fails (If Applicable) |
| AT-UC22-06  | Failure End Scenario – System Fails to Store Published State |

---

### Acceptance Test Cases

---

#### AT-UC22-01 — Publish Conference Schedule Successfully (Main Success Scenario)

**Purpose:**  
Verify that an administrator can publish an existing schedule and that it becomes visible to intended users.

**Preconditions:**
- CMS is running and accessible.
- Administrator is logged in.
- A conference schedule exists and is currently **unpublished**.
- The schedule is valid (has assigned time slots and rooms/locations for scheduled items).

**Test Steps:**
1. Log in to the CMS as an administrator.
2. Navigate to **Conference Scheduling** / **Schedule Management**.
3. Open the existing generated schedule.
4. Select **Publish Schedule** (or equivalent).
5. Confirm the publish action (if confirmation is required).
6. Log out and log in as a non-admin user (e.g., author with an accepted paper) or access as a guest (depending on visibility rules).
7. Navigate to the schedule view page.

**Expected Results:**
- The system marks the schedule as **Published**.
- The system displays a success confirmation message to the administrator.
- The schedule is visible to intended users according to access rules.
- The published status persists after refresh/reload (state is stored).

---

#### AT-UC22-02 — No Schedule Exists to Publish (Extension)

**Purpose:**  
Verify that the system blocks publishing when there is no generated schedule.

**Preconditions:**
- CMS is running and accessible.
- Administrator is logged in.
- No conference schedule exists (no generated schedule stored).

**Test Steps:**
1. Log in to the CMS as an administrator.
2. Navigate to **Conference Scheduling** / **Schedule Management**.
3. Attempt to publish the schedule (if the option is available), or attempt to open a schedule publish workflow.

**Expected Results:**
- The system indicates there is no schedule to publish.
- The system prevents publication.
- No schedule visibility changes occur.
- The system does not show a success confirmation.

---

#### AT-UC22-03 — Schedule Invalid or Incomplete (Extension)

**Purpose:**  
Verify that the system prevents publishing an invalid or incomplete schedule and provides clear feedback.

**Preconditions:**
- CMS is running and accessible.
- Administrator is logged in.
- A schedule exists but is invalid/incomplete (e.g., missing room assignments, missing time slots, conflicts).

**Test Steps:**
1. Log in to the CMS as an administrator.
2. Navigate to **Schedule Management** and open the existing schedule.
3. Select **Publish Schedule**.
4. Observe system feedback.

**Expected Results:**
- The system detects the schedule is invalid/incomplete.
- The system blocks publication.
- The system displays a clear error message describing what must be fixed (e.g., missing assignments/conflicts).
- The schedule remains unpublished and not visible to intended non-admin audiences.

---

#### AT-UC22-04 — Administrator Not Logged In / Not Authorized (Extension)

**Purpose:**  
Verify that only administrators can publish schedules.

**Preconditions:**
- CMS is running and accessible.
- A schedule exists (published or unpublished).
- User is not logged in OR is logged in as a non-admin role.

**Test Steps:**
1. Attempt to access **Schedule Management** or the publish action URL without logging in.
2. Observe system behavior.
3. Log in as a non-admin user (optional).
4. Attempt to publish the schedule.

**Expected Results:**
- If not logged in: system redirects to login and prevents access to publish actions.
- If logged in as non-admin: system denies access and displays an authorization error.
- No schedule is published by unauthorized users.

---

#### AT-UC22-05 — Notification Delivery Fails (Extension, If Applicable)

**Purpose:**  
Verify system behavior when publishing succeeds but notifying users fails (if notifications are part of the implementation).

**Preconditions:**
- CMS is running and accessible.
- Administrator is logged in.
- A valid unpublished schedule exists.
- Notification service is unavailable (simulate email/in-app notification failure).

**Test Steps:**
1. Log in to the CMS as an administrator.
2. Navigate to **Schedule Management** and select **Publish Schedule** while notification failure exists.
3. Observe system response.
4. Log in as a non-admin user and attempt to view the schedule.

**Expected Results:**
- The schedule is published successfully (published state recorded).
- The system informs the administrator that notification delivery failed (message or logged warning), if applicable.
- The schedule remains visible to intended users even if notifications fail.
- The system does not crash or expose sensitive internal error details.

---

#### AT-UC22-06 — Fail to Store Published State (Failure End Scenario)

**Purpose:**  
Verify system behavior when the system cannot persist the published status due to a storage/database failure.

**Preconditions:**
- CMS is running and accessible (UI reachable).
- Administrator is logged in.
- A valid unpublished schedule exists.
- A backend/database failure can be simulated during the “store published state” step.

**Test Steps:**
1. Log in to the CMS as an administrator.
2. Navigate to **Schedule Management** and attempt to **Publish Schedule** while the storage failure condition exists.
3. Observe the system response.
4. Refresh the schedule page and check published status.
5. Log in as a non-admin user and attempt to view the schedule.

**Expected Results:**
- The system displays an error message indicating publication could not be completed/saved.
- The system does not display a success confirmation.
- The schedule remains unpublished (or the system rolls back to a consistent unpublished state).
- The schedule is not visible to users who should only see published schedules.
- The use case ends in failure for this publish attempt.

---

### Completion Criteria

UC-22 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-23: Publish Conference Schedule

---

### Use Case Under Test

**Use Case ID:** UC-23  
**Use Case Name:** Publish Conference Schedule  
**Primary Actor:** Administrator  
**Goal:** Allow an administrator to publish the finalized conference schedule so that authors, attendees, and the public can view it.

---

### Acceptance Criteria

The system satisfies UC-23 if:

- A logged-in administrator can initiate schedule publication from the conference scheduling section.
- The system validates that the schedule is **finalized and approved** before publishing.
- On success, the schedule becomes accessible on the CMS website to intended users (authors, attendees, and guests/public).
- The system stores the schedule state as **published** in the database.
- The system sends notifications to authors and attendees (if supported by the implementation).
- The system prevents publication if the schedule is not finalized/approved and provides clear feedback.
- If publication fails (server/deployment issue), the system reports the failure and the schedule remains unpublished.
- If notification delivery fails, the schedule remains accessible and the system logs/indicates the notification failure appropriately.
- All main, alternate, and failure flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- Administrator accesses the system using a modern web browser.
- Administrator is registered and logged in unless otherwise specified.
- A conference schedule exists in the system with one of the following states:
  - Finalized & Approved (eligible to publish)
  - Not Finalized and/or Not Approved (not eligible to publish)
- Publishing makes the schedule available on a public-facing schedule page or portal page.
- Notifications may be in-app notifications and/or email depending on system implementation.
- Database/server failures can be simulated for negative testing.

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC23-01  | Main Success Scenario – Publish Approved Schedule |
| AT-UC23-02  | Extension 1a – Administrator Not Logged In |
| AT-UC23-03  | Extension 4a – Schedule Not Finalized or Approved |
| AT-UC23-04  | Extension 5a – System Fails to Publish Schedule (Server/Deployment Error) |
| AT-UC23-05  | Extension 7a – Notification Delivery Fails |
| AT-UC23-06  | Failure End Scenario – System Error Updating Publication Status |

---

### Acceptance Test Cases

---

#### AT-UC23-01 — Publish Approved Schedule Successfully (Main Success Scenario)

**Purpose:**  
Verify that an administrator can publish a finalized and approved schedule, making it accessible to intended users, and that the system records the published state.

**Preconditions:**
- CMS is running and accessible.
- Administrator is logged in.
- A schedule exists that is finalized and approved.
- Schedule is currently unpublished.

**Test Steps:**
1. Log in to the CMS as an administrator.
2. Navigate to the **Conference Scheduling** section.
3. Select the option to **Publish Conference Schedule**.
4. Confirm the publish action (if confirmation is required).
5. Navigate to the public schedule page (as a guest) or to an author/attendee schedule page (as logged-in user), depending on visibility rules.
6. Refresh the schedule management page and verify published status.

**Expected Results:**
- The system validates that the schedule is finalized and approved.
- The system publishes the schedule and makes it accessible to intended users.
- The system stores the schedule status as **published**.
- The administrator sees a confirmation message indicating successful publication.
- The schedule remains accessible after refresh/reload (publication persists).

---

#### AT-UC23-02 — Administrator Not Logged In (Extension 1a)

**Purpose:**  
Verify that an administrator must be authenticated to publish the schedule and is redirected to login if not logged in.

**Preconditions:**
- CMS is running and accessible.
- Administrator is not logged in.
- A finalized and approved schedule exists in the system.

**Test Steps:**
1. Attempt to access the schedule publication action/page without logging in (via navigation or direct URL).
2. Observe the system behavior.
3. Log in with valid administrator credentials.
4. Navigate back to **Conference Scheduling** and attempt publication again.

**Expected Results:**
- The system redirects the user to the login page when not authenticated.
- No publication occurs before login.
- After login, the use case resumes and the administrator can proceed to publish.

---

#### AT-UC23-03 — Schedule Not Finalized or Approved (Extension 4a)

**Purpose:**  
Verify that the system prevents publication if the schedule is incomplete or not approved, and provides clear feedback.

**Preconditions:**
- CMS is running and accessible.
- Administrator is logged in.
- A schedule exists but is not finalized and/or not approved.

**Test Steps:**
1. Navigate to **Conference Scheduling** as an administrator.
2. Select **Publish Conference Schedule**.
3. Observe system feedback.

**Expected Results:**
- The system detects the schedule is not finalized/approved.
- The system prevents publication.
- The system displays a message indicating finalization/approval is required.
- The schedule remains unpublished and inaccessible to users who require published access.

---

#### AT-UC23-04 — System Fails to Publish Schedule (Server/Deployment Error) (Extension 5a)

**Purpose:**  
Verify system behavior when a server/deployment error prevents publication and the schedule remains unpublished.

**Preconditions:**
- CMS is running and accessible (UI reachable).
- Administrator is logged in.
- A schedule exists that is finalized and approved.
- A server/deployment failure can be simulated during the publish operation.

**Test Steps:**
1. Navigate to **Conference Scheduling** as an administrator.
2. Select **Publish Conference Schedule** while the publish failure condition exists.
3. Observe the system response.
4. Attempt to view the schedule as an intended user (author/attendee/guest as applicable).
5. Refresh the admin schedule status page.

**Expected Results:**
- The system displays an error message indicating publication failure.
- The system does not display a success confirmation.
- The schedule remains unpublished and not accessible to audiences that require published access.
- The schedule’s published status is not set (no partial success).

---

#### AT-UC23-05 — Notification Delivery Fails (Extension 7a)

**Purpose:**  
Verify that if notification delivery fails, the schedule is still published and accessible, and the system reports/logs the notification failure.

**Preconditions:**
- CMS is running and accessible.
- Administrator is logged in.
- A schedule exists that is finalized and approved.
- Notification service is unavailable (simulate notification failure).

**Test Steps:**
1. Navigate to **Conference Scheduling** as an administrator.
2. Select **Publish Conference Schedule** while notification failure condition exists.
3. Observe system feedback regarding notifications (if presented).
4. Attempt to access the schedule as an author/attendee/guest (as applicable).

**Expected Results:**
- The system publishes the schedule successfully (schedule accessible to intended users).
- The system indicates and/or logs that notification delivery failed.
- The system does not roll back schedule publication due to notification failure.
- The administrator sees a publication confirmation (optionally accompanied by a warning about notifications).

---

#### AT-UC23-06 — System Error Updating Publication Status (Failure End Scenario)

**Purpose:**  
Verify system behavior when publication status cannot be updated in the database due to a database/server error and the schedule remains unpublished.

**Preconditions:**
- CMS is running and accessible (UI reachable).
- Administrator is logged in.
- A schedule exists that is finalized and approved.
- A database/server failure can be simulated during “set published status” storage/update.

**Test Steps:**
1. Navigate to **Conference Scheduling** as an administrator.
2. Select **Publish Conference Schedule** while the storage/update failure condition exists.
3. Observe the system response.
4. Refresh the admin schedule status page.
5. Attempt to access the schedule as an author/attendee/guest (as applicable).

**Expected Results:**
- The system displays an error message indicating the schedule could not be published at this time.
- The system does not show a success confirmation.
- The schedule remains unpublished (or the system rolls back to a consistent unpublished state).
- The schedule is not accessible to audiences that require published access.
- The use case ends in failure for this publish attempt.

---

### Completion Criteria

UC-23 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-24: Register for Conference Attendance

---

### Use Case Under Test

**Use Case ID:** UC-24  
**Use Case Name:** Register for Conference Attendance  
**Primary Actor:** Attendee (Registered User)  
**Goal:** Allow an attendee to register for conference attendance so they can participate in the event.

---

### Acceptance Criteria

The system satisfies UC-24 if:

- A logged-in attendee can register for the conference when registration is open.
- The system displays available attendance types (if applicable) and accepts a valid selection.
- The system records the attendee’s registration and confirms success.
- The system directs the attendee to the payment process (if payment is required).
- The system prevents registration when registration is closed and provides clear feedback.
- The system prevents unauthenticated registration attempts by redirecting to login.
- The system handles invalid attendance type selections and storage/system errors gracefully.
- All main, alternate, and failure flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- Attendee accesses the system using a modern web browser.
- Attendee account exists in the CMS.
- Conference registration status (open/closed) is controlled via system configuration.
- Attendance types (e.g., Student/Professional/Virtual) may be configured and may become unavailable.
- Payment may be required and is triggered after successful registration (implementation-dependent).
- Database/server failures can be simulated for negative testing.

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC24-01  | Main Success Scenario |
| AT-UC24-02  | Extension – Attendee Not Logged In |
| AT-UC24-03  | Extension – Conference Registration Closed |
| AT-UC24-04  | Extension – Invalid or Unavailable Attendance Type |
| AT-UC24-05  | Extension – Payment Service Unavailable (If Applicable) |
| AT-UC24-06  | Failure End Scenario – System Fails to Record Registration |

---

### Acceptance Test Cases

---

#### AT-UC24-01 — Register for Conference Successfully (Main Success Scenario)

**Purpose:**  
Verify that an authenticated attendee can successfully register for the conference and proceed to payment if required.

**Preconditions:**
- CMS is running and accessible.
- Conference registration is open.
- Attendee is registered and logged in.
- At least one valid attendance type exists (if attendance types are used).

**Test Steps:**
1. Log in to the CMS as an attendee.
2. Navigate to the **Conference Registration** section.
3. Select **Register for Conference** (or equivalent).
4. If prompted, select a valid attendance type.
5. Confirm the registration request.
6. Observe the system response after confirmation.

**Expected Results:**
- The system accepts the registration request.
- The system records the attendee registration.
- The system displays a confirmation message indicating registration success.
- If payment is required, the system directs the attendee to the payment process/page.

---

#### AT-UC24-02 — Attendee Not Logged In (Extension)

**Purpose:**  
Verify that unauthenticated users are redirected to login before registering, and can continue registration after login.

**Preconditions:**
- CMS is running and accessible.
- Conference registration is open.
- User is not logged in.

**Test Steps:**
1. Attempt to access the conference registration page (via navigation or direct URL).
2. Observe the system response.
3. Log in with valid attendee credentials when prompted.
4. Continue the registration flow and confirm registration using a valid attendance type (if applicable).

**Expected Results:**
- The system redirects the user to the login page when not authenticated.
- The user cannot register without logging in.
- After successful login, the user can access the registration page and complete registration.

---

#### AT-UC24-03 — Conference Registration Closed (Extension)

**Purpose:**  
Verify that the system blocks registration attempts when registration is closed.

**Preconditions:**
- CMS is running and accessible.
- Conference registration is closed.
- Attendee is logged in.

**Test Steps:**
1. Log in to the CMS as an attendee.
2. Navigate to the **Conference Registration** section.
3. Attempt to register for the conference.

**Expected Results:**
- The system detects that registration is closed.
- The system displays a clear message indicating registration is not currently available.
- The attendee cannot proceed with registration.
- No registration record is created.

---

#### AT-UC24-04 — Invalid or Unavailable Attendance Type (Extension)

**Purpose:**  
Verify that the system rejects an invalid/unavailable attendance type selection and allows the attendee to choose a valid option.

**Preconditions:**
- CMS is running and accessible.
- Conference registration is open.
- Attendee is logged in.
- At least one attendance type is invalid/unavailable (e.g., removed, disabled, sold out) OR an invalid type can be simulated (e.g., stale form submission).

**Test Steps:**
1. Log in to the CMS as an attendee.
2. Navigate to **Conference Registration** and begin the registration flow.
3. Select an invalid/unavailable attendance type (or simulate submitting an invalid type).
4. Attempt to confirm registration.
5. Select a valid available attendance type.
6. Confirm registration again.

**Expected Results:**
- The system rejects the invalid/unavailable attendance type.
- The system displays a clear error message explaining the issue.
- The system does not record the registration with the invalid type.
- After selecting a valid type, the registration completes successfully and confirmation is shown.

---

#### AT-UC24-05 — Payment Service Unavailable (Extension, If Applicable)

**Purpose:**  
Verify system behavior when registration succeeds but the payment service is unavailable (if payment is required).

**Preconditions:**
- CMS is running and accessible.
- Conference registration is open.
- Attendee is logged in.
- Payment is required for registration (if applicable).
- Payment service is unavailable (simulated).

**Test Steps:**
1. Log in as an attendee.
2. Complete the registration flow using a valid attendance type.
3. Proceed to the payment step while the payment service failure condition exists.
4. Observe the system response.

**Expected Results:**
- The system records the registration request (or places it in a pending/unpaid state, depending on implementation).
- The system displays an error message indicating payment cannot be completed at this time.
- The system provides a safe recovery path (retry payment later or alternative instructions), if implemented.
- The system does not mark payment as completed.

---

#### AT-UC24-06 — System Fails to Record Registration (Failure End Scenario)

**Purpose:**  
Verify system behavior when a backend/database error prevents saving the attendee registration.

**Preconditions:**
- CMS is running and accessible (UI reachable).
- Conference registration is open.
- Attendee is logged in.
- A backend/database failure can be simulated during registration storage.

**Test Steps:**
1. Log in to the CMS as an attendee.
2. Navigate to **Conference Registration** and start registration.
3. Select a valid attendance type (if applicable).
4. Confirm registration while the storage failure condition exists.
5. Observe the system response.
6. Refresh and check registration status (e.g., attendee profile/registration page).

**Expected Results:**
- The system displays an error message indicating registration could not be saved.
- The system does not display a success confirmation.
- No registration record is created (or the system rolls back to a consistent unregistered state).
- The use case ends in failure for this attempt.

---

### Completion Criteria

UC-24 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-25: Make Conference Registration Payment

---

### Use Case Under Test

**Use Case ID:** UC-25  
**Use Case Name:** Make Conference Registration Payment  
**Primary Actor:** Attendee (Registered User)  
**Secondary Actor(s):** Payment Service / Payment Gateway  
**Goal:** Allow an attendee to pay the conference registration fee so their registration is confirmed as paid.

---

### Acceptance Criteria

The system satisfies UC-25 if:

- A logged-in attendee with a pending/unpaid conference registration can access the payment workflow.
- The system displays the correct payable amount and payment details before payment submission.
- The attendee can successfully submit payment through the payment gateway.
- On successful payment, the system records the payment and updates the attendee’s registration status to **Paid/Confirmed**.
- The attendee receives a confirmation message (and receipt/confirmation email if implemented).
- The system handles payment failures (declined, canceled, timeout) with clear feedback and allows retry.
- The system prevents duplicate charges (or clearly handles multiple payment attempts safely).
- The system handles payment gateway unavailability and internal storage errors gracefully.
- All main, alternate, and failure flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- Attendee accesses the system using a modern web browser.
- Attendee is registered and logged in unless otherwise specified.
- Attendee has an existing conference registration in **Unpaid/Pending Payment** state.
- The CMS integrates with an external payment gateway/service.
- Payment confirmation updates are stored in a database and visible in the attendee’s registration status view.
- Payment gateway test modes (success/fail/cancel/timeout) can be simulated.

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC25-01  | Main Success Scenario – Successful Payment |
| AT-UC25-02  | Extension – Attendee Not Logged In |
| AT-UC25-03  | Extension – No Pending Registration / Nothing to Pay |
| AT-UC25-04  | Extension – Payment Declined by Gateway |
| AT-UC25-05  | Extension – Payment Canceled by Attendee |
| AT-UC25-06  | Extension – Payment Gateway Timeout / Unavailable |
| AT-UC25-07  | Extension – Duplicate Payment Attempt / Already Paid |
| AT-UC25-08  | Failure End Scenario – System Fails to Record Successful Payment |

---

### Acceptance Test Cases

---

#### AT-UC25-01 — Pay Registration Successfully (Main Success Scenario)

**Purpose:**  
Verify that an attendee can successfully pay for registration and the system records payment and updates status to paid/confirmed.

**Preconditions:**
- CMS is running and accessible.
- Attendee is logged in.
- Attendee has a registration in **Pending/Unpaid** state.
- Payment gateway is available and configured for successful payments.

**Test Steps:**
1. Log in to the CMS as an attendee.
2. Navigate to **My Registration** or **Payment** section.
3. Select **Pay Registration Fee** (or equivalent).
4. Verify the displayed payment amount and registration details.
5. Proceed to the payment gateway and submit valid payment information.
6. Complete the payment and return to the CMS confirmation page.
7. Navigate to the attendee’s registration status page.

**Expected Results:**
- The system displays correct amount and payment details before submission.
- The payment gateway processes the payment successfully.
- The CMS receives confirmation and records the payment.
- The registration status updates to **Paid/Confirmed**.
- The attendee sees a payment success confirmation (and receipt if implemented).

---

#### AT-UC25-02 — Attendee Not Logged In (Extension)

**Purpose:**  
Verify that unauthenticated users are redirected to login before accessing payment.

**Preconditions:**
- CMS is running and accessible.
- Attendee is not logged in.
- Attendee has an unpaid registration.

**Test Steps:**
1. Attempt to access the payment page directly (via URL) without logging in.
2. Observe system behavior.
3. Log in with valid attendee credentials.
4. Navigate to the payment workflow and attempt payment.

**Expected Results:**
- The system redirects to login when not authenticated.
- The user cannot access payment workflow without logging in.
- After login, the attendee can proceed to payment normally.

---

#### AT-UC25-03 — No Pending Registration / Nothing to Pay (Extension)

**Purpose:**  
Verify system behavior when the attendee has no pending/unpaid registration.

**Preconditions:**
- CMS is running and accessible.
- Attendee is logged in.
- Attendee has no registration OR registration is already paid/confirmed.

**Test Steps:**
1. Log in to the CMS as the attendee.
2. Navigate to **My Registration** / **Payment** section.
3. Attempt to initiate payment.

**Expected Results:**
- The system indicates there is no pending payment required.
- The system blocks payment initiation (no payment gateway redirect).
- No payment record is created.

---

#### AT-UC25-04 — Payment Declined by Gateway (Extension)

**Purpose:**  
Verify that the system handles a payment decline and allows the attendee to retry.

**Preconditions:**
- CMS is running and accessible.
- Attendee is logged in.
- Attendee has an unpaid registration.
- Payment gateway can simulate a declined payment.

**Test Steps:**
1. Navigate to the payment workflow.
2. Submit payment via the gateway using a test method that results in a decline.
3. Return to the CMS (or observe failure callback/redirect).
4. Check registration payment status.
5. Retry payment using a method that succeeds (optional).

**Expected Results:**
- The system reports that payment was declined.
- No payment is recorded as successful.
- Registration remains **Unpaid/Pending**.
- The attendee can retry payment.

---

#### AT-UC25-05 — Payment Canceled by Attendee (Extension)

**Purpose:**  
Verify that the system handles user-initiated payment cancellation without charging and keeps registration unpaid.

**Preconditions:**
- CMS is running and accessible.
- Attendee is logged in.
- Attendee has an unpaid registration.
- Payment gateway supports a cancel flow.

**Test Steps:**
1. Navigate to the payment workflow.
2. Proceed to the payment gateway.
3. Cancel the payment process (use gateway cancel option).
4. Return to the CMS (cancel callback/redirect).
5. Check registration status.

**Expected Results:**
- The system indicates the payment was canceled.
- No successful payment is recorded.
- Registration remains **Unpaid/Pending**.
- The attendee can restart payment later.

---

#### AT-UC25-06 — Payment Gateway Timeout / Unavailable (Extension)

**Purpose:**  
Verify system behavior when the payment gateway is unavailable or times out.

**Preconditions:**
- CMS is running and accessible.
- Attendee is logged in.
- Attendee has an unpaid registration.
- Payment gateway is unavailable or configured to timeout.

**Test Steps:**
1. Navigate to the payment workflow.
2. Attempt to proceed to payment while gateway is unavailable/timeout occurs.
3. Observe system response.
4. Check registration status.

**Expected Results:**
- The system displays a clear error message indicating payment service is unavailable or timed out.
- No successful payment is recorded.
- Registration remains **Unpaid/Pending**.
- The attendee can retry later without duplicate charge risk.

---

#### AT-UC25-07 — Duplicate Payment Attempt / Already Paid (Extension)

**Purpose:**  
Verify that the system prevents duplicate charges and handles repeated payment attempts safely.

**Preconditions:**
- CMS is running and accessible.
- Attendee is logged in.
- Attendee’s registration is already marked **Paid/Confirmed** OR a successful payment has just been completed.

**Test Steps:**
1. Log in to the CMS as the attendee.
2. Attempt to initiate payment again (e.g., revisit payment page, click pay again, refresh callbacks).
3. Observe system behavior.

**Expected Results:**
- The system prevents a second payment attempt OR clearly indicates payment is already completed.
- The system does not create a duplicate successful payment record.
- Registration remains **Paid/Confirmed**.

---

#### AT-UC25-08 — System Fails to Record Successful Payment (Failure End Scenario)

**Purpose:**  
Verify system behavior when the payment gateway reports success but the CMS fails to record the payment due to a system/database error.

**Preconditions:**
- CMS is running and accessible (UI reachable).
- Attendee is logged in.
- Attendee has an unpaid registration.
- Payment gateway is available and can return success.
- A backend/database failure can be simulated during payment recording/status update.

**Test Steps:**
1. Navigate to the payment workflow.
2. Complete a successful payment through the payment gateway.
3. Trigger the storage failure condition during the CMS payment recording step.
4. Observe the system response upon return to CMS.
5. Refresh and check registration status and payment history (if available).

**Expected Results:**
- The system displays an error message indicating payment could not be fully recorded/confirmed.
- The system does not falsely mark the registration as **Paid/Confirmed** if it cannot verify persistence.
- The system provides guidance for resolution (e.g., contact support or retry verification) if implemented.
- No duplicate charge is initiated by the CMS as part of error handling.
- The use case ends in failure for recording/confirmation in the CMS (even if the gateway succeeded).

---

### Completion Criteria

UC-25 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.

# Acceptance Test Suites

## Acceptance Test Suite — UC-26: View Registration Confirmation / Receipt

---

### Use Case Under Test

**Use Case ID:** UC-26  
**Use Case Name:** View Registration Confirmation / Receipt  
**Primary Actor:** Attendee (Registered User)  
**Goal:** Allow an attendee to view confirmation that their conference registration is complete (and view/download a receipt if applicable).

---

### Acceptance Criteria

The system satisfies UC-26 if:

- A logged-in attendee with a completed (paid/confirmed) registration can view their registration confirmation.
- The system displays correct registration details (e.g., attendee name, attendance type, conference name, status).
- The system displays payment confirmation details (e.g., amount, date/time, transaction/reference ID) if payment is part of the registration.
- The attendee can view and/or download a receipt (if the system supports receipt generation/download).
- The system prevents access to confirmation/receipt for users who are not logged in or who do not own the registration.
- The system provides clear feedback if the attendee has not completed payment/registration.
- The system handles retrieval/generation failures gracefully with clear error feedback.
- All main, alternate, and failure flows defined in the use case are covered by acceptance tests.

---

### Test Environment & Assumptions

- System under test is a web-based Conference Management System (CMS).
- Attendee accesses the system using a modern web browser.
- Attendee is registered and logged in unless otherwise specified.
- Attendee has one of the following states depending on test case:
  - **Paid/Confirmed** registration
  - **Unpaid/Pending** registration
  - No registration record
- Receipt generation may be implemented as:
  - an on-screen receipt page,
  - a downloadable PDF, and/or
  - an email receipt.
- Database/server failures can be simulated for negative tests.

---

### Flow Coverage Matrix

| Test Case ID | Flow Covered |
|-------------|-------------|
| AT-UC26-01  | Main Success Scenario – View Confirmation (Paid/Confirmed) |
| AT-UC26-02  | Main Success Scenario Variant – Download/View Receipt (If Supported) |
| AT-UC26-03  | Extension – Attendee Not Logged In |
| AT-UC26-04  | Extension – Registration Not Paid / Not Confirmed |
| AT-UC26-05  | Extension – Access Another User’s Receipt (Authorization Blocked) |
| AT-UC26-06  | Failure End Scenario – System Error Retrieving or Generating Receipt |

---

### Acceptance Test Cases

---

#### AT-UC26-01 — View Registration Confirmation Successfully (Main Success Scenario)

**Purpose:**  
Verify that an attendee with a paid/confirmed registration can view confirmation details in the CMS.

**Preconditions:**
- CMS is running and accessible.
- Attendee is logged in.
- Attendee has a registration in **Paid/Confirmed** state.
- Payment record exists if payment is required.

**Test Steps:**
1. Log in to the CMS as the attendee.
2. Navigate to **My Registration** / **Registration Status** (or equivalent).
3. Select **View Confirmation** (or equivalent).
4. Observe the confirmation page details.
5. Refresh the page (optional) to confirm consistent retrieval.

**Expected Results:**
- The system displays registration status as **Paid/Confirmed**.
- The system shows correct registration details (attendee identity, attendance type, conference name).
- The system shows payment confirmation details (amount, date/time, transaction/reference ID) if applicable.
- No errors are displayed.

---

#### AT-UC26-02 — Download or View Receipt (Main Success Scenario Variant, If Supported)

**Purpose:**  
Verify that the attendee can view and/or download a receipt for a paid registration (if receipt functionality exists).

**Preconditions:**
- CMS is running and accessible.
- Attendee is logged in.
- Attendee has a registration in **Paid/Confirmed** state.
- Receipt generation/download feature is enabled.

**Test Steps:**
1. Log in as the attendee.
2. Navigate to the registration confirmation page.
3. Select **View Receipt** and/or **Download Receipt** (or equivalent).
4. If a download occurs, open the downloaded file.
5. Verify receipt contents.

**Expected Results:**
- The receipt is generated and displayed/downloaded successfully.
- The receipt includes accurate payment and registration details (amount paid, attendee name, conference info, transaction/reference ID).
- The receipt corresponds to the attendee’s registration (no other user’s data is included).
- No errors are displayed.

---

#### AT-UC26-03 — Attendee Not Logged In (Extension)

**Purpose:**  
Verify that unauthenticated users cannot view confirmation/receipt and are redirected to login.

**Preconditions:**
- CMS is running and accessible.
- Attendee is not logged in.
- Attendee has a paid registration.

**Test Steps:**
1. Attempt to access the confirmation/receipt page directly (via URL) without logging in.
2. Observe system behavior.
3. Log in with valid attendee credentials.
4. Navigate to **My Registration** and view confirmation.

**Expected Results:**
- The system redirects to login when not authenticated.
- Confirmation/receipt content is not shown before login.
- After login, the attendee can view their confirmation/receipt normally.

---

#### AT-UC26-04 — Registration Not Paid / Not Confirmed (Extension)

**Purpose:**  
Verify that the system provides clear feedback when the attendee tries to view confirmation/receipt without having completed registration/payment.

**Preconditions:**
- CMS is running and accessible.
- Attendee is logged in.
- Attendee has either:
  - an **Unpaid/Pending** registration, or
  - no completed registration.

**Test Steps:**
1. Log in as the attendee.
2. Navigate to **My Registration** / **Registration Status**.
3. Attempt to select **View Confirmation** or **View/Download Receipt**.

**Expected Results:**
- The system indicates the registration is not confirmed/paid (or that no completed registration exists).
- The system blocks receipt generation/download for unpaid/unconfirmed registration.
- The system provides a path to complete registration/payment (e.g., link to payment), if applicable.

---

#### AT-UC26-05 — Attempt to Access Another User’s Receipt (Authorization Blocked) (Extension)

**Purpose:**  
Verify that attendees cannot access other users’ registration confirmations/receipts.

**Preconditions:**
- CMS is running and accessible.
- Attendee A is logged in.
- Attendee B exists with a paid/confirmed registration.
- A receipt/confirmation URL or identifier for Attendee B can be simulated/guessed (e.g., by changing an ID in the URL).

**Test Steps:**
1. Log in as Attendee A.
2. Attempt to access Attendee B’s confirmation/receipt by URL manipulation or selecting a non-owned registration reference (if possible).
3. Observe the system response.

**Expected Results:**
- The system denies access to the other user’s confirmation/receipt.
- The system displays an authorization error or redirects to a safe page.
- No private data from Attendee B is displayed.

---

#### AT-UC26-06 — System Error Retrieving or Generating Confirmation/Receipt (Failure End Scenario)

**Purpose:**  
Verify system behavior when a backend/database error prevents retrieving confirmation data or generating a receipt.

**Preconditions:**
- CMS is running and accessible (UI reachable).
- Attendee is logged in.
- Attendee has a paid/confirmed registration.
- A backend/database/service failure can be simulated during confirmation retrieval or receipt generation.

**Test Steps:**
1. Log in as the attendee.
2. Navigate to the registration confirmation page.
3. Attempt to view confirmation and/or generate/download the receipt while the failure condition exists.
4. Observe the system response.
5. Retry after removing the failure condition (optional).

**Expected Results:**
- The system displays a clear error message indicating confirmation/receipt cannot be retrieved/generated.
- The system does not display incorrect or partial information as if complete.
- The attendee remains authenticated and can navigate away safely.
- If the attendee abandons the attempt, the use case ends in failure for retrieval/generation.

---

### Completion Criteria

UC-26 is considered accepted when all test cases pass and all defined flows (main, alternate, and failure) are successfully validated.





























