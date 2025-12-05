"""
Router de Chat - Endpoint para conversación con el LLM
"""
from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.services.gemini_service import GeminiService

router = APIRouter(
    prefix="/api",
    tags=["chat"]
)

# Instancia global del servicio de Gemini
gemini_service = GeminiService()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Endpoint principal de chat con el LLM
    
    - **message**: Mensaje del usuario
    - **conversation_history**: Historial de conversación previo (opcional)
    
    Returns:
        Respuesta del asistente con metadata de funciones llamadas y tokens usados
    """
    try:
        # Convertir historial al formato correcto
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in request.conversation_history
        ]
        
        # Generar respuesta
        result = await gemini_service.generate_response(
            user_message=request.message,
            conversation_history=history
        )
        
        return ChatResponse(
            response=result["response"],
            functions_called=result.get("functions_called"),
            tokens_used=result.get("tokens_used")
        )
        
    except Exception as e:
        print(f"❌ Error en /api/chat: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generando respuesta: {str(e)}"
        )


@router.post("/chat/reset")
async def reset_conversation():
    """
    Reinicia el contexto de la conversación
    Limpia cachés y logs
    """
    try:
        gemini_service.rag_service.clear_cache()
        gemini_service.tool_executor.clear_log()
        gemini_service.catalog_loaded = False
        
        return {
            "message": "Conversación reiniciada exitosamente",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reiniciando conversación: {str(e)}"
        )


@router.get("/chat/health")
async def health_check():
    """
    Health check del servicio de chat
    """
    return {
        "status": "healthy",
        "service": "LLM Orchestrator",
        "catalog_loaded": gemini_service.catalog_loaded
    }
