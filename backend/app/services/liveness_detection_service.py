from app.utils.image_processing import check_liveness
from typing import Dict

class LivenessDetectionService:
    
    @staticmethod
    def check_liveness(image_path: str) -> Dict:
        """
        Detecta se a imagem é de uma pessoa real ou foto/vídeo
        """
        return check_liveness(image_path)

