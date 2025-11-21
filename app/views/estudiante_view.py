"""
Vista (Router) para los endpoints de estudiantes
Define las rutas HTTP y conecta con el controlador
"""
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.controllers.estudiante_controller import EstudianteController
from app.schemas.estudiante_schema import (
    EstudianteCreate,
    EstudianteUpdate,
    EstudianteResponse,
    CambiarEstadoEstudiante,
    CambiarEstadoResponse
)
from app.schemas.estudiante_curso_schema import EstudianteConCursos, EstudianteConCursosGestion
from typing import Optional
from datetime import datetime

# Crear router con prefijo y etiquetas
router = APIRouter(
    prefix="/api/estudiantes",
    tags=["Estudiantes"]
)

@router.get(
    "/",
    response_model=List[EstudianteConCursos],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los estudiantes con sus cursos",
    description="Obtiene una lista de todos los estudiantes registrados con sus cursos asignados y paginación opcional"
)
def listar_estudiantes(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    db: Session = Depends(get_db)
):
    """
    Endpoint para listar todos los estudiantes con sus cursos
    """
    return EstudianteController.obtener_todos(db, skip=skip, limit=limit)

@router.get(
    "/por-gestion",
    status_code=status.HTTP_200_OK,
    summary="Listar estudiantes por gestión",
    description="Obtiene estudiantes filtrados por gestión (año académico), mostrando SOLO los cursos de esa gestión. Por defecto usa el año actual."
)
def listar_estudiantes_por_gestion(
    gestion: Optional[str] = Query(None, description="Gestión a filtrar. Por defecto: año actual"),
    nivel: Optional[str] = Query(None, description="Filtrar por nivel (inicial, primaria, secundaria)"),
    id_curso: Optional[int] = Query(None, description="Filtrar por ID de curso específico"),
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    db: Session = Depends(get_db)
):
    """
    Endpoint para listar estudiantes filtrados por gestión.
    Por defecto filtra por el año actual.
    Los cursos mostrados corresponden SOLO a la gestión especificada.
    """
    # Si no se especifica gestión, usar el año actual
    if gestion is None:
        gestion = str(datetime.now().year)
    
    return EstudianteController.obtener_por_gestion(
        db, 
        gestion=gestion,
        nivel=nivel,
        id_curso=id_curso,
        skip=skip,
        limit=limit
    )

@router.get(
    "/{id_estudiante}",
    response_model=EstudianteConCursos,
    status_code=status.HTTP_200_OK,
    summary="Obtener estudiante por ID con sus cursos",
    description="Obtiene la información detallada de un estudiante específico incluyendo los cursos asignados"
)
def obtener_estudiante(
    id_estudiante: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener un estudiante por su ID con sus cursos
    """
    return EstudianteController.obtener_por_id(db, id_estudiante)

@router.post(
    "/",
    response_model=EstudianteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo estudiante",
    description="Registra un nuevo estudiante en el sistema"
)
def crear_estudiante(
    estudiante: EstudianteCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para crear un nuevo estudiante
    """
    return EstudianteController.crear(db, estudiante)

@router.put(
    "/{id_estudiante}",
    response_model=EstudianteResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar estudiante",
    description="Actualiza la información de un estudiante existente"
)
def actualizar_estudiante(
    id_estudiante: int,
    estudiante: EstudianteUpdate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para actualizar un estudiante existente
    """
    return EstudianteController.actualizar(db, id_estudiante, estudiante)

@router.delete(
    "/{id_estudiante}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar estudiante",
    description="Elimina un estudiante del sistema"
)
def eliminar_estudiante(
    id_estudiante: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para eliminar un estudiante
    """
    return EstudianteController.eliminar(db, id_estudiante)

@router.patch(
    "/{id_estudiante}/estado",
    response_model=CambiarEstadoResponse,
    status_code=status.HTTP_200_OK,
    summary="Cambiar estado del estudiante",
    description="Cambia el estado de un estudiante (Activo, Abandono, Retirado)"
)
def cambiar_estado_estudiante(
    id_estudiante: int,
    estado_data: CambiarEstadoEstudiante,
    db: Session = Depends(get_db)
):
    """
    Endpoint para cambiar el estado de un estudiante.
    Estados válidos: Activo, Abandono, Retirado
    """
    return EstudianteController.cambiar_estado(
        db, 
        id_estudiante, 
        estado_data.estado_estudiante
    )

@router.get(
    "/por-estado/{estado}",
    response_model=List[EstudianteConCursos],
    status_code=status.HTTP_200_OK,
    summary="Listar estudiantes por estado",
    description="Obtiene estudiantes filtrados por estado (Activo, Retirado, Abandono)"
)
def listar_estudiantes_por_estado(
    estado: str,
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    db: Session = Depends(get_db)
):
    """
    Endpoint para listar estudiantes filtrados por estado.
    Estados válidos: Activo, Retirado, Abandono
    """
    return EstudianteController.obtener_por_estado(
        db,
        estado=estado,
        skip=skip,
        limit=limit
    )
