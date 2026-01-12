from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.employee import EmployeeResponse

class AccessLogBase(BaseModel):
    access_granted: bool
    confidence_score: Optional[float] = None
    liveness_passed: Optional[bool] = None
    device_id: Optional[str] = None
    device_location: Optional[str] = None
    denial_reason: Optional[str] = None

class AccessLog(AccessLogBase):
    id: int
    employee_id: Optional[int] = None
    attempted_at: datetime
    
    class Config:
        from_attributes = True

class AccessLogResponse(AccessLog):
    employee: Optional[EmployeeResponse] = None

