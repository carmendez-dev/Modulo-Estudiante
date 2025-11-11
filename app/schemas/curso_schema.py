"""
Esquemas Pydantic para validación de datos de cursos
Define la estructura de entrada y salida de datos en la API
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Literal

class CursoBase(BaseModel):
    """
    Esquema base con campos comunes de curso
    """
    nombre_curso: str = Field(..., min_length=1, max_length=50, description="Nombre del curso")
    nivel: Literal['inicial', 'primaria', 'secundaria'] = Field(..., description="Nivel educativo")
    gestion: str = Field(..., min_length=1, max_length=20, description="Gestión o año académico")
    
    @validator('nombre_curso', 'gestion')
    def validar_no_vacio(cls, v):
        """Validar que los campos obligatorios no estén vacíos"""
        if v and not v.strip():
            raise ValueError('El campo no puede estar vacío')
        return v.strip() if v else v
    
    @validator('gestion')
    def validar_gestion(cls, v):
        """Validar formato de gestión (ejemplo: 2024, 2024-1, etc.)"""
        if v and not v.strip():
            raise ValueError('La gestión no puede estar vacía')
        return v.strip()

class CursoCreate(CursoBase):
    """
    Esquema para crear un nuevo curso
    Hereda todos los campos de CursoBase
    """
    pass

class CursoUpdate(BaseModel):
    """
    Esquema para actualizar un curso
    Todos los campos son opcionales
    """
    nombre_curso: Optional[str] = Field(None, min_length=1, max_length=50)
    nivel: Optional[Literal['inicial', 'primaria', 'secundaria']] = None
    gestion: Optional[str] = Field(None, min_length=1, max_length=20)
    
    @validator('nombre_curso', 'gestion')
    def validar_no_vacio(cls, v):
        """Validar que los campos no estén vacíos si se proporcionan"""
        if v is not None and not v.strip():
            raise ValueError('El campo no puede estar vacío')
        return v.strip() if v else v

class CursoResponse(CursoBase):
    """
    Esquema de respuesta que incluye el ID del curso
    """
    id_curso: int = Field(..., description="ID único del curso")
    
    class Config:
        from_attributes = True  # Permite crear desde objetos ORM
