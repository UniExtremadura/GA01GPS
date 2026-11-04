from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Servicios - Subsonic Festival")

# Configuración CORS fundamental para que tu archivo HTML/JS pueda hacer peticiones a este backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELOS DE DATOS ---
class Servicio(BaseModel):
    id: int
    nombre: str
    categoria: str
    descripcion: str
    precio: float
    disponible: bool

class AdquisicionRequest(BaseModel):
    idUsuario: int
    idServicio: int

# --- BASE DE DATOS SIMULADA ---
servicios_db = [
    Servicio(id=1, nombre="Zona de descanso", categoria="Bienestar", descripcion="Acceso a un espacio tranquilo para descansar entre actuaciones.", precio=12.0, disponible=True),
    Servicio(id=2, nombre="Taquilla inteligente", categoria="Comodidad", descripcion="Guarda tus pertenencias de forma segura durante el festival.", precio=8.0, disponible=True),
    Servicio(id=3, nombre="Consigna premium", categoria="Comodidad", descripcion="Espacio de consigna ampliado con acceso durante toda la jornada.", precio=18.0, disponible=True),
    Servicio(id=4, nombre="Lanzadera nocturna", categoria="Transporte", descripcion="Traslado de vuelta al centro al finalizar los conciertos.", precio=6.0, disponible=False)
]

# Tabla intermedia simulada para guardar las compras de cada usuario
adquisiciones_db = []

# --- ENDPOINTS (RUTAS) ---

# US-013-AC-01: El usuario puede consultar los servicios disponibles
@app.get("/api/servicios", response_model=List[Servicio])
def listar_servicios():
    """Devuelve la lista completa de servicios para que el frontend pinte las tarjetas."""
    return servicios_db

# US-013-AC-04, 05, 06 y 07: Adquisición y validación
@app.post("/api/servicios/adquirir")
def adquirir_servicio(req: AdquisicionRequest):
    """Procesa la compra comprobando disponibilidad."""
    
    # 1. Buscar el servicio en la base de datos
    servicio = next((s for s in servicios_db if s.id == req.idServicio), None)
    
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado.")
        
    # 2. US-013-AC-04 y 05: Comprobar que el servicio está disponible
    if not servicio.disponible:
        raise HTTPException(
            status_code=400, 
            detail="Este servicio no está disponible actualmente y no se puede adquirir."
        )
        
    # 3. US-013-AC-06: Registrar la adquisición vinculándola al usuario
    nueva_adquisicion = {
        "idUsuario": req.idUsuario,
        "idServicio": req.idServicio,
        "servicio_nombre": servicio.nombre
    }
    adquisiciones_db.append(nueva_adquisicion)
    
    # 4. US-013-AC-07: Informar de que se ha realizado correctamente
    return {
        "mensaje": f"Servicio '{servicio.nombre}' adquirido correctamente.",
        "registro": nueva_adquisicion
    }