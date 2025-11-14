# 📝 Changelog - Sistema Bienestar Estudiantil

## [1.3.0] - 2025-11-14

### 🚀 Nuevas Funcionalidades

#### Operaciones Masivas

- ✅ **Creación masiva de cursos**: Endpoint para crear múltiples cursos en una sola petición
- ✅ **Asignación masiva de estudiantes**: Endpoint para asignar múltiples estudiantes a un curso de forma simultánea

#### Filtros Avanzados

- ✅ **Filtrado de cursos por año**: Nuevo endpoint para obtener cursos de un año específico con datos simplificados
- ✅ **Estudiantes habilitados por curso**: Endpoint para obtener solo estudiantes con estado "habilitado" de un curso

#### Mejoras en Modelos

- ✅ **Campo `estado_estudiante`**: Agregado a modelo de estudiantes para gestión de estados (habilitado/inhabilitado)
- ✅ **Normalización de enums**: Campo `nivel` en cursos actualizado a mayúsculas (INICIAL, PRIMARIA, SECUNDARIA)

#### Endpoints Nuevos

```
POST   /api/cursos/masivo                                    # Crear múltiples cursos
POST   /api/asignaciones/masivo                              # Asignar múltiples estudiantes a un curso
GET    /api/cursos/anio/{anio}                              # Obtener cursos por año
GET    /api/asignaciones/curso/{id}/estudiantes-habilitados # Estudiantes habilitados de un curso
```

#### Schemas Actualizados

- ✅ **CursosCreateBulk**: Schema para creación masiva de cursos
- ✅ **CursosCreateBulkResponse**: Respuesta con total de cursos creados y lista detallada
- ✅ **AsignarEstudiantesCursoMasivo**: Schema para asignación masiva
- ✅ **AsignacionMasivaResponse**: Respuesta con total asignados y manejo de errores
- ✅ **CursoSimple**: Schema simplificado para exportación (id, nombre, nivel)

#### Controladores Actualizados

- ✅ **CursoController**:
  - `crear_cursos_masivo()`: Crea múltiples cursos con validación individual
  - `obtener_cursos_por_anio()`: Filtra y retorna cursos de un año específico
- ✅ **EstudianteCursoController**:

  - `asignar_estudiantes_masivo()`: Asigna lista de estudiantes con manejo de duplicados
  - `obtener_estudiantes_habilitados_de_curso()`: Retorna solo estudiantes activos

- ✅ **EstudianteController**:
  - `eliminar()`: Modificado para eliminación lógica (cambia estado a "inhabilitado")

#### Validaciones y Mejoras

- ✅ Validación de duplicados en asignaciones masivas
- ✅ Manejo de errores individuales en operaciones bulk
- ✅ Respuestas detalladas con conteo de operaciones exitosas
- ✅ Eliminación lógica de estudiantes preservando datos históricos
- ✅ Alineación de valores enum con la base de datos

#### Ejemplos de Uso

**Crear cursos masivamente**:

```json
POST /api/cursos/masivo
{
  "cursos": [
    {
      "nombre_curso": "Matemáticas Avanzadas",
      "nivel": "SECUNDARIA",
      "gestion": "2025"
    },
    {
      "nombre_curso": "Historia Universal",
      "nivel": "PRIMARIA",
      "gestion": "2025"
    }
  ]
}
```

**Asignar estudiantes masivamente**:

```json
POST /api/asignaciones/masivo
{
  "id_curso": 1,
  "ids_estudiantes": [1, 2, 3, 4, 5]
}
```

**Obtener cursos por año**:

```
GET /api/cursos/anio/2025
```

**Inhabilitar estudiante**:

```
DELETE /api/estudiantes/{id}
# Ahora cambia el estado a "inhabilitado" en lugar de eliminar el registro
```

---

## [1.2.0] - 2024-11-11

### ✨ Nuevo Módulo: Asignaciones Estudiante-Curso

#### Backend

- ✅ **Modelo**: `app/models/estudiante_curso_model.py`
  - Tabla de relación muchos a muchos
  - Claves foráneas a estudiantes y cursos
- ✅ **Schema**: `app/schemas/estudiante_curso_schema.py`
  - EstudianteConCursos (estudiante con sus cursos)
  - CursoConEstudiantes (curso con sus estudiantes)
  - AsignarEstudianteCurso (para asignaciones)
- ✅ **Controlador**: `app/controllers/estudiante_curso_controller.py`
  - Asignar estudiante a curso
  - Desasignar estudiante de curso
  - Obtener estudiantes de un curso
  - Obtener cursos de un estudiante
- ✅ **Vista**: `app/views/estudiante_curso_view.py`
  - 4 endpoints nuevos para asignaciones

#### Endpoints Nuevos

```
POST   /api/asignaciones              # Asignar estudiante a curso
DELETE /api/asignaciones              # Desasignar estudiante de curso
GET    /api/asignaciones/curso/{id}   # Estudiantes de un curso
GET    /api/asignaciones/estudiante/{id}  # Cursos de un estudiante
```

#### Endpoints Actualizados

- ✅ `GET /api/estudiantes/{id}` - Ahora incluye cursos asignados
- ✅ `GET /api/cursos/{id}` - Ahora incluye estudiantes asignados

#### Modelos Actualizados

- ✅ **Estudiante**: Agregada relación `cursos` (muchos a muchos)
- ✅ **Curso**: Agregada relación `estudiantes` (muchos a muchos)

#### Documentación Frontend

- ✅ **ASIGNACIONES_API_GUIDE.md** - Referencia completa de API
- ✅ **ASIGNACIONES_SVELTE_EXAMPLES.md** - Ejemplos de código Svelte

#### Validaciones

- ✅ No permitir asignaciones duplicadas
- ✅ Verificar existencia de estudiante y curso
- ✅ Validar desasignación solo si existe la relación

---

## [1.1.0] - 2024-11-11

### ✨ Nuevo Módulo: Cursos

#### Backend

- ✅ **Modelo**: `app/models/curso_model.py`
  - Tabla `cursos` con 4 campos
  - Enum para niveles (inicial, primaria, secundaria)
- ✅ **Schema**: `app/schemas/curso_schema.py`
  - Validación con Pydantic
  - CursoCreate, CursoUpdate, CursoResponse
  - Validación de niveles educativos
- ✅ **Controlador**: `app/controllers/curso_controller.py`
  - CRUD completo
  - Filtros por nivel y gestión
  - Manejo de errores HTTP
- ✅ **Vista**: `app/views/curso_view.py`
  - 5 endpoints REST
  - Documentación automática
  - Query parameters para filtros

#### Endpoints Nuevos

```
GET    /api/cursos              # Listar con filtros
GET    /api/cursos/{id}         # Obtener por ID
POST   /api/cursos              # Crear
PUT    /api/cursos/{id}         # Actualizar
DELETE /api/cursos/{id}         # Eliminar
```

#### Documentación Frontend

- ✅ **CURSOS_API_GUIDE.md** - Referencia completa de API
- ✅ **CURSOS_SVELTE_EXAMPLES.md** - Ejemplos de código Svelte
- ✅ **CURSOS_APP_MINIMA.md** - Aplicación funcional mínima
- ✅ **PROMPT_IMPLEMENTACION_CURSOS.md** - Guía de implementación

#### Actualizaciones

- ✅ Actualizado `app/main.py` para incluir router de cursos
- ✅ Actualizado `documentacion/README.md` con módulo de cursos
- ✅ Creado `RESUMEN_COMPLETO.md` con ambos módulos

### 🎨 Diseño

- Badges de colores por nivel educativo
- Filtros dinámicos por nivel y gestión
- Vista agrupada por niveles
- Paleta de colores consistente

---

## [1.0.0] - 2024-10-21

### 🎉 Lanzamiento Inicial

#### Backend

- ✅ Arquitectura MVC completa
- ✅ Módulo de Estudiantes
- ✅ Conexión MySQL con SQLAlchemy
- ✅ Validación con Pydantic
- ✅ CORS configurado
- ✅ Documentación Swagger automática

#### Endpoints Estudiantes

```
GET    /api/estudiantes         # Listar todos
GET    /api/estudiantes/{id}    # Obtener por ID
POST   /api/estudiantes         # Crear
PUT    /api/estudiantes/{id}    # Actualizar
DELETE /api/estudiantes/{id}    # Eliminar
```

#### Documentación Frontend

- ✅ 15+ archivos de documentación
- ✅ Guías de implementación Svelte
- ✅ Componentes reutilizables
- ✅ Sistema de validación
- ✅ Paleta de colores definida

#### Infraestructura

- ✅ Repositorio Git configurado
- ✅ .gitignore optimizado
- ✅ Scripts de inicio (run.py, iniciar_servidor.bat)
- ✅ Test de conexión a BD

---

## 📊 Estadísticas del Proyecto

### Backend

- **Módulos**: 3 (Estudiantes, Cursos, Asignaciones)
- **Endpoints**: 18 (5 estudiantes + 7 cursos + 6 asignaciones)
- **Modelos**: 3 (+ tabla de relación)
- **Controladores**: 3
- **Schemas**: 17
- **Líneas de código**: ~3,200+

### Documentación

- **Archivos**: 23+
- **Guías completas**: 10
- **Ejemplos de código**: 25+
- **Líneas de documentación**: ~4,500+

### Base de Datos

- **Tablas**: 3 (estudiantes, cursos, estudiantes_cursos)
- **Campos totales**: 20 (15 estudiantes + 3 cursos + 2 relación)
- **Relaciones**: 1 muchos a muchos
- **Motor**: MySQL 8.0+

---

## 🔄 Próximas Versiones Planificadas

### [1.4.0] - Autenticación

- [ ] JWT authentication
- [ ] Roles de usuario
- [ ] Permisos por módulo

### [1.5.0] - Reportes

- [ ] Exportar a Excel
- [ ] Exportar a PDF
- [ ] Estadísticas y gráficos

---

## 🐛 Correcciones

### [1.3.0]

- ✅ Corregida eliminación física de estudiantes (ahora es lógica)
- ✅ Alineados valores enum de nivel con base de datos
- ✅ Normalizados nombres de campos en schemas

### [1.2.0]

- Ninguna (primera versión del módulo)

### [1.1.0]

- Ninguna (primera versión del módulo)

### [1.0.0]

- Ninguna (lanzamiento inicial)

---

## 📝 Notas de Migración

### De 1.2.0 a 1.3.0

**Backend**:

1. Los nuevos endpoints se agregan automáticamente sin afectar funcionalidad existente
2. Campo `estado_estudiante` ya existe en modelo, solo se usa ahora en eliminación
3. Valores de `nivel` actualizados a mayúsculas en base de datos
4. Endpoints DELETE de estudiantes ahora hacen eliminación lógica

**Base de Datos**:

```sql
-- Actualizar valores de nivel a mayúsculas (si es necesario)
UPDATE cursos SET nivel = UPPER(nivel);

-- Verificar/Actualizar enum de nivel
ALTER TABLE cursos MODIFY COLUMN nivel
  ENUM('INICIAL', 'PRIMARIA', 'SECUNDARIA') NOT NULL;

-- Asegurar que estado_estudiante existe
-- (Ya debería existir desde versiones anteriores)
```

**Frontend**:

1. Actualizar llamadas a API para usar nuevos endpoints bulk
2. Ajustar valores de nivel a mayúsculas: 'INICIAL', 'PRIMARIA', 'SECUNDARIA'
3. Implementar manejo de respuestas bulk con contadores
4. Actualizar UI de eliminación para reflejar que es lógica (inhabilitar)

### De 1.1.0 a 1.2.0

**Backend**:

1. El servidor detectará automáticamente la tabla de relación
2. No requiere cambios en código existente
3. Los endpoints previos siguen funcionando igual

### De 1.0.0 a 1.1.0

**Backend**:

1. El servidor detectará automáticamente la nueva tabla `cursos`
2. No requiere cambios en código existente
3. Los endpoints de estudiantes siguen funcionando igual

**Frontend**:

1. Agregar nuevo servicio `cursosService.js`
2. Crear nueva ruta `/cursos`
3. Opcional: Agregar navegación entre módulos

**Base de Datos**:

```sql
-- Ejecutar en MySQL
CREATE TABLE `cursos` (
  `id_curso` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_curso` varchar(50) NOT NULL,
  `nivel` enum('inicial','primaria','secundaria') NOT NULL,
  `gestion` varchar(20) NOT NULL,
  PRIMARY KEY (`id_curso`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```

---

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- SQLAlchemy por el ORM robusto
- Pydantic por la validación de datos
- Svelte por la documentación de referencia

---

## 📞 Soporte

- **Documentación**: `documentacion/README.md`
- **API Docs**: http://localhost:8000/docs
- **Repositorio**: https://github.com/carmendez-dev/Modulo-Estudiante.git

---

**Versión actual**: 1.3.0  
**Última actualización**: 2025-11-14
