from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List, TYPE_CHECKING
from app.models.curso_model import NivelEnum

if TYPE_CHECKING:
    from app.schemas.estudiante_schema import EstudianteResponseBase

class CursoBase(BaseModel):
    nombre_curso: str = Field(..., min_length=1, max_length=100, description="Nombre del curso")
    nivel: NivelEnum = Field(..., description="Nivel educativo: inicial, primaria o secundaria")
    gestion: str = Field(..., min_length=4, max_length=10, description="Gestión/año del curso (ej: 2024)")

class CursoCreate(CursoBase):
    """Schema para crear un nuevo curso"""
    pass

class CursoUpdate(BaseModel):
    """Schema para actualizar un curso (todos los campos opcionales)"""
    nombre_curso: Optional[str] = Field(None, min_length=1, max_length=100)
    nivel: Optional[NivelEnum] = None
    gestion: Optional[str] = Field(None, min_length=4, max_length=10)

class CursoResponseBase(CursoBase):
    """Schema base de respuesta sin estudiantes (para evitar ciclos)"""
    id_curso: int = Field(..., description="ID único del curso")
    
    class Config:
        from_attributes = True

class CursoResponse(CursoResponseBase):
    """Schema de respuesta completo con estudiantes"""
    estudiantes: List['EstudianteResponseBase'] = []
    
    class Config:
        from_attributes = True
