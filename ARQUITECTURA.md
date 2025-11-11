# Arquitectura del Sistema - Gestión de Cursos e Inscripciones

## 📐 Diagrama de la Arquitectura MVC

```
┌─────────────────────────────────────────────────────────────────────┐
│                          CLIENTE / FRONTEND                          │
│                    (Navegador, Postman, cURL)                        │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ HTTP Requests
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         FASTAPI APPLICATION                          │
│                          (app/main.py)                               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  MIDDLEWARES                                                 │   │
│  │  - CORS (Cross-Origin Resource Sharing)                     │   │
│  │  - Error Handling                                            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  ROUTERS (app/views/)                                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐    │   │
│  │  │ Estudiantes │  │   Cursos    │  │  Inscripciones   │    │   │
│  │  │    View     │  │    View     │  │      View        │    │   │
│  │  └──────┬──────┘  └──────┬──────┘  └────────┬─────────┘    │   │
│  └─────────┼─────────────────┼──────────────────┼──────────────┘   │
└────────────┼─────────────────┼──────────────────┼──────────────────┘
             │                 │                  │
             ▼                 ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    CONTROLLERS (app/controllers/)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐      │
│  │  Estudiante  │  │    Curso     │  │    Inscripcion       │      │
│  │  Controller  │  │  Controller  │  │    Controller        │      │
│  │              │  │              │  │                      │      │
│  │ - CRUD       │  │ - CRUD       │  │ - inscribir()        │      │
│  │ - Validar    │  │ - Validar    │  │ - desinscribir()     │      │
│  │ - Lógica     │  │ - Lógica     │  │ - obtener_cursos()   │      │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘      │
└─────────┼──────────────────┼─────────────────────┼──────────────────┘
          │                  │                     │
          ▼                  ▼                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      MODELS (app/models/)                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐      │
│  │  Estudiante  │  │    Curso     │  │ estudiantes_cursos   │      │
│  │    Model     │  │    Model     │  │  (Tabla Asociación)  │      │
│  │              │◄─┼──────────────┼──┼──────────────────────┤      │
│  │ - Campos     │  │ - Campos     │  │ - id_estudiante (FK) │      │
│  │ - cursos     │  │ - estudiantes│  │ - id_curso (FK)      │      │
│  │   (relation) │  │   (relation) │  │                      │      │
│  └──────┬───────┘  └──────┬───────┘  └──────────────────────┘      │
└─────────┼──────────────────┼──────────────────────────────────────┘
          │                  │
          ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    DATABASE CONFIG (app/config/)                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  database.py                                                 │   │
│  │  - SQLAlchemy Engine                                         │   │
│  │  - SessionLocal                                              │   │
│  │  - get_db() dependency                                       │   │
│  └──────────────────────────┬───────────────────────────────────┘   │
└─────────────────────────────┼───────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        MYSQL DATABASE                                │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐        │
│  │ estudiantes │  │   cursos    │  │ estudiantes_cursos   │        │
│  │             │  │             │  │                      │        │
│  │ id ◄────────┼──┼─────────────┼──┼─ id_estudiante      │        │
│  │ nombres     │  │ id ◄────────┼──┼─ id_curso           │        │
│  │ apellidos   │  │ nombre_curso│  │                      │        │
│  │ ...         │  │ nivel       │  │                      │        │
│  └─────────────┘  │ gestion     │  └──────────────────────┘        │
│                   └─────────────┘                                   │
└─────────────────────────────────────────────────────────────────────┘
```

## 🔄 Flujo de Datos - Ejemplo: Inscribir Estudiante

```
1. CLIENTE
   │
   ├─► POST /api/inscripciones/inscribir
   │   Body: { "id_estudiante": 1, "id_curso": 3 }
   │
   ▼

2. VIEW (inscripcion_view.py)
   │
   ├─► Recibe request HTTP
   ├─► Valida con Pydantic (InscripcionCreate)
   ├─► Obtiene sesión DB con get_db()
   │
   ▼

3. CONTROLLER (inscripcion_controller.py)
   │
   ├─► inscribir_estudiante(db, inscripcion)
   ├─► Valida que estudiante existe
   ├─► Valida que curso existe
   ├─► Valida que no esté ya inscrito
   ├─► Ejecuta: estudiante.cursos.append(curso)
   ├─► db.commit()
   │
   ▼

4. MODEL (estudiante_model.py, curso_model.py)
   │
   ├─► SQLAlchemy maneja la relación many-to-many
   ├─► Inserta en tabla estudiantes_cursos
   │
   ▼

5. DATABASE (MySQL)
   │
   ├─► INSERT INTO estudiantes_cursos
   │   VALUES (1, 3)
   │
   ▼

6. RESPUESTA
   │
   ├─► Controller retorna mensaje de éxito
   ├─► View serializa con Pydantic
   ├─► Cliente recibe JSON
   │
   └─► { "mensaje": "Estudiante inscrito..." }
```

## 🗂️ Estructura de Carpetas Detallada

```
Modulo-Estudiante/
│
├── app/
│   │
│   ├── __init__.py
│   ├── main.py                      # 🎯 Punto de entrada, registra routers
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── database.py              # 🔧 Configuración SQLAlchemy + get_db()
│   │
│   ├── models/                      # 📊 CAPA DE DATOS
│   │   ├── __init__.py
│   │   ├── estudiante_model.py      # Tabla estudiantes + relación cursos
│   │   └── curso_model.py           # Tabla cursos + relación estudiantes
│   │
│   ├── schemas/                     # ✅ VALIDACIONES (Pydantic)
│   │   ├── __init__.py
│   │   ├── estudiante_schema.py     # Validaciones estudiante + cursos field
│   │   ├── curso_schema.py          # Validaciones curso + estudiantes field
│   │   └── inscripcion_schema.py    # Validaciones inscripción
│   │
│   ├── controllers/                 # 🧠 LÓGICA DE NEGOCIO
│   │   ├── __init__.py
│   │   ├── estudiante_controller.py # CRUD estudiantes
│   │   ├── curso_controller.py      # CRUD cursos
│   │   └── inscripcion_controller.py# Lógica many-to-many
│   │
│   └── views/                       # 🌐 ENDPOINTS HTTP (Routers)
│       ├── __init__.py
│       ├── estudiante_view.py       # Rutas /api/estudiantes
│       ├── curso_view.py            # Rutas /api/cursos
│       └── inscripcion_view.py      # Rutas /api/inscripciones
│
├── run.py                           # 🚀 Script para iniciar servidor
├── test_connection.py               # 🧪 Test de conexión DB
├── test_api_cursos.py               # 🧪 Test de endpoints
├── crear_tablas_cursos.sql          # 📝 Script SQL
├── requirements.txt                 # 📦 Dependencias
│
└── Documentación/
    ├── README.md
    ├── DOCUMENTACION_CURSOS.md      # 📚 Referencia completa
    ├── RESUMEN_IMPLEMENTACION.md    # 📋 Detalles técnicos
    └── GUIA_RAPIDA_CURSOS.md        # ⚡ Inicio rápido
```

## 🔗 Relación Many-to-Many

```
┌─────────────────┐                    ┌─────────────────┐
│   ESTUDIANTE    │                    │      CURSO      │
├─────────────────┤                    ├─────────────────┤
│ id_estudiante   │◄───┐          ┌───►│ id_curso        │
│ nombres         │    │          │    │ nombre_curso    │
│ apellidos       │    │          │    │ nivel           │
│ ...             │    │          │    │ gestion         │
│                 │    │          │    │                 │
│ cursos []       │    │          │    │ estudiantes []  │
└─────────────────┘    │          │    └─────────────────┘
                       │          │
                       │          │
              ┌────────┴──────────┴────────┐
              │  ESTUDIANTES_CURSOS         │
              ├─────────────────────────────┤
              │ id_estudiante (FK, PK)      │
              │ id_curso (FK, PK)           │
              └─────────────────────────────┘
```

**Características:**

- Un estudiante puede tener **múltiples cursos**
- Un curso puede tener **múltiples estudiantes**
- La tabla `estudiantes_cursos` almacena las relaciones
- `CASCADE DELETE`: Si eliminas un estudiante/curso, se eliminan sus inscripciones

## 📡 Endpoints por Módulo

### Módulo Estudiantes

```
GET    /api/estudiantes/getAll           → Lista estudiantes
GET    /api/estudiantes/getById/{id}     → Obtiene estudiante
POST   /api/estudiantes/create           → Crea estudiante
PUT    /api/estudiantes/update/{id}      → Actualiza estudiante
DELETE /api/estudiantes/delete/{id}      → Elimina estudiante
```

### Módulo Cursos

```
GET    /api/cursos/                      → Lista cursos
GET    /api/cursos/{id}                  → Obtiene curso
POST   /api/cursos/                      → Crea curso
PUT    /api/cursos/{id}                  → Actualiza curso
DELETE /api/cursos/{id}                  → Elimina curso
```

### Módulo Inscripciones

```
POST   /api/inscripciones/inscribir                    → Inscribe estudiante
DELETE /api/inscripciones/desinscribir                 → Desinscribe estudiante
GET    /api/inscripciones/estudiante/{id}/cursos      → Cursos del estudiante
GET    /api/inscripciones/curso/{id}/estudiantes      → Estudiantes del curso
```

## 🎨 Patrón de Diseño Utilizado

### MVC (Model-View-Controller)

**Model** (Modelos):

- Define la estructura de datos
- Maneja relaciones entre entidades
- Mapea a tablas de base de datos

**View** (Vistas/Routers):

- Expone endpoints HTTP
- Valida entrada con schemas
- Retorna respuestas HTTP

**Controller** (Controladores):

- Contiene lógica de negocio
- Interactúa con modelos
- Maneja excepciones y validaciones

### Ventajas:

✅ Separación de responsabilidades
✅ Código más mantenible
✅ Fácil de escalar
✅ Reutilización de código
✅ Testing más sencillo

## 🛡️ Validaciones Implementadas

### A nivel de Schema (Pydantic)

- Tipos de datos correctos
- Longitudes de campos
- Campos obligatorios vs opcionales
- Formatos (fechas, enums)

### A nivel de Controller (Lógica de Negocio)

- Estudiante/Curso existe
- Inscripción no duplicada
- Relación existe antes de eliminar
- Manejo de errores con HTTPException

### A nivel de Database (Constraints)

- Primary Keys
- Foreign Keys
- Unique constraints
- NOT NULL constraints

## 🔐 Seguridad y Buenas Prácticas

✅ Variables de entorno para credenciales (`.env`)
✅ Dependency Injection (`Depends(get_db)`)
✅ Validación automática de datos (Pydantic)
✅ Manejo de excepciones HTTP
✅ Documentación automática (Swagger)
✅ CORS configurado
✅ Transacciones de DB (`db.commit()`, `db.rollback()`)

---

Esta arquitectura garantiza un código limpio, mantenible y escalable siguiendo las mejores prácticas de desarrollo con FastAPI. 🚀
