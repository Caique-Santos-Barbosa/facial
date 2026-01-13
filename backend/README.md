# HDT Energy - Sistema de Reconhecimento Facial (Backend)

Sistema de reconhecimento facial com detecção de vivacidade e controle de acesso.

## 🚀 Tecnologias

- Python 3.11
- FastAPI
- PostgreSQL
- Redis
- DeepFace (TensorFlow)
- SQLAlchemy

## 📦 Instalação Local

### 1. Clone o repositório
```bash
git clone <seu-repo>
cd backend
```

### 2. Crie ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale dependências
```bash
pip install -r requirements.txt
```

### 4. Configure variáveis de ambiente
```bash
cp .env.example .env
# Edite .env com suas configurações
```

### 5. Inicie com Docker Compose
```bash
docker-compose up -d
```

### 6. Inicialize o banco de dados
```bash
python scripts/init_db.py
```

### 7. Acesse a documentação
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔑 Credenciais Padrão

**IMPORTANTE: Altere em produção!**

- Username: `admin`
- Password: `admin123`

## 📚 Endpoints Principais

### Autenticação
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/register` - Registro
- `GET /api/v1/auth/me` - Usuário atual

### Colaboradores
- `GET /api/v1/employees` - Listar colaboradores
- `POST /api/v1/employees` - Criar colaborador (com foto)
- `GET /api/v1/employees/{id}` - Detalhes do colaborador
- `PUT /api/v1/employees/{id}` - Atualizar colaborador
- `DELETE /api/v1/employees/{id}` - Desativar colaborador

### Reconhecimento
- `POST /api/v1/recognition/recognize` - Reconhecer face (app mobile)

### Logs
- `GET /api/v1/access-logs` - Listar logs de acesso
- `GET /api/v1/access-logs/stats` - Estatísticas

## 🐳 Deploy no Easypanel

1. Conecte seu repositório GitHub
2. Configure as variáveis de ambiente
3. Deploy automático a cada push

## 📝 Variáveis de Ambiente

Ver arquivo `.env.example` para lista completa.

## 🧪 Testes

```bash
pytest
```

## 📄 Licença

Propriedade de HDT Energy