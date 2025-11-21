"""
Controlador para inscripción masiva de estudiantes
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, status
from typing import List
from app.models.curso_model import Curso
from app.models.estudiante_model import Estudiante

class InscripcionMasivaController:
    """
    Controlador para operaciones de inscripción masiva
    """
    
    @staticmethod
    def obtener_gestiones_disponibles(db: Session) -> List[dict]:
        """
        Obtener lista de gestiones disponibles ordenadas descendentemente
        
        Args:
            db: Sesión de base de datos
            
        Returns:
            Lista de gestiones únicas
        """
        sql = text("SELECT DISTINCT gestion FROM cursos ORDER BY gestion DESC")
        result = db.execute(sql)
        
        gestiones = [{"gestion": row[0]} for row in result]
        
        if not gestiones:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron gestiones disponibles"
            )
        
        return gestiones
    
    @staticmethod
    def obtener_cursos_por_gestion(db: Session, gestion: str) -> List[dict]:
        """
        Obtener cursos de una gestión específica
        
        Args:
            db: Sesión de base de datos
            gestion: Año de gestión
            
        Returns:
            Lista de cursos con id, nombre y nivel
        """
        cursos = db.query(
            Curso.id_curso,
            Curso.nombre_curso,
            Curso.nivel
        ).filter(
            Curso.gestion == gestion
        ).order_by(
            Curso.nivel,
            Curso.nombre_curso
        ).all()
        
        if not cursos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontraron cursos para la gestión {gestion}"
            )
        
        return [
            {
                "id_curso": curso.id_curso,
                "nombre_curso": curso.nombre_curso,
                "nivel": curso.nivel
            }
            for curso in cursos
        ]
    
    @staticmethod
    def obtener_estudiantes_para_inscripcion(
        db: Session,
        id_curso_origen: int,
        gestion_destino: str
    ) -> List[dict]:
        """
        Obtener estudiantes de un curso origen con información de si ya están inscritos
        en la gestión destino
        
        Args:
            db: Sesión de base de datos
            id_curso_origen: ID del curso de origen
            gestion_destino: Gestión destino para verificar inscripciones
            
        Returns:
            Lista de estudiantes con información de inscripción
        """
        # Verificar que el curso origen existe
        curso_origen = db.query(Curso).filter(Curso.id_curso == id_curso_origen).first()
        if not curso_origen:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Curso con ID {id_curso_origen} no encontrado"
            )
        
        # Query SQL para obtener estudiantes con estado de inscripción
        sql = text("""
            SELECT 
                e.id_estudiante,
                e.ci,
                e.nombres,
                e.apellido_paterno,
                e.apellido_materno,
                (EXISTS (
                    SELECT 1
                    FROM estudiantes_cursos ec_new
                    JOIN cursos c_new ON ec_new.id_curso = c_new.id_curso
                    WHERE c_new.gestion = :gestion_destino
                    AND ec_new.id_estudiante = e.id_estudiante
                )) AS ya_inscrito
            FROM estudiantes e
            JOIN estudiantes_cursos ec_source ON e.id_estudiante = ec_source.id_estudiante
            WHERE ec_source.id_curso = :id_curso_origen
            AND e.estado_estudiante = 'Activo'
            ORDER BY e.apellido_paterno, e.apellido_materno, e.nombres
        """)
        
        result = db.execute(
            sql,
            {
                "id_curso_origen": id_curso_origen,
                "gestion_destino": gestion_destino
            }
        )
        
        estudiantes = [
            {
                "id_estudiante": row[0],
                "ci": row[1],
                "nombres": row[2],
                "apellido_paterno": row[3],
                "apellido_materno": row[4],
                "ya_inscrito": bool(row[5])
            }
            for row in result
        ]
        
        if not estudiantes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontraron estudiantes activos en el curso {curso_origen.nombre_curso}"
            )
        
        return estudiantes
    
    @staticmethod
    def inscribir_estudiantes_masivamente(
        db: Session,
        id_curso_destino: int,
        ids_estudiantes: List[int]
    ) -> dict:
        """
        Inscribir múltiples estudiantes a un curso
        
        Args:
            db: Sesión de base de datos
            id_curso_destino: ID del curso destino
            ids_estudiantes: Lista de IDs de estudiantes a inscribir
            
        Returns:
            Diccionario con información de la operación
        """
        # Verificar que el curso destino existe
        curso_destino = db.query(Curso).filter(Curso.id_curso == id_curso_destino).first()
        if not curso_destino:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Curso destino con ID {id_curso_destino} no encontrado"
            )
        
        # Verificar que todos los estudiantes existen y están activos
        estudiantes = db.query(Estudiante).filter(
            Estudiante.id_estudiante.in_(ids_estudiantes),
            Estudiante.estado_estudiante == 'Activo'
        ).all()
        
        if len(estudiantes) != len(ids_estudiantes):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Algunos estudiantes no existen o no están activos"
            )
        
        try:
            estudiantes_inscritos = 0
            estudiantes_ya_inscritos = 0
            
            for id_estudiante in ids_estudiantes:
                # Verificar si ya está inscrito
                ya_inscrito = db.execute(
                    text("""
                        SELECT 1 FROM estudiantes_cursos 
                        WHERE id_estudiante = :id_estudiante 
                        AND id_curso = :id_curso
                    """),
                    {"id_estudiante": id_estudiante, "id_curso": id_curso_destino}
                ).first()
                
                if ya_inscrito:
                    estudiantes_ya_inscritos += 1
                else:
                    # Inscribir estudiante
                    db.execute(
                        text("""
                            INSERT INTO estudiantes_cursos (id_estudiante, id_curso)
                            VALUES (:id_estudiante, :id_curso)
                        """),
                        {"id_estudiante": id_estudiante, "id_curso": id_curso_destino}
                    )
                    estudiantes_inscritos += 1
            
            db.commit()
            
            return {
                "mensaje": f"Inscripción masiva completada en {curso_destino.nombre_curso}",
                "estudiantes_inscritos": estudiantes_inscritos,
                "estudiantes_ya_inscritos": estudiantes_ya_inscritos,
                "total_procesados": len(ids_estudiantes)
            }
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al inscribir estudiantes: {str(e)}"
            )
