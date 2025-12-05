"""
Gemini Service - Maneja las llamadas al API de Gemini
Implementa RAG + Tool Calling con recursión
"""
import httpx
from typing import List, Dict, Any, Optional
from app.config import get_settings
from app.schemas.tools import TOOL_SCHEMAS
from app.services.tool_executor import ToolExecutor
from app.services.rag_service import RAGService

settings = get_settings()


class GeminiService:
    """Servicio para interactuar con Gemini API"""
    
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.api_url = f"{settings.GEMINI_API_URL}/{settings.GEMINI_MODEL}:generateContent"
        self.tool_executor = ToolExecutor()
        self.rag_service = RAGService()
        self.catalog_loaded = False
    
    async def initialize(self):
        """Inicializa el servicio cargando el catálogo"""
        if not self.catalog_loaded:
            print("📚 Cargando catálogo para RAG...")
            await self.rag_service.load_catalog()
            self.catalog_loaded = True
            print("✅ Catálogo cargado")
    
    def get_system_instruction(self) -> str:
        """
        Genera el System Prompt con RAG integrado
        """
        catalog = self.rag_service.catalog_cache or "Catálogo no disponible"
        
        return f"""
Eres un Agente de Soporte de Pedidos de una tienda de tecnología.
Tu propósito es asistir al cliente respondiendo preguntas sobre nuestros productos y su inventario.
Siempre mantente profesional y amigable.

{catalog}

IMPORTANTE - USO DE HERRAMIENTAS:
- La lista anterior es SOLO REFERENCIA para conocer qué productos existen
- Para verificar STOCK en tiempo real, SIEMPRE usa la herramienta verificar_stock(product_id)
- Para BUSCAR productos específicos, usa la herramienta buscar_productos(query)
- Para consultar PRECIO actualizado, usa la herramienta consultar_precio(product_id)
- NUNCA inventes stock o precios, siempre usa las herramientas para datos precisos

REGLA CRÍTICA - LLAMADAS A HERRAMIENTAS:
- Si necesitas llamar MÚLTIPLES herramientas para responder (ej: precio Y stock), NO generes texto intermedio
- Llama TODAS las herramientas que necesites PRIMERO
- SOLO responde con texto cuando tengas TODA la información necesaria
- NUNCA digas cosas como "voy a verificar..." o "ahora consultaré..." - simplemente llama las herramientas
- Genera una respuesta completa y final con toda la información recopilada

FORMATO DE RESPUESTAS:
- Usa **texto** solo para enfatizar nombres de productos o información importante
- Mantén las respuestas claras y bien estructuradas
- Si te preguntan sobre temas NO relacionados con tecnología, recuerda amablemente tu rol

RESTRICCIONES:
- Solo respondes sobre productos de tecnología
- No hablas de otros temas (deportes, cocina, etc.)
- Siempre usas las herramientas para datos actualizados
"""
    
    def format_conversation_history(self, messages: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Convierte el historial de mensajes al formato de Gemini
        """
        formatted = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            formatted.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        return formatted
    
    async def generate_response(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Genera una respuesta usando Gemini con Tool Calling
        
        Args:
            user_message: Mensaje del usuario
            conversation_history: Historial de conversación previo
            
        Returns:
            Dict con la respuesta y metadata
        """
        # Asegurar que el catálogo esté cargado
        await self.initialize()
        
        # Limpiar log de ejecuciones previas
        self.tool_executor.clear_log()
        
        # Preparar historial
        history = self.format_conversation_history(conversation_history or [])
        
        # Construir contenido
        contents = [
            *history,
            {"role": "user", "parts": [{"text": user_message}]}
        ]
        
        # Primera llamada a Gemini
        response_text, tokens_used = await self._call_gemini_with_tools(contents)
        
        return {
            "response": response_text,
            "functions_called": self.tool_executor.get_execution_log(),
            "tokens_used": tokens_used
        }
    
    async def _call_gemini_with_tools(
        self,
        contents: List[Dict[str, Any]],
        max_recursion: int = None
    ) -> tuple[str, Dict[str, int]]:
        """
        Llama a Gemini API con soporte para Tool Calling recursivo
        
        Returns:
            Tupla (respuesta_texto, tokens_usados)
        """
        if max_recursion is None:
            max_recursion = settings.MAX_RECURSION_DEPTH
        
        payload = {
            "contents": contents,
            "systemInstruction": {"parts": [{"text": self.get_system_instruction()}]},
            "tools": [{"functionDeclarations": TOOL_SCHEMAS}],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000,
            }
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.api_url}?key={self.api_key}",
                json=payload
            )
            response.raise_for_status()
            result = response.json()
        
        # Extraer metadata de tokens
        tokens_used = result.get("usageMetadata", {})
        tokens_info = {
            "prompt_tokens": tokens_used.get("promptTokenCount", 0),
            "completion_tokens": tokens_used.get("candidatesTokenCount", 0),
            "total_tokens": tokens_used.get("totalTokenCount", 0)
        }
        
        # Obtener candidato
        candidate = result.get("candidates", [{}])[0]
        parts = candidate.get("content", {}).get("parts", [])
        
        # ¿Hay una llamada a función?
        function_call_part = next((p for p in parts if "functionCall" in p), None)
        
        if function_call_part:
            function_call = function_call_part["functionCall"]
            print(f"🎯 LLM decidió llamar: {function_call['name']}")
            
            # Ejecutar la función
            function_result = await self.tool_executor.execute(
                function_call["name"],
                function_call.get("args", {})
            )
            
            # Construir nuevo contenido con el resultado
            updated_contents = [
                *contents,
                {"role": "model", "parts": [{"functionCall": function_call}]},
                {
                    "role": "function",
                    "parts": [{
                        "functionResponse": {
                            "name": function_call["name"],
                            "response": function_result
                        }
                    }]
                }
            ]
            
            # Llamada recursiva si quedan iteraciones
            if max_recursion > 0:
                print(f"🔄 Continuando conversación (recursión restante: {max_recursion})")
                return await self._call_gemini_with_tools(updated_contents, max_recursion - 1)
            else:
                print("⚠️ Máximo de recursiones alcanzado")
                return "He recopilado la información necesaria.", tokens_info
        
        # Respuesta de texto final
        text_part = next((p for p in parts if "text" in p), None)
        if text_part:
            return text_part["text"], tokens_info
        
        return "No pude generar una respuesta.", tokens_info
    
    async def close(self):
        """Cierra conexiones"""
        await self.tool_executor.close()
