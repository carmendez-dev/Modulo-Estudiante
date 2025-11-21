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

    @staticmethod
    def cambiar_estado(db: Session, id_estudiante: int, nuevo_estado: str) -> dict:
        """
        Cambiar el estado de un estudiante
        
        Args:
            db: Sesión de base de datos
            id_estudiante: ID del estudiante
            nuevo_estado: Nuevo estado (Activo, Abandono, Retirado)
            
        Returns:
            Diccionario con información del cambio
            
        Raises:
            HTTPException: Si el estudiante no existe
        """
        # Buscar estudiante
        estudiante = EstudianteController.obtener_por_id(db, id_estudiante)
        
        # Guardar estado anterior
        estado_anterior = estudiante.estado_estudiante
        
        # Validar que el estado sea diferente
        if estado_anterior == nuevo_estado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El estudiante ya tiene el estado '{nuevo_estado}'"
            )
        
        try:
            # Cambiar estado
            estudiante.estado_estudiante = nuevo_estado
            db.commit()
            db.refresh(estudiante)
            
            return {
                "mensaje": f"Estado del estudiante cambiado de '{estado_anterior}' a '{nuevo_estado}'",
                "id_estudiante": id_estudiante,
                "estado_anterior": estado_anterior,
                "estado_nuevo": nuevo_estado
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al cambiar estado del estudiante: {str(e)}"
            )

    @staticmethod
    def obtener_por_gestion(
        db: Session,
        gestion: str,
        nivel: Optional[str] = None,
        id_curso: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[dict]:
        """
        Obtener estudiantes filtrados por gestión, con filtros opcionales por nivel y curso
        
        Args:
            db: Sesión de base de datos
            gestion: Gestión a filtrar (año académico)
            nivel: Filtrar por nivel (inicial, primaria, secundaria) - opcional
            id_curso: Filtrar por ID de curso específico - opcional
            skip: Número de registros a saltar
            limit: Número máximo de registros
            
        Returns:
            Lista de estudiantes con SOLO los cursos de la gestión especificada
        """
        from app.models.curso_model import Curso
        from sqlalchemy.orm import joinedload
        
        # Query base de estudiantes con sus cursos
        query = db.query(Estudiante).join(Estudiante.cursos)
        
        # Filtrar por gestión
        query = query.filter(Curso.gestion == gestion)
        
        # Filtrar por nivel si se especifica
        if nivel:
            query = query.filter(Curso.nivel == nivel)
        
        # Filtrar por curso específico si se especifica
        if id_curso:
            query = query.filter(Curso.id_curso == id_curso)
        
        # Eliminar duplicados y aplicar paginación
        estudiantes = query.distinct().offset(skip).limit(limit).all()
        
        # Filtrar los cursos de cada estudiante para mostrar solo los de la gestión especificada
        resultado = []
        for estudiante in estudiantes:
            # Crear diccionario con datos del estudiante
            est_dict = {
                "id_estudiante": estudiante.id_estudiante,
                "ci": estudiante.ci,
                "nombres": estudiante.nombres,
                "apellido_paterno": estudiante.apellido_paterno,
                "apellido_materno": estudiante.apellido_materno,
                "fecha_nacimiento": estudiante.fecha_nacimiento,
                "direccion": estudiante.direccion,
                "estado_estudiante": estudiante.estado_estudiante,
                "nombre_padre": estudiante.nombre_padre,
                "apellido_paterno_padre": estudiante.apellido_paterno_padre,
                "apellido_materno_padre": estudiante.apellido_materno_padre,
                "telefono_padre": estudiante.telefono_padre,
                "nombre_madre": estudiante.nombre_madre,
                "apellido_paterno_madre": estudiante.apellido_paterno_madre,
                "apellido_materno_madre": estudiante.apellido_materno_madre,
                "telefono_madre": estudiante.telefono_madre,
                "cursos": []
            }
            
            # Filtrar cursos por gestión (y opcionalmente por nivel e id_curso)
            for curso in estudiante.cursos:
                if curso.gestion == gestion:
                    if nivel and curso.nivel != nivel:
                        continue
                    if id_curso and curso.id_curso != id_curso:
                        continue
                    
                    est_dict["cursos"].append({
                        "id_curso": curso.id_curso,
                        "nombre_curso": curso.nombre_curso,
                        "nivel": curso.nivel,
                        "gestion": curso.gestion
                    })
            
            resultado.append(est_dict)
        
        return resultado

    @staticmethod
    def obtener_por_estado(
        db: Session,
        estado: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Estudiante]:
        """
        Obtener estudiantes filtrados por estado
        
        Args:
            db: Sesión de base de datos
            estado: Estado a filtrar (Activo, Retirado, Abandono)
            skip: Número de registros a saltar
            limit: Número máximo de registros
            
        Returns:
            Lista de estudiantes con el estado especificado
        """
        # Validar que el estado sea válido
        estados_validos = ["Activo", "Retirado", "Abandono"]
        if estado not in estados_validos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estado inválido. Estados válidos: {', '.join(estados_validos)}"
            )
        
        # Filtrar estudiantes por estado
        estudiantes = db.query(Estudiante).filter(
            Estudiante.estado_estudiante == estado
        ).offset(skip).limit(limit).all()
        
        return estudiantes
