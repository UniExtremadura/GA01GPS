from typing import List
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Header

app = FastAPI(title="API Adquisición de Servicios - Subsonic Festival (US-013)")

# --- MODELOS DE DATOS ---
class Servicio(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float
    disponible: bool

class AdquisicionRequest(BaseModel):
    servicio_id: int = Field(..., description="ID del servicio que se desea adquirir")

class AdquisicionServicio(BaseModel):
    id_adquisicion: int
    usuario_id: int
    servicio: Servicio
    estado_operacion: str

# MODIFICACIÓN: BASE DE DATOS EN MEMORIA DE EJEMPLO PARA SERVICIOS Y REGISTRO DE ADQUISICIONES
DB_SERVICIOS = [
    Servicio(id=1, nombre="Zona de Acampada VIP", descripcion="Acceso exclusivo con servicios", precio=45.0, disponible=True),
    Servicio(id=2, nombre="Locker / Taquilla", descripcion="Taquilla segura para pertenencias", precio=15.0, disponible=False) # No disponible para probar US-013-AC-05
]

DB_ADQUISICIONES: List[AdquisicionServicio] = []
contador_adquisicion = 1

# --- CRITERIO US-013-AC-01: CONSULTAR SERVICIOS DISPONIBLES ---
@app.get("/api/adquisicion/servicios", response_model=List[Servicio])
def listar_servicios_disponibles():
    # MODIFICACIÓN: PERMITIR AL USUARIO CONSULTAR LOS SERVICIOS DISPONIBLES PARA ADQUISICIÓN
    return DB_SERVICIOS

# --- CRITERIO US-013-AC-02 Y AC-03: CONSULTAR DETALLE Y PRECIO ANTES DE CONFIRMAR ---
@app.get("/api/adquisicion/servicios/{servicio_id}", response_model=Servicio)
def consultar_detalle_servicio(servicio_id: int):
    # MODIFICACIÓN: SELECCIONAR Y MOSTRAR LA INFORMACIÓN Y EL PRECIO DEL SERVICIO ANTES DE LA ADQUISICIÓN
    for servicio in DB_SERVICIOS:
        if servicio.id == servicio_id:
            return servicio
    raise HTTPException(status_code=404, detail="El servicio seleccionado no existe.")

# --- CRITERIOS US-013-AC-04, AC-05, AC-06 Y AC-07: PROCESO DE ADQUISICIÓN Y ASOCIACIÓN ---
@app.post("/api/adquisicion/comprar", response_model=dict)
def adquirir_servicio(request: AdquisicionRequest, usuario_id: int = Header(..., description="ID del usuario autenticado")):
    global contador_adquisicion
    
    # MODIFICACIÓN: BUSCAR EL SERVICIO SELECCIONADO POR EL USUARIO (US-013-AC-02)
    servicio_encontrado = None
    for servicio in DB_SERVICIOS:
        if servicio.id == request.servicio_id:
            servicio_encontrado = servicio
            break
            
    if not servicio_encontrado:
        raise HTTPException(status_code=404, detail="El servicio seleccionado no existe.")
        
    # MODIFICACIÓN: COMPROBAR QUE EL SERVICIO ESTÁ DISPONIBLE ANTES DE COMPLETAR LA OPERACIÓN (US-013-AC-04)
    # MODIFICACIÓN: IMPEDIR LA ADQUISICIÓN E INFORMAR SI NO ESTÁ DISPONIBLE (US-013-AC-05)
    if not servicio_encontrado.disponible:
        raise HTTPException(
            status_code=400,
            detail="Error: El servicio no se encuentra disponible actualmente. No se puede completar la adquisición."
        )
        
    # MODIFICACIÓN: REGISTRAR LA ADQUISICIÓN Y ASOCIAR EL SERVICIO A LA CUENTA DEL USUARIO (US-013-AC-06)
    nueva_adquisicion = AdquisicionServicio(
        id_adquisicion=contador_adquisicion,
        usuario_id=usuario_id,
        servicio=servicio_encontrado,
        estado_operacion="COMPLETADA"
    )
    DB_ADQUISICIONES.append(nueva_adquisicion)
    contador_adquisicion += 1
    
    # MODIFICACIÓN: INFORMAR AL USUARIO DE QUE LA ADQUISICIÓN SE HA REALIZADO CORRECTAMENTE (US-013-AC-07)
    return {
        "mensaje": "La adquisición se ha realizado correctamente.",
        "resultado": "EXITO",
        "adquisicion": nueva_adquisicion
    }