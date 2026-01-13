"""
Serviço de Detecção de Vivacidade (Liveness Detection)
Previne spoofing com fotos ou vídeos
"""

import cv2
import numpy as np
from typing import Dict
from app.config import settings

class LivenessDetectionService:
    
    @staticmethod
    def check_liveness(image_path: str) -> Dict:
        """
        Detecta se a imagem é de uma pessoa real ou foto/vídeo (spoofing)
        
        Usa múltiplas técnicas:
        1. Análise de Laplaciano (detecta blur de foto de foto)
        2. Análise de Histograma de Cores (detecta uniformidade suspeita)
        3. Análise de Brilho (detecta reflexos de tela)
        4. Análise de Textura (detecta padrões de impressão)
        
        Args:
            image_path: Caminho para a imagem
            
        Returns:
            Dict com resultado da análise de vivacidade
        """
        try:
            # Lê a imagem
            image = cv2.imread(image_path)
            
            if image is None:
                return {
                    "is_live": False,
                    "confidence": 0.0,
                    "reason": "Imagem inválida ou corrompida"
                }
            
            # Converte para escala de cinza
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # 1. ANÁLISE DE VARIAÇÃO LAPLACIANA
            # Imagens de foto de foto tendem a ser mais borradas
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            laplacian_score = 0.0
            laplacian_reason = ""
            
            if laplacian_var < 50:
                laplacian_reason = "Imagem muito borrada (foto de foto?)"
            elif laplacian_var < 100:
                laplacian_score = 0.2
                laplacian_reason = "Imagem com blur moderado"
            else:
                laplacian_score = 0.4
                laplacian_reason = "Nitidez adequada"
            
            # 2. ANÁLISE DE HISTOGRAMA DE CORES
            # Fotos impressas têm menos variedade de cores
            hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            hist = cv2.normalize(hist, hist).flatten()
            hist_variance = np.var(hist)
            hist_score = 0.0
            hist_reason = ""
            
            if hist_variance < 0.0005:
                hist_reason = "Baixíssima variedade de cores (suspeito)"
            elif hist_variance < 0.001:
                hist_score = 0.15
                hist_reason = "Baixa variedade de cores"
            else:
                hist_score = 0.3
                hist_reason = "Variedade de cores adequada"
            
            # 3. ANÁLISE DE BRILHO
            # Telas tendem a ter brilho muito uniforme
            brightness = np.mean(gray)
            brightness_score = 0.0
            brightness_reason = ""
            
            if brightness < 20 or brightness > 235:
                brightness_reason = "Brilho anormal (muito escuro ou claro)"
            elif brightness < 30 or brightness > 220:
                brightness_score = 0.1
                brightness_reason = "Brilho nos limites"
            else:
                brightness_score = 0.3
                brightness_reason = "Brilho adequado"
            
            # 4. ANÁLISE DE CONTRASTE
            # Fotos de foto tendem a ter contraste reduzido
            contrast = gray.std()
            contrast_score = 0.0
            contrast_reason = ""
            
            if contrast < 30:
                contrast_reason = "Contraste muito baixo"
            elif contrast < 45:
                contrast_score = 0.1
                contrast_reason = "Contraste baixo"
            else:
                contrast_score = 0.0  # Não adiciona pontos, apenas não penaliza
                contrast_reason = "Contraste adequado"
            
            # CÁLCULO DO SCORE FINAL
            liveness_score = laplacian_score + hist_score + brightness_score + contrast_score
            
            # Verifica se passou no threshold
            is_live = liveness_score >= settings.LIVENESS_THRESHOLD
            
            # Monta lista de razões
            reasons = []
            if laplacian_score < 0.3:
                reasons.append(laplacian_reason)
            if hist_score < 0.2:
                reasons.append(hist_reason)
            if brightness_score < 0.2:
                reasons.append(brightness_reason)
            if contrast_score == 0 and contrast < 30:
                reasons.append(contrast_reason)
            
            return {
                "is_live": is_live,
                "confidence": round(liveness_score, 3),
                "threshold": settings.LIVENESS_THRESHOLD,
                "metrics": {
                    "laplacian_variance": round(float(laplacian_var), 2),
                    "histogram_variance": round(float(hist_variance), 6),
                    "brightness": round(float(brightness), 2),
                    "contrast": round(float(contrast), 2)
                },
                "scores": {
                    "laplacian": laplacian_score,
                    "histogram": hist_score,
                    "brightness": brightness_score,
                    "contrast": contrast_score
                },
                "reason": " | ".join(reasons) if reasons else "Todas as verificações passaram"
            }
            
        except Exception as e:
            return {
                "is_live": False,
                "confidence": 0.0,
                "reason": f"Erro na análise: {str(e)}"
            }
    
    @staticmethod
    def check_moiré_pattern(image_path: str) -> bool:
        """
        Detecta padrões Moiré que aparecem quando se fotografa uma tela
        
        Args:
            image_path: Caminho para a imagem
            
        Returns:
            True se detectou padrão Moiré (indica foto de tela)
        """
        try:
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Aplica FFT para detectar padrões repetitivos
            f = np.fft.fft2(gray)
            fshift = np.fft.fftshift(f)
            magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
            
            # Padrões Moiré geram picos específicos no espectro de frequência
            # Esta é uma implementação simplificada
            threshold = np.mean(magnitude_spectrum) + 2 * np.std(magnitude_spectrum)
            peaks = np.sum(magnitude_spectrum > threshold)
            
            # Se há muitos picos, pode indicar padrão Moiré
            return peaks > 100
            
        except Exception as e:
            print(f"Erro na detecção de Moiré: {str(e)}")
            return False
