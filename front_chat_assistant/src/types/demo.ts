// --- TIPOS Y CONFIGURACIÓN DEL FRONTEND ---

export interface Product {
  id: string;
  name: string;
  price: number;
  stock: number;
  description: string;
}

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