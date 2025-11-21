"""
Vista (Router) para los endpoints de importación/exportación Excel
"""
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.controllers.excel_controller import ExcelController
from datetime import datetime

# Crear router
router = APIRouter(
    prefix="/api/excel",
    tags=["Excel - Importar/Exportar"]
)

@router.get(
    "/exportar-estudiantes",
    summary="Exportar todos los estudiantes a Excel",
    description="Descarga un archivo Excel con todos los estudiantes registrados"
)
def exportar_estudiantes(db: Session = Depends(get_db)):
    """
    Endpoint para exportar todos los estudiantes a un archivo Excel
    """
    excel_file = ExcelController.exportar_estudiantes(db)
    
    # Generar nombre de archivo con fecha
    fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"estudiantes_{fecha_actual}.xlsx"
    
    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get(
    "/exportar-estudiante/{id_estudiante}",
    summary="Exportar un estudiante específico a Excel",
    description="Descarga un archivo Excel con los datos de un estudiante específico y sus cursos"
)
def exportar_estudiante_por_id(
    id_estudiante: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para exportar un estudiante específico a un archivo Excel.
    Incluye una hoja con los datos del estudiante y otra con sus cursos.
    """
    excel_file = ExcelController.exportar_estudiante_por_id(db, id_estudiante)
    
    # Generar nombre de archivo con ID del estudiante
    filename = f"estudiante_{id_estudiante}.xlsx"
    
    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.post(
    "/importar-estudiantes",
    summary="Importar estudiantes desde Excel",
    description="Sube un archivo Excel para crear o actualizar estudiantes masivamente"
)
def importar_estudiantes(
    file: UploadFile = File(..., description="Archivo Excel con datos de estudiantes"),
    db: Session = Depends(get_db)
):
    """
    Endpoint para importar estudiantes desde un archivo Excel.
    Si el CI ya existe, actualiza el estudiante.
    Si el CI no existe, crea un nuevo estudiante.
    """
    return ExcelController.importar_estudiantes(db, file)

@router.get(
    "/plantilla-estudiantes",
    summary="Descargar plantilla Excel",
    description="Descarga una plantilla Excel con el formato correcto para importar estudiantes"
)
def descargar_plantilla():
    """
    Endpoint para descargar una plantilla Excel vacía con instrucciones
    """
    plantilla = ExcelController.descargar_plantilla()
    
    return StreamingResponse(
        plantilla,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=plantilla_estudiantes.xlsx"}
    )
