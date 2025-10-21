"""
Configuración de la conexión a la base de datos MySQL
usando SQLAlchemy y variables de entorno
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener credenciales de la base de datos
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "bienestar_estudiantil")
DB_PORT = os.getenv("DB_PORT", "3306")

# Construir URL de conexión para MySQL con pymysql
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear motor de base de datos
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Mostrar queries SQL en consola (útil para desarrollo)
    pool_pre_ping=True  # Verificar conexión antes de usar
)

# Crear sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Dependencia para obtener la sesión de base de datos
def get_db():
    """
    Generador que proporciona una sesión de base de datos
    y la cierra automáticamente después de su uso
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
