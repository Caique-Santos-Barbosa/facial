"""
Schemas para colaboradores
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class EmployeeBase(BaseModel):
    full_name: str
    cpf: str
    email: EmailStr
    phone: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    is_active: Optional[bool] = None

class EmployeeResponse(EmployeeBase):
    id: int
    is_active: bool
    face_image_path: str
    face_registered_at: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class EmployeeListResponse(BaseModel):
    id: int
    full_name: str
    cpf: str
    email: str
    department: Optional[str]
    position: Optional[str]
    is_active: bool
    face_registered_at: datetime
    
    class Config:
        from_attributes = True
