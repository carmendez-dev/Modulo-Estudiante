from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.estudiante_model import Estudiante
from app.schemas.estudiante_schema import EstudianteCreate, EstudianteUpdate
from typing import List, Optional

class EstudianteController:
    @staticmethod
    def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Estudiante]:
        return db.query(Estudiante).offset(skip).limit(limit).all()
    
    @staticmethod
    def obtener_por_id(db: Session, id_estudiante: int) -> Estudiante:
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
    def crear(db: Session, estudiante_data: EstudianteCreate) -> Estudiante:
        # Crear instancia del modelo
        nuevo_estudiante = Estudiante(**estudiante_data.model_dump())
        
        try:
            # Agregar a la sesión y confirmar
            db.add(nuevo_estudiante)
            db.commit()
            db.refresh(nuevo_estudiante)
            return nuevo_estudiante
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear estudiante: {str(e)}"
            )
    
    @staticmethod
    def actualizar(
        db: Session, 
        id_estudiante: int, 
        estudiante_data: EstudianteUpdate
    ) -> Estudiante:
        # Buscar estudiante
        estudiante = EstudianteController.obtener_por_id(db, id_estudiante)
        
        # Actualizar solo los campos proporcionados
        update_data = estudiante_data.model_dump(exclude_unset=True)
        
        for campo, valor in update_data.items():
            setattr(estudiante, campo, valor)
        
        try:
            db.commit()
            db.refresh(estudiante)
            return estudiante
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar estudiante: {str(e)}"
            )
    
    @staticmethod
    def eliminar(db: Session, id_estudiante: int) -> dict:
        # Buscar estudiante
        estudiante = EstudianteController.obtener_por_id(db, id_estudiante)
        
        try:
            db.delete(estudiante)
            db.commit()
            return {"mensaje": f"Estudiante con ID {id_estudiante} eliminado exitosamente"}
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al eliminar estudiante: {str(e)}"
            )
