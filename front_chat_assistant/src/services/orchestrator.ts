/**
 * Servicio para comunicarse con el microservicio orquestador LLM
 */

const ORCHESTRATOR_URL = import.meta.env.VITE_ORCHESTRATOR_URL || 'http://localhost:8001';

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}

export interface ChatRequest {
  message: string;
  conversation_history: Message[];
}

export interface FunctionCall {
  name: string;
  args: Record<string, any>;
  result: any;
}

export interface ChatResponse {
  response: string;
  functions_called?: FunctionCall[];
  tokens_used?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

/**
 * Envía un mensaje al orquestador LLM
 */
export async function sendMessage(
  message: string,
  conversationHistory: Message[]
): Promise<ChatResponse> {
  try {
    const response = await fetch(`${ORCHESTRATOR_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        conversation_history: conversationHistory
      } as ChatRequest)
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Error del orquestador: ${response.status} - ${errorText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error llamando al orquestador:', error);
    throw error;
  }
}

/**
 * Reinicia la conversación (limpia caché)
 */
export async function resetConversation(): Promise<void> {
  try {
    const response = await fetch(`${ORCHESTRATOR_URL}/api/chat/reset`, {
      method: 'POST'
    });

    if (!response.ok) {
      throw new Error(`Error reseteando conversación: ${response.status}`);
    }
  } catch (error) {
    console.error('Error reseteando conversación:', error);
    throw error;
  }
}

/**
 * Verifica el estado del orquestador
 */
export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${ORCHESTRATOR_URL}/health`);
    const data = await response.json();
    return data.status === 'healthy';
  } catch (error) {
    console.error('Error verificando salud del orquestador:', error);
    return false;
  }
}
