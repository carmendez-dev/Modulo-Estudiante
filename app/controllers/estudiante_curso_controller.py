"""
Controlador para gestionar la relación estudiantes-cursos
Maneja asignaciones, desasignaciones y consultas
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.estudiante_model import Estudiante
from app.models.curso_model import Curso
from typing import List

class EstudianteCursoController:
    """
    Controlador para operaciones de asignación estudiante-curso
    """
    
    @staticmethod
    def asignar_estudiante_a_curso(db: Session, id_estudiante: int, id_curso: int) -> dict:
        """
        Asignar un estudiante a un curso
        
        Args:
            db: Sesión de base de datos
            id_estudiante: ID del estudiante
            id_curso: ID del curso
            
        Returns:
            Mensaje de confirmación
            
        Raises:
            HTTPException: Si el estudiante o curso no existe, o si ya está asignado
        """
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
        curso = db.query(Curso).filter(Curso.id_curso == id_curso).first()
        
        if not curso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Curso con ID {id_curso} no encontrado"
            )
        
        # Verificar si ya está asignado
        if curso in estudiante.cursos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El estudiante ya está asignado a este curso"
            )
        
        try:
            # Asignar estudiante al curso
            estudiante.cursos.append(curso)
            db.commit()
            
            return {
                "mensaje": f"Estudiante {estudiante.nombres} {estudiante.apellido_paterno} asignado al curso {curso.nombre_curso}",
                "id_estudiante": id_estudiante,
                "id_curso": id_curso
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al asignar estudiante al curso: {str(e)}"
            )
    
    @staticmethod
    def desasignar_estudiante_de_curso(db: Session, id_estudiante: int, id_curso: int) -> dict:
        """
        Desasignar un estudiante de un curso
        
        Args:
            db: Sesión de base de datos
            id_estudiante: ID del estudiante
            id_curso: ID del curso
            
        Returns:
            Mensaje de confirmación
            
        Raises:
            HTTPException: Si el estudiante o curso no existe, o si no está asignado
        """
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
        curso = db.query(Curso).filter(Curso.id_curso == id_curso).first()
        
        if not curso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Curso con ID {id_curso} no encontrado"
            )
        
        # Verificar si está asignado
        if curso not in estudiante.cursos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El estudiante no está asignado a este curso"
            )
        
        try:
            # Desasignar estudiante del curso
            estudiante.cursos.remove(curso)
            db.commit()
            
            return {
                "mensaje": f"Estudiante {estudiante.nombres} {estudiante.apellido_paterno} desasignado del curso {curso.nombre_curso}",
                "id_estudiante": id_estudiante,
                "id_curso": id_curso
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al desasignar estudiante del curso: {str(e)}"
            )
    
    @staticmethod
    def obtener_estudiantes_de_curso(db: Session, id_curso: int) -> Curso:
        """
        Obtener todos los estudiantes asignados a un curso
        
        Args:
            db: Sesión de base de datos
            id_curso: ID del curso
            
        Returns:
            Curso con lista de estudiantes
            
        Raises:
            HTTPException: Si el curso no existe
        """
        curso = db.query(Curso).filter(Curso.id_curso == id_curso).first()
        
        if not curso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Curso con ID {id_curso} no encontrado"
            )
        
        return curso
    
    @staticmethod
    def obtener_cursos_de_estudiante(db: Session, id_estudiante: int) -> Estudiante:
        """
        Obtener todos los cursos asignados a un estudiante
        
        Args:
            db: Sesión de base de datos
            id_estudiante: ID del estudiante
            
        Returns:
            Estudiante con lista de cursos
            
        Raises:
            HTTPException: Si el estudiante no existe
        """
        estudiante = db.query(Estudiante).filter(
            Estudiante.id_estudiante == id_estudiante
        ).first()
        
        if not estudiante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con ID {id_estudiante} no encontrado"
            )
        
        return estudiante

    @staticmethod
    def obtener_estudiantes_habilitados_de_curso(db: Session, id_curso: int) -> List[dict]:
        """
        Obtener estudiantes habilitados de un curso específico
        
        Args:
            db: Sesión de base de datos
            id_curso: ID del curso
            
        Returns:
            Lista de diccionarios con id_estudiante y nombre_completo de estudiantes habilitados
            
        Raises:
            HTTPException: Si el curso no existe
        """
        curso = db.query(Curso).filter(Curso.id_curso == id_curso).first()
        
        if not curso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Curso con ID {id_curso} no encontrado"
            )
        
        # Filtrar solo estudiantes habilitados
        estudiantes_habilitados = [
            {
                "id_estudiante": est.id_estudiante,
                "nombre_completo": f"{est.nombres} {est.apellido_paterno} {est.apellido_materno}",
                "estado_estudiante": est.estado_estudiante
            }
            for est in curso.estudiantes
            if est.estado_estudiante == 'habilitado'
        ]
        
        return estudiantes_habilitados
    
    @staticmethod
    def asignar_estudiantes_masivo(db: Session, id_curso: int, ids_estudiantes: List[int]) -> dict:
        """
        Asignar múltiples estudiantes a un curso de una vez
        
        Args:
            db: Sesión de base de datos
            id_curso: ID del curso
            ids_estudiantes: Lista de IDs de estudiantes
            
        Returns:
            Diccionario con mensaje, total asignado y lista de IDs asignados
        """
        # Verificar que el curso existe
        curso = db.query(Curso).filter(Curso.id_curso == id_curso).first()
        
        if not curso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Curso con ID {id_curso} no encontrado"
            )
        
        estudiantes_asignados = []
        errores = []
        
        try:
            for id_estudiante in ids_estudiantes:
                # Verificar que el estudiante existe
                estudiante = db.query(Estudiante).filter(
                    Estudiante.id_estudiante == id_estudiante
                ).first()
                
                if not estudiante:
                    errores.append(f"Estudiante con ID {id_estudiante} no encontrado")
                    continue
                
                # Verificar si ya está asignado
                if curso in estudiante.cursos:
                    errores.append(f"Estudiante con ID {id_estudiante} ya está asignado al curso")
                    continue
                
                # Asignar estudiante al curso
                estudiante.cursos.append(curso)
                estudiantes_asignados.append(id_estudiante)
            
            db.commit()
            
            return {
                "mensaje": f"Se asignaron {len(estudiantes_asignados)} estudiantes al curso {curso.nombre_curso}",
                "id_curso": id_curso,
                "total_asignados": len(estudiantes_asignados),
                "estudiantes_asignados": estudiantes_asignados,
                "errores": errores
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al asignar estudiantes masivamente: {str(e)}"
            )
