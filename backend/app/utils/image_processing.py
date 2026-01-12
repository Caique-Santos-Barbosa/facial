import cv2
import numpy as np
from typing import Dict
from app.config import settings

def check_liveness(image_path: str) -> Dict:
    """
    Detecta se a imagem é de uma pessoa real ou foto/vídeo
    Usa análise de textura, brilho e outros indicadores
    """
    try:
        image = cv2.imread(image_path)
        
        if image is None:
            return {
                "is_live": False,
                "confidence": 0.0,
                "reason": "Imagem inválida"
            }
        
        # Converte para escala de cinza
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 1. Análise de variação Laplaciana (detecta blur/imagem de imagem)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # 2. Análise de histograma de cores
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        hist_variance = np.var(hist)
        
        # 3. Análise de brilho
        brightness = np.mean(gray)
        
        # Scoring baseado nos indicadores
        liveness_score = 0.0
        reasons = []
        
        # Imagem muito borrada pode ser foto de foto
        if laplacian_var < 100:
            reasons.append("Imagem muito borrada")
        else:
            liveness_score += 0.4
        
        # Variedade de cores muito baixa pode indicar imagem impressa
        if hist_variance < 0.001:
            reasons.append("Baixa variedade de cores")
        else:
            liveness_score += 0.3
        
        # Brilho muito uniforme pode indicar tela
        if 30 < brightness < 220:
            liveness_score += 0.3
        else:
            reasons.append("Brilho anormal")
        
        is_live = liveness_score >= settings.LIVENESS_THRESHOLD
        
        return {
            "is_live": is_live,
            "confidence": liveness_score,
            "metrics": {
                "laplacian_variance": float(laplacian_var),
                "histogram_variance": float(hist_variance),
                "brightness": float(brightness)
            },
            "reason": " | ".join(reasons) if reasons else "Liveness check passed"
        }
        
    except Exception as e:
        return {
            "is_live": False,
            "confidence": 0.0,
            "reason": f"Erro: {str(e)}"
        }

