# 📝 Changelog - Sistema Bienestar Estudiantil

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
- **Endpoints**: 14 (5 estudiantes + 5 cursos + 4 asignaciones)
- **Modelos**: 3 (+ tabla de relación)
- **Controladores**: 3
- **Schemas**: 11
- **Líneas de código**: ~2,500+

### Documentación
- **Archivos**: 23+
- **Guías completas**: 10
- **Ejemplos de código**: 20+
- **Líneas de documentación**: ~4,000+

### Base de Datos
- **Tablas**: 3 (estudiantes, cursos, estudiantes_cursos)
- **Campos totales**: 20 (15 estudiantes + 3 cursos + 2 relación)
- **Relaciones**: 1 muchos a muchos
- **Motor**: MySQL 8.0+

---

## 🔄 Próximas Versiones Planificadas

### [1.3.0] - Autenticación
- [ ] JWT authentication
- [ ] Roles de usuario
- [ ] Permisos por módulo

### [1.4.0] - Reportes
- [ ] Exportar a Excel
- [ ] Exportar a PDF
- [ ] Estadísticas y gráficos

---

## 🐛 Correcciones

### [1.1.0]
- Ninguna (primera versión del módulo)

### [1.0.0]
- Ninguna (lanzamiento inicial)

---

## 📝 Notas de Migración

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

**Versión actual**: 1.1.0  
**Última actualización**: 2024-11-11
