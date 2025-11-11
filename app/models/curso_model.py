"""
Modelo SQLAlchemy para la tabla cursos
Define la estructura de la tabla en la base de datos
"""
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.config.database import Base
from app.models.estudiante_model import estudiantes_cursos

class Curso(Base):
    """
    Modelo de la tabla cursos en la base de datos
    """
    __tablename__ = "cursos"
    
    # Campos de la tabla
    id_curso = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_curso = Column(String(50), nullable=False)
    nivel = Column(Enum('inicial', 'primaria', 'secundaria', name='nivel_enum'), nullable=False)
    gestion = Column(String(20), nullable=False)
    
    # Relación con estudiantes (muchos a muchos)
    estudiantes = relationship(
        "Estudiante",
        secondary=estudiantes_cursos,
        back_populates="cursos",
        lazy="joined"
    )
    
    def __repr__(self):
        return f"<Curso(id={self.id_curso}, nombre={self.nombre_curso}, nivel={self.nivel})>"
