"""
Aplicação principal FastAPI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.config import settings
from app.database import engine, Base
from app.api.endpoints import auth, employees, recognition, access_logs

# Cria diretórios necessários
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.FACES_DIR, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle da aplicação
    """
    # Startup
    print("🚀 Iniciando HDT Energy Facial Recognition System...")
    
    # Cria tabelas no banco
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas do banco de dados criadas/verificadas")
    
    yield
    
    # Shutdown
    print("👋 Encerrando aplicação...")

# Cria aplicação FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve arquivos estáticos (imagens de faces)
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Registra rotas
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["Autenticação"]
)

app.include_router(
    employees.router,
    prefix=f"{settings.API_V1_STR}/employees",
    tags=["Colaboradores"]
)

app.include_router(
    recognition.router,
    prefix=f"{settings.API_V1_STR}/recognition",
    tags=["Reconhecimento Facial"]
)

app.include_router(
    access_logs.router,
    prefix=f"{settings.API_V1_STR}/access-logs",
    tags=["Logs de Acesso"]
)

# Rotas raiz
@app.get("/")
def root():
    """
    Endpoint raiz - informações da API
    """
    return {
        "message": "HDT Energy - Sistema de Reconhecimento Facial",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    """
    Health check para monitoramento
    """
    return {
        "status": "ok",
        "version": settings.VERSION
    }
