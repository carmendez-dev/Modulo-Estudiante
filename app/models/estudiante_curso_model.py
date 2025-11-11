"""
Modelo SQLAlchemy para la tabla estudiantes_cursos (relación muchos a muchos)
Define la relación entre estudiantes y cursos
"""
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.config.database import Base

# Tabla de asociación para la relación muchos a muchos
estudiantes_cursos = Table(
    'estudiantes_cursos',
    Base.metadata,
    Column('id_estudiante', Integer, ForeignKey('estudiantes.id_estudiante'), primary_key=True),
    Column('id_curso', Integer, ForeignKey('cursos.id_curso'), primary_key=True)
)
