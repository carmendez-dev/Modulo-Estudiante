from pydantic import BaseModel, Field

class InscripcionBase(BaseModel):
    """Schema base para inscripciones"""
    id_estudiante: int = Field(..., description="ID del estudiante a inscribir")
    id_curso: int = Field(..., description="ID del curso")

class InscripcionCreate(InscripcionBase):
    """Schema para crear una nueva inscripción"""
    pass

class InscripcionResponse(InscripcionBase):
    """Schema de respuesta para inscripciones"""
    
    class Config:
        from_attributes = True
