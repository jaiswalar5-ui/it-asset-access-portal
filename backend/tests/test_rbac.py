import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid
import jwt
from datetime import datetime, timedelta

from app.main import app
from app.db.database import get_db, Base
from app.models.models import User, AuditLog
from app.core.config import get_settings

from sqlalchemy.pool import StaticPool

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
settings = get_settings()

def create_token(user_id: int):
    payload = {"sub": str(user_id), "exp": datetime.utcnow() + timedelta(minutes=15)}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    uid = str(uuid.uuid4())[:8]
    admin = User(name="Admin", email=f"admin_{uid}@test.com", role="IT_ADMIN", is_active=True)
    manager = User(name="Manager", email=f"manager_{uid}@test.com", role="MANAGER", is_active=True)
    employee = User(name="Employee", email=f"employee_{uid}@test.com", role="EMPLOYEE", is_active=True)
    employee2 = User(name="Employee2", email=f"employee2_{uid}@test.com", role="EMPLOYEE", is_active=True)
    
    db.add_all([admin, manager, employee, employee2])
    db.commit()
    
    employee.manager_id = manager.id
    db.commit()
    
    yield {
        "admin": admin,
        "manager": manager,
        "employee": employee,
        "employee2": employee2,
    }
    
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_unauthenticated_request():
    resp = client.get("/users")
    assert resp.status_code == 401

def test_employee_cannot_access_get_users(setup_database):
    emp = setup_database["employee"]
    token = create_token(emp.id)
    resp = client.get("/users", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403

def test_manager_cannot_access_get_users(setup_database):
    mgr = setup_database["manager"]
    token = create_token(mgr.id)
    resp = client.get("/users", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403

def test_admin_can_access_get_users(setup_database):
    admin = setup_database["admin"]
    token = create_token(admin.id)
    resp = client.get("/users", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert len(resp.json()) == 4

def test_employee_can_view_own_profile(setup_database):
    emp = setup_database["employee"]
    token = create_token(emp.id)
    resp = client.get(f"/users/{emp.id}", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["id"] == emp.id
    assert "password_hash" not in resp.json()

def test_employee_cannot_view_another_employee(setup_database):
    emp = setup_database["employee"]
    emp2 = setup_database["employee2"]
    token = create_token(emp.id)
    resp = client.get(f"/users/{emp2.id}", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403

def test_manager_can_view_assigned_employee(setup_database):
    mgr = setup_database["manager"]
    emp = setup_database["employee"]
    token = create_token(mgr.id)
    resp = client.get(f"/users/{emp.id}", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200

def test_manager_cannot_view_unassigned_employee(setup_database):
    mgr = setup_database["manager"]
    emp2 = setup_database["employee2"]
    token = create_token(mgr.id)
    resp = client.get(f"/users/{emp2.id}", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403

def test_employee_cannot_patch_user_status(setup_database):
    emp = setup_database["employee"]
    token = create_token(emp.id)
    resp = client.patch(f"/users/{emp.id}/status", json={"is_active": False}, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403

def test_manager_cannot_patch_user_status(setup_database):
    mgr = setup_database["manager"]
    emp = setup_database["employee"]
    token = create_token(mgr.id)
    resp = client.patch(f"/users/{emp.id}/status", json={"is_active": False}, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403

def test_admin_can_deactivate_user(setup_database):
    admin = setup_database["admin"]
    emp = setup_database["employee"]
    token = create_token(admin.id)
    resp = client.patch(f"/users/{emp.id}/status", json={"is_active": False}, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["is_active"] is False

def test_self_deactivation_is_prevented(setup_database):
    admin = setup_database["admin"]
    token = create_token(admin.id)
    resp = client.patch(f"/users/{admin.id}/status", json={"is_active": False}, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 400

def test_user_status_change_writes_audit_log(setup_database):
    admin = setup_database["admin"]
    emp2 = setup_database["employee2"]
    token = create_token(admin.id)
    
    # Deactivate employee2
    client.patch(f"/users/{emp2.id}/status", json={"is_active": False}, headers={"Authorization": f"Bearer {token}"})
    
    db = TestingSessionLocal()
    audit_deact = db.query(AuditLog).filter(AuditLog.entity_id == emp2.id, AuditLog.action == "DEACTIVATE_USER").first()
    db.close()
    
    assert audit_deact is not None
    assert audit_deact.user_id == admin.id

def test_admin_can_activate_user(setup_database):
    admin = setup_database["admin"]
    emp2 = setup_database["employee2"]
    token = create_token(admin.id)
    
    # First ensure it's deactivated (from previous test or manually)
    client.patch(f"/users/{emp2.id}/status", json={"is_active": False}, headers={"Authorization": f"Bearer {token}"})
    
    # Activate employee2
    resp = client.patch(f"/users/{emp2.id}/status", json={"is_active": True}, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["is_active"] is True
    
    db = TestingSessionLocal()
    audit_act = db.query(AuditLog).filter(AuditLog.entity_id == emp2.id, AuditLog.action == "ACTIVATE_USER").order_by(AuditLog.id.desc()).first()
    db.close()
    
    assert audit_act is not None
    assert audit_act.user_id == admin.id
