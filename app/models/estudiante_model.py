from sqlalchemy import Column, Integer, String, Date
from app.config.database import Base

class Estudiante(Base):
    __tablename__ = "estudiantes"
    
    # Campos de la tabla
    id_estudiante = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ci = Column(String(20), nullable=True)
    nombres = Column(String(50), nullable=False)
    apellido_paterno = Column(String(50), nullable=False)
    apellido_materno = Column(String(50), nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    direccion = Column(String(100), nullable=True)
    
    # Información del padre
    nombre_padre = Column(String(50), nullable=True)
    apellido_paterno_padre = Column(String(50), nullable=True)
    apellido_materno_padre = Column(String(50), nullable=True)
    telefono_padre = Column(String(20), nullable=True)
    
    # Información de la madre
    nombre_madre = Column(String(50), nullable=True)
    apellido_paterno_madre = Column(String(50), nullable=True)
    apellido_materno_madre = Column(String(50), nullable=True)
    telefono_madre = Column(String(20), nullable=True)
    
    def __repr__(self):
        return f"<Estudiante(id={self.id_estudiante}, nombres={self.nombres})>"
