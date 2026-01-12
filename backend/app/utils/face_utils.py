import face_recognition
import numpy as np
import pickle
from typing import Optional, Tuple
from app.config import settings

def encode_face(image_path: str) -> Optional[np.ndarray]:
    """
    Gera encoding da face a partir de uma imagem
    """
    try:
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(
            image, 
            model=settings.FACE_DETECTION_MODEL
        )
        
        if not face_locations:
            return None
        
        # Pega apenas a primeira face detectada
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        if not face_encodings:
            return None
            
        return face_encodings[0]
        
    except Exception as e:
        print(f"Erro ao processar face: {str(e)}")
        return None

def serialize_face_encoding(encoding: np.ndarray) -> bytes:
    """
    Serializa encoding numpy para bytes
    """
    return pickle.dumps(encoding)

def deserialize_face_encoding(encoding_bytes: bytes) -> np.ndarray:
    """
    Deserializa bytes para encoding numpy
    """
    return pickle.loads(encoding_bytes)

def compare_faces(known_encoding: bytes, unknown_image_path: str) -> Tuple[bool, float]:
    """
    Compara face conhecida com imagem desconhecida
    Retorna (match, confidence_score)
    """
    try:
        # Deserializa o encoding conhecido
        known_face = deserialize_face_encoding(known_encoding)
        
        # Processa a imagem desconhecida
        unknown_encoding = encode_face(unknown_image_path)
        
        if unknown_encoding is None:
            return False, 0.0
        
        # Compara as faces
        face_distances = face_recognition.face_distance([known_face], unknown_encoding)
        distance = face_distances[0]
        
        # Calcula confidence score (1 - distance)
        confidence = 1 - distance
        
        # Verifica se passou no threshold
        matches = face_recognition.compare_faces(
            [known_face], 
            unknown_encoding,
            tolerance=settings.FACE_RECOGNITION_TOLERANCE
        )
        
        return matches[0], float(confidence)
        
    except Exception as e:
        print(f"Erro na comparação: {str(e)}")
        return False, 0.0

def validate_face_image(image_path: str) -> dict:
    """
    Valida se a imagem contém uma face válida
    """
    try:
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        
        if not face_locations:
            return {
                "valid": False,
                "error": "Nenhuma face detectada na imagem"
            }
        
        if len(face_locations) > 1:
            return {
                "valid": False,
                "error": "Múltiplas faces detectadas. Use uma imagem com apenas uma pessoa"
            }
        
        # Verifica tamanho mínimo da face
        top, right, bottom, left = face_locations[0]
        face_width = right - left
        face_height = bottom - top
        
        if face_width < settings.MIN_FACE_SIZE or face_height < settings.MIN_FACE_SIZE:
            return {
                "valid": False,
                "error": f"Face muito pequena. Tamanho mínimo: {settings.MIN_FACE_SIZE}px"
            }
        
        return {
            "valid": True,
            "face_location": face_locations[0]
        }
        
    except Exception as e:
        return {
            "valid": False,
            "error": f"Erro ao processar imagem: {str(e)}"
        }

