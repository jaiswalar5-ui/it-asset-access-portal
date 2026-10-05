# Database Design

The application uses a relational SQLite database.

## Tables

### `users`
- `id` (PK)
- `email` (Unique)
- `hashed_password`
- `full_name`
- `role` (Enum: EMPLOYEE, MANAGER, IT_ADMIN)
- `manager_id` (FK to `users.id`, nullable)
- `is_active` (Boolean)

### `assets`
- `id` (PK)
- `asset_type` (Enum: Laptop, Desktop, Monitor, Keyboard, Mouse, Mobile Device)
- `status` (Enum: Available, Requested, Assigned, Maintenance, Retired)
- `serial_number` (Unique, string)
- `assigned_to` (FK to `users.id`, nullable)

### `asset_requests`
- `id` (PK)
- `requester_id` (FK to `users.id`)
- `asset_type` (String)
- `justification` (Text)
- `status` (Enum: PENDING_MANAGER_APPROVAL, PENDING_IT_FULFILLMENT, FULFILLED, REJECTED, CANCELLED)
- `manager_id` (FK to `users.id`, nullable) - who approved/rejected it
- `it_admin_id` (FK to `users.id`, nullable) - who fulfilled/rejected it
- `created_at`
- `updated_at`

### `access_requests`
- `id` (PK)
- `requester_id` (FK to `users.id`)
- `application_name` (String: GitHub, AWS, etc.)
- `access_type` (Enum: READ_ONLY, READ_WRITE, ADMIN)
- `justification` (Text)
- `status` (Enum: PENDING_MANAGER_APPROVAL, PENDING_IT_APPROVAL, ACCESS_GRANTED, REJECTED, REVOKED, CANCELLED)
- `manager_id` (FK to `users.id`, nullable)
- `it_admin_id` (FK to `users.id`, nullable)
- `created_at`
- `updated_at`

### `access_assignments`
- `id` (PK)
- `user_id` (FK to `users.id`)
- `application_name` (String)
- `access_type` (String)
- `granted_by` (FK to `users.id`)
- `granted_at`
- `revoked_at` (nullable)
- `status` (Enum: ACTIVE, REVOKED)

### `audit_logs`
- `id` (PK)
- `user_id` (FK to `users.id`, nullable)
- `action` (String - e.g., "LOGIN", "APPROVE_ASSET", "REVOKE_ACCESS")
- `resource_type` (String)
- `resource_id` (Integer, nullable)
- `details` (JSON/Text)
- `timestamp`

## Relationships
- Users can have a self-referencing relationship to a Manager (`manager_id`).
- Assets belong to Users when `assigned_to` is populated.
- Requests link to the Requester (User), and optionally track the Manager and IT Admin who acted upon them.
- Audit Logs track actions performed by Users on specific resources.
