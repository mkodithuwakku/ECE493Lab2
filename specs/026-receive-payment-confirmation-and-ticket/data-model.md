# Data Model: Receive Payment Confirmation and Ticket

## Entities

### PaymentConfirmation
- **Description**: Record of successful payment confirmation details.
- **Key Fields**:
  - `id`
  - `registration_id`
  - `amount`
  - `currency` (optional if single currency)
  - `transaction_reference_id`
  - `confirmed_at` (timestamp)

### ConferenceTicket
- **Description**: Unique ticket associated with a paid/confirmed registration.
- **Key Fields**:
  - `id`
  - `registration_id`
  - `ticket_code` (unique)
  - `issued_at` (timestamp)

### Receipt
- **Description**: Optional receipt document for a paid/confirmed registration.
- **Key Fields**:
  - `id`
  - `registration_id`
  - `receipt_number`
  - `generated_at` (timestamp)

## Validation Rules

- Confirmation and ticket are accessible only when registration is paid/confirmed.
- Receipt access is available only when receipt functionality is enabled.
- Ticket access is limited to the owning attendee.

## State Transitions

- None beyond visibility constraints; this use case is read/retrieve focused.
