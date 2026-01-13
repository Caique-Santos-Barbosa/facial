"""
Endpoints para logs de acesso
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime, timedelta

from app.database import get_db
from app.models.employee import AccessLog, Employee
from app.models.user import User
from app.api.deps import get_current_user
from pydantic import BaseModel

router = APIRouter()

class AccessLogResponse(BaseModel):
    id: int
    employee_id: Optional[int]
    employee_name: Optional[str]
    access_granted: bool
    confidence_score: Optional[float]
    liveness_passed: Optional[bool]
    attempted_at: datetime
    device_id: Optional[str]
    denial_reason: Optional[str]
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[AccessLogResponse])
def list_access_logs(
    skip: int = 0,
    limit: int = 100,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    granted_only: Optional[bool] = None,
    employee_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista logs de acesso com filtros opcionais
    """
    query = db.query(
        AccessLog.id,
        AccessLog.employee_id,
        Employee.full_name.label("employee_name"),
        AccessLog.access_granted,
        AccessLog.confidence_score,
        AccessLog.liveness_passed,
        AccessLog.attempted_at,
        AccessLog.device_id,
        AccessLog.denial_reason
    ).outerjoin(Employee, AccessLog.employee_id == Employee.id)
    
    # Filtros
    if date_from:
        query = query.filter(AccessLog.attempted_at >= date_from)
    
    if date_to:
        query = query.filter(AccessLog.attempted_at <= date_to)
    
    if granted_only is not None:
        query = query.filter(AccessLog.access_granted == granted_only)
    
    if employee_id:
        query = query.filter(AccessLog.employee_id == employee_id)
    
    # Ordena por mais recente
    query = query.order_by(desc(AccessLog.attempted_at))
    
    logs = query.offset(skip).limit(limit).all()
    
    return [
        {
            "id": log.id,
            "employee_id": log.employee_id,
            "employee_name": log.employee_name or "Desconhecido",
            "access_granted": log.access_granted,
            "confidence_score": log.confidence_score,
            "liveness_passed": log.liveness_passed,
            "attempted_at": log.attempted_at,
            "device_id": log.device_id,
            "denial_reason": log.denial_reason
        }
        for log in logs
    ]

@router.get("/stats")
def get_access_stats(
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna estatísticas de acesso
    """
    date_from = datetime.utcnow() - timedelta(days=days)
    
    total_attempts = db.query(AccessLog).filter(
        AccessLog.attempted_at >= date_from
    ).count()
    
    granted = db.query(AccessLog).filter(
        AccessLog.attempted_at >= date_from,
        AccessLog.access_granted == True
    ).count()
    
    denied = db.query(AccessLog).filter(
        AccessLog.attempted_at >= date_from,
        AccessLog.access_granted == False
    ).count()
    
    liveness_failed = db.query(AccessLog).filter(
        AccessLog.attempted_at >= date_from,
        AccessLog.liveness_passed == False
    ).count()
    
    return {
        "period_days": days,
        "total_attempts": total_attempts,
        "granted": granted,
        "denied": denied,
        "liveness_failed": liveness_failed,
        "success_rate": round((granted / total_attempts * 100) if total_attempts > 0 else 0, 2)
    }
