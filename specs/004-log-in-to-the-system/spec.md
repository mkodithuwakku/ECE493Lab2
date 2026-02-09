# Feature Specification: UC-04 Log In to the System

**Feature Branch**: `004-log-in-to-the-system`  
**Created**: February 8, 2026  
**Status**: Draft  
**Input**: User description: "Generate the specification for UC-04 only. Use UC-04 from `GeneratedUseCases.md` and ONLY acceptance tests `AT-UC04-*` from `GeneratedTestSuites.md`. Ignore all other use cases and tests. Do not invent requirements or flows; derive functional requirements directly from UC-04 main and extension flows and ensure each requirement is verifiable by the provided acceptance tests. Fill the “Use Case Scope” section with UC-04 and list the AT-UC04 tests used."

## Clarifications

### Session 2026-02-08

- Q: What identifier does the login accept? → A: Username or email.
- Q: Are username and email comparisons case-sensitive? → A: Both username and email are case-insensitive.
- Q: What is the lockout threshold for failed logins? → A: Lock after 5 failed attempts within 15 minutes.
- Q: What error details are shown for incorrect credentials? → A: “Invalid credentials” plus remaining attempts count.
- Q: How long does a lockout last? → A: Auto-unlock after 15 minutes.

## Use Case Scope *(mandatory)*

- **Use Case**: UC-04 - Log In to the System
- **Acceptance Tests**: AT-UC04-01, AT-UC04-02, AT-UC04-03, AT-UC04-04, AT-UC04-05, AT-UC04-06

## User Scenarios & Testing *(mandatory)*

Assumptions used for testing and scope: the CMS is a web-based system reachable via a modern browser; the login page is accessible; a registered user account exists; accounts may be active, locked, or disabled; login accepts a username or email plus password; and authentication depends on an authentication service and supporting database availability as noted in UC-04 and AT-UC04 tests.

### User Story 1 - Log In Successfully (Priority: P1)

A registered user logs in with valid credentials and gains access to their personalized homepage.

**Why this priority**: This is the primary goal of UC-04 and enables access to authorized functionality.

**Independent Test**: Can be fully tested by completing AT-UC04-01 and verifying successful authentication and redirect.

**Acceptance Scenarios**:

1. **Given** the CMS is accessible and the account is active, **When** the user submits valid credentials, **Then** the system authenticates the user and redirects them to their personalized homepage.
2. **Given** the CMS is accessible, **When** the user logs in successfully, **Then** no authentication error message is displayed.

---

### User Story 2 - Handle Missing Login Information (Priority: P2)

A user submits the login form without a username or without a password and receives a clear request to complete required fields.

**Why this priority**: Prevents incomplete submissions from being treated as valid and guides the user to correct the issue.

**Independent Test**: Can be fully tested by completing AT-UC04-02 and verifying the required-field feedback.

**Acceptance Scenarios**:

1. **Given** the login page is reachable, **When** the user submits the form with a missing username or password, **Then** the system displays a required-fields message and does not authenticate the user.

---

### User Story 3 - Handle Incorrect Credentials (Priority: P2)

A user submits an incorrect username or password and is informed that authentication failed.

**Why this priority**: Protects account access and provides feedback for incorrect credentials.

**Independent Test**: Can be fully tested by completing AT-UC04-03 and verifying the authentication failure message and denial of access.

**Acceptance Scenarios**:

1. **Given** a registered user account exists, **When** the user submits an incorrect username or password, **Then** the system displays an authentication failure message and does not log the user in.

---

### User Story 4 - Block Locked or Disabled Accounts (Priority: P3)

A user with a locked or disabled account is prevented from logging in and receives an account status message.

**Why this priority**: Ensures inactive accounts do not gain access to authorized features.

**Independent Test**: Can be fully tested by completing AT-UC04-04 and verifying the account-inactive message and denial of access.

**Acceptance Scenarios**:

1. **Given** an account is locked or disabled, **When** the user submits valid credentials, **Then** the system blocks authentication and displays an account inactive message.

---

### User Story 5 - Handle Authentication Service Unavailability (Priority: P3)

A user attempting to log in during an authentication service or database outage receives a temporary system issue message and is not logged in.

**Why this priority**: Communicates system availability issues without granting access.

**Independent Test**: Can be fully tested by completing AT-UC04-05 and verifying the temporary system issue message and lack of login.

**Acceptance Scenarios**:

1. **Given** the authentication service or database is unavailable, **When** the user submits valid credentials, **Then** the system shows a temporary system issue message and does not authenticate the user.

---

### User Story 6 - Handle Critical Authentication Failure (Priority: P3)

A user attempting to log in during a critical authentication failure receives a message that authentication cannot be completed and no session is created.

**Why this priority**: Ensures users are not partially logged in during critical errors and clearly communicates failure.

**Independent Test**: Can be fully tested by completing AT-UC04-06 and verifying the failure message and lack of session/redirect.

**Acceptance Scenarios**:

1. **Given** a critical server or database error occurs during authentication, **When** the user submits valid credentials, **Then** the system reports authentication cannot be completed, does not create a session, and does not redirect to the personalized homepage.

---

### Edge Cases

- What happens when the username or password field is missing at submission time?
- How does the system handle authentication when the authentication service or database is unavailable?
- How does the system behave when a critical error interrupts authentication after credentials are submitted?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST authenticate a registered user when valid credentials are submitted. 
- **FR-002**: System MUST redirect an authenticated user to their personalized homepage after successful login.
- **FR-003**: System MUST detect missing username or password input, display a required-fields error message, and keep the user unauthenticated on the login page.
- **FR-004**: System MUST detect incorrect username or password input, display an authentication failure message including remaining attempts count, and deny login.
- **FR-004a**: System MUST lock an account after 5 failed login attempts within 15 minutes.
- **FR-004b**: System MUST auto-unlock a locked account after 15 minutes.
- **FR-005**: System MUST prevent login for locked or disabled accounts and display an account inactive message.
- **FR-006**: System MUST display a temporary system issue message and deny login when authentication services are unavailable.
- **FR-007**: System MUST display an authentication cannot be completed message, create no session, and deny login when a critical authentication error occurs.

### Key Entities *(include if feature involves data)*

- **User Account**: Registered user record, including account status (active, locked, disabled).
- **Credentials**: Username (or email) and password supplied for authentication; username and email are case-insensitive.
- **Authentication Result**: Outcome of credential validation (success, failure, service unavailable, critical error).
- **Session**: Represents an authenticated user session when login succeeds.

## Interfaces & Contracts *(mandatory)*

- **Login UI Flow**: Inputs username (or email) and password; outputs successful authentication with redirect to personalized homepage or one of the specified error messages for missing fields, invalid credentials, locked/disabled account, service unavailability, or critical authentication failure.

## Security & Privacy Considerations *(mandatory)*

- **AuthN/AuthZ**: Only registered users with valid credentials and active accounts may authenticate and access authorized features.
- **Sensitive Data**: Credentials are used for authentication; no access is granted when authentication fails or cannot be completed.
- **Auditability**: No audit or logging requirements are specified in UC-04.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of AT-UC04-01 executions authenticate the user and redirect to the personalized homepage.
- **SC-002**: 100% of AT-UC04-02 executions display a required-fields message and do not authenticate the user.
- **SC-003**: 100% of AT-UC04-03 executions display an authentication failure message and do not authenticate the user.
- **SC-004**: 100% of AT-UC04-04 executions block login for locked/disabled accounts with an account inactive message.
- **SC-005**: 100% of AT-UC04-05 and AT-UC04-06 executions display the specified failure message and do not authenticate the user or create a session.
