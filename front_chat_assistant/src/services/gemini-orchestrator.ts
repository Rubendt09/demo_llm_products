import { API_CONFIG, TOOL_SCHEMAS, type Message } from '../types/demo';
import { verificar_stock, buscar_productos, consultar_precio, getCatalogSummary } from './backend';

/**
 * ORQUESTADOR FULL STACK CON RAG HÍBRIDO + TOOL CALLING
 * 
 * Estrategia:
 * 1. RAG: Carga catálogo completo UNA VEZ en el System Prompt (solo nombres + precios)
 * 2. Tool Calling: Llama funciones SOLO cuando se necesitan datos en tiempo real
 * 
 * Esto optimiza tokens y reduce costos vs enviar 39 productos completos cada vez
 */
export class GeminiOrchestrator {
  private apiKey: string;
  private catalogSummary: string | null = null;

  constructor(apiKey: string) {
    this.apiKey = apiKey;
  }

  /**
   * Carga el catálogo de productos UNA VEZ para RAG
   */
  async initializeCatalog() {
    if (!this.catalogSummary) {
      console.log('📚 Cargando catálogo para RAG...');
      this.catalogSummary = await getCatalogSummary();
      console.log('✅ Catálogo cargado para contexto');
    }
  }

  /**
   * System Prompt con RAG integrado
   */
  private getSystemInstruction(): string {
    return `
Eres un Agente de Soporte de Pedidos de una tienda de tecnología.
Tu propósito es asistir al cliente respondiendo preguntas sobre nuestros productos y su inventario.
Siempre mantente profesional y amigable.

CATÁLOGO DE PRODUCTOS DISPONIBLES (para referencia):
${this.catalogSummary || 'Cargando catálogo...'}

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
    `;
  }

  /**
   * Construye el contexto de la conversación
   */
  private formatConversationHistory(messages: Message[]) {
    return messages.map(msg => ({ 
      role: msg.sender === 'user' ? 'user' : 'model', 
      parts: [{ text: msg.text }] 
    }));
  }

  /**
   * Ejecuta las funciones del backend (Tool Calling)
   */
  private async executeFunction(functionName: string, args: Record<string, any>): Promise<any> {
    // Limpiar el prefijo "default_api:" si existe
    const cleanFunctionName = functionName.replace('default_api:', '');
    console.log(`🔧 Ejecutando función: ${cleanFunctionName}`, args);
    
    try {
      switch (cleanFunctionName) {
        case 'verificar_stock':
          return await verificar_stock(args.product_id);
        
        case 'buscar_productos':
          const results = await buscar_productos(args.query, args.limit || 5);
          return {
            query: args.query,
            total_encontrados: results.length,
            productos: results.map(p => ({
              id: p.id,
              name: p.name,
              price: p.price,
              stock: p.stock
            }))
          };
        
        case 'consultar_precio':
          return await consultar_precio(args.product_id);
        
        default:
          return { error: `Función ${cleanFunctionName} no encontrada` };
      }
    } catch (error) {
      console.error(`Error ejecutando ${cleanFunctionName}:`, error);
      return { error: `Error al ejecutar ${cleanFunctionName}` };
    }
  }

  /**
   * Maneja Tool Calling con soporte para llamadas encadenadas (recursive)
   * El LLM puede decidir llamar múltiples funciones antes de responder
   */
  private async handleToolCalling(
    functionCall: any, 
    originalContents: any[],
    maxRecursion: number = 5
  ): Promise<string> {
    // 1. Ejecutar la función del backend
    const functionResult = await this.executeFunction(
      functionCall.name,
      functionCall.args
    );
    
    console.log('✅ Resultado de la función:', functionResult);
    
    // 2. Construir nuevo contenido con el resultado
    const updatedContents = [
      ...originalContents,
      { 
        role: 'model', 
        parts: [{ functionCall }] 
      },
      { 
        role: 'function', 
        parts: [{ 
          functionResponse: { 
            name: functionCall.name, 
            response: functionResult 
          } 
        }] 
      }
    ];
    
    // 3. Llamada al LLM con tools disponibles (puede llamar más funciones)
    const toolResponsePayload = {
      contents: updatedContents,
      systemInstruction: { parts: [{ text: this.getSystemInstruction() }] },
      tools: [{ functionDeclarations: TOOL_SCHEMAS }], // ⚠️ Incluir tools para permitir más llamadas
      generationConfig: {
        temperature: 0.7,
        maxOutputTokens: 1000,
      }
    };

    const toolResponse = await fetch(`${API_CONFIG.API_URL}?key=${this.apiKey}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(toolResponsePayload)
    });
    
    if (!toolResponse.ok) {
      const errorText = await toolResponse.text();
      console.error('❌ Error en Tool Response:', errorText);
      throw new Error(`Tool response failed: ${toolResponse.status}`);
    }

    const result = await toolResponse.json();
    console.log('🔍 Respuesta completa del LLM después de Tool Calling:', JSON.stringify(result, null, 2));
    
    const candidate = result.candidates?.[0];
    if (!candidate) {
      console.error('❌ No se encontró candidate en la respuesta');
      return "Lo siento, no pude procesar la respuesta del Tool Calling.";
    }
    
    // 4. ¿El LLM decidió llamar OTRA función? (Recursive Function Calling)
    const nextFunctionCall = candidate.content?.parts?.find((part: any) => part.functionCall)?.functionCall;
    
    if (nextFunctionCall) {
      if (maxRecursion <= 0) {
        console.warn('⚠️ Máximo de llamadas encadenadas alcanzado');
        return "He recopilado la información necesaria. ¿En qué más puedo ayudarte?";
      }
      
      console.log('🔄 LLM decidió llamar otra función:', nextFunctionCall.name);
      // Recursión: manejar la siguiente llamada
      return this.handleToolCalling(nextFunctionCall, updatedContents, maxRecursion - 1);
    }
    
    // 5. Finalmente tenemos una respuesta de texto
    const textPart = candidate.content?.parts?.find((part: any) => part.text);
    if (!textPart || !textPart.text) {
      console.error('❌ No se encontró texto en la respuesta:', candidate);
      return "Lo siento, no pude generar una respuesta con la información obtenida.";
    }
    
    return textPart.text;
  }

  /**
   * Llamada principal al API de Gemini con retry logic
   */
  async generateResponse(
    conversationHistory: Message[], 
    query: string, 
    attempt: number = 1
  ): Promise<string> {
    // Asegurar que el catálogo está cargado
    await this.initializeCatalog();
    
    try {
      // 1. Preparar el historial de conversación
      const formattedHistory = this.formatConversationHistory(conversationHistory);
      
      // 2. Construir el contenido con la pregunta del usuario
      const contents = [
        ...formattedHistory,
        { role: 'user', parts: [{ text: query }] }
      ];

      // 3. Preparar el payload con RAG + Tool Schemas
      const payload = {
        contents,
        systemInstruction: { parts: [{ text: this.getSystemInstruction() }] },
        // Herramientas disponibles para Tool Calling
        tools: [{ functionDeclarations: TOOL_SCHEMAS }],
        generationConfig: {
          temperature: 0.7,
          maxOutputTokens: 1000,
        }
      };
      
      // 4. Primera llamada al LLM
      const response = await fetch(`${API_CONFIG.API_URL}?key=${this.apiKey}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API request failed: ${response.status} - ${errorText}`);
      }

      const result = await response.json();
      const candidate = result.candidates?.[0];
      
      if (!candidate) {
        throw new Error('No candidate response received');
      }
      
      // 5. ¿El LLM decidió usar Tool Calling?
      if (candidate.content?.parts?.[0]?.functionCall) {
        const functionCall = candidate.content.parts[0].functionCall;
        console.log('🎯 LLM decidió llamar:', functionCall.name);
        return await this.handleToolCalling(functionCall, contents);
      }

      // 6. Respuesta directa (sin Tool Calling)
      return candidate.content?.parts[0]?.text || "No pude generar una respuesta.";

    } catch (error) {
      console.error(`Attempt ${attempt} failed:`, error);
      
      // 7. Retry logic con Exponential Backoff
      if (attempt < API_CONFIG.MAX_RETRIES) {
        const delay = Math.pow(2, attempt) * 1000;
        await new Promise(resolve => setTimeout(resolve, delay));
        return this.generateResponse(conversationHistory, query, attempt + 1);
      }
      
      return `Lo siento, hubo un error al contactar al Agente Inteligente: ${error instanceof Error ? error.message : 'Error desconocido'}. Intenta de nuevo más tarde.`;
    }
  }
}