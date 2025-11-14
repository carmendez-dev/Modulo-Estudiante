"""
Módulo de modelos
Importar en el orden correcto para evitar importaciones circulares
"""
from app.models.estudiante_model import Estudiante, estudiantes_cursos
from app.models.curso_model import Curso

__all__ = ['Estudiante', 'Curso', 'estudiantes_cursos']
