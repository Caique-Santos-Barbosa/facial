# Sistema de Reconhecimento Facial HDT Energy

Sistema completo de reconhecimento facial com controle de acesso físico, composto por:

1. **Backend API** (Python FastAPI) - hospedagem no Easypanel via Docker
2. **Painel Web Administrativo** (React/Next.js) - cadastro e gestão de colaboradores
3. **Aplicativo Android** (React Native/Expo) - reconhecimento facial com liveness detection

## 📁 Estrutura do Projeto

```
facial-recognition-system/
├── backend/          # API FastAPI
├── frontend-web/     # Painel administrativo Next.js
└── mobile-app/       # App React Native/Expo
```

## 🚀 Início Rápido

### Backend

1. Entre na pasta `backend`
2. Copie `.env.example` para `.env` e configure as variáveis
3. Execute `docker-compose up -d` para subir PostgreSQL e Redis
4. Instale as dependências: `pip install -r requirements.txt`
5. Execute as migrations: `alembic upgrade head`
6. Inicie o servidor: `uvicorn app.main:app --reload`

### Frontend Web

1. Entre na pasta `frontend-web`
2. Instale as dependências: `npm install`
3. Crie `.env.local` com `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1`
4. Execute: `npm run dev`
5. Acesse `http://localhost:3000`

### Mobile App

1. Entre na pasta `mobile-app`
2. Instale as dependências: `npm install`
3. Configure `.env` com a URL da API
4. Execute: `npm start`
5. Escaneie o QR code com Expo Go ou execute `npm run android`

## 📚 Documentação

- Backend API: `http://localhost:8000/docs`
- Cada módulo possui seu próprio README.md com instruções detalhadas

## 🔐 Segurança

- Autenticação JWT
- Hash bcrypt para senhas
- CORS configurado
- Validação de inputs
- Liveness detection para prevenir fraudes

## 📝 Licença

Proprietário - HDT Energy

