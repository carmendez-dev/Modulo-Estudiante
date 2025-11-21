"""
Vista (Router) para los endpoints de inscripción masiva
"""
from fastapi import APIRouter, Depends, status, Query, Path
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.controllers.inscripcion_masiva_controller import InscripcionMasivaController
from app.schemas.inscripcion_masiva_schema import (
    GestionResponse,
    CursoSimpleResponse,
    EstudianteParaInscripcionResponse,
    InscripcionMasivaRequest,
    InscripcionMasivaResponse
)

# Crear router con prefijo y etiquetas
router = APIRouter(
    prefix="/api/inscripcion-masiva",
    tags=["Inscripción Masiva"]
)

@router.get(
    "/gestiones",
    response_model=List[GestionResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener gestiones disponibles",
    description="Obtiene la lista de gestiones (años académicos) disponibles ordenadas descendentemente"
)
def obtener_gestiones(
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener todas las gestiones disponibles.
    Útil para poblar un dropdown de selección de gestión.
    """
    return InscripcionMasivaController.obtener_gestiones_disponibles(db)

@router.get(
    "/cursos/{gestion}",
    response_model=List[CursoSimpleResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener cursos por gestión",
    description="Obtiene la lista de cursos de una gestión específica ordenados por nivel y nombre"
)
def obtener_cursos_por_gestion(
    gestion: str = Path(..., description="Gestión (año académico) a consultar"),
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener cursos de una gestión específica.
    Útil para poblar un dropdown de selección de curso origen.
    """
    return InscripcionMasivaController.obtener_cursos_por_gestion(db, gestion)

@router.get(
    "/estudiantes/{id_curso_origen}",
    response_model=List[EstudianteParaInscripcionResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener estudiantes de un curso para inscripción",
    description="Obtiene los estudiantes activos de un curso origen con información de si ya están inscritos en la gestión destino"
)
def obtener_estudiantes_para_inscripcion(
    id_curso_origen: int = Path(..., description="ID del curso de origen"),
    gestion_destino: str = Query(..., description="Gestión destino para verificar inscripciones"),
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener estudiantes de un curso origen.
    Incluye información de si el estudiante ya está inscrito en algún curso de la gestión destino.
    Solo retorna estudiantes con estado 'Activo'.
    """
    return InscripcionMasivaController.obtener_estudiantes_para_inscripcion(
        db, 
        id_curso_origen, 
        gestion_destino
    )

@router.post(
    "/inscribir",
    response_model=InscripcionMasivaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Inscribir múltiples estudiantes a un curso",
    description="Inscribe una lista de estudiantes a un curso destino. Omite estudiantes ya inscritos."
)
def inscribir_estudiantes_masivamente(
    request: InscripcionMasivaRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint para inscribir múltiples estudiantes a un curso.
    
    Ejemplo de uso:
    ```json
    {
        "id_curso_destino": 15,
        "ids_estudiantes": [1, 2, 3, 4, 5]
    }
    ```
    
    Nota: Si un estudiante ya está inscrito en el curso, se omite sin generar error.
    """
    return InscripcionMasivaController.inscribir_estudiantes_masivamente(
        db,
        request.id_curso_destino,
        request.ids_estudiantes
    )
