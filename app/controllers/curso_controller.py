"""
Controlador con la lógica de negocio para gestionar cursos
Maneja las operaciones CRUD en la base de datos
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.curso_model import Curso
from app.schemas.curso_schema import CursoCreate, CursoUpdate
from typing import List, Optional

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
    def obtener_cursos_por_gestion(db: Session, gestion: str) -> List[dict]:
        """
        Obtener cursos simplificados de un año específico (solo nombre y nivel)
        
        Args:
            db: Sesión de base de datos
            gestion: Año o gestión a filtrar
            
        Returns:
            Lista de diccionarios con id_curso, nombre_curso y nivel
        """
        cursos = db.query(Curso).filter(Curso.gestion == gestion).all()
        
        return [
            {
                "id_curso": curso.id_curso,
                "nombre_curso": curso.nombre_curso,
                "nivel": curso.nivel
            }
            for curso in cursos
        ]
    
    @staticmethod
    def crear_masivo(db: Session, cursos_data: List[CursoCreate]) -> dict:
        """
        Crear múltiples cursos de una vez
        
        Args:
            db: Sesión de base de datos
            cursos_data: Lista de datos de cursos a crear
            
        Returns:
            Diccionario con mensaje, total creado y lista de cursos creados
        """
        cursos_creados = []
        
        try:
            for curso_data in cursos_data:
                nuevo_curso = Curso(**curso_data.model_dump())
                db.add(nuevo_curso)
                cursos_creados.append(nuevo_curso)
            
            db.commit()
            
            # Refrescar todos los cursos creados para obtener sus IDs
            for curso in cursos_creados:
                db.refresh(curso)
            
            return {
                "mensaje": f"Se crearon {len(cursos_creados)} cursos exitosamente",
                "total_creados": len(cursos_creados),
                "cursos_creados": cursos_creados
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear cursos masivamente: {str(e)}"
            )
