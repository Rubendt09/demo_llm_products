"""
Modelos Pydantic para el chat
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class Message(BaseModel):
    """Modelo de mensaje en la conversación"""
    role: str = Field(..., description="Rol: 'user' o 'assistant'")
    content: str = Field(..., description="Contenido del mensaje")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)


class ChatRequest(BaseModel):
    """Request para el endpoint de chat"""
    message: str = Field(..., description="Mensaje del usuario", min_length=1)
    conversation_history: List[Message] = Field(
        default_factory=list,
        description="Historial de conversación previo"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "¿Hay stock del producto S001?",
                "conversation_history": [
                    {
                        "role": "user",
                        "content": "Hola"
                    },
                    {
                        "role": "assistant",
                        "content": "¡Hola! Soy tu agente de soporte..."
                    }
                ]
            }
        }


class ChatResponse(BaseModel):
    """Response del endpoint de chat"""
    response: str = Field(..., description="Respuesta del asistente")
    functions_called: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Funciones ejecutadas durante la respuesta"
    )
    tokens_used: Optional[Dict[str, int]] = Field(
        default=None,
        description="Tokens utilizados en la llamada"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "Sí, el producto S001 tiene 15 unidades disponibles.",
                "functions_called": [
                    {
                        "name": "verificar_stock",
                        "args": {"product_id": "S001"},
                        "result": {"stock": 15, "status": "Disponible"}
                    }
                ],
                "tokens_used": {
                    "prompt_tokens": 1200,
                    "completion_tokens": 50,
                    "total_tokens": 1250
                }
            }
        }
