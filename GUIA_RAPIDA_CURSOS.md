# Guía Rápida - Gestión de Cursos e Inscripciones

## 🚀 Pasos para Empezar

### 1. Preparar la Base de Datos

Opción A - Automático (Recomendado):

```bash
# Las tablas se crearán automáticamente al iniciar el servidor
python run.py
```

Opción B - Manual:

```bash
# Ejecutar el script SQL en MySQL
mysql -u root -p bienestar_estudiantil < crear_tablas_cursos.sql
```

### 2. Iniciar el Servidor

```bash
python run.py
```

El servidor estará disponible en: http://localhost:8000

### 3. Acceder a la Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📝 Casos de Uso Prácticos

### Caso 1: Crear un Curso Nuevo

**Endpoint**: `POST /api/cursos/`

**Request:**

```json
{
  "nombre_curso": "Primero A",
  "nivel": "primaria",
  "gestion": "2024"
}
```

**Response:**

```json
{
  "id_curso": 1,
  "nombre_curso": "Primero A",
  "nivel": "primaria",
  "gestion": "2024",
  "estudiantes": []
}
```

### Caso 2: Crear un Estudiante

**Endpoint**: `POST /api/estudiantes/create`

**Request:**

```json
{
  "nombres": "María José",
  "apellido_paterno": "López",
  "apellido_materno": "Fernández",
  "ci": "98765432",
  "fecha_nacimiento": "2015-05-20",
  "direccion": "Calle Falsa 123"
}
```

### Caso 3: Inscribir Estudiante a Curso

**Endpoint**: `POST /api/inscripciones/inscribir`

**Request:**

```json
{
  "id_estudiante": 1,
  "id_curso": 1
}
```

**Response:**

```json
{
  "mensaje": "Estudiante 'María José López' inscrito exitosamente en 'Primero A'",
  "id_estudiante": 1,
  "id_curso": 1
}
```

### Caso 4: Ver Cursos de un Estudiante

**Endpoint**: `GET /api/inscripciones/estudiante/1/cursos`

**Response:**

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

### Caso 5: Ver Estudiantes de un Curso

**Endpoint**: `GET /api/inscripciones/curso/1/estudiantes`

**Response:**

```json
[
  {
    "id_estudiante": 1,
    "nombres": "María José",
    "apellido_paterno": "López",
    "apellido_materno": "Fernández",
    "ci": "98765432",
    "cursos": []
  }
]
```

### Caso 6: Desinscribir Estudiante

**Endpoint**: `DELETE /api/inscripciones/desinscribir?id_estudiante=1&id_curso=1`

**Response:**

```json
{
  "mensaje": "Estudiante 'María José López' desinscrito exitosamente de 'Primero A'",
  "id_estudiante": 1,
  "id_curso": 1
}
```

---

## 🧪 Probar con el Script de Pruebas

```bash
# Instalar requests si es necesario
pip install requests

# Ejecutar el script de pruebas
python test_api_cursos.py
```

Este script prueba automáticamente todos los endpoints de Cursos e Inscripciones.

---

## 🔍 Casos de Error Comunes

### Error 404: Estudiante/Curso no encontrado

```json
{
  "detail": "Estudiante con ID 999 no encontrado"
}
```

**Solución**: Verificar que el ID existe antes de hacer la inscripción.

### Error 400: Ya inscrito

```json
{
  "detail": "El estudiante ya está inscrito en el curso 'Primero A'"
}
```

**Solución**: No se puede inscribir dos veces al mismo curso. Primero desinscribir si es necesario.

### Error 400: No inscrito

```json
{
  "detail": "El estudiante no está inscrito en el curso 'Primero A'"
}
```

**Solución**: No se puede desinscribir de un curso en el que no está inscrito.

---

## 📊 Flujo Completo de Trabajo

```
1. Crear Cursos
   POST /api/cursos/

2. Crear Estudiantes
   POST /api/estudiantes/create

3. Inscribir Estudiantes
   POST /api/inscripciones/inscribir

4. Consultar Inscripciones
   GET /api/inscripciones/estudiante/{id}/cursos
   GET /api/inscripciones/curso/{id}/estudiantes

5. Gestionar Cambios
   DELETE /api/inscripciones/desinscribir
   PUT /api/cursos/{id}
   PUT /api/estudiantes/update/{id}
```

---

## 🎯 Ejemplos con cURL

### Crear un Curso

```bash
curl -X POST "http://localhost:8000/api/cursos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_curso": "Segundo A",
    "nivel": "primaria",
    "gestion": "2024"
  }'
```

### Listar Cursos

```bash
curl "http://localhost:8000/api/cursos/"
```

### Inscribir Estudiante

```bash
curl -X POST "http://localhost:8000/api/inscripciones/inscribir" \
  -H "Content-Type: application/json" \
  -d '{
    "id_estudiante": 1,
    "id_curso": 1
  }'
```

### Desinscribir Estudiante

```bash
curl -X DELETE "http://localhost:8000/api/inscripciones/desinscribir?id_estudiante=1&id_curso=1"
```

---

## 📚 Niveles Válidos para Cursos

- `inicial` - Educación inicial (prekinder, kinder)
- `primaria` - Educación primaria (1° a 6°)
- `secundaria` - Educación secundaria (1° a 6° de secundaria)

---

## ⚡ Consejos de Performance

1. **Paginación**: Usa los parámetros `skip` y `limit` para grandes cantidades de datos

   ```
   GET /api/cursos/?skip=0&limit=50
   ```

2. **Consultas específicas**: Usa los endpoints de inscripciones para obtener solo lo necesario

   ```
   GET /api/inscripciones/estudiante/1/cursos
   ```

3. **Validaciones**: La API valida automáticamente todos los datos, no es necesario validar en el cliente

---

## 🛠️ Archivos Importantes

- `DOCUMENTACION_CURSOS.md` - Documentación completa de endpoints
- `RESUMEN_IMPLEMENTACION.md` - Detalles técnicos de la implementación
- `crear_tablas_cursos.sql` - Script SQL para crear tablas
- `test_api_cursos.py` - Script de pruebas automatizado

---

## ✅ Checklist de Implementación

- [x] Modelo de Curso creado
- [x] Tabla de asociación estudiantes_cursos
- [x] Relación many-to-many configurada
- [x] CRUD completo de Cursos
- [x] Endpoints de Inscripciones
- [x] Validaciones de negocio
- [x] Documentación completa
- [x] Scripts de prueba
- [x] Sin errores de sintaxis

---

## 🎓 Próximos Pasos

1. Probar los endpoints desde Swagger UI
2. Crear algunos cursos de ejemplo
3. Crear algunos estudiantes de ejemplo
4. Hacer inscripciones de prueba
5. Verificar las consultas de relaciones

¡Todo está listo para usar! 🚀
