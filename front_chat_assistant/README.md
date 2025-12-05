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

## 📖 Documentación Completa

Ver [README-DEMO.md](./README-DEMO.md) para casos de uso detallados y arquitectura.

## 🎤 Para la Charla

Esta demo está diseñada para mostrar cómo los LLMs pueden transformar APIs tradicionales en experiencias conversacionales naturales.

**Tema:** "Ingeniería de Prompts y Patrones de Diseño Full Stack con Modelos de Lenguaje"

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
