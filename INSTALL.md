# Guia de Instalação Completo - Sistema de Reconhecimento Facial HDT Energy

## 📋 Pré-requisitos

- Python 3.11+
- Node.js 18+
- Docker e Docker Compose
- PostgreSQL 15+ (ou via Docker)
- Redis (ou via Docker)

## 🚀 Instalação Passo a Passo

### 1. Backend (FastAPI)

```bash
cd backend

# 1. Crie o arquivo .env
cp .env.example .env
# Edite o .env com suas configurações

# 2. Suba os serviços (PostgreSQL e Redis)
docker-compose up -d postgres redis

# 3. Instale as dependências Python
pip install -r requirements.txt

# 4. Inicialize o banco de dados
python -m scripts.init_db

# 5. Execute as migrations (se necessário)
alembic upgrade head

# 6. Inicie o servidor
uvicorn app.main:app --reload
```

O backend estará disponível em `http://localhost:8000`
Documentação da API: `http://localhost:8000/docs`

**Usuário admin padrão:**
- Usuário: `admin`
- Senha: `admin123`
- ⚠️ **ALTERE A SENHA APÓS O PRIMEIRO LOGIN!**

### 2. Frontend Web (Next.js)

```bash
cd frontend-web

# 1. Instale as dependências
npm install

# 2. Crie o arquivo .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local

# 3. Inicie o servidor de desenvolvimento
npm run dev
```

O frontend estará disponível em `http://localhost:3000`

### 3. Mobile App (React Native/Expo)

```bash
cd mobile-app

# 1. Instale as dependências
npm install

# 2. Configure o .env
echo "EXPO_PUBLIC_API_URL=http://SEU-IP:8000/api/v1" > .env
# Substitua SEU-IP pelo IP da sua máquina na rede local

# 3. Inicie o Expo
npm start

# 4. Escaneie o QR code com Expo Go (Android/iOS)
# Ou execute diretamente:
npm run android  # Para Android
npm run ios      # Para iOS
```

**Importante:** Para o app mobile funcionar, você precisa:
- Estar na mesma rede Wi-Fi que o servidor backend
- Usar o IP local da máquina (não localhost)
- Permitir conexões na porta 8000 no firewall

## 🔧 Configuração do Backend

### Variáveis de Ambiente (.env)

```env
# API Configuration
SECRET_KEY=seu-secret-key-super-seguro-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Database
POSTGRES_SERVER=postgres
POSTGRES_USER=facial_user
POSTGRES_PASSWORD=senha-segura-aqui
POSTGRES_DB=facial_recognition_db

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Face Recognition
FACE_RECOGNITION_TOLERANCE=0.6
FACE_DETECTION_MODEL=hog
MIN_FACE_SIZE=100

# Liveness Detection
LIVENESS_ENABLED=true
LIVENESS_THRESHOLD=0.7

# Door Control
DOOR_CONTROLLER_BASE_URL=http://187.50.63.194:8080
DOOR_CONTROLLER_USERNAME=abc
DOOR_CONTROLLER_PASSWORD=123

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:19006"]
```

### Gerar SECRET_KEY

```bash
# Linux/Mac
openssl rand -hex 32

# Windows (PowerShell)
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))
```

## 🐳 Deploy com Docker

### Backend Completo

```bash
cd backend
docker-compose up -d
```

Isso sobe:
- PostgreSQL na porta 5432
- Redis na porta 6379
- API na porta 8000

### Deploy no Easypanel

1. Crie um novo projeto no Easypanel
2. Adicione um serviço Docker
3. Configure o Dockerfile do backend
4. Configure as variáveis de ambiente
5. Configure o volume para `uploads/`
6. Configure o banco de dados PostgreSQL
7. Configure o Redis (opcional)

## 📱 Build do App Mobile

### Android APK

```bash
cd mobile-app

# Build de desenvolvimento
npx expo build:android -t apk

# Build de produção
npx expo build:android -t app-bundle
```

### iOS (requer Mac e conta Apple Developer)

```bash
cd mobile-app
npx expo build:ios
```

## ✅ Verificação Pós-Instalação

1. **Backend:**
   - Acesse `http://localhost:8000/docs`
   - Teste o endpoint `/health`
   - Faça login em `/api/v1/auth/login`

2. **Frontend:**
   - Acesse `http://localhost:3000`
   - Faça login com admin/admin123
   - Cadastre um colaborador

3. **Mobile:**
   - Abra o app
   - Verifique se a câmera está funcionando
   - Teste o reconhecimento facial

## 🔍 Troubleshooting

### Backend não inicia

- Verifique se PostgreSQL e Redis estão rodando
- Verifique as variáveis de ambiente
- Verifique os logs: `docker-compose logs api`

### Frontend não conecta ao backend

- Verifique se `NEXT_PUBLIC_API_URL` está correto
- Verifique CORS no backend
- Verifique se o backend está rodando

### Mobile não conecta ao backend

- Use o IP local (não localhost)
- Verifique se está na mesma rede
- Verifique o firewall
- Verifique se `EXPO_PUBLIC_API_URL` está correto

### Reconhecimento facial não funciona

- Verifique se a imagem tem uma face clara
- Verifique se o colaborador foi cadastrado corretamente
- Verifique os logs do backend
- Ajuste `FACE_RECOGNITION_TOLERANCE` se necessário

## 📚 Próximos Passos

1. Altere a senha do admin
2. Cadastre colaboradores
3. Teste o reconhecimento facial
4. Configure o controlador de porta
5. Ajuste os parâmetros de liveness detection
6. Configure backups do banco de dados

## 🆘 Suporte

Para problemas ou dúvidas, consulte:
- Documentação da API: `http://localhost:8000/docs`
- Logs do backend: `docker-compose logs -f api`
- Logs do frontend: console do navegador
- Logs do mobile: `npx expo start --clear`

