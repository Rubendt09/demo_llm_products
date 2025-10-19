"""
Microservicio Orquestador LLM
Maneja conversaciones con Gemini y Tool Calling
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.routers import chat
from app.config import get_settings

# Cargar variables de entorno
load_dotenv()

# Obtener configuración
settings = get_settings()

# Crear la aplicación FastAPI
app = FastAPI(
    title="LLM Orchestrator - Microservicio de Chat",
    description="Orquestador de conversaciones con Gemini usando RAG + Tool Calling",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
cors_origins = settings.CORS_ORIGINS.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(chat.router)


@app.get("/")
def root():
    """
    Endpoint raíz - Información del servicio
    """
    return {
        "service": "LLM Orchestrator",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs",
        "endpoints": {
            "chat": "POST /api/chat",
            "reset": "POST /api/chat/reset",
            "health": "GET /api/chat/health"
        }
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "LLM Orchestrator"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )
