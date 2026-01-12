from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.endpoints import auth, employees, recognition, access_control

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
def root():
    return {
        "message": "HDT Energy - Sistema de Reconhecimento Facial API",
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_STR}/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

