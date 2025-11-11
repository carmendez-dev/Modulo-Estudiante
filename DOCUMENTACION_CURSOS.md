# Documentación - Gestión de Cursos e Inscripciones

## Nuevas Funcionalidades Implementadas

Se ha ampliado la API para incluir la gestión de **Cursos** y la relación **many-to-many** entre Estudiantes y Cursos mediante **Inscripciones**.

---

## Estructura de Archivos Creados/Actualizados

### Archivos Actualizados

- `app/models/estudiante_model.py` - Agregada tabla de asociación `estudiantes_cursos` y relación `cursos`
- `app/schemas/estudiante_schema.py` - Agregado campo `cursos` en `EstudianteResponse`
- `app/main.py` - Registrados los nuevos routers de cursos e inscripciones

### Archivos Creados

**Modelos:**

- `app/models/curso_model.py` - Modelo SQLAlchemy para Curso

**Schemas:**

- `app/schemas/curso_schema.py` - Validaciones Pydantic para Curso
- `app/schemas/inscripcion_schema.py` - Validaciones Pydantic para Inscripción

**Controladores:**

- `app/controllers/curso_controller.py` - Lógica de negocio CRUD para Curso
- `app/controllers/inscripcion_controller.py` - Lógica para gestionar inscripciones

**Vistas:**

- `app/views/curso_view.py` - Rutas API para `/api/cursos`
- `app/views/inscripcion_view.py` - Rutas API para `/api/inscripciones`

**SQL:**

- `crear_tablas_cursos.sql` - Script para crear tablas en MySQL

---

## Tablas de Base de Datos

### Tabla: `cursos`

| Campo        | Tipo                                      | Descripción            |
| ------------ | ----------------------------------------- | ---------------------- |
| id_curso     | INT (PK, AUTO_INCREMENT)                  | ID único del curso     |
| nombre_curso | VARCHAR(100)                              | Nombre del curso       |
| nivel        | ENUM('inicial', 'primaria', 'secundaria') | Nivel educativo        |
| gestion      | VARCHAR(10)                               | Año/gestión (ej: 2024) |

### Tabla: `estudiantes_cursos` (asociación many-to-many)

| Campo         | Tipo         | Descripción              |
| ------------- | ------------ | ------------------------ |
| id_estudiante | INT (FK, PK) | Referencia a estudiantes |
| id_curso      | INT (FK, PK) | Referencia a cursos      |

---

## Endpoints de la API

### 📚 CURSOS (`/api/cursos`)

#### 1. Listar todos los cursos

```http
GET /api/cursos?skip=0&limit=100
```

**Respuesta exitosa (200):**

```json
[
  {
    "id_curso": 1,
    "nombre_curso": "Primero A",
    "nivel": "primaria",
    "gestion": "2024",
    "estudiantes": []
  }
]
```

#### 2. Obtener curso por ID

```http
GET /api/cursos/{id_curso}
```

**Ejemplo:** `GET /api/cursos/1`

**Respuesta exitosa (200):**

```json
{
  "id_curso": 1,
  "nombre_curso": "Primero A",
  "nivel": "primaria",
  "gestion": "2024",
  "estudiantes": [
    {
      "id_estudiante": 5,
      "nombres": "Juan Carlos",
      "apellido_paterno": "Pérez",
      "apellido_materno": "García",
      ...
    }
  ]
}
```

#### 3. Crear nuevo curso

```http
POST /api/cursos
Content-Type: application/json
```

**Body:**

```json
{
  "nombre_curso": "Segundo B",
  "nivel": "primaria",
  "gestion": "2024"
}
```

**Respuesta exitosa (201):**

```json
{
  "id_curso": 5,
  "nombre_curso": "Segundo B",
  "nivel": "primaria",
  "gestion": "2024",
  "estudiantes": []
}
```

#### 4. Actualizar curso

```http
PUT /api/cursos/{id_curso}
Content-Type: application/json
```

**Body (todos los campos opcionales):**

```json
{
  "nombre_curso": "Segundo B - Actualizado",
  "gestion": "2025"
}
```

**Respuesta exitosa (200):**

```json
{
  "id_curso": 5,
  "nombre_curso": "Segundo B - Actualizado",
  "nivel": "primaria",
  "gestion": "2025",
  "estudiantes": []
}
```

#### 5. Eliminar curso

```http
DELETE /api/cursos/{id_curso}
```

**Respuesta exitosa (200):**

```json
{
  "mensaje": "Curso con ID 5 eliminado exitosamente"
}
```

---

### 🎓 INSCRIPCIONES (`/api/inscripciones`)

#### 1. Inscribir estudiante a un curso

```http
POST /api/inscripciones/inscribir
Content-Type: application/json
```

**Body:**

```json
{
  "id_estudiante": 1,
  "id_curso": 3
}
```

**Respuesta exitosa (201):**

```json
{
  "mensaje": "Estudiante 'Juan Carlos Pérez' inscrito exitosamente en 'Primero A'",
  "id_estudiante": 1,
  "id_curso": 3
}
```

**Errores posibles:**

- `404`: Estudiante o curso no encontrado
- `400`: El estudiante ya está inscrito en el curso

#### 2. Desinscribir estudiante de un curso

```http
DELETE /api/inscripciones/desinscribir?id_estudiante=1&id_curso=3
```

**Respuesta exitosa (200):**

```json
{
  "mensaje": "Estudiante 'Juan Carlos Pérez' desinscrito exitosamente de 'Primero A'",
  "id_estudiante": 1,
  "id_curso": 3
}
```

**Errores posibles:**

- `404`: Estudiante o curso no encontrado
- `400`: El estudiante no está inscrito en el curso

#### 3. Obtener cursos de un estudiante

```http
GET /api/inscripciones/estudiante/{id_estudiante}/cursos
```

**Ejemplo:** `GET /api/inscripciones/estudiante/1/cursos`

**Respuesta exitosa (200):**

```json
[
  {
    "id_curso": 3,
    "nombre_curso": "Primero A",
    "nivel": "primaria",
    "gestion": "2024",
    "estudiantes": []
  },
  {
    "id_curso": 7,
    "nombre_curso": "Matemática Avanzada",
    "nivel": "primaria",
    "gestion": "2024",
    "estudiantes": []
  }
]
```

#### 4. Obtener estudiantes de un curso

```http
GET /api/inscripciones/curso/{id_curso}/estudiantes
```

**Ejemplo:** `GET /api/inscripciones/curso/3/estudiantes`

**Respuesta exitosa (200):**

```json
[
  {
    "id_estudiante": 1,
    "nombres": "Juan Carlos",
    "apellido_paterno": "Pérez",
    "apellido_materno": "García",
    "ci": "12345678",
    "fecha_nacimiento": "2015-03-15",
    "direccion": "Av. Principal #123",
    "cursos": []
  }
]
```

---

## Flujo de Trabajo Recomendado

### 1. Crear cursos

```bash
POST /api/cursos
```

### 2. Crear estudiantes

```bash
POST /api/estudiantes/create
```

### 3. Inscribir estudiantes a cursos

```bash
POST /api/inscripciones/inscribir
```

### 4. Consultar inscripciones

```bash
GET /api/inscripciones/estudiante/{id}/cursos
GET /api/inscripciones/curso/{id}/estudiantes
```

---

## Notas Importantes

1. **Relación Many-to-Many**: Un estudiante puede estar inscrito en múltiples cursos, y un curso puede tener múltiples estudiantes.

2. **Cascada en eliminaciones**: Si eliminas un estudiante o un curso, las inscripciones relacionadas se eliminan automáticamente (configurado en las foreign keys).

3. **Validaciones**:

   - No se puede inscribir un estudiante dos veces al mismo curso
   - No se puede desinscribir un estudiante que no está inscrito
   - Los niveles válidos son: `inicial`, `primaria`, `secundaria`

4. **Documentación interactiva**: Accede a http://localhost:8000/docs para probar todos los endpoints desde Swagger UI.

---

## Ejemplos de Uso con cURL

### Crear un curso

```bash
curl -X POST http://localhost:8000/api/cursos \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_curso": "Tercero A",
    "nivel": "primaria",
    "gestion": "2024"
  }'
```

### Inscribir estudiante

```bash
curl -X POST http://localhost:8000/api/inscripciones/inscribir \
  -H "Content-Type: application/json" \
  -d '{
    "id_estudiante": 1,
    "id_curso": 3
  }'
```

### Listar cursos de un estudiante

```bash
curl http://localhost:8000/api/inscripciones/estudiante/1/cursos
```

### Desinscribir estudiante

```bash
curl -X DELETE "http://localhost:8000/api/inscripciones/desinscribir?id_estudiante=1&id_curso=3"
```

---

## Instalación y Configuración

1. **Ejecutar el script SQL**:

   ```bash
   mysql -u root -p bienestar_estudiantil < crear_tablas_cursos.sql
   ```

2. **Las tablas se crean automáticamente** cuando inicias el servidor (gracias a SQLAlchemy):

   ```bash
   python run.py
   ```

3. **Acceder a la documentación**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
