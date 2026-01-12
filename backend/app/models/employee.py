from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, LargeBinary, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False, index=True)
    cpf = Column(String(14), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    department = Column(String(100), nullable=True)
    position = Column(String(100), nullable=True)
    
    # Face Recognition Data
    face_encoding = Column(LargeBinary, nullable=False)  # numpy array serializado
    face_image_path = Column(String(500), nullable=False)
    face_registered_at = Column(DateTime, default=datetime.utcnow)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    access_logs = relationship("AccessLog", back_populates="employee")

class AccessLog(Base):
    __tablename__ = "access_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    
    # Access Details
    access_granted = Column(Boolean, nullable=False)
    confidence_score = Column(Float, nullable=True)
    liveness_passed = Column(Boolean, nullable=True)
    
    # Timestamps
    attempted_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Device Info
    device_id = Column(String(100), nullable=True)
    device_location = Column(String(255), nullable=True)
    
    # Images
    capture_image_path = Column(String(500), nullable=True)
    
    # Denial Reason
    denial_reason = Column(String(255), nullable=True)
    
    # Relationships
    employee = relationship("Employee", back_populates="access_logs")

