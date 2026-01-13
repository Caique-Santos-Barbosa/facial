# 🚀 Deploy do Frontend Web no Easypanel

## 📋 Pré-requisitos

- ✅ Código commitado e pushed para o GitHub
- ✅ Dockerfile criado
- ✅ next.config.js configurado com `output: 'standalone'`

## 🎯 Passo a Passo no Easypanel

### 1. Criar Novo Serviço

1. Acesse seu projeto no Easypanel
2. Clique em **"Add Service"**
3. Selecione **"From Source"** → **"GitHub"**

### 2. Configurar o Serviço

#### General:
- **Name:** `facial-web`
- **Repository:** Selecione seu repositório
- **Branch:** `main`
- **Source Directory:** `frontend-web`
- **Build Type:** `Dockerfile`

#### Domains:
- **Add Domain**
- **Domain:** `hdt-energy-facial-web.mqtl34.easypanel.host` (ou escolha outro)
- **Container Port:** `3000`
- **Protocol:** `HTTP`
- **Enable HTTPS:** ✅

#### Environment Variables:
```
NEXT_PUBLIC_API_URL=https://hdt-energy-facial.mqtl34.easypanel.host/api/v1
NODE_ENV=production
```

### 3. Criar e Aguardar Build

1. Clique em **"Create"**
2. Aguarde o build completar (~5-10 minutos na primeira vez)
3. Monitore os logs em **Services → facial-web → Logs**

## 🔧 Configurar CORS no Backend

Como o frontend estará em outro domínio, atualize o CORS no backend:

### No Easypanel - Serviço `facial`:

**Atualizar a variável de ambiente:**

```env
BACKEND_CORS_ORIGINS=["https://hdt-energy-facial-web.mqtl34.easypanel.host","http://localhost:3000"]
```

**Reiniciar o serviço:**
```
Services → facial → Restart
```

## ✅ Verificação

### 1. Acesse o frontend
```
https://hdt-energy-facial-web.mqtl34.easypanel.host
```

Deve aparecer a tela de login!

### 2. Faça login
- Username: `admin`
- Password: `HDT@2026!Admin`

### 3. Teste funcionalidades
- ✅ Dashboard
- ✅ Colaboradores
- ✅ Novo colaborador
- ✅ Logs

## 🐛 Troubleshooting

### Build falha

1. **Veja os logs:**
   ```
   Services → facial-web → Logs
   ```

2. **Erros comuns:**
   - Faltou `next.config.js` com `output: 'standalone'`
   - Porta errada (deve ser 3000)
   - Variável de ambiente faltando

### Não conecta na API

1. **Verifique CORS no backend:**
   ```env
   BACKEND_CORS_ORIGINS=["https://hdt-energy-facial-web.mqtl34.easypanel.host"]
   ```

2. **Reinicie o backend:**
   ```
   Services → facial → Restart
   ```

### Página não carrega

1. **Verifique o domínio:**
   - Container Port: `3000`
   - Protocol: `HTTP`
   - HTTPS: Habilitado

2. **Aguarde 2-3 minutos** após o build

## 📊 Estrutura Final no Easypanel

```
hdt_energy/
├── facial-postgres    (PostgreSQL) ✅
├── facial             (Backend API) ✅
└── facial-web         (Frontend Web) 🆕
```

## 🌐 URLs do Sistema

**Backend API:**
```
https://hdt-energy-facial.mqtl34.easypanel.host
```

**Frontend Web:**
```
https://hdt-energy-facial-web.mqtl34.easypanel.host
```

**Documentação API:**
```
https://hdt-energy-facial.mqtl34.easypanel.host/docs
```
