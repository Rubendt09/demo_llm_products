from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.routers import products
from app.database import engine, Base

# Cargar variables de entorno
load_dotenv()

# Crear todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de Productos",
    description="API REST para gestión de productos e inventario",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir peticiones desde el frontend
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(products.router)


@app.get("/")
def root():
    """
    Endpoint raíz - Health check
    """
    return {
        "message": "API de Productos",
        "status": "active",
        "docs": "/docs",
        "endpoints": {
            "products": "/api/products",
            "stock": "/api/products/{product_id}/stock",
            "pricing": "/api/products/{product_id}/pricing"
        }
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint para monitoreo
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True
    )