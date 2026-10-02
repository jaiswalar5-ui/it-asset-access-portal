# API Plan

## Auth
- `POST /api/auth/login` - Authenticate and return JWT (rate-limited).

## Users
- `GET /api/users/me` - Get current user profile.
- `GET /api/users` - List users (IT_ADMIN only).
- `PATCH /api/users/{user_id}/status` - Activate/deactivate user (IT_ADMIN only).

## Assets
- `GET /api/assets` - List all company assets (IT_ADMIN only).
- `GET /api/assets/my` - List assets currently assigned to the user.

## Asset Requests
- `GET /api/asset-requests` - List requests based on role (Employee: own, Manager: team's, IT_ADMIN: all).
- `POST /api/asset-requests` - Create a new asset request.
- `GET /api/asset-requests/{request_id}` - Get specific request details.
- `POST /api/asset-requests/{request_id}/cancel` - Cancel a pending request (Employee only).
- `POST /api/asset-requests/{request_id}/approve` - Approve request (Manager only).
- `POST /api/asset-requests/{request_id}/reject` - Reject request (Manager or IT_ADMIN).
- `POST /api/asset-requests/{request_id}/fulfill` - Fulfill request (IT_ADMIN only).

## Access Requests
- `GET /api/access-requests` - List requests based on role.
- `POST /api/access-requests` - Create a new access request.
- `GET /api/access-requests/{request_id}` - Get specific request details.
- `POST /api/access-requests/{request_id}/cancel` - Cancel a pending request (Employee only).
- `POST /api/access-requests/{request_id}/approve` - Approve request (Manager only).
- `POST /api/access-requests/{request_id}/reject` - Reject request (Manager or IT_ADMIN).
- `POST /api/access-requests/{request_id}/grant` - Grant access (IT_ADMIN only).
- `POST /api/access-requests/{request_id}/revoke` - Revoke access (IT_ADMIN only).

## Audit Logs
- `GET /api/audit-logs` - View system audit logs (IT_ADMIN only).
