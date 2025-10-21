"""
Script para probar la conexión a la base de datos
"""
from app.config.database import engine, SessionLocal
from app.models.estudiante_model import Estudiante
from sqlalchemy import text

def test_connection():
    """Probar conexión a la base de datos"""
    try:
        # Probar conexión
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Conexión a MySQL exitosa!")
            
        # Probar sesión
        db = SessionLocal()
        try:
            # Contar estudiantes
            count = db.query(Estudiante).count()
            print(f"Tabla 'estudiantes' encontrada. Total de registros: {count}")
        finally:
            db.close()
            
        print("\nTodo está configurado correctamente!")
        print("Puedes iniciar el servidor con: uvicorn app.main:app --reload")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nVerifica:")
        print("1. MySQL está corriendo")
        print("2. La base de datos 'bienestar_estudiantil' existe")
        print("3. Las credenciales en .env son correctas")

if __name__ == "__main__":
    test_connection()
