from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import os
import uuid
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.services.face_recognition_service import FaceRecognitionService
from app.utils.face_utils import serialize_face_encoding
from app.config import settings

router = APIRouter()

@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(
    full_name: str,
    cpf: str,
    email: str,
    phone: str = None,
    department: str = None,
    position: str = None,
    face_image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cria um novo colaborador com foto facial
    """
    # Verifica se CPF já existe
    existing = db.query(Employee).filter(Employee.cpf == cpf).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já cadastrado"
        )
    
    # Verifica se email já existe
    existing_email = db.query(Employee).filter(Employee.email == email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Cria diretório se não existir
    os.makedirs(settings.FACES_DIR, exist_ok=True)
    
    # Salva imagem
    file_extension = os.path.splitext(face_image.filename)[1]
    face_filename = f"{uuid.uuid4()}{file_extension}"
    face_path = os.path.join(settings.FACES_DIR, face_filename)
    
    with open(face_path, "wb") as buffer:
        content = await face_image.read()
        buffer.write(content)
    
    # Valida face na imagem
    validation = FaceRecognitionService.validate_face_image(face_path)
    if not validation["valid"]:
        os.remove(face_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=validation["error"]
        )
    
    # Gera encoding facial
    face_encoding = FaceRecognitionService.encode_face(face_path)
    if face_encoding is None:
        os.remove(face_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível gerar encoding facial"
        )
    
    # Cria colaborador
    employee = Employee(
        full_name=full_name,
        cpf=cpf,
        email=email,
        phone=phone,
        department=department,
        position=position,
        face_encoding=face_encoding,
        face_image_path=face_path,
        face_registered_at=datetime.utcnow()
    )
    
    db.add(employee)
    db.commit()
    db.refresh(employee)
    
    return employee

@router.get("", response_model=List[EmployeeResponse])
def list_employees(
    skip: int = 0,
    limit: int = 100,
    is_active: bool = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista todos os colaboradores
    """
    query = db.query(Employee)
    
    if is_active is not None:
        query = query.filter(Employee.is_active == is_active)
    
    employees = query.offset(skip).limit(limit).all()
    return employees

@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém um colaborador por ID
    """
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colaborador não encontrado"
        )
    return employee

@router.patch("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza um colaborador
    """
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colaborador não encontrado"
        )
    
    update_data = employee_update.dict(exclude_unset=True)
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
    Desativa um colaborador (soft delete)
    """
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colaborador não encontrado"
        )
    
    employee.is_active = False
    employee.updated_at = datetime.utcnow()
    db.commit()
    
    return None

