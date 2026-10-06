from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    department: Optional[str] = None
    manager_id: Optional[int] = None
    is_active: bool

    class Config:
        from_attributes = True

class UserStatusUpdate(BaseModel):
    is_active: bool
