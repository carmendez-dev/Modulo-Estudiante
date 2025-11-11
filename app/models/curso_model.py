from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.config.database import Base
from app.models.estudiante_model import estudiantes_cursos
import enum

class NivelEnum(str, enum.Enum):
    """Enum para los niveles educativos"""
    INICIAL = "inicial"
    PRIMARIA = "primaria"
    SECUNDARIA = "secundaria"

class Curso(Base):
    __tablename__ = "cursos"
    
    # Campos de la tabla
    id_curso = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_curso = Column(String(100), nullable=False)
    nivel = Column(SQLEnum(NivelEnum), nullable=False)
    gestion = Column(String(10), nullable=False)
    
    # Relación many-to-many con Estudiante
    estudiantes = relationship(
        "Estudiante",
        secondary=estudiantes_cursos,
        back_populates="cursos"
    )
    
    def __repr__(self):
        return f"<Curso(id={self.id_curso}, nombre={self.nombre_curso}, nivel={self.nivel})>"
