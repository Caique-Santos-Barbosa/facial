"""
Endpoint de reconhecimento facial
"""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks, Form
from sqlalchemy.orm import Session
from typing import Optional
import os
import uuid
from datetime import datetime

from app.database import get_db
from app.services.face_recognition_service import FaceRecognitionService
from app.services.liveness_detection_service import LivenessDetectionService
from app.services.door_control_service import DoorControlService
from app.models.employee import Employee, AccessLog
from app.config import settings

router = APIRouter()

@router.post("/recognize")
async def recognize_face(
    image: UploadFile = File(...),
    device_id: Optional[str] = Form(None),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Endpoint principal de reconhecimento facial
    Usado pelo app mobile para validar acesso
    """
    
    temp_image_path = f"/tmp/{uuid.uuid4()}.jpg"
    
    try:
        # Salva arquivo enviado
        with open(temp_image_path, "wb") as buffer:
            content = await image.read()
            buffer.write(content)
        
        # 1. LIVENESS DETECTION
        liveness_result = None
        if settings.LIVENESS_ENABLED:
            liveness_result = LivenessDetectionService.check_liveness(temp_image_path)
            
            if not liveness_result["is_live"]:
                # Registra tentativa falha
                log = AccessLog(
                    employee_id=None,
                    access_granted=False,
                    liveness_passed=False,
                    denial_reason=f"Liveness check failed: {liveness_result['reason']}",
                    device_id=device_id,
                    attempted_at=datetime.utcnow()
                )
                db.add(log)
                db.commit()
                
                return {
                    "success": False,
                    "access_granted": False,
                    "message": "Falha na detecção de vivacidade. Use uma câmera ao vivo.",
                    "liveness_details": liveness_result
                }
        
        # 2. BUSCA COLABORADORES ATIVOS
        employees = db.query(Employee).filter(Employee.is_active == True).all()
        
        if not employees:
            raise HTTPException(
                status_code=404,
                detail="Nenhum colaborador cadastrado no sistema"
            )
        
        # 3. COMPARA COM CADA COLABORADOR
        best_match = None
        best_confidence = 0.0
        
        for employee in employees:
            try:
                match, confidence = FaceRecognitionService.compare_faces(
                    employee.face_encoding,
                    temp_image_path
                )
                
                if match and confidence > best_confidence:
                    best_match = employee
                    best_confidence = confidence
            except Exception as e:
                print(f"Erro ao comparar com colaborador {employee.id}: {str(e)}")
                continue
        
        # 4. PROCESSA RESULTADO
        if best_match and best_confidence >= settings.FACE_RECOGNITION_TOLERANCE:
            # ACESSO CONCEDIDO
            access_log = AccessLog(
                employee_id=best_match.id,
                access_granted=True,
                confidence_score=best_confidence,
                liveness_passed=liveness_result.get("is_live") if liveness_result else None,
                device_id=device_id,
                attempted_at=datetime.utcnow()
            )
            db.add(access_log)
            db.commit()
            
            # Abre porta em background
            def open_door_task():
                try:
                    door_service = DoorControlService()
                    door_service.open_door(1)
                except Exception as e:
                    print(f"Erro ao abrir porta: {str(e)}")
            
            if background_tasks:
                background_tasks.add_task(open_door_task)
            
            # Saudação baseada na hora
            hour = datetime.now().hour
            if 5 <= hour < 12:
                greeting = "Bom dia"
            elif 12 <= hour < 18:
                greeting = "Boa tarde"
            else:
                greeting = "Boa noite"
            
            return {
                "success": True,
                "access_granted": True,
                "employee": {
                    "id": best_match.id,
                    "name": best_match.full_name,
                    "department": best_match.department,
                    "position": best_match.position
                },
                "confidence": round(best_confidence, 2),
                "message": f"{greeting}, {best_match.full_name}!",
                "timestamp": datetime.now().isoformat()
            }
        else:
            # ACESSO NEGADO
            access_log = AccessLog(
                employee_id=None,
                access_granted=False,
                confidence_score=best_confidence if best_match else 0.0,
                liveness_passed=liveness_result.get("is_live") if liveness_result else None,
                denial_reason="Face não reconhecida ou confiança insuficiente",
                device_id=device_id,
                attempted_at=datetime.utcnow()
            )
            db.add(access_log)
            db.commit()
            
            return {
                "success": False,
                "access_granted": False,
                "message": "Face não reconhecida. Acesso negado.",
                "confidence": round(best_confidence, 2) if best_match else 0.0,
                "timestamp": datetime.now().isoformat()
            }
    
    except Exception as e:
        print(f"Erro no reconhecimento facial: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar reconhecimento: {str(e)}"
        )
    finally:
        # Limpa arquivo temporário
        if os.path.exists(temp_image_path):
            try:
                os.remove(temp_image_path)
            except:
                pass
