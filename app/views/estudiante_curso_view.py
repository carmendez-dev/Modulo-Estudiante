"""
Vista (Router) para los endpoints de asignación estudiantes-cursos
Define las rutas HTTP para gestionar las relaciones
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.controllers.estudiante_curso_controller import EstudianteCursoController
from app.schemas.estudiante_curso_schema import (
    AsignarEstudianteCurso,
    AsignacionResponse,
    CursoConEstudiantes,
    EstudianteConCursos,
    AsignarEstudiantesCursoMasivo,
    AsignacionMasivaResponse
)

# Crear router con prefijo y etiquetas
router = APIRouter(
    prefix="/api/asignaciones",
    tags=["Asignaciones Estudiante-Curso"]
)

@router.post(
    "/",
    response_model=AsignacionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Asignar estudiante a curso",
    description="Asigna un estudiante a un curso específico"
)
def asignar_estudiante_a_curso(
    asignacion: AsignarEstudianteCurso,
    db: Session = Depends(get_db)
):
    """
    Endpoint para asignar un estudiante a un curso
    """
    return EstudianteCursoController.asignar_estudiante_a_curso(
        db, 
        asignacion.id_estudiante, 
        asignacion.id_curso
    )

@router.delete(
    "/",
    response_model=AsignacionResponse,
    status_code=status.HTTP_200_OK,
    summary="Desasignar estudiante de curso",
    description="Elimina la asignación de un estudiante de un curso"
)
def desasignar_estudiante_de_curso(
    asignacion: AsignarEstudianteCurso,
    db: Session = Depends(get_db)
):
    """
    Endpoint para desasignar un estudiante de un curso
    """
    return EstudianteCursoController.desasignar_estudiante_de_curso(
        db,
        asignacion.id_estudiante,
        asignacion.id_curso
    )

@router.get(
    "/curso/{id_curso}",
    response_model=CursoConEstudiantes,
    status_code=status.HTTP_200_OK,
    summary="Obtener estudiantes de un curso",
    description="Obtiene todos los estudiantes asignados a un curso específico"
)
def obtener_estudiantes_de_curso(
    id_curso: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener todos los estudiantes de un curso
    """
    return EstudianteCursoController.obtener_estudiantes_de_curso(db, id_curso)

@router.get(
    "/estudiante/{id_estudiante}",
    response_model=EstudianteConCursos,
    status_code=status.HTTP_200_OK,
    summary="Obtener cursos de un estudiante",
    description="Obtiene todos los cursos asignados a un estudiante específico"
)
def obtener_cursos_de_estudiante(
    id_estudiante: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener todos los cursos de un estudiante
    """
    return EstudianteCursoController.obtener_cursos_de_estudiante(db, id_estudiante)

@router.get(
    "/curso/{id_curso}/estudiantes-habilitados",
    response_model=List[dict],
    status_code=status.HTTP_200_OK,
    summary="Obtener estudiantes habilitados de un curso",
    description="Obtiene solo los estudiantes con estado 'habilitado' de un curso específico (id_estudiante y nombre_completo)"
)
def obtener_estudiantes_habilitados_de_curso(
    id_curso: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener estudiantes habilitados de un curso
    """
    return EstudianteCursoController.obtener_estudiantes_habilitados_de_curso(db, id_curso)

@router.post(
    "/masivo",
    response_model=AsignacionMasivaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Asignar múltiples estudiantes a un curso",
    description="Asigna una lista de estudiantes a un curso específico de una sola vez"
)
def asignar_estudiantes_masivo(
    asignacion: AsignarEstudiantesCursoMasivo,
    db: Session = Depends(get_db)
):
    """
    Endpoint para asignar múltiples estudiantes a un curso
    """
    return EstudianteCursoController.asignar_estudiantes_masivo(
        db, 
        asignacion.id_curso, 
        asignacion.ids_estudiantes
    )
