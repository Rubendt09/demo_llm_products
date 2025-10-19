"""
Tool Executor - Ejecuta las funciones llamadas por el LLM
Conecta con el microservicio de productos
"""
import httpx
from typing import Dict, Any
from app.config import get_settings

settings = get_settings()


class ToolExecutor:
    """Ejecutor de herramientas para Tool Calling"""
    
    def __init__(self):
        self.products_api_url = settings.PRODUCTS_API_URL
        self.client = httpx.AsyncClient(timeout=10.0)
        self.execution_log: list[Dict[str, Any]] = []
    
    async def execute(self, function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta una función basada en su nombre
        
        Args:
            function_name: Nombre de la función a ejecutar
            arguments: Argumentos para la función
            
        Returns:
            Resultado de la ejecución de la función
        """
        # Limpiar prefijo si existe (default_api:verificar_stock -> verificar_stock)
        clean_name = function_name.split(":")[-1]
        
        print(f"🔧 Ejecutando función: {clean_name} con args: {arguments}")
        
        try:
            result = None
            
            if clean_name == "verificar_stock":
                result = await self._verificar_stock(arguments["product_id"])
            
            elif clean_name == "buscar_productos":
                query = arguments["query"]
                limit = arguments.get("limit", 5)
                result = await self._buscar_productos(query, limit)
            
            elif clean_name == "consultar_precio":
                result = await self._consultar_precio(arguments["product_id"])
            
            else:
                result = {"error": f"Función {clean_name} no encontrada"}
            
            # Registrar ejecución
            self.execution_log.append({
                "name": clean_name,
                "args": arguments,
                "result": result
            })
            
            print(f"✅ Resultado: {result}")
            return result
                
        except Exception as e:
            error_result = {"error": f"Error ejecutando {clean_name}: {str(e)}"}
            print(f"❌ Error: {error_result}")
            return error_result
    
    async def _verificar_stock(self, product_id: str) -> Dict[str, Any]:
        """Verifica stock de un producto"""
        try:
            response = await self.client.get(
                f"{self.products_api_url}/products/{product_id}/stock"
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": f"Error al verificar stock: {str(e)}", "product_id": product_id}
    
    async def _buscar_productos(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """Busca productos por término"""
        try:
            response = await self.client.get(
                f"{self.products_api_url}/products/search/query",
                params={"query": query, "limit": limit}
            )
            response.raise_for_status()
            results = response.json()
            
            # Formatear para el LLM
            return {
                "query": query,
                "total_encontrados": len(results),
                "productos": [
                    {
                        "id": p["id"],
                        "name": p["name"],
                        "price": p["price"],
                        "stock": p["stock"]
                    }
                    for p in results
                ]
            }
        except httpx.HTTPError as e:
            return {"error": f"Error al buscar productos: {str(e)}"}
    
    async def _consultar_precio(self, product_id: str) -> Dict[str, Any]:
        """Consulta precio de un producto"""
        try:
            response = await self.client.get(
                f"{self.products_api_url}/products/{product_id}"
            )
            response.raise_for_status()
            data = response.json()
            return {
                "product_id": product_id,
                "price": data["price"],
                "currency": "USD"
            }
        except httpx.HTTPError as e:
            return {"error": f"Error al consultar precio: {str(e)}", "product_id": product_id}
    
    def get_execution_log(self) -> list[Dict[str, Any]]:
        """Retorna el log de ejecuciones"""
        return self.execution_log
    
    def clear_log(self):
        """Limpia el log de ejecuciones"""
        self.execution_log = []
    
    async def close(self):
        """Cierra el cliente HTTP"""
        await self.client.aclose()
