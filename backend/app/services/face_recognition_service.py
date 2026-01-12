from app.utils.face_utils import encode_face, serialize_face_encoding, compare_faces, validate_face_image
from typing import Optional, Tuple

class FaceRecognitionService:
    
    @staticmethod
    def encode_face(image_path: str) -> Optional[bytes]:
        """
        Gera encoding da face e retorna serializado
        """
        encoding = encode_face(image_path)
        if encoding is None:
            return None
        return serialize_face_encoding(encoding)
    
    @staticmethod
    def compare_faces(known_encoding: bytes, unknown_image_path: str) -> Tuple[bool, float]:
        """
        Compara face conhecida com imagem desconhecida
        """
        return compare_faces(known_encoding, unknown_image_path)
    
    @staticmethod
    def validate_face_image(image_path: str) -> dict:
        """
        Valida se a imagem contém uma face válida
        """
        return validate_face_image(image_path)

