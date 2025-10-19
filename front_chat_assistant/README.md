# Agente de Pedidos Inteligente - Demo Full Stack

Esta demo ilustra la **"Ingeniería de Prompts y Patrones de Diseño Full Stack con Modelos de Lenguaje (LLMs)"**, mostrando cómo convertir una API tradicional en una **API conversacional**.

## 🎯 Objetivo

Demostrar la integración de LLMs (Gemini) como capa de servicio en arquitecturas Full Stack, implementando:

- **System Prompts** - Control de comportamiento del agente
- **RAG (Retrieval Augmented Generation)** - Contexto de base de datos
- **Tool Calling** - Ejecución de funciones del backend

## 🚀 Setup Rápido

```bash
# 1. Instalar dependencias
npm install

# 2. Configurar API key
cp .env.example .env
# Edita .env y agrega tu Gemini API Key

# 3. Ejecutar demo
npm run dev
```

## 🔑 Obtener API Key

1. Visita [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Crea una nueva API key
3. Agrega `VITE_GEMINI_API_KEY=tu_key` en `.env`

