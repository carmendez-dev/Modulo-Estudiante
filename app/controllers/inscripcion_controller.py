from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.estudiante_model import Estudiante
from app.models.curso_model import Curso
from app.schemas.inscripcion_schema import InscripcionCreate
from typing import List

class InscripcionController:
    """Controlador para gestionar inscripciones (relación many-to-many)"""
    
    @staticmethod
    def inscribir_estudiante(db: Session, inscripcion: InscripcionCreate) -> dict:
        """Inscribe un estudiante a un curso"""
        # Verificar que el estudiante existe
        estudiante = db.query(Estudiante).filter(
            Estudiante.id_estudiante == inscripcion.id_estudiante
        ).first()
        
        if not estudiante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con ID {inscripcion.id_estudiante} no encontrado"
            )
        
        # Verificar que el curso existe
        curso = db.query(Curso).filter(
            Curso.id_curso == inscripcion.id_curso
        ).first()
        
        if not curso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Curso con ID {inscripcion.id_curso} no encontrado"
            )
        
        # Verificar que la inscripción no existe ya
        if curso in estudiante.cursos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El estudiante ya está inscrito en el curso '{curso.nombre_curso}'"
            )
        
        try:
            # Agregar la relación
            estudiante.cursos.append(curso)
            db.commit()
            db.refresh(estudiante)
            
            return {
                "mensaje": f"Estudiante '{estudiante.nombres} {estudiante.apellido_paterno}' inscrito exitosamente en '{curso.nombre_curso}'",
                "id_estudiante": inscripcion.id_estudiante,
                "id_curso": inscripcion.id_curso
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al inscribir estudiante: {str(e)}"
            )
    
    @staticmethod
    def desinscribir_estudiante(db: Session, id_estudiante: int, id_curso: int) -> dict:
        """Desinscribe un estudiante de un curso"""
        # Verificar que el estudiante existe
        estudiante = db.query(Estudiante).filter(
            Estudiante.id_estudiante == id_estudiante
        ).first()
        
        if not estudiante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con ID {id_estudiante} no encontrado"
            )
        
        # Verificar que el curso existe
        curso = db.query(Curso).filter(
            Curso.id_curso == id_curso
        ).first()
        
        if not curso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Curso con ID {id_curso} no encontrado"
            )
        
        # Verificar que la inscripción existe
        if curso not in estudiante.cursos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El estudiante no está inscrito en el curso '{curso.nombre_curso}'"
            )
        
        try:
            # Remover la relación
            estudiante.cursos.remove(curso)
            db.commit()
            db.refresh(estudiante)
            
            return {
                "mensaje": f"Estudiante '{estudiante.nombres} {estudiante.apellido_paterno}' desinscrito exitosamente de '{curso.nombre_curso}'",
                "id_estudiante": id_estudiante,
                "id_curso": id_curso
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al desinscribir estudiante: {str(e)}"
            )
    
    @staticmethod
    def obtener_cursos_por_estudiante(db: Session, id_estudiante: int) -> List[Curso]:
        """Obtiene todos los cursos de un estudiante"""
        # Verificar que el estudiante existe
        estudiante = db.query(Estudiante).filter(
            Estudiante.id_estudiante == id_estudiante
        ).first()
        
        if not estudiante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con ID {id_estudiante} no encontrado"
            )
        
        return estudiante.cursos
    
    @staticmethod
    def obtener_estudiantes_por_curso(db: Session, id_curso: int) -> List[Estudiante]:
        """Obtiene todos los estudiantes de un curso"""
        # Verificar que el curso existe
        curso = db.query(Curso).filter(
            Curso.id_curso == id_curso
        ).first()
        
        if not curso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Curso con ID {id_curso} no encontrado"
            )
        
        return curso.estudiantes
