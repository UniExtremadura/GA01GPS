from typing import List
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException

app = FastAPI(title="API Servicios - Subsonic Festival (US-012)")

# --- MODELO DE DATOS PARA LOS SERVICIOS ---
class Servicio(BaseModel):
    id: int = Field(..., description="Identificador único del servicio")
    nombre: str = Field(..., min_length=2, description="Nombre del servicio")
    descripcion: str = Field(..., description="Información detallada sobre el servicio")
    precio: float = Field(..., ge=0, description="Precio del servicio")
    disponible: bool = Field(True, description="Estado de disponibilidad del servicio")

# MODIFICACIÓN: BASE DE DATOS EN MEMORIA DE EJEMPLO PARA LOS SERVICIOS DEL FESTIVAL
DB_SERVICIOS = [
    Servicio(id=1, nombre="Zona de Acampada VIP", descripcion="Acceso a zona de camping exclusiva con baños privados y electricidad.", precio=45.0, disponible=True),
    Servicio(id=2, nombre="Locker / Taquilla", descripcion="Taquilla segura para guardar objetos personales durante el festival.", precio=15.0, disponible=True),
    Servicio(id=3, nombre="Parking Oficial", descripcion="Plaza de aparcamiento vigilada cercana a los escenarios principales.", precio=25.0, disponible=True)
]

# --- CRITERIO US-012-AC-01, AC-02, AC-04 Y AC-05: CONSULTAR LISTADO DE SERVICIOS ---
@app.get("/api/servicios", response_model=List[Servicio])
def listar_servicios():
    # MODIFICACIÓN: VERIFICAR SI EXISTEN SERVICIOS DISPONIBLES EN EL SISTEMA (US-012-AC-05)
    if not DB_SERVICIOS:
        raise HTTPException(
            status_code=404, 
            detail="Actualmente no existen servicios disponibles en la plataforma."
        )
    
    # MODIFICACIÓN: MOSTRAR EL LISTADO COMPLETO CON LA INFORMACIÓN CORRESPONDIENTE (US-012-AC-01, AC-02, AC-04)
    return DB_SERVICIOS

# --- CRITERIO US-012-AC-03 Y AC-04: CONSULTAR INFORMACIÓN DETALLADA DE UN SERVICIO ---
@app.get("/api/servicios/{servicio_id}", response_model=Servicio)
def consultar_detalle_servicio(servicio_id: int):
    # MODIFICACIÓN: BUSCAR EL SERVICIO ESPECÍFICO SELECCIONADO POR SU ID
    for servicio in DB_SERVICIOS:
        if servicio.id == servicio_id:
            # MODIFICACIÓN: RETORNAR LOS DATOS REGISTRADOS PARA EL SERVICIO CONCRETO (US-012-AC-04)
            return servicio
            
    # MODIFICACIÓN: LANZAR ERROR SI EL SERVICIO SELECCIONADO NO EXISTE
    raise HTTPException(
        status_code=404, 
        detail="El servicio seleccionado no se encuentra registrado o no existe."
    )