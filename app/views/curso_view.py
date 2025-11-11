"""
Vista (Router) para los endpoints de cursos
Define las rutas HTTP y conecta con el controlador
"""
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.controllers.curso_controller import CursoController
from app.schemas.curso_schema import (
    CursoCreate,
    CursoUpdate,
    CursoResponse
)

# Crear router con prefijo y etiquetas
router = APIRouter(
    prefix="/api/cursos",
    tags=["Cursos"]
)

@router.get(
    "/",
    response_model=List[CursoResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los cursos",
    description="Obtiene una lista de todos los cursos registrados con paginación opcional"
)
def listar_cursos(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    db: Session = Depends(get_db)
):
    """Endpoint para listar todos los cursos"""
    return CursoController.obtener_todos(db, skip=skip, limit=limit)

@router.get(
    "/{id_curso}",
    response_model=CursoResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener curso por ID",
    description="Obtiene la información detallada de un curso específico"
)
def obtener_curso(
    id_curso: int,
    db: Session = Depends(get_db)
):
    """Endpoint para obtener un curso por su ID"""
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
    """Endpoint para crear un nuevo curso"""
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
    """Endpoint para actualizar un curso existente"""
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
    """Endpoint para eliminar un curso"""
    return CursoController.eliminar(db, id_curso)
