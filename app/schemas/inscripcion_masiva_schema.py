"""
Esquemas Pydantic para inscripción masiva de estudiantes
"""
from pydantic import BaseModel, Field
from typing import List, Optional

class GestionResponse(BaseModel):
    """
    Esquema para respuesta de gestiones disponibles
    """
    gestion: str = Field(..., description="Año de gestión")
    
    class Config:
        from_attributes = True

class CursoSimpleResponse(BaseModel):
    """
    Esquema simplificado de curso para selección
    """
    id_curso: int = Field(..., description="ID del curso")
    nombre_curso: str = Field(..., description="Nombre del curso")
    nivel: str = Field(..., description="Nivel del curso")
    
    class Config:
        from_attributes = True

class EstudianteParaInscripcionResponse(BaseModel):
    """
    Esquema de estudiante con información de inscripción
    """
    id_estudiante: int = Field(..., description="ID del estudiante")
    ci: Optional[str] = Field(None, description="Cédula de identidad")
    nombres: str = Field(..., description="Nombres del estudiante")
    apellido_paterno: str = Field(..., description="Apellido paterno")
    apellido_materno: str = Field(..., description="Apellido materno")
    ya_inscrito: bool = Field(..., description="Si el estudiante ya está inscrito en la gestión destino")
    
    class Config:
        from_attributes = True

class InscripcionMasivaRequest(BaseModel):
    """
    Esquema para inscribir múltiples estudiantes a un curso
    """
    id_curso_destino: int = Field(..., description="ID del curso destino donde se inscribirán los estudiantes")
    ids_estudiantes: List[int] = Field(..., min_items=1, description="Lista de IDs de estudiantes a inscribir")

class InscripcionMasivaResponse(BaseModel):
    """
    Esquema de respuesta para inscripción masiva
    """
    mensaje: str = Field(..., description="Mensaje de confirmación")
    estudiantes_inscritos: int = Field(..., description="Cantidad de estudiantes inscritos exitosamente")
    estudiantes_ya_inscritos: int = Field(..., description="Cantidad de estudiantes que ya estaban inscritos")
    total_procesados: int = Field(..., description="Total de estudiantes procesados")
