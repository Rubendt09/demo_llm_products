# API de Productos - Backend para Demo LLM Tool Calling

Backend REST API desarrollado con FastAPI y PostgreSQL para demostrar **Tool Calling** con LLMs (Gemini).

## 🎯 Propósito

Este backend simula un sistema de e-commerce real que el LLM puede consultar mediante **Tool Calling** para obtener información actualizada sobre productos y stock.

## 🏗️ Arquitectura del Sistema Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + TypeScript)                │
│                      http://localhost:5173                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ POST /api/chat
                             │ { message: "¿Hay stock de S001?" }
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│           MICROSERVICIO ORQUESTADOR LLM (FastAPI)               │
│                   http://localhost:8001                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ GET /api/products/{id}/stock
                             │ GET /api/products/search/query
                             │ GET /api/products/{id}
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│        MICROSERVICIO DE PRODUCTOS (FastAPI) ← AQUÍ ESTAMOS      │
│                   http://localhost:8000                         │
│                                                                 │
│  Endpoints REST para gestión de productos:                      │
│  • GET  /api/products                  - Listar todos           │
│  • GET  /api/products/{id}             - Detalle producto       │
│  • GET  /api/products/{id}/stock       - Verificar stock        │
│  • GET  /api/products/search/query     - Buscar productos       │
│  • GET  /api/products/summary/catalog  - Catálogo para RAG      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ SQL Queries
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  POSTGRESQL DATABASE                            │
│                     puerto 5431                                 │
│                                                                 │
│  • Tabla: products                                              │
│  • 39 productos de tecnología                                   │
│  • Datos: ID, nombre, precio, stock, descripción                │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 Rol de Este Microservicio

Este backend es el **Microservicio de Productos** - la fuente de verdad para:

- ✅ **Datos de productos**: Nombre, precio, descripción
- ✅ **Inventario en tiempo real**: Stock disponible
- ✅ **Búsquedas**: Encontrar productos por término
- ✅ **Catálogo RAG**: Resumen ligero para contexto del LLM

**No maneja:**
- ❌ Lógica de conversación con LLMs (eso es el orquestador)
- ❌ Llamadas a Gemini API (eso es el orquestador)
- ❌ Interfaz de usuario (eso es el frontend)

## 📋 Endpoints Implementados

### 1. **GET** `/api/products`
Lista todos los productos disponibles.

**Respuesta:**
```json
[
  {
    "id": "S001",
    "name": "Silla Ergonómica Pro",
    "description": "Silla de oficina con soporte lumbar...",
    "price": 299.99,
    "stock": 15
  }
]
```

### 2. **GET** `/api/products/{product_id}`
Obtiene detalles de un producto específico.

**Ejemplo:** `GET /api/products/S001`

### 3. **GET** `/api/products/{product_id}/stock` 🔧 Tool Calling
**Verifica stock en tiempo real** - Este es el endpoint que el LLM llamará.

**Ejemplo:** `GET /api/products/S001/stock`

**Respuesta:**
```json
{
  "product_id": "S001",
  "product_name": "Silla Ergonómica Pro",
  "stock": 15,
  "status": "Disponible"
}
```

### 4. **GET** `/api/products/{product_id}/pricing` 🔧 Tool Calling
**Consulta precio actual** - Otro endpoint para Tool Calling.

**Ejemplo:** `GET /api/products/T010/pricing`

**Respuesta:**
```json
{
  "product_id": "T010",
  "price": 99.99,
  "currency": "USD"
}
```

## 🚀 Instalación y Uso

### Opción 1: Con Docker (Recomendado)

```bash
# Levantar servicios (PostgreSQL + FastAPI)
docker-compose up -d

# Ver logs
docker-compose logs -f api-fastapi

# Inicializar base de datos con datos de demo
docker-compose exec api-fastapi python init_db.py

# Detener servicios
docker-compose down
```

### Opción 2: Local (Sin Docker)

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Asegurarte de que PostgreSQL está corriendo (puerto 5431)
# Puedes usar solo el contenedor de PostgreSQL:
docker-compose up db-postgres -d

# 4. Inicializar base de datos
python init_db.py

# 5. Ejecutar servidor
uvicorn app.main:app --reload --port 8000
```

## 📊 Datos de Demo

El sistema viene pre-cargado con 3 productos:

| ID   | Producto                | Precio  | Stock |
|------|-------------------------|---------|-------|
| S001 | Silla Ergonómica Pro    | $299.99 | 15    |
| M005 | Monitor 4K Curvo        | $549.99 | 0     |
| T010 | Teclado Mecánico RGB    | $99.99  | 40    |

## 🔍 Probar la API

### 1. Documentación Interactiva (Swagger)
Abre en tu navegador: http://localhost:8000/docs

### 2. Con curl

```bash
# Listar productos
curl http://localhost:8000/api/products

# Verificar stock (Tool Calling)
curl http://localhost:8000/api/products/S001/stock

# Consultar precio (Tool Calling)
curl http://localhost:8000/api/products/T010/pricing
```

### 3. Con Python

```python
import requests

# Verificar stock
response = requests.get("http://localhost:8000/api/products/S001/stock")
print(response.json())
# {"product_id": "S001", "product_name": "Silla...", "stock": 15, "status": "Disponible"}
```

## 🛠️ Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para PostgreSQL
- **Pydantic**: Validación de datos
- **PostgreSQL**: Base de datos relacional
- **Docker**: Contenedorización

## ⚡ Tips de Desarrollo

```bash
# Ver logs en tiempo real
docker-compose logs -f api-fastapi

# Reiniciar solo la API
docker-compose restart api-fastapi

# Acceder a la base de datos
docker-compose exec db-postgres psql -U RubenDev -d bd_demo -p 5431

# Ver productos en la DB
docker-compose exec db-postgres psql -U RubenDev -d bd_demo -p 5431 -c "SELECT * FROM products;"
```


