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
    CursoSimple,
    CursosCreateBulk,
    CursosCreateBulkResponse
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
    nivel: Optional[str] = Query(None, description="Filtrar por nivel (INICIAL, PRIMARIA, SECUNDARIA)"),
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

@router.get(
    "/gestion/{gestion}",
    response_model=List[CursoSimple],
    status_code=status.HTTP_200_OK,
    summary="Obtener cursos de un año específico",
    description="Obtiene solo nombre y nivel de todos los cursos de una gestión específica (ejemplo: 2024)"
)
def obtener_cursos_por_gestion(
    gestion: str,
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener cursos simplificados de un año específico
    """
    return CursoController.obtener_cursos_por_gestion(db, gestion)

@router.post(
    "/masivo",
    response_model=CursosCreateBulkResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear múltiples cursos",
    description="Crea múltiples cursos de una sola vez recibiendo una lista de cursos"
)
def crear_cursos_masivo(
    cursos_bulk: CursosCreateBulk,
    db: Session = Depends(get_db)
):
    """
    Endpoint para crear múltiples cursos a la vez
    """
    return CursoController.crear_masivo(db, cursos_bulk.cursos)
