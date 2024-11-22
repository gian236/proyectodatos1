# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import crud, models, database

# Crear la aplicación FastAPI
app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL del frontend React
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Incluir el enrutador de usuarios
app.include_router(crud.router, prefix="/usuarios", tags=["usuarios"])

# Ruta raíz
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Mi Préstamo S.A."}
