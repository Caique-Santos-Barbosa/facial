from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.employee import AccessLog
from app.schemas.access_log import AccessLogResponse

router = APIRouter()

@router.get("/logs", response_model=List[AccessLogResponse])
def get_access_logs(
    skip: int = 0,
    limit: int = 100,
    employee_id: Optional[int] = None,
    access_granted: Optional[bool] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista logs de acesso com filtros
    """
    query = db.query(AccessLog)
    
    if employee_id:
        query = query.filter(AccessLog.employee_id == employee_id)
    
    if access_granted is not None:
        query = query.filter(AccessLog.access_granted == access_granted)
    
    if start_date:
        query = query.filter(AccessLog.attempted_at >= start_date)
    
    if end_date:
        query = query.filter(AccessLog.attempted_at <= end_date)
    
    logs = query.order_by(AccessLog.attempted_at.desc()).offset(skip).limit(limit).all()
    return logs

@router.get("/stats")
def get_access_stats(
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna estatísticas de acesso
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    total_attempts = db.query(AccessLog).filter(
        AccessLog.attempted_at >= start_date
    ).count()
    
    granted = db.query(AccessLog).filter(
        AccessLog.attempted_at >= start_date,
        AccessLog.access_granted == True
    ).count()
    
    denied = db.query(AccessLog).filter(
        AccessLog.attempted_at >= start_date,
        AccessLog.access_granted == False
    ).count()
    
    return {
        "period_days": days,
        "total_attempts": total_attempts,
        "granted": granted,
        "denied": denied,
        "success_rate": round((granted / total_attempts * 100) if total_attempts > 0 else 0, 2)
    }

