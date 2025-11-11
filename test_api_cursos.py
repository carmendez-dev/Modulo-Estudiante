"""
Script de prueba para los endpoints de Cursos e Inscripciones
Ejecutar después de iniciar el servidor: python run.py
"""
import requests
import json

# URL base de la API
BASE_URL = "http://localhost:8000"

def print_response(response, title):
    """Imprime la respuesta de manera formateada"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")

def test_cursos():
    """Prueba los endpoints de cursos"""
    print("\n" + "="*60)
    print("  PRUEBAS DE CURSOS")
    print("="*60)
    
    # 1. Crear un curso
    nuevo_curso = {
        "nombre_curso": "Primero A - Prueba",
        "nivel": "primaria",
        "gestion": "2024"
    }
    response = requests.post(f"{BASE_URL}/api/cursos/", json=nuevo_curso)
    print_response(response, "1. Crear Curso")
    curso_id = response.json().get("id_curso") if response.status_code == 201 else None
    
    # 2. Listar cursos
    response = requests.get(f"{BASE_URL}/api/cursos/")
    print_response(response, "2. Listar Cursos")
    
    # 3. Obtener curso por ID
    if curso_id:
        response = requests.get(f"{BASE_URL}/api/cursos/{curso_id}")
        print_response(response, f"3. Obtener Curso ID {curso_id}")
    
    # 4. Actualizar curso
    if curso_id:
        actualizar_curso = {
            "nombre_curso": "Primero A - Actualizado"
        }
        response = requests.put(f"{BASE_URL}/api/cursos/{curso_id}", json=actualizar_curso)
        print_response(response, f"4. Actualizar Curso ID {curso_id}")
    
    return curso_id

def test_estudiantes():
    """Prueba los endpoints de estudiantes y obtiene un ID"""
    print("\n" + "="*60)
    print("  PRUEBAS DE ESTUDIANTES")
    print("="*60)
    
    # Crear un estudiante de prueba
    nuevo_estudiante = {
        "nombres": "Juan Carlos",
        "apellido_paterno": "Pérez",
        "apellido_materno": "García",
        "ci": "12345678",
        "fecha_nacimiento": "2015-03-15",
        "direccion": "Av. Principal #123"
    }
    response = requests.post(f"{BASE_URL}/api/estudiantes/create", json=nuevo_estudiante)
    print_response(response, "Crear Estudiante de Prueba")
    estudiante_id = response.json().get("id_estudiante") if response.status_code == 201 else None
    
    # Listar estudiantes
    response = requests.get(f"{BASE_URL}/api/estudiantes/getAll")
    print_response(response, "Listar Estudiantes")
    
    # Si no se creó, intentar obtener el primer estudiante existente
    if not estudiante_id and response.status_code == 200:
        estudiantes = response.json()
        if estudiantes:
            estudiante_id = estudiantes[0].get("id_estudiante")
    
    return estudiante_id

def test_inscripciones(estudiante_id, curso_id):
    """Prueba los endpoints de inscripciones"""
    if not estudiante_id or not curso_id:
        print("\n⚠️ No se puede probar inscripciones sin estudiante_id y curso_id")
        return
    
    print("\n" + "="*60)
    print("  PRUEBAS DE INSCRIPCIONES")
    print("="*60)
    
    # 1. Inscribir estudiante
    inscripcion = {
        "id_estudiante": estudiante_id,
        "id_curso": curso_id
    }
    response = requests.post(f"{BASE_URL}/api/inscripciones/inscribir", json=inscripcion)
    print_response(response, "1. Inscribir Estudiante")
    
    # 2. Intentar inscribir de nuevo (debe fallar)
    response = requests.post(f"{BASE_URL}/api/inscripciones/inscribir", json=inscripcion)
    print_response(response, "2. Intentar Inscribir de Nuevo (debe fallar)")
    
    # 3. Obtener cursos del estudiante
    response = requests.get(f"{BASE_URL}/api/inscripciones/estudiante/{estudiante_id}/cursos")
    print_response(response, f"3. Cursos del Estudiante {estudiante_id}")
    
    # 4. Obtener estudiantes del curso
    response = requests.get(f"{BASE_URL}/api/inscripciones/curso/{curso_id}/estudiantes")
    print_response(response, f"4. Estudiantes del Curso {curso_id}")
    
    # 5. Desinscribir estudiante
    response = requests.delete(
        f"{BASE_URL}/api/inscripciones/desinscribir",
        params={"id_estudiante": estudiante_id, "id_curso": curso_id}
    )
    print_response(response, "5. Desinscribir Estudiante")
    
    # 6. Verificar que se desinscribió
    response = requests.get(f"{BASE_URL}/api/inscripciones/estudiante/{estudiante_id}/cursos")
    print_response(response, "6. Verificar Desinscripción (cursos vacíos)")

def test_health():
    """Prueba el endpoint de salud"""
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health Check")

def main():
    """Función principal que ejecuta todas las pruebas"""
    print("\n" + "="*60)
    print("  INICIANDO PRUEBAS DE LA API")
    print("  Asegúrate de que el servidor esté corriendo")
    print("="*60)
    
    try:
        # Probar conexión
        test_health()
        
        # Probar estudiantes y obtener un ID
        estudiante_id = test_estudiantes()
        
        # Probar cursos y obtener un ID
        curso_id = test_cursos()
        
        # Probar inscripciones
        test_inscripciones(estudiante_id, curso_id)
        
        print("\n" + "="*60)
        print("  ✅ PRUEBAS COMPLETADAS")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se puede conectar al servidor")
        print("   Asegúrate de que el servidor esté corriendo: python run.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == "__main__":
    main()
