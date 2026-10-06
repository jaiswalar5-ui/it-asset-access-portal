from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.db.database import get_db
from app.models.models import User

settings = get_settings()
security = HTTPBearer(auto_error=False)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise credentials_exception
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

def require_role(roles: list[str]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail="Not enough privileges")
        return current_user
    return role_checker

def require_employee(current_user: User = Depends(get_current_user)):
    if current_user.role not in ["EMPLOYEE", "MANAGER", "IT_ADMIN"]:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return current_user

def require_manager(current_user: User = Depends(get_current_user)):
    if current_user.role not in ["MANAGER", "IT_ADMIN"]:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return current_user

def require_it_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "IT_ADMIN":
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return current_user
