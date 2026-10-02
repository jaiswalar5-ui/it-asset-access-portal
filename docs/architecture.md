# Architecture

## Overview
This is a simple 2-tier monolithic architecture designed to be clean, readable, and secure without over-engineering.

```
[ React Frontend ]  <--- HTTP/REST (JSON, JWT) --->  [ FastAPI Backend ]  <--- SQLAlchemy --->  [ SQLite DB ]
```

## Layers

### Frontend (React)
- **Vite** for fast bundling.
- **React Router** for client-side routing.
- Context API for state management (auth state).
- Simple CSS modules or plain CSS for styling.
- API utility layer to handle HTTP requests and attach JWT tokens.

### Backend (FastAPI)
- **API Routers**: Handle HTTP requests, input validation (Pydantic), and formatting responses.
- **Services/Core**: Contain business logic, authorization checks, and workflow state transitions.
- **Database/Models**: SQLAlchemy ORM models mapping to SQLite tables.
- **Security**: JWT for stateless authentication, Argon2 for password hashing, and explicit server-side checks for IDOR/RBAC.

## Backend Modules
- `auth`: Login, token generation, and password hashing.
- `users`: User management and profiling.
- `assets`: Asset catalog and status management.
- `asset_requests`: Lifecycle of asset requests.
- `access_requests`: Lifecycle of access requests.
- `approvals`: Manager and IT admin approval logic.
- `audit_logs`: Centralized logging for sensitive actions.

## Constraints
- **No Microservices**: The entire backend runs as a single FastAPI process.
- **No Orchestration**: No Docker, Kubernetes, etc.
- **No Message Queues**: All state transitions happen synchronously in the HTTP request cycle.
