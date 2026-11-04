from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Incidencias - Subsonic Festival")

# Configuración CORS para que el Frontend pueda comunicarse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELOS DE DATOS ---
class IncidenciaCreate(BaseModel):
    idUsuario: int = Field(..., description="ID del usuario que reporta la incidencia")
    titulo: str = Field(min_length=5, max_length=100, description="Breve resumen del problema")
    descripcion: str = Field(min_length=10, description="Detalle completo de la incidencia")

class Incidencia(IncidenciaCreate):
    idIncidencia: int
    fechaRegistro: str
    estado: str = "Pendiente" # Preparado para que el admin lo cambie luego (AC-06)

# --- BASE DE DATOS SIMULADA ---
incidencias_db = []
contador_id = 1

# --- ENDPOINTS ---

# US-019-AC-01, AC-02, AC-03, AC-09: Registrar incidencia
@app.post("/api/incidencias", response_model=dict)
def registrar_incidencia(incidencia: IncidenciaCreate):
    global contador_id
    
    try:
        nueva_incidencia = Incidencia(
            idIncidencia=contador_id,
            idUsuario=incidencia.idUsuario,
            titulo=incidencia.titulo,
            descripcion=incidencia.descripcion,
            fechaRegistro=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            estado="Pendiente"
        )
        incidencias_db.append(nueva_incidencia)
        contador_id += 1
        
        # AC-03 y AC-08: El sistema informa que se ha registrado correctamente
        return {
            "mensaje": "Incidencia registrada correctamente. Nuestro equipo la revisará pronto.",
            "idIncidencia": nueva_incidencia.idIncidencia
        }
    except Exception as e:
        # AC-09: Si se produce un error, el sistema informa y evita inconsistencias
        raise HTTPException(status_code=500, detail="Error interno al guardar la incidencia.")

# Subtarea: Permitir consultar la información de una incidencia (Vista del usuario)
@app.get("/api/incidencias/usuario/{id_usuario}", response_model=List[Incidencia])
def listar_incidencias_usuario(id_usuario: int):
    # Filtramos las incidencias para devolver solo las del usuario que pregunta
    mis_incidencias = [inc for inc in incidencias_db if inc.idUsuario == id_usuario]
    return mis_incidencias