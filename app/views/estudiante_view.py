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
    EstudianteResponse
)

# Crear router con prefijo y etiquetas
router = APIRouter(
    prefix="/api/estudiantes",
    tags=["Estudiantes"]
)

@router.get(
    "/",
    response_model=List[EstudianteResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los estudiantes",
    description="Obtiene una lista de todos los estudiantes registrados con paginación opcional"
)
def listar_estudiantes(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    db: Session = Depends(get_db)
):
    """
    Endpoint para listar todos los estudiantes
    """
    return EstudianteController.obtener_todos(db, skip=skip, limit=limit)

@router.get(
    "/{id_estudiante}",
    response_model=EstudianteResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener estudiante por ID",
    description="Obtiene la información detallada de un estudiante específico"
)
def obtener_estudiante(
    id_estudiante: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener un estudiante por su ID
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
