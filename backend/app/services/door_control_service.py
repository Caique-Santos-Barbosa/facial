"""
Serviço de Controle de Porta
Integra com o controlador físico via HTTP
"""

import requests
import tempfile
import os
from typing import Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class DoorControlService:
    """
    Serviço para controlar portas via HTTP
    Baseado no comando curl fornecido
    """
    
    def __init__(self):
        self.base_url = settings.DOOR_CONTROLLER_BASE_URL
        self.username = settings.DOOR_CONTROLLER_USERNAME
        self.password = settings.DOOR_CONTROLLER_PASSWORD
        self.cookie_file = None
        self.session = requests.Session()
    
    def _login(self) -> bool:
        """
        Realiza login no controlador de porta
        
        Returns:
            True se login bem-sucedido
        """
        try:
            logger.info("Tentando login no controlador de porta...")
            
            # Cria arquivo temporário para cookie
            self.cookie_file = tempfile.NamedTemporaryFile(
                mode='w', 
                delete=False, 
                suffix='.cookie'
            )
            cookie_path = self.cookie_file.name
            self.cookie_file.close()
            
            # Endpoint de login
            login_url = f"{self.base_url}/ACT_ID_1"
            
            # Dados de login
            data = {
                "username": self.username,
                "pwd": self.password,
                "logId": "20101222"
            }
            
            # Faz requisição de login
            response = self.session.post(
                login_url,
                data=data,
                timeout=10,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                # Salva cookies no arquivo
                with open(cookie_path, 'w') as f:
                    for cookie in self.session.cookies:
                        f.write(f"{cookie.name}={cookie.value}\n")
                
                logger.info("Login realizado com sucesso")
                return True
            else:
                logger.error(f"Falha no login. Status: {response.status_code}")
                return False
            
        except requests.exceptions.Timeout:
            logger.error("Timeout ao tentar login no controlador")
            return False
        except Exception as e:
            logger.error(f"Erro no login do controlador: {str(e)}")
            return False
    
    def open_door(self, door_number: int = 1) -> bool:
        """
        Abre a porta especificada
        
        Args:
            door_number: Número da porta (padrão: 1)
            
        Returns:
            True se comando enviado com sucesso
        """
        try:
            logger.info(f"Tentando abrir porta #{door_number}...")
            
            # Faz login primeiro
            if not self._login():
                logger.error("Não foi possível fazer login para abrir porta")
                return False
            
            # Lê cookies do arquivo
            cookies = {}
            if self.cookie_file:
                try:
                    with open(self.cookie_file.name, 'r') as f:
                        for line in f:
                            if '=' in line:
                                name, value = line.strip().split('=', 1)
                                cookies[name] = value
                except FileNotFoundError:
                    logger.warning("Arquivo de cookie não encontrado, usando session cookies")
            
            # Endpoint para abrir porta
            open_url = f"{self.base_url}/ACT_ID_701"
            
            # Dados do comando
            data = {
                f"UNCLOSE{door_number}": f"Remote Open #{door_number} Door"
            }
            
            # Envia comando para abrir porta
            response = self.session.post(
                open_url,
                data=data,
                cookies=cookies if cookies else None,
                timeout=10
            )
            
            success = response.status_code == 200
            
            if success:
                logger.info(f"Porta #{door_number} aberta com sucesso")
            else:
                logger.error(f"Falha ao abrir porta. Status: {response.status_code}")
            
            # Limpa arquivo de cookie
            self._cleanup()
            
            return success
            
        except requests.exceptions.Timeout:
            logger.error("Timeout ao enviar comando para abrir porta")
            self._cleanup()
            return False
        except Exception as e:
            logger.error(f"Erro ao abrir porta: {str(e)}")
            self._cleanup()
            return False
    
    def _cleanup(self):
        """Limpa recursos temporários"""
        try:
            if self.cookie_file and os.path.exists(self.cookie_file.name):
                os.unlink(self.cookie_file.name)
                logger.debug("Arquivo de cookie removido")
        except Exception as e:
            logger.warning(f"Erro ao limpar cookie: {str(e)}")
    
    def __del__(self):
        """Destrutor - garante limpeza de recursos"""
        self._cleanup()
        if hasattr(self, 'session'):
            self.session.close()
