
# 🤖 Agente Conversacional Full Stack: Orquestación de LLMs con Tool Calling

Este proyecto es una demostración práctica de cómo integrar **Modelos de Lenguaje Grandes (LLMs)** como una capa de servicio en una arquitectura **Full Stack moderna**.  
El objetivo es transformar una **API tradicional** en un **agente conversacional inteligente**.

---

## 🎯 Conceptos Clave Demostrados

### 🧠 Servicio Orquestador (Backend)
El **Backend con FastAPI** centraliza la lógica de IA, asegurando que las **API Keys estén protegidas** y manejando de forma segura la interacción con el LLM.

### 🧩 Tool Calling
El **LLM puede “llamar” funciones** expuestas por el Backend (por ejemplo: `/products/list`) para ejecutar acciones o recuperar datos en tiempo real.

### 📚 RAG (Retrieval-Augmented Generation)
El modelo **inyecta datos desde PostgreSQL** en su contexto antes de generar respuestas, evitando **alucinaciones** y mejorando la precisión contextual.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Propósito |
|-------------|-------------|------------|
| **Frontend** | React, Vite, Tailwind CSS | Interfaz conversacional y experiencia de usuario. |
| **Backend** | FastAPI (Python) | Servicio Orquestador, Tool Calling y capa de API. |
| **Base de Datos** | PostgreSQL | Almacenamiento de datos de negocio (ej. productos, pedidos). |
| **Inteligencia** | Gemini / OpenAI (a través de FastAPI) | Generación de lenguaje natural y enrutamiento de funciones. |

---

## 🔁 Flujo Principal

El **Frontend nunca llama directamente a la IA**.  
Toda la comunicación se enruta a través de **FastAPI**, garantizando **seguridad y control total** sobre la lógica de negocio y el contexto.

```

Usuario ➡️ Frontend (React)
Frontend ➡️ Backend (FastAPI)
FastAPI (Orquestador) ➡️ LLM (Tool Calling / RAG)
LLM ➡️ FastAPI (con instrucciones de Tool Calling o respuesta final)
FastAPI ↔️ PostgreSQL (si Tool Calling requiere datos)
FastAPI ➡️ Frontend (Respuesta final)

```

---

## 🧩 Beneficios de la Arquitectura

- 🔒 **Seguridad total**: las claves de API y lógica sensible se mantienen en el servidor.  
- 🧠 **Respuestas más precisas** gracias a RAG.  
- ⚙️ **Escalabilidad modular**: fácil de integrar con nuevos servicios o endpoints.  
- 🗣️ **Experiencia natural**: el usuario interactúa con la app como si fuera un asistente humano.



