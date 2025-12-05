"""
Tool Schemas para Gemini Function Calling
Define las funciones que el LLM puede ejecutar
"""

TOOL_SCHEMAS = [
    {
        "name": "verificar_stock",
        "description": "Verifica la disponibilidad de inventario en tiempo real desde la base de datos para un producto específico.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": "El ID del producto a verificar (ej: S001, M005, T010)"
                }
            },
            "required": ["product_id"]
        }
    },
    {
        "name": "buscar_productos",
        "description": "Busca productos por término de búsqueda. Retorna máximo 5 resultados relevantes.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Término de búsqueda (ej: 'gaming', 'laptop', 'monitor')"
                },
                "limit": {
                    "type": "number",
                    "description": "Número máximo de resultados (default: 5, max: 5)",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "consultar_precio",
        "description": "Obtiene el precio actualizado de un producto específico desde la base de datos.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": "El ID del producto (ej: S001, M005, T010)"
                }
            },
            "required": ["product_id"]
        }
    }
]
