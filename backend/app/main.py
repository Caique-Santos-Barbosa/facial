from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database import engine, Base
from app.api.endpoints import auth, employees, recognition, access_control
import os

# Cria tabelas
Base.metadata.create_all(bind=engine)

# Cria diretórios necessários
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.FACES_DIR, exist_ok=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Routers
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["authentication"]
)

app.include_router(
    employees.router,
    prefix=f"{settings.API_V1_STR}/employees",
    tags=["employees"]
)

app.include_router(
    recognition.router,
    prefix=f"{settings.API_V1_STR}/recognition",
    tags=["recognition"]
)

app.include_router(
    access_control.router,
    prefix=f"{settings.API_V1_STR}/access",
    tags=["access-control"]
)

@app.get("/")
def read_root():
    return {
        "message": "HDT Energy - Sistema de Reconhecimento Facial",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

