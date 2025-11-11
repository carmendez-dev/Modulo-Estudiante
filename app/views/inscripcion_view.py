"""
Vista (Router) para los endpoints de inscripciones
Define las rutas HTTP para gestionar la relación many-to-many entre estudiantes y cursos
"""
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.controllers.inscripcion_controller import InscripcionController
from app.schemas.inscripcion_schema import InscripcionCreate
from app.schemas.curso_schema import CursoResponse
from app.schemas.estudiante_schema import EstudianteResponse

# Crear router con prefijo y etiquetas
router = APIRouter(
    prefix="/api/inscripciones",
    tags=["Inscripciones"]
)

@router.post(
    "/inscribir",
    status_code=status.HTTP_201_CREATED,
    summary="Inscribir estudiante a un curso",
    description="Crea una relación entre un estudiante y un curso"
)
def inscribir_estudiante(
    inscripcion: InscripcionCreate,
    db: Session = Depends(get_db)
):
    """Endpoint para inscribir un estudiante a un curso"""
    return InscripcionController.inscribir_estudiante(db, inscripcion)

@router.delete(
    "/desinscribir",
    status_code=status.HTTP_200_OK,
    summary="Desinscribir estudiante de un curso",
    description="Elimina la relación entre un estudiante y un curso"
)
def desinscribir_estudiante(
    id_estudiante: int = Query(..., description="ID del estudiante"),
    id_curso: int = Query(..., description="ID del curso"),
    db: Session = Depends(get_db)
):
    """Endpoint para desinscribir un estudiante de un curso"""
    return InscripcionController.desinscribir_estudiante(db, id_estudiante, id_curso)

@router.get(
    "/estudiante/{id_estudiante}/cursos",
    response_model=List[CursoResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener cursos de un estudiante",
    description="Lista todos los cursos en los que está inscrito un estudiante"
)
def obtener_cursos_por_estudiante(
    id_estudiante: int,
    db: Session = Depends(get_db)
):
    """Endpoint para obtener todos los cursos de un estudiante"""
    return InscripcionController.obtener_cursos_por_estudiante(db, id_estudiante)

@router.get(
    "/curso/{id_curso}/estudiantes",
    response_model=List[EstudianteResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener estudiantes de un curso",
    description="Lista todos los estudiantes inscritos en un curso"
)
def obtener_estudiantes_por_curso(
    id_curso: int,
    db: Session = Depends(get_db)
):
    """Endpoint para obtener todos los estudiantes de un curso"""
    return InscripcionController.obtener_estudiantes_por_curso(db, id_curso)
