// --- CONFIGURACIÓN DE LA DEMO Y DATOS DE PRODUCTO ---

export interface Product {
  id: string;
  name: string;
  price: number;
  stock: number;
  description: string;
}

// Configuración de la API
export const API_CONFIG = {
  API_URL: "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent",
  MAX_RETRIES: 3
};

// Tool Schemas para Gemini - Funciones que el LLM puede llamar
export const TOOL_SCHEMAS = [
  {
    name: "verificar_stock",
    description: "Verifica la disponibilidad de inventario en tiempo real desde la base de datos para un producto específico.",
    parameters: {
      type: "object",
      properties: {
        product_id: {
          type: "string",
          description: "El ID del producto a verificar (ej: S001, M005, T010)"
        }
      },
      required: ["product_id"]
    }
  },
  {
    name: "buscar_productos",
    description: "Busca productos por término de búsqueda. Retorna máximo 5 resultados relevantes. Usa esto en lugar de listar todos los productos.",
    parameters: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "Término de búsqueda (ej: 'gaming', 'laptop', 'monitor', 'mouse')"
        },
        limit: {
          type: "number",
          description: "Número máximo de resultados (default: 5, max: 5)",
          default: 5
        }
      },
      required: ["query"]
    }
  },
  {
    name: "consultar_precio",
    description: "Obtiene el precio actualizado de un producto específico desde la base de datos.",
    parameters: {
      type: "object",
      properties: {
        product_id: {
          type: "string",
          description: "El ID del producto (ej: S001, M005, T010)"
        }
      },
      required: ["product_id"]
    }
  }
];

// Tipos para el chat
export interface Message {
  sender: 'user' | 'bot';
  text: string;
  timestamp?: Date;
}

export interface StockResult {
  product_id: string;
  product_name?: string;
  stock?: number;
  status?: string;
  error?: string;
}