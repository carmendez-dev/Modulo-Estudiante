"""
Aplicación principal FastAPI
Configura la aplicación, middlewares y rutas
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.views import estudiante_view, curso_view, inscripcion_view
from app.config.database import engine, Base

# Crear tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

# Crear instancia de FastAPI
app = FastAPI(
    title="API Bienestar Estudiantil",
    description="API REST para gestión de estudiantes con arquitectura MVC",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir peticiones desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los headers
)

# Incluir routers
app.include_router(estudiante_view.router)
app.include_router(curso_view.router)
app.include_router(inscripcion_view.router)

# Ruta raíz
@app.get("/", tags=["Root"])
def root():
    """
    Endpoint raíz de bienvenida
    """
    return {
        "mensaje": "API Bienestar Estudiantil",
        "version": "1.0.0",
        "documentacion": "/docs"
    }

# Endpoint de salud
@app.get("/health", tags=["Health"])
def health_check():
    """
    Endpoint para verificar el estado de la API
    """
    return {"status": "ok", "mensaje": "API funcionando correctamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
