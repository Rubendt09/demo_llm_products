"""
RAG Service - Carga el catálogo de productos para contexto
"""
import httpx
from typing import List, Dict, Any
from app.config import get_settings

settings = get_settings()


class RAGService:
    """Servicio para Retrieval Augmented Generation"""
    
    def __init__(self):
        self.products_api_url = settings.PRODUCTS_API_URL
        self.catalog_cache: str | None = None
    
    async def load_catalog(self) -> str:
        """
        Carga el catálogo completo de productos para RAG
        Retorna un string formateado para incluir en el System Prompt
        """
        # Si ya está en caché, retornar
        if self.catalog_cache:
            return self.catalog_cache
            
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.products_api_url}/products/summary/catalog")
                response.raise_for_status()
                data = response.json()
                
                # Crear resumen ligero para el contexto
                catalog_text = "CATÁLOGO DE PRODUCTOS DISPONIBLES:\n"
                for product in data.get("catalog", []):
                    catalog_text += f"- {product['id']}: {product['name']} (${product['price']})\n"
                
                self.catalog_cache = catalog_text
                return catalog_text
                
        except Exception as e:
            print(f"⚠️ Error cargando catálogo: {e}")
            return "CATÁLOGO: No disponible en este momento"
    
    def clear_cache(self):
        """Limpia el caché del catálogo"""
        self.catalog_cache = None
