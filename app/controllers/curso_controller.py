from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.curso_model import Curso
from app.schemas.curso_schema import CursoCreate, CursoUpdate
from typing import List

class CursoController:
    """Controlador para la gestión de cursos"""
    
    @staticmethod
    def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Curso]:
        """Obtiene todos los cursos con paginación"""
        return db.query(Curso).offset(skip).limit(limit).all()
    
    @staticmethod
    def obtener_por_id(db: Session, id_curso: int) -> Curso:
        """Obtiene un curso por su ID"""
        curso = db.query(Curso).filter(
            Curso.id_curso == id_curso
        ).first()
        
        if not curso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Curso con ID {id_curso} no encontrado"
            )
        
        return curso
    
    @staticmethod
    def crear(db: Session, curso_data: CursoCreate) -> Curso:
        """Crea un nuevo curso"""
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
        """Actualiza un curso existente"""
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
        """Elimina un curso (borrado físico)"""
        # Buscar curso
        curso = CursoController.obtener_por_id(db, id_curso)
        
        try:
            # Borrado físico
            db.delete(curso)
            db.commit()
            return {"mensaje": f"Curso con ID {id_curso} eliminado exitosamente"}
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al eliminar curso: {str(e)}"
            )
