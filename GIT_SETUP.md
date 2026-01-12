# 🚀 Guia de Setup do Git para GitHub

## ⚠️ Importante

Execute estes comandos **dentro do diretório do projeto** (`facial`).

## 📝 Passos para Fazer Push no GitHub

### 1. Abra o terminal no diretório do projeto

```powershell
cd "C:\Users\CaiqueSantosBarbosaB\OneDrive - CSB Tech Consulting\Área de Trabalho\facial"
```

### 2. Inicialize o Git (se ainda não foi feito)

```bash
git init
```

### 3. Adicione o remote do GitHub

```bash
git remote add origin https://github.com/Caique-Santos-Barbosa/facial.git
```

Se já existir, remova primeiro:
```bash
git remote remove origin
git remote add origin https://github.com/Caique-Santos-Barbosa/facial.git
```

### 4. Adicione os arquivos do projeto

```bash
git add .
```

### 5. Faça o commit inicial

```bash
git commit -m "Initial commit: Sistema de Reconhecimento Facial HDT Energy"
```

### 6. Renomeie a branch para main

```bash
git branch -M main
```

### 7. Faça o push

```bash
git push -u origin main
```

## 🔐 Autenticação

Se pedir credenciais:
- **Usuário:** Seu username do GitHub
- **Senha:** Use um **Personal Access Token** (não sua senha normal)

Para criar um token:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Selecione escopos: `repo`
4. Copie o token e use como senha

## ✅ Verificação

Após o push, acesse:
https://github.com/Caique-Santos-Barbosa/facial

Você deve ver todos os arquivos do projeto!

## 🆘 Problemas Comuns

### Erro: "fatal: not a git repository"
- Certifique-se de estar no diretório correto
- Execute `git init` primeiro

### Erro: "remote origin already exists"
- Execute: `git remote remove origin`
- Depois: `git remote add origin https://github.com/Caique-Santos-Barbosa/facial.git`

### Erro: "filename too long"
- O Windows tem limite de 260 caracteres
- Arquivos em `.gradle/` podem causar isso
- Verifique se o `.gitignore` está ignorando `.gradle/`

### Erro de autenticação
- Use Personal Access Token, não a senha
- Ou configure SSH keys

## 📋 Comandos Completos (Copy & Paste)

```bash
cd "C:\Users\CaiqueSantosBarbosaB\OneDrive - CSB Tech Consulting\Área de Trabalho\facial"
git init
git remote add origin https://github.com/Caique-Santos-Barbosa/facial.git
git add .
git commit -m "Initial commit: Sistema de Reconhecimento Facial HDT Energy"
git branch -M main
git push -u origin main
```
