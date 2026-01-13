"""
Serviço de Reconhecimento Facial usando DeepFace
Mais moderno, preciso e fácil de instalar que dlib
"""

from deepface import DeepFace
import numpy as np
import cv2
from typing import Optional, Tuple, Dict
import pickle
from app.config import settings
import os

class FaceRecognitionService:
    
    # Modelo a ser usado (pode ser: VGG-Face, Facenet, OpenFace, DeepFace, DeepID, ArcFace, Dlib, SFace)
    MODEL_NAME = "Facenet"  # Facenet é rápido e preciso
    DETECTOR_BACKEND = "opencv"  # opencv, ssd, dlib, mtcnn, retinaface
    
    @staticmethod
    def encode_face(image_path: str) -> Optional[bytes]:
        """
        Gera embedding da face usando DeepFace
        
        Args:
            image_path: Caminho para a imagem
            
        Returns:
            bytes serializados com o embedding da face ou None se falhar
        """
        try:
            if not os.path.exists(image_path):
                print(f"Arquivo não encontrado: {image_path}")
                return None
            
            # Extrai embedding da face
            embedding_objs = DeepFace.represent(
                img_path=image_path,
                model_name=FaceRecognitionService.MODEL_NAME,
                enforce_detection=True,
                detector_backend=FaceRecognitionService.DETECTOR_BACKEND
            )
            
            if not embedding_objs:
                return None
            
            # Pega o primeiro embedding (primeira face detectada)
            embedding = np.array(embedding_objs[0]["embedding"])
            
            # Serializa para bytes
            return pickle.dumps(embedding)
            
        except ValueError as e:
            print(f"Nenhuma face detectada: {str(e)}")
            return None
        except Exception as e:
            print(f"Erro ao processar face: {str(e)}")
            return None
    
    @staticmethod
    def compare_faces(known_encoding: bytes, unknown_image_path: str) -> Tuple[bool, float]:
        """
        Compara face conhecida com imagem desconhecida
        
        Args:
            known_encoding: Encoding serializado da face conhecida
            unknown_image_path: Caminho para a imagem a ser comparada
            
        Returns:
            Tupla (match: bool, confidence: float)
        """
        try:
            # Deserializa o encoding conhecido
            known_face = pickle.loads(known_encoding)
            
            # Processa a imagem desconhecida
            unknown_encoding = FaceRecognitionService.encode_face(unknown_image_path)
            
            if unknown_encoding is None:
                return False, 0.0
            
            # Deserializa o encoding desconhecido
            unknown_face = pickle.loads(unknown_encoding)
            
            # Calcula distância cosine entre os embeddings
            from scipy.spatial.distance import cosine
            distance = cosine(known_face, unknown_face)
            
            # Converte distância para similaridade (0-1, onde 1 é idêntico)
            # Para Facenet, threshold típico de distância é 0.4
            # Convertendo: similarity = 1 - distance
            similarity = 1 - distance
            
            # Verifica se passou no threshold
            # Se FACE_RECOGNITION_TOLERANCE = 0.6, significa que aceitamos 60% de similaridade
            threshold = settings.FACE_RECOGNITION_TOLERANCE
            matches = similarity >= threshold
            
            return matches, float(similarity)
            
        except Exception as e:
            print(f"Erro na comparação: {str(e)}")
            return False, 0.0
    
    @staticmethod
    def validate_face_image(image_path: str) -> Dict:
        """
        Valida se a imagem contém uma face válida
        
        Args:
            image_path: Caminho para a imagem
            
        Returns:
            Dict com resultado da validação
        """
        try:
            if not os.path.exists(image_path):
                return {
                    "valid": False,
                    "error": "Arquivo de imagem não encontrado"
                }
            
            # Extrai faces da imagem
            result = DeepFace.extract_faces(
                img_path=image_path,
                enforce_detection=True,
                detector_backend=FaceRecognitionService.DETECTOR_BACKEND,
                align=True
            )
            
            if not result:
                return {
                    "valid": False,
                    "error": "Nenhuma face detectada na imagem"
                }
            
            if len(result) > 1:
                return {
                    "valid": False,
                    "error": "Múltiplas faces detectadas. Use uma imagem com apenas uma pessoa"
                }
            
            # Verifica tamanho da face
            face_info = result[0]
            facial_area = face_info.get("facial_area", {})
            
            width = facial_area.get("w", 0)
            height = facial_area.get("h", 0)
            
            if width < settings.MIN_FACE_SIZE or height < settings.MIN_FACE_SIZE:
                return {
                    "valid": False,
                    "error": f"Face muito pequena. Tamanho mínimo: {settings.MIN_FACE_SIZE}px"
                }
            
            # Verifica confiança da detecção
            confidence = face_info.get("confidence", 0)
            if confidence < 0.8:  # 80% de confiança mínima
                return {
                    "valid": False,
                    "error": f"Baixa confiança na detecção facial: {confidence:.2%}"
                }
            
            return {
                "valid": True,
                "face_location": facial_area,
                "confidence": confidence
            }
            
        except ValueError as e:
            return {
                "valid": False,
                "error": f"Nenhuma face detectada: {str(e)}"
            }
        except Exception as e:
            return {
                "valid": False,
                "error": f"Erro ao processar imagem: {str(e)}"
            }
    
    @staticmethod
    def analyze_face(image_path: str) -> Dict:
        """
        Analisa atributos faciais (idade, gênero, emoção, etc)
        Útil para estatísticas adicionais
        
        Args:
            image_path: Caminho para a imagem
            
        Returns:
            Dict com análise facial
        """
        try:
            analysis = DeepFace.analyze(
                img_path=image_path,
                actions=['age', 'gender', 'emotion'],
                enforce_detection=False,
                detector_backend=FaceRecognitionService.DETECTOR_BACKEND
            )
            
            if not analysis:
                return {}
            
            return analysis[0] if isinstance(analysis, list) else analysis
            
        except Exception as e:
            print(f"Erro na análise facial: {str(e)}")
            return {}
