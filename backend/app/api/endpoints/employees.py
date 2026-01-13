"""
Endpoints para gerenciamento de colaboradores
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
import pickle
from datetime import datetime

from app.database import get_db
from app.schemas.employee import EmployeeResponse, EmployeeListResponse, EmployeeUpdate
from app.models.employee import Employee
from app.api.deps import get_current_user
from app.models.user import User
from app.config import settings
from app.services.face_recognition_service import FaceRecognitionService

router = APIRouter()

@router.get("/", response_model=List[EmployeeListResponse])
def list_employees(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista todos os colaboradores
    """
    query = db.query(Employee)
    
    if active_only:
        query = query.filter(Employee.is_active == True)
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Employee.full_name.ilike(search_filter)) |
            (Employee.cpf.ilike(search_filter)) |
            (Employee.email.ilike(search_filter))
        )
    
    employees = query.offset(skip).limit(limit).all()
    return employees

@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém detalhes de um colaborador
    """
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colaborador não encontrado"
        )
    
    return employee

@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(
    full_name: str = Form(...),
    cpf: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None),
    department: str = Form(None),
    position: str = Form(None),
    face_image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cria novo colaborador com foto facial
    """
    # Verifica se CPF já existe
    if db.query(Employee).filter(Employee.cpf == cpf).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já cadastrado"
        )
    
    # Verifica se email já existe
    if db.query(Employee).filter(Employee.email == email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Salva imagem temporariamente
    temp_image_path = f"/tmp/{uuid.uuid4()}.jpg"
    
    try:
        # Salva arquivo enviado
        with open(temp_image_path, "wb") as buffer:
            content = await face_image.read()
            buffer.write(content)
        
        # Valida imagem facial
        validation = FaceRecognitionService.validate_face_image(temp_image_path)
        
        if not validation["valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=validation["error"]
            )
        
        # Gera encoding da face
        face_encoding = FaceRecognitionService.encode_face(temp_image_path)
        
        if face_encoding is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não foi possível processar a face na imagem"
            )
        
        # Salva imagem permanentemente
        os.makedirs(settings.FACES_DIR, exist_ok=True)
        permanent_filename = f"{uuid.uuid4()}.jpg"
        permanent_path = os.path.join(settings.FACES_DIR, permanent_filename)
        
        with open(permanent_path, "wb") as f:
            with open(temp_image_path, "rb") as tmp:
                f.write(tmp.read())
        
        # face_encoding já vem serializado do serviço
        face_encoding_bytes = face_encoding
        
        # Cria colaborador
        new_employee = Employee(
            full_name=full_name,
            cpf=cpf,
            email=email,
            phone=phone,
            department=department,
            position=position,
            face_encoding=face_encoding_bytes,
            face_image_path=permanent_path,
            face_registered_at=datetime.utcnow()
        )
        
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
        
        return new_employee
        
    finally:
        # Limpa arquivo temporário
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)

@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza dados de um colaborador
    """
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colaborador não encontrado"
        )
    
    # Atualiza campos fornecidos
    update_data = employee_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(employee, field, value)
    
    employee.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(employee)
    
    return employee

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove um colaborador (soft delete)
    """
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colaborador não encontrado"
        )
    
    # Soft delete
    employee.is_active = False
    employee.updated_at = datetime.utcnow()
    
    db.commit()
    
    return None
