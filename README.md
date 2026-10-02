# Enterprise IT Asset & Access Management Portal

## Project Overview
A complete, monolithic web application simulating an internal company system for IT asset and access management. Employees can request assets and access, managers can approve or reject these requests, and IT admins can fulfill requests, manage access, and audit activities.

## Problem Statement
Organizations need a centralized way to track who has what hardware and what software access, ensuring proper approval chains and maintaining an audit trail for compliance and security.

## Target Users
- **Employees**: Request hardware (laptops, monitors, etc.) and software access.
- **Managers**: Review and approve/reject requests from their direct reports.
- **IT Admins**: Fulfill approved requests, manage users, and review the system's audit logs.

## Roles
- `EMPLOYEE`
- `MANAGER`
- `IT_ADMIN`

## Tech Stack
- **Backend**: Python, FastAPI, SQLAlchemy, SQLite, PyJWT, argon2-cffi.
- **Frontend**: React, JavaScript, Vite, React Router.

## How to Run

### Backend
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Note
This is a learning/portfolio project built with secure engineering practices, not a production-grade enterprise system. It uses a local SQLite database and omits complex enterprise integrations like SSO, email servers, or orchestration (Docker/Kubernetes).
