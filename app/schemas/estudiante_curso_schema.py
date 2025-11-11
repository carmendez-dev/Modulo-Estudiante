"""
Esquemas Pydantic para la relación estudiantes-cursos
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

# Schemas simplificados para evitar referencias circulares

class CursoSimple(BaseModel):
    """Schema simplificado de curso para mostrar en estudiante"""
    id_curso: int
    nombre_curso: str
    nivel: str
    gestion: str
    
    class Config:
        from_attributes = True

class EstudianteSimple(BaseModel):
    """Schema simplificado de estudiante para mostrar en curso"""
    id_estudiante: int
    ci: Optional[str] = None
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    
    class Config:
        from_attributes = True

class EstudianteConCursos(BaseModel):
    """Schema de estudiante con sus cursos asignados"""
    id_estudiante: int
    ci: Optional[str] = None
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    nombre_padre: Optional[str] = None
    apellido_paterno_padre: Optional[str] = None
    apellido_materno_padre: Optional[str] = None
    telefono_padre: Optional[str] = None
    nombre_madre: Optional[str] = None
    apellido_paterno_madre: Optional[str] = None
    apellido_materno_madre: Optional[str] = None
    telefono_madre: Optional[str] = None
    cursos: List[CursoSimple] = []
    
    class Config:
        from_attributes = True

class CursoConEstudiantes(BaseModel):
    """Schema de curso con sus estudiantes asignados"""
    id_curso: int
    nombre_curso: str
    nivel: str
    gestion: str
    estudiantes: List[EstudianteSimple] = []
    
    class Config:
        from_attributes = True

class AsignarEstudianteCurso(BaseModel):
    """Schema para asignar un estudiante a un curso"""
    id_estudiante: int = Field(..., description="ID del estudiante")
    id_curso: int = Field(..., description="ID del curso")

class AsignacionResponse(BaseModel):
    """Schema de respuesta para asignaciones"""
    mensaje: str
    id_estudiante: int
    id_curso: int
