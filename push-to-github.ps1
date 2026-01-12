# Script para fazer push do projeto para o GitHub
# Execute este script no diretório do projeto (facial)

Write-Host "🚀 Configurando Git e fazendo push para GitHub..." -ForegroundColor Green

# Remove repositório Git do home se existir
if (Test-Path "$HOME\.git") {
    Write-Host "⚠️  Removendo repositório Git do diretório home..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "$HOME\.git" -ErrorAction SilentlyContinue
}

# Verifica se estamos no diretório correto
if (-not (Test-Path "backend") -or -not (Test-Path "frontend-web") -or -not (Test-Path "mobile-app")) {
    Write-Host "❌ Erro: Execute este script no diretório do projeto (facial)" -ForegroundColor Red
    Write-Host "   Diretório atual: $(Get-Location)" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Diretório correto detectado!" -ForegroundColor Green

# Remove .git se já existir
if (Test-Path ".git") {
    Write-Host "⚠️  Removendo repositório Git existente..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force .git
}

# Inicializa Git
Write-Host "📦 Inicializando repositório Git..." -ForegroundColor Cyan
git init

# Adiciona remote
Write-Host "🔗 Configurando remote do GitHub..." -ForegroundColor Cyan
git remote remove origin -ErrorAction SilentlyContinue
git remote add origin https://github.com/Caique-Santos-Barbosa/facial.git

# Adiciona apenas arquivos do projeto (ignora .gradle e outros)
Write-Host "📝 Adicionando arquivos do projeto..." -ForegroundColor Cyan
git add backend/ frontend-web/ mobile-app/ *.md *.gitignore *.ps1 -f

# Commit
Write-Host "💾 Criando commit..." -ForegroundColor Cyan
git commit -m "Initial commit: Sistema de Reconhecimento Facial HDT Energy"

# Renomeia branch
Write-Host "🌿 Configurando branch main..." -ForegroundColor Cyan
git branch -M main

# Push
Write-Host "⬆️  Fazendo push para GitHub..." -ForegroundColor Cyan
Write-Host "   (Você precisará autenticar com seu Personal Access Token)" -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Push realizado com sucesso!" -ForegroundColor Green
    Write-Host "🌐 Acesse: https://github.com/Caique-Santos-Barbosa/facial" -ForegroundColor Cyan
} else {
    Write-Host "❌ Erro ao fazer push. Verifique suas credenciais." -ForegroundColor Red
    Write-Host "   Você precisa usar um Personal Access Token, não sua senha." -ForegroundColor Yellow
}
