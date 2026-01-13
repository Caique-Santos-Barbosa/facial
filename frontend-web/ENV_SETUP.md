# 🔧 Configuração de Variáveis de Ambiente

## ⚠️ IMPORTANTE

O Next.js precisa das variáveis `NEXT_PUBLIC_*` no **momento do build**, não no runtime!

## 📋 Variáveis Necessárias

### No Easypanel - Serviço `facial-web`

**Environment Variables:**
```env
NEXT_PUBLIC_API_URL=https://hdt-energy-facial.mqtl34.easypanel.host/api/v1
NODE_ENV=production
```

**Build Args (IMPORTANTE!):**
```env
NEXT_PUBLIC_API_URL=https://hdt-energy-facial.mqtl34.easypanel.host/api/v1
```

## 🎯 Como Configurar no Easypanel

### Passo 1: Environment Variables

1. Vá em: `Services → facial-web → Environment Variables`
2. Adicione/Verifique:
   - **Name:** `NEXT_PUBLIC_API_URL`
   - **Value:** `https://hdt-energy-facial.mqtl34.easypanel.host/api/v1`
   - **Name:** `NODE_ENV`
   - **Value:** `production`

### Passo 2: Build Args (CRÍTICO!)

1. Vá em: `Services → facial-web → Settings → Build`
2. Procure por **"Build Arguments"** ou **"Build Args"**
3. Adicione:
   - **Name:** `NEXT_PUBLIC_API_URL`
   - **Value:** `https://hdt-energy-facial.mqtl34.easypanel.host/api/v1`

**Por que Build Args?**
- As variáveis `NEXT_PUBLIC_*` são injetadas no código durante o build
- Elas precisam estar disponíveis quando `npm run build` é executado
- Environment Variables sozinhas não são suficientes!

### Passo 3: Rebuild

Depois de configurar:
```
Services → facial-web → Actions → Rebuild
```

## 🔍 Verificar se Funcionou

### 1. Verificar no Browser

Abra o DevTools (F12) → Network → Faça login

**Deve aparecer:**
```
✅ https://hdt-energy-facial.mqtl34.easypanel.host/api/v1/auth/login
✅ https://hdt-energy-facial.mqtl34.easypanel.host/api/v1/employees
```

**Não deve aparecer:**
```
❌ /api/v1/auth/login (404)
❌ /employees (404)
```

### 2. Verificar no Código

No browser, abra o console e digite:
```javascript
console.log(process.env.NEXT_PUBLIC_API_URL)
```

**Deve mostrar:**
```
https://hdt-energy-facial.mqtl34.easypanel.host/api/v1
```

## 🐛 Troubleshooting

### Problema: API ainda chamando `/employees`

**Solução:**
1. Verifique se Build Args está configurado
2. Faça rebuild completo
3. Limpe cache do browser

### Problema: Variável undefined

**Solução:**
1. Certifique-se que Build Args está configurado
2. Rebuild forçado (sem cache)
3. Verifique se o nome está correto: `NEXT_PUBLIC_API_URL` (com NEXT_PUBLIC_)

### Problema: CORS Error

**Solução:**
1. Atualize CORS no backend:
   ```env
   BACKEND_CORS_ORIGINS=["https://hdt-energy-facial-web.mqtl34.easypanel.host"]
   ```
2. Reinicie o backend

## 📊 Checklist

- [ ] Build Args configurado com `NEXT_PUBLIC_API_URL`
- [ ] Environment Variables configurado
- [ ] Rebuild realizado
- [ ] Browser mostra URL correta no Network
- [ ] Login funcionando
- [ ] API respondendo corretamente
