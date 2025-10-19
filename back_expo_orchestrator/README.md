# Microservicio Orquestador LLM

Microservicio FastAPI que actúa como cerebro central del sistema, orquestando conversaciones inteligentes con **Gemini** usando **RAG** (Retrieval-Augmented Generation) y **Tool Calling**.

## � Propósito

El orquestador es el **intermediario inteligente** entre el frontend (React) y el backend de productos (FastAPI + PostgreSQL). Su función es:

- **Recibir** mensajes del usuario desde el frontend
- **Decidir** qué información necesita del backend usando IA
- **Ejecutar** llamadas a funciones automáticamente (Tool Calling)
- **Generar** respuestas conversacionales naturales

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + TypeScript)                │
│                      http://localhost:5173                      │
│                                                                 │
│  • Interfaz de chat                                             │
│  • Captura mensajes del usuario                                 │
│  • Renderiza respuestas del bot                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ POST /api/chat
                             │ { 
                             │   "message": "¿Hay stock de S001?",
                             │   "conversation_history": [...]
                             │ }
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│         MICROSERVICIO ORQUESTADOR LLM (FastAPI) ← AQUÍ          │
│                   http://localhost:8001                         │
│                                                                 │
│  🧠 PROCESAMIENTO INTELIGENTE:                                  │
│  1. RAG: Carga catálogo de productos                            │
│  2. System Prompt: Define comportamiento del agente             │
│  3. Gemini API: Procesa mensaje + decide Tool Calling           │
│  4. Tool Executor: Ejecuta funciones si es necesario            │
│  5. Response: Genera respuesta conversacional                   │ 
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Tool Calling (cuando es necesario)
                             │ GET /api/products/{id}/stock
                             │ GET /api/products/search/query
                             │ GET /api/products/{id}
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│        MICROSERVICIO DE PRODUCTOS (FastAPI)                     │
│                   http://localhost:8000                         │
│                                                                 │
│  • Gestión de productos y stock                                 │
│  • Base de datos PostgreSQL                                     │
│  • APIs REST para consultas                                     │
└─────────────────────────────────────────────────────────────────┘
                             ▲
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GEMINI API (Google Cloud)                    │
│              https://generativelanguage.googleapis.com          │
│                                                                 │
│  • Procesamiento de lenguaje natural                            │
│  • Tool Calling (decisión automática de llamar funciones)       │
│  • Generación de respuestas conversacionales                    │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Cómo Levantar el Servicio

### Opción 1: Docker (Recomendado)

```bash
# Navegar al directorio
cd back_expo_orchestrator

# Construir imagen
docker build -t llm-orchestrator .

# Ejecutar contenedor
docker run -p 8001:8001 --env-file .env llm-orchestrator
```

### Opción 2: Localmente

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

## 🛠️ Estructura del Proyecto

```
app/
├── main.py                    # 🚀 FastAPI app principal + CORS
├── config.py                  # ⚙️ Configuración (API keys, URLs)
│
├── models/
│   └── chat.py               # 📝 Modelos: ChatRequest, ChatResponse
│
├── routers/
│   └── chat.py               # 🌐 Endpoints: POST /api/chat
│
├── services/                  # 🧠 SERVICIOS CORE
│   ├── gemini_service.py     # 🤖 Lógica de Gemini + RAG
│   ├── tool_executor.py      # 🔧 Ejecutor de Tool Calling
│   └── rag_service.py        # 📚 Carga catálogo para contexto
│
└── schemas/
    └── tools.py              # 🛠️ Tool Schemas (definición de funciones)
```

## 🤖 Funcionamiento del LLM (Gemini)

### 1. **System Prompt + RAG Context**
```
System Instruction = Base Prompt + Catálogo de Productos
```

- **Base Prompt**: Define que es un "Agente de Soporte de Pedidos"
- **RAG Context**: Inyecta lista de productos disponibles (S001: Silla $299, T010: Teclado $99...)
- **Restricciones**: Solo habla de tecnología, nunca inventa precios/stock

### 2. **Procesamiento del Mensaje**
```
Usuario: "¿Hay stock del mouse M001?"
   ↓
Gemini analiza: "Necesito verificar stock en tiempo real"
   ↓
Gemini genera: functionCall("verificar_stock", {"product_id": "M001"})
```

### 3. **Respuesta Final**
```
Tool Result: {"stock": 50, "status": "available"}
   ↓
Gemini genera: "El Mouse Inalámbrico Gamer (M001) tiene 50 unidades disponibles."
```

## � Funcionamiento del Tool Calling

### **Tool Schemas Disponibles:**

1. **`verificar_stock(product_id)`**
   - Verifica inventario en tiempo real
   - Llama: `GET /api/products/{id}/stock`

2. **`buscar_productos(query, limit=5)`**
   - Busca productos por término
   - Llama: `GET /api/products/search/query`

3. **`consultar_precio(product_id)`**
   - Obtiene precio actualizado
   - Llama: `GET /api/products/{id}`

### **Flujo de Tool Calling:**

```
1. LLM decide: "Necesito llamar una función"
   ↓
2. Orquestador ejecuta: await tool_executor.execute()
   ↓
3. HTTP Request al backend de productos
   ↓
4. Resultado vuelve al LLM
   ↓
5. LLM puede decidir llamar OTRA función (recursive calling)
   ↓
6. Finalmente genera respuesta en lenguaje natural
```

## 🔗 Relación con Otros Servicios

### **Frontend → Orquestador**
- **Protocolo**: HTTP REST
- **Endpoint**: `POST /api/chat`
- **Datos**: Mensaje + historial de conversación
- **Respuesta**: Texto + metadata (funciones llamadas, tokens usados)

### **Orquestador → Backend Productos**
- **Protocolo**: HTTP REST
- **Endpoints**: `/api/products/*` (stock, search, pricing)
- **Propósito**: Tool Calling automático según decisiones del LLM
- **Datos**: IDs de productos, términos de búsqueda

### **Orquestador → Gemini API**
- **Protocolo**: HTTPS REST
- **Endpoint**: `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview:generateContent`
- **Datos**: System Prompt + Tool Schemas + Conversación
- **Respuesta**: Texto OR functionCall

## 📊 Tipos de Respuesta

### **Respuesta Directa (Sin Tool Calling)**
```json
{
  "response": "Vendemos sillas ergonómicas, teclados mecánicos, monitores...",
  "functions_called": null,
  "tokens_used": {"total_tokens": 1200}
}
```

### **Respuesta con Tool Calling**
```json
{
  "response": "El Mouse M001 tiene 50 unidades disponibles.",
  "functions_called": [
    {
      "name": "verificar_stock",
      "args": {"product_id": "M001"},
      "result": {"stock": 50, "status": "available"}
    }
  ],
  "tokens_used": {"total_tokens": 1800}
}
```

## � Tecnologías Utilizadas

### **Backend Framework**
- **FastAPI**: Web framework asíncrono para APIs REST
- **Uvicorn**: Servidor ASGI de alta performance
- **Pydantic**: Validación de datos y serialización

### **LLM Integration**
- **Gemini 2.5 Flash Preview**: Modelo de Google para conversación + Tool Calling
- **httpx**: Cliente HTTP asíncrono para llamadas a APIs

### **Arquitectura**
- **RAG (Retrieval-Augmented Generation)**: Contexto de productos
- **Tool Calling**: Ejecución automática de funciones
- **Microservicios**: Separación de responsabilidades

### **Deployment**
- **Docker**: Containerización del servicio
- **Environment Variables**: Configuración segura (API keys)

## � Endpoints Principales

| Endpoint | Método | Propósito |
|----------|--------|-----------|
| `/api/chat` | POST | Conversación principal con el LLM |
| `/api/chat/reset` | POST | Reiniciar contexto de conversación |
| `/api/chat/health` | GET | Health check del servicio |
| `/health` | GET | Health check general |
| `/docs` | GET | Documentación Swagger UI |

## 🧪 Testing Rápido

```bash
# Health check
curl http://localhost:8001/health

# Mensaje simple
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Qué productos tienes?"}'

# Mensaje que requiere Tool Calling
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Hay stock del producto S001?"}'
```
