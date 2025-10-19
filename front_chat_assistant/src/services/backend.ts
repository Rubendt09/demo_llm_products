import { type Product, type StockResult } from '../types/demo';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

/**
 * Servicio de Backend - Funciones que conectan con la API real
 * Estas funciones son llamadas por el LLM mediante Tool Calling
 */

/**
 * Función que consulta stock en tiempo real desde la base de datos.
 * TOOL CALLING: El LLM llama a esta función cuando necesita verificar inventario
 */
export const verificar_stock = async (product_id: string): Promise<StockResult> => {
  try {
    const response = await fetch(`${API_BASE_URL}/products/${product_id}/stock`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error verificando stock:', error);
    return { 
      error: "No se pudo verificar el stock en este momento", 
      product_id 
    };
  }
};

/**
 * Busca productos por término de búsqueda (limitado a max 5 resultados)
 * TOOL CALLING: El LLM usa esto en lugar de cargar TODOS los productos
 */
export const buscar_productos = async (query: string, limit: number = 5): Promise<Product[]> => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/products/search/query?q=${encodeURIComponent(query)}&limit=${limit}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error buscando productos:', error);
    return [];
  }
};

/**
 * Consulta precio actualizado de un producto
 * TOOL CALLING: Para obtener precios en tiempo real
 */
export const consultar_precio = async (product_id: string) => {
  try {
    const response = await fetch(`${API_BASE_URL}/products/${product_id}/pricing`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error consultando precio:', error);
    return { error: "No se pudo consultar el precio" };
  }
};

/**
 * Obtiene resumen ligero del catálogo para RAG
 * NO ES TOOL CALLING - Se usa para construir el System Prompt
 */
export const getCatalogSummary = async (): Promise<string> => {
  try {
    const response = await fetch(`${API_BASE_URL}/products/summary/catalog`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    
    // Formatear como texto legible para el LLM
    return data.catalog
      .map((p: any) => `${p.id}: ${p.name} - $${p.price}`)
      .join('\n');
      
  } catch (error) {
    console.error('Error obteniendo catálogo:', error);
    return 'Error al cargar catálogo de productos';
  }
};