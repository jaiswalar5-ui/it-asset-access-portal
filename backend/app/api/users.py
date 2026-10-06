from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import User
from app.schemas.schemas import UserResponse, UserStatusUpdate
from app.api.deps import get_current_user, require_it_admin
from app.services.audit import log_audit

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_it_admin),
    role: Optional[str] = None,
    department: Optional[str] = None,
    is_active: Optional[bool] = None
):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    if department:
        query = query.filter(User.department == department)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    return query.all()

@router.get("/{id}", response_model=UserResponse)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if current_user.role == "IT_ADMIN":
        return user
    
    if current_user.id == user.id:
        return user
        
    if current_user.role == "MANAGER" and user.manager_id == current_user.id:
        return user
        
    raise HTTPException(status_code=403, detail="Not enough privileges")

@router.patch("/{id}/status", response_model=UserResponse)
def update_user_status(
    id: int,
    status_update: UserStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_it_admin)
):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if not status_update.is_active and user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot deactivate yourself")
        
    user.is_active = status_update.is_active
    
    action = "DEACTIVATE_USER" if not status_update.is_active else "ACTIVATE_USER"
    log_audit(db, current_user.id, action, "User", user.id, f"User status changed to {status_update.is_active}", commit=False)
    
    db.commit()
    db.refresh(user)
    
    return user
