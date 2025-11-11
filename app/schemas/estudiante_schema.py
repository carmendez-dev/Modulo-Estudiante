from __future__ import annotations
from pydantic import BaseModel, Field, validator
from typing import Optional, List, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from app.schemas.curso_schema import CursoResponseBase

class EstudianteBase(BaseModel):
    ci: Optional[str] = Field(None, max_length=20, description="Cédula de identidad")
    nombres: str = Field(..., min_length=1, max_length=50, description="Nombres del estudiante")
    apellido_paterno: str = Field(..., min_length=1, max_length=50, description="Apellido paterno")
    apellido_materno: str = Field(..., min_length=1, max_length=50, description="Apellido materno")
    fecha_nacimiento: Optional[date] = Field(None, description="Fecha de nacimiento")
    direccion: Optional[str] = Field(None, max_length=100, description="Dirección")
    
    # Información del padre
    nombre_padre: Optional[str] = Field(None, max_length=50)
    apellido_paterno_padre: Optional[str] = Field(None, max_length=50)
    apellido_materno_padre: Optional[str] = Field(None, max_length=50)
    telefono_padre: Optional[str] = Field(None, max_length=20)
    
    # Información de la madre
    nombre_madre: Optional[str] = Field(None, max_length=50)
    apellido_paterno_madre: Optional[str] = Field(None, max_length=50)
    apellido_materno_madre: Optional[str] = Field(None, max_length=50)
    telefono_madre: Optional[str] = Field(None, max_length=20)
    
    @validator('nombres', 'apellido_paterno', 'apellido_materno')
    def validar_no_vacio(cls, v):
        """Validar que los campos obligatorios no estén vacíos"""
        if v and not v.strip():
            raise ValueError('El campo no puede estar vacío')
        return v.strip() if v else v

class EstudianteCreate(EstudianteBase):
    pass

class EstudianteUpdate(BaseModel):
    ci: Optional[str] = Field(None, max_length=20)
    nombres: Optional[str] = Field(None, min_length=1, max_length=50)
    apellido_paterno: Optional[str] = Field(None, min_length=1, max_length=50)
    apellido_materno: Optional[str] = Field(None, min_length=1, max_length=50)
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = Field(None, max_length=100)
    nombre_padre: Optional[str] = Field(None, max_length=50)
    apellido_paterno_padre: Optional[str] = Field(None, max_length=50)
    apellido_materno_padre: Optional[str] = Field(None, max_length=50)
    telefono_padre: Optional[str] = Field(None, max_length=20)
    nombre_madre: Optional[str] = Field(None, max_length=50)
    apellido_paterno_madre: Optional[str] = Field(None, max_length=50)
    apellido_materno_madre: Optional[str] = Field(None, max_length=50)
    telefono_madre: Optional[str] = Field(None, max_length=20)

class EstudianteResponseBase(EstudianteBase):
    """Schema base de respuesta sin cursos (para evitar ciclos)"""
    id_estudiante: int = Field(..., description="ID único del estudiante")
    
    class Config:
        from_attributes = True

class EstudianteResponse(EstudianteResponseBase):
    """Schema de respuesta completo con cursos"""
    cursos: List['CursoResponseBase'] = []
    
    class Config:
        from_attributes = True

# Reconstruir los modelos para resolver referencias circulares
from app.schemas.curso_schema import CursoResponseBase, CursoResponse

EstudianteResponse.model_rebuild()
CursoResponse.model_rebuild()

