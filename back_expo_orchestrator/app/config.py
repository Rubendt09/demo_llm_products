"""
Configuración del microservicio orquestador
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # API Keys
    GEMINI_API_KEY: str
    
    # URLs de Microservicios
    PRODUCTS_API_URL: str = "http://localhost:8000/api"
    
    # Configuración de la API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8001
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:5173"
    
    # Configuración de Gemini
    GEMINI_MODEL: str = "gemini-2.5-flash-preview-09-2025"
    GEMINI_API_URL: str = "https://generativelanguage.googleapis.com/v1beta/models"
    
    # Límites
    MAX_RECURSION_DEPTH: int = 5
    MAX_HISTORY_LENGTH: int = 20
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Obtener configuración singleton"""
    return Settings()
