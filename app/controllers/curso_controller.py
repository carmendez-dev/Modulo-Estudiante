"""
Controlador con la lógica de negocio para gestionar cursos
Maneja las operaciones CRUD en la base de datos
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.curso_model import Curso
from app.schemas.curso_schema import CursoCreate, CursoUpdate
from typing import List, Optional
from sqlalchemy import text

class CursoController:
    """
    Controlador para operaciones CRUD de cursos
    """
    
    @staticmethod
    def obtener_todos(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        nivel: Optional[str] = None,
        gestion: Optional[str] = None
    ) -> List[Curso]:
        """
        Obtener lista de todos los cursos con paginación y filtros opcionales
        
        Args:
            db: Sesión de base de datos
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            nivel: Filtrar por nivel (opcional)
            gestion: Filtrar por gestión (opcional)
            
        Returns:
            Lista de cursos
        """
        query = db.query(Curso)
        
        # Aplicar filtros si se proporcionan
        if nivel:
            query = query.filter(Curso.nivel == nivel)
        if gestion:
            query = query.filter(Curso.gestion == gestion)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def obtener_por_id(db: Session, id_curso: int) -> Curso:
        """
        Obtener un curso por su ID
        
        Args:
            db: Sesión de base de datos
            id_curso: ID del curso a buscar
            
        Returns:
            Objeto Curso
            
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
    def crear(db: Session, curso_data: CursoCreate) -> Curso:
        """
        Crear un nuevo curso
        
        Args:
            db: Sesión de base de datos
            curso_data: Datos del curso a crear
            
        Returns:
            Curso creado
        """
        # Crear instancia del modelo
        nuevo_curso = Curso(**curso_data.model_dump())
        
        try:
            # Agregar a la sesión y confirmar
            db.add(nuevo_curso)
            db.commit()
            db.refresh(nuevo_curso)
            return nuevo_curso
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear curso: {str(e)}"
            )
    
    @staticmethod
    def actualizar(
        db: Session, 
        id_curso: int, 
        curso_data: CursoUpdate
    ) -> Curso:
        """
        Actualizar un curso existente
        
        Args:
            db: Sesión de base de datos
            id_curso: ID del curso a actualizar
            curso_data: Nuevos datos del curso
            
        Returns:
            Curso actualizado
            
        Raises:
            HTTPException: Si el curso no existe
        """
        # Buscar curso
        curso = CursoController.obtener_por_id(db, id_curso)
        
        # Actualizar solo los campos proporcionados
        update_data = curso_data.model_dump(exclude_unset=True)
        
        for campo, valor in update_data.items():
            setattr(curso, campo, valor)
        
        try:
            db.commit()
            db.refresh(curso)
            return curso
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar curso: {str(e)}"
            )
    
    @staticmethod
    def eliminar(db: Session, id_curso: int) -> dict:
        """
        Eliminar un curso
        
        Args:
            db: Sesión de base de datos
            id_curso: ID del curso a eliminar
            
        Returns:
            Mensaje de confirmación
            
        Raises:
            HTTPException: Si el curso no existe
        """
        # Buscar curso
        curso = CursoController.obtener_por_id(db, id_curso)
        
        try:
            db.delete(curso)
            db.commit()
            return {"mensaje": f"Curso con ID {id_curso} eliminado exitosamente"}
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al eliminar curso: {str(e)}"
            )
    
    @staticmethod
    def copiar_cursos_gestion(
        db: Session, 
        gestion_origen: str, 
        gestion_destino: str
    ) -> dict:
        """
        Copiar todos los cursos de una gestión a otra
        
        Args:
            db: Sesión de base de datos
            gestion_origen: Gestión de origen (ej: 2025)
            gestion_destino: Gestión de destino (ej: 2026)
            
        Returns:
            Diccionario con información de la operación
            
        Raises:
            HTTPException: Si hay errores en la operación
        """
        try:
            # Verificar que existan cursos en la gestión origen
            cursos_origen = db.query(Curso).filter(
                Curso.gestion == gestion_origen
            ).all()
            
            if not cursos_origen:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontraron cursos en la gestión {gestion_origen}"
                )
            
            # Verificar si ya existen cursos en la gestión destino
            cursos_destino_existentes = db.query(Curso).filter(
                Curso.gestion == gestion_destino
            ).count()
            
            if cursos_destino_existentes > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existen {cursos_destino_existentes} cursos en la gestión {gestion_destino}. Elimínelos primero si desea reemplazarlos."
                )
            
            # Copiar cursos usando SQL directo para mejor rendimiento
            sql = text("""
                INSERT INTO cursos (nombre_curso, nivel, gestion)
                SELECT nombre_curso, nivel, :gestion_destino
                FROM cursos 
                WHERE gestion = :gestion_origen
            """)
            
            result = db.execute(
                sql, 
                {
                    "gestion_origen": gestion_origen,
                    "gestion_destino": gestion_destino
                }
            )
            
            db.commit()
            
            cursos_copiados = result.rowcount
            
            return {
                "mensaje": f"Cursos copiados exitosamente de {gestion_origen} a {gestion_destino}",
                "cursos_copiados": cursos_copiados,
                "gestion_origen": gestion_origen,
                "gestion_destino": gestion_destino
            }
            
        except HTTPException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al copiar cursos: {str(e)}"
            )
