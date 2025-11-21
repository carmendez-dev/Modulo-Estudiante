"""
Vista (Router) para los endpoints de cursos
Define las rutas HTTP y conecta con el controlador
"""
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.config.database import get_db
from app.controllers.curso_controller import CursoController
from app.schemas.curso_schema import (
    CursoCreate,
    CursoUpdate,
    CursoResponse,
    CopiarCursosRequest,
    CopiarCursosResponse
)
from app.schemas.estudiante_curso_schema import CursoConEstudiantes

# Crear router con prefijo y etiquetas
router = APIRouter(
    prefix="/api/cursos",
    tags=["Cursos"]
)

@router.get(
    "/",
    response_model=List[CursoConEstudiantes],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los cursos con sus estudiantes",
    description="Obtiene una lista de todos los cursos registrados con sus estudiantes asignados. Por defecto filtra por el año actual. Usa gestion='all' para ver todos los años."
)
def listar_cursos(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    nivel: Optional[str] = Query(None, description="Filtrar por nivel (inicial, primaria, secundaria)"),
    gestion: Optional[str] = Query(None, description="Filtrar por gestión. Por defecto: año actual. Usa 'all' para ver todos"),
    db: Session = Depends(get_db)
):
    """
    Endpoint para listar todos los cursos con sus estudiantes y filtros opcionales.
    Por defecto filtra por el año actual. Para ver todos los años, usa gestion='all'
    """
    # Si no se especifica gestión, usar el año actual
    if gestion is None:
        gestion = str(datetime.now().year)
    # Si se especifica 'all', no filtrar por gestión
    elif gestion.lower() == 'all':
        gestion = None
    
    return CursoController.obtener_todos(db, skip=skip, limit=limit, nivel=nivel, gestion=gestion)

@router.get(
    "/por-gestion-nivel",
    response_model=List[CursoConEstudiantes],
    status_code=status.HTTP_200_OK,
    summary="Listar cursos por gestión y nivel",
    description="Endpoint específico para obtener cursos filtrados por gestión y opcionalmente por nivel. Por defecto usa el año actual."
)
def listar_cursos_por_gestion_nivel(
    gestion: Optional[str] = Query(None, description="Gestión a filtrar. Por defecto: año actual"),
    nivel: Optional[str] = Query(None, description="Filtrar por nivel (inicial, primaria, secundaria)"),
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    db: Session = Depends(get_db)
):
    """
    Endpoint para listar cursos filtrados por gestión y nivel.
    Por defecto filtra por el año actual.
    
    Ejemplos:
    - /api/cursos/por-gestion-nivel → Cursos del año actual
    - /api/cursos/por-gestion-nivel?gestion=2025 → Cursos de 2025
    - /api/cursos/por-gestion-nivel?gestion=2025&nivel=primaria → Cursos de primaria 2025
    - /api/cursos/por-gestion-nivel?nivel=secundaria → Cursos de secundaria del año actual
    """
    # Si no se especifica gestión, usar el año actual
    if gestion is None:
        gestion = str(datetime.now().year)
    
    return CursoController.obtener_todos(
        db, 
        skip=skip, 
        limit=limit, 
        nivel=nivel, 
        gestion=gestion
    )

@router.get(
    "/{id_curso}",
    response_model=CursoConEstudiantes,
    status_code=status.HTTP_200_OK,
    summary="Obtener curso por ID con sus estudiantes",
    description="Obtiene la información detallada de un curso específico incluyendo los estudiantes asignados"
)
def obtener_curso(
    id_curso: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener un curso por su ID con sus estudiantes
    """
    return CursoController.obtener_por_id(db, id_curso)

@router.post(
    "/",
    response_model=CursoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo curso",
    description="Registra un nuevo curso en el sistema"
)
def crear_curso(
    curso: CursoCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para crear un nuevo curso
    """
    return CursoController.crear(db, curso)

@router.put(
    "/{id_curso}",
    response_model=CursoResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar curso",
    description="Actualiza la información de un curso existente"
)
def actualizar_curso(
    id_curso: int,
    curso: CursoUpdate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para actualizar un curso existente
    """
    return CursoController.actualizar(db, id_curso, curso)

@router.delete(
    "/{id_curso}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar curso",
    description="Elimina un curso del sistema"
)
def eliminar_curso(
    id_curso: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para eliminar un curso
    """
    return CursoController.eliminar(db, id_curso)

@router.post(
    "/copiar-gestion",
    response_model=CopiarCursosResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Copiar cursos de una gestión a otra",
    description="Copia todos los cursos de una gestión origen a una gestión destino. No copia los estudiantes asignados, solo la estructura de cursos."
)
def copiar_cursos_gestion(
    request: CopiarCursosRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint para copiar todos los cursos de una gestión a otra.
    
    Ejemplo de uso:
    ```json
    {
        "gestion_origen": "2025",
        "gestion_destino": "2026"
    }
    ```
    
    Nota: Solo copia la estructura de cursos (nombre, nivel, gestión).
    No copia las asignaciones de estudiantes.
    """
    return CursoController.copiar_cursos_gestion(
        db, 
        request.gestion_origen, 
        request.gestion_destino
    )
