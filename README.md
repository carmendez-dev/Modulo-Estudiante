# API Bienestar Estudiantil

Backend completo en Python con FastAPI y arquitectura MVC para gestionar estudiantes.

## 📋 Requisitos Previos

- Python 3.8 o superior
- MySQL Server
- phpMyAdmin (opcional, para administración visual)

## 🚀 Instalación

### 1. Crear base de datos

Ejecuta este script SQL en phpMyAdmin o MySQL:

```sql
CREATE DATABASE IF NOT EXISTS bienestar_estudiantil;
USE bienestar_estudiantil;

CREATE TABLE `estudiantes` (
  `id_estudiante` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `ci` varchar(20) DEFAULT NULL,
  `nombres` varchar(50) NOT NULL,
  `apellido_paterno` varchar(50) NOT NULL,
  `apellido_materno` varchar(50) NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `direccion` varchar(100) DEFAULT NULL,
  `nombre_padre` varchar(50) DEFAULT NULL,
  `apellido_paterno_padre` varchar(50) DEFAULT NULL,
  `apellido_materno_padre` varchar(50) DEFAULT NULL,
  `telefono_padre` varchar(20) DEFAULT NULL,
  `nombre_madre` varchar(50) DEFAULT NULL,
  `apellido_paterno_madre` varchar(50) DEFAULT NULL,
  `apellido_materno_madre` varchar(50) DEFAULT NULL,
  `telefono_madre` varchar(20) DEFAULT NULL,
  `estado_estudiante` BOOLEAN NOT NULL DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Edita el archivo `.env` con tus credenciales de MySQL:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=bienestar_estudiantil
DB_PORT=3306
```

### 4. Probar la conexión (opcional)

```bash
python test_connection.py
```

### 5. Ejecutar la aplicación

```bash
# Opción 1: Usando el script run.py (recomendado)
python run.py

# Opción 2: Usando uvicorn directamente
uvicorn app.main:app --reload

# Opción 3: Como módulo
python -m uvicorn app.main:app --reload
```

La API estará disponible en: `http://localhost:8000`

## 📚 Documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 Endpoints

### Listar todos los estudiantes
```
GET /api/estudiantes
```

### Obtener estudiante por ID
```
GET /api/estudiantes/{id}
```

### Crear nuevo estudiante
```
POST /api/estudiantes
Content-Type: application/json

{
  "ci": "12345678",
  "nombres": "Juan Carlos",
  "apellido_paterno": "Pérez",
  "apellido_materno": "García",
  "fecha_nacimiento": "2005-03-15",
  "direccion": "Av. Principal #123",
  "nombre_padre": "Carlos",
  "apellido_paterno_padre": "Pérez",
  "apellido_materno_padre": "López",
  "telefono_padre": "71234567",
  "nombre_madre": "María",
  "apellido_paterno_madre": "García",
  "apellido_materno_madre": "Rodríguez",
  "telefono_madre": "72345678"
}
```

### Actualizar estudiante
```
PUT /api/estudiantes/{id}
Content-Type: application/json

{
  "direccion": "Nueva dirección #456",
  "telefono_padre": "73456789"
}
```

### Eliminar estudiante
```
DELETE /api/estudiantes/{id}
```

## 📁 Estructura del Proyecto

```
bienestar_estudiantil/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Aplicación principal
│   ├── config/
│   │   ├── __init__.py
│   │   └── database.py            # Configuración de BD
│   ├── models/
│   │   ├── __init__.py
│   │   └── estudiante_model.py    # Modelo SQLAlchemy
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── estudiante_controller.py  # Lógica de negocio
│   ├── views/
│   │   ├── __init__.py
│   │   └── estudiante_view.py     # Rutas/Endpoints
│   └── schemas/
│       ├── __init__.py
│       └── estudiante_schema.py   # Validación Pydantic
├── .env                           # Variables de entorno
├── requirements.txt               # Dependencias
└── README.md                      # Este archivo
```

## 🛠️ Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para Python
- **Pydantic**: Validación de datos
- **PyMySQL**: Conector MySQL
- **Uvicorn**: Servidor ASGI
- **Python-dotenv**: Gestión de variables de entorno

## ✅ Características

- ✓ Arquitectura MVC bien estructurada
- ✓ Validación de datos con Pydantic
- ✓ Manejo de excepciones HTTP
- ✓ Documentación automática (Swagger/ReDoc)
- ✓ CORS configurado para frontend
- ✓ Variables de entorno para seguridad
- ✓ Paginación en listado de estudiantes
- ✓ Comentarios explicativos en código

## 🧪 Pruebas

Puedes probar los endpoints usando:

1. **Swagger UI** en http://localhost:8000/docs
2. **Postman** o **Insomnia**
3. **cURL**:

```bash
# Listar estudiantes
curl http://localhost:8000/api/estudiantes

# Crear estudiante
curl -X POST http://localhost:8000/api/estudiantes \
  -H "Content-Type: application/json" \
  -d '{"nombres":"Juan","apellido_paterno":"Pérez","apellido_materno":"García"}'
```

## 📝 Notas

- Los campos `nombres`, `apellido_paterno` y `apellido_materno` son obligatorios
- Los demás campos son opcionales
- La fecha debe estar en formato ISO: `YYYY-MM-DD`
- El ID se genera automáticamente (AUTO_INCREMENT)
