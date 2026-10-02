# Functional Requirements

## Roles and Capabilities

### Employee
- View own profile and assigned assets/access.
- Create asset requests for allowed asset types.
- Create access requests for allowed applications.
- Cancel own pending requests.
- View history of own requests.
- Cannot approve or fulfill their own requests.
- Cannot grant access to themselves.

### Manager
- All Employee capabilities.
- View pending requests from their assigned employees.
- Approve or reject asset/access requests from their assigned employees.

### IT Admin
- All Employee capabilities.
- View all requests pending IT fulfillment/approval.
- Fulfill or reject IT asset requests.
- Grant or reject application access requests.
- Revoke existing application access.
- Change user statuses (e.g., mark as inactive).
- View full system audit logs.

## Workflows

### Asset Request Workflow
1. **PENDING_MANAGER_APPROVAL**: Employee submits a request.
2. **PENDING_IT_FULFILLMENT** or **REJECTED**: Manager reviews the request.
3. **FULFILLED** or **REJECTED**: IT Admin processes the approved request.
*Requester can transition request to **CANCELLED** if it is in PENDING_MANAGER_APPROVAL state.*

### Access Request Workflow
1. **PENDING_MANAGER_APPROVAL**: Employee submits an access request.
2. **PENDING_IT_APPROVAL** or **REJECTED**: Manager reviews the request.
3. **ACCESS_GRANTED** or **REJECTED**: IT Admin processes the approved request.
4. **REVOKED**: IT Admin revokes previously granted access.
*Requester can transition request to **CANCELLED** if it is in PENDING_MANAGER_APPROVAL state.*
