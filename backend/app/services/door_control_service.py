import requests
import tempfile
import os
from app.config import settings

class DoorControlService:
    
    def __init__(self):
        self.base_url = settings.DOOR_CONTROLLER_BASE_URL
        self.username = settings.DOOR_CONTROLLER_USERNAME
        self.password = settings.DOOR_CONTROLLER_PASSWORD
        self.cookie_file = None
    
    def _login(self) -> bool:
        """
        Realiza login no controlador de porta
        """
        try:
            # Cria arquivo temporário para cookie
            self.cookie_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.cookie')
            cookie_path = self.cookie_file.name
            self.cookie_file.close()
            
            # Faz login
            login_url = f"{self.base_url}/ACT_ID_1"
            data = {
                "username": self.username,
                "pwd": self.password,
                "logId": "20101222"
            }
            
            response = requests.post(
                login_url,
                data=data,
                cookies={},
                timeout=10
            )
            
            if response.status_code == 200:
                # Salva cookies
                with open(cookie_path, 'w') as f:
                    for cookie in response.cookies:
                        f.write(f"{cookie.name}={cookie.value}\n")
                return True
            
            return False
            
        except Exception as e:
            print(f"Erro no login do controlador: {str(e)}")
            return False
    
    def open_door(self, door_number: int = 1) -> bool:
        """
        Abre a porta especificada
        """
        try:
            # Faz login
            if not self._login():
                return False
            
            # Lê cookies
            cookies = {}
            if self.cookie_file and os.path.exists(self.cookie_file.name):
                with open(self.cookie_file.name, 'r') as f:
                    for line in f:
                        if '=' in line:
                            name, value = line.strip().split('=', 1)
                            cookies[name] = value
            
            # Envia comando para abrir porta
            open_url = f"{self.base_url}/ACT_ID_701"
            data = {
                f"UNCLOSE{door_number}": f"Remote Open #{door_number} Door"
            }
            
            response = requests.post(
                open_url,
                data=data,
                cookies=cookies,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"Erro ao abrir porta: {str(e)}")
            return False
        finally:
            # Garante limpeza do cookie
            if self.cookie_file and os.path.exists(self.cookie_file.name):
                try:
                    os.unlink(self.cookie_file.name)
                except:
                    pass

