# 🚀 Início Rápido - Sistema de Reconhecimento Facial

## ⚡ Setup Rápido (5 minutos)

### 1. Backend

```bash
cd backend
cp .env.example .env
# Edite .env com suas configurações

docker-compose up -d postgres redis
pip install -r requirements.txt
python -m scripts.init_db
uvicorn app.main:app --reload
```

✅ Backend rodando em `http://localhost:8000`

### 2. Frontend Web

```bash
cd frontend-web
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local
npm run dev
```

✅ Frontend rodando em `http://localhost:3000`

### 3. Mobile App

```bash
cd mobile-app
npm install
echo "EXPO_PUBLIC_API_URL=http://SEU-IP:8000/api/v1" > .env
npm start
```

✅ Escaneie o QR code com Expo Go

## 🔑 Credenciais Padrão

- **Usuário:** admin
- **Senha:** admin123
- ⚠️ **Altere após o primeiro login!**

## 📖 Documentação Completa

Veja `INSTALL.md` para instruções detalhadas.

## 🆘 Problemas?

1. Verifique se PostgreSQL e Redis estão rodando
2. Verifique as variáveis de ambiente
3. Veja os logs: `docker-compose logs -f`
4. Consulte `INSTALL.md` para troubleshooting

