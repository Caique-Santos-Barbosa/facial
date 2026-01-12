# Backend - Sistema de Reconhecimento Facial HDT Energy

## Instalação

1. Crie um arquivo `.env` baseado no `.env.example`
2. Execute `docker-compose up -d` para subir PostgreSQL e Redis
3. Instale as dependências: `pip install -r requirements.txt`
4. Execute as migrations: `alembic upgrade head`
5. Inicie o servidor: `uvicorn app.main:app --reload`

## Endpoints

- `GET /` - Informações da API
- `GET /health` - Health check
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Usuário atual
- `GET /api/v1/employees` - Lista colaboradores
- `POST /api/v1/employees` - Cria colaborador
- `POST /api/v1/recognition/recognize` - Reconhecimento facial
- `GET /api/v1/access/logs` - Logs de acesso
- `GET /api/v1/access/stats` - Estatísticas

## Documentação

Acesse `http://localhost:8000/docs` para ver a documentação interativa da API.

