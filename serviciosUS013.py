import os
from threading import Lock

import httpx
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field
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


class ServicioDatos(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    nombre: str = Field(min_length=2, max_length=100)
    categoria: str = Field(min_length=2, max_length=60)
    descripcion: str = Field(min_length=5, max_length=500)
    precio: float = Field(ge=0, allow_inf_nan=False, strict=True)
    disponible: bool = Field(default=True, strict=True)

# --- BASE DE DATOS SIMULADA ---
servicios_db = [
    Servicio(id=1, nombre="Zona de descanso", categoria="Bienestar", descripcion="Acceso a un espacio tranquilo para descansar entre actuaciones.", precio=12.0, disponible=True),
    Servicio(id=2, nombre="Taquilla inteligente", categoria="Comodidad", descripcion="Guarda tus pertenencias de forma segura durante el festival.", precio=8.0, disponible=True),
    Servicio(id=3, nombre="Consigna premium", categoria="Comodidad", descripcion="Espacio de consigna ampliado con acceso durante toda la jornada.", precio=18.0, disponible=True),
    Servicio(id=4, nombre="Lanzadera nocturna", categoria="Transporte", descripcion="Traslado de vuelta al centro al finalizar los conciertos.", precio=6.0, disponible=False)
]

# Tabla intermedia simulada para guardar las compras de cada usuario
adquisiciones_db = []
_bloqueo = Lock()
URL_SESION = os.getenv("SUBSONIC_URL_SESION", "http://127.0.0.1:8000").rstrip("/")


def verificar_administrador(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Inicia sesión para gestionar servicios.")
    try:
        respuesta = httpx.get(
            f"{URL_SESION}/api/privado", headers={"Authorization": authorization}, timeout=4,
        )
        if respuesta.status_code == 401:
            raise HTTPException(401, "Tu sesión no es válida. Vuelve a iniciar sesión.")
        respuesta.raise_for_status()
        sesion = respuesta.json()
        if not isinstance(sesion, dict) or not isinstance(sesion.get("rol"), str):
            raise ValueError("Respuesta de sesión incompleta.")
    except (httpx.HTTPError, ValueError) as error:
        raise HTTPException(503, "No se pudo verificar la sesión.") from error
    if sesion["rol"] != "admin":
        raise HTTPException(403, "Se requieren permisos de administrador.")


@app.exception_handler(RequestValidationError)
async def validar_solicitud(request, exc):
    if not request.url.path.startswith("/api/admin/servicios"):
        return await request_validation_exception_handler(request, exc)
    return JSONResponse(status_code=400, content={
        "mensaje": "Revisa los datos del servicio.",
        "errores": [
            {"campo": str(error["loc"][-1]), "mensaje": error["msg"]}
            for error in exc.errors()
        ],
    })


def buscar_servicio(servicio_id: int) -> tuple[int, Servicio]:
    for indice, servicio in enumerate(servicios_db):
        if servicio.id == servicio_id:
            return indice, servicio
    raise HTTPException(404, "Servicio no encontrado.")


def validar_nombre(nombre: str, excluir_id: int | None = None):
    if any(s.id != excluir_id and s.nombre.casefold() == nombre.casefold() for s in servicios_db):
        raise HTTPException(409, "Ya existe un servicio con ese nombre.")


ruta_admin = "/api/admin/servicios"
permisos_admin = [Depends(verificar_administrador)]


@app.get(ruta_admin, response_model=list[Servicio], dependencies=permisos_admin)
def listar_servicios_admin():
    with _bloqueo:
        return list(servicios_db)


@app.get(ruta_admin + "/{servicio_id}", response_model=Servicio, dependencies=permisos_admin)
def detalle_servicio_admin(servicio_id: int):
    with _bloqueo:
        return buscar_servicio(servicio_id)[1]


@app.post(ruta_admin, response_model=Servicio, status_code=201, dependencies=permisos_admin)
def registrar_servicio(datos: ServicioDatos):
    with _bloqueo:
        validar_nombre(datos.nombre)
        nuevo = Servicio(id=max((s.id for s in servicios_db), default=0) + 1, **datos.model_dump())
        servicios_db.append(nuevo)
        return nuevo


@app.put(ruta_admin + "/{servicio_id}", response_model=Servicio, dependencies=permisos_admin)
def modificar_servicio(servicio_id: int, datos: ServicioDatos):
    with _bloqueo:
        indice, _ = buscar_servicio(servicio_id)
        validar_nombre(datos.nombre, excluir_id=servicio_id)
        actualizado = Servicio(id=servicio_id, **datos.model_dump())
        servicios_db[indice] = actualizado
        return actualizado


@app.delete(ruta_admin + "/{servicio_id}", response_model=Servicio, dependencies=permisos_admin)
def deshabilitar_servicio(servicio_id: int):
    with _bloqueo:
        indice, servicio = buscar_servicio(servicio_id)
        actualizado = servicio.model_copy(update={"disponible": False})
        servicios_db[indice] = actualizado
        return actualizado

# --- ENDPOINTS (RUTAS) ---

# US-013-AC-01: El usuario puede consultar los servicios disponibles
@app.get("/api/servicios", response_model=List[Servicio])
def listar_servicios():
    """Devuelve la lista completa de servicios para que el frontend pinte las tarjetas."""
    with _bloqueo:
        return list(servicios_db)

# US-013-AC-04, 05, 06 y 07: Adquisición y validación
@app.post("/api/servicios/adquirir")
def adquirir_servicio(req: AdquisicionRequest):
    """Procesa la compra comprobando disponibilidad."""
    
    with _bloqueo:
        _, servicio = buscar_servicio(req.idServicio)
        if not servicio.disponible:
            raise HTTPException(
                status_code=400,
                detail="Este servicio no está disponible actualmente y no se puede adquirir."
            )
        nueva_adquisicion = {
            "idUsuario": req.idUsuario,
            "idServicio": req.idServicio,
            "servicio_nombre": servicio.nombre,
        }
        adquisiciones_db.append(nueva_adquisicion)
    
    # 4. US-013-AC-07: Informar de que se ha realizado correctamente
    return {
        "mensaje": f"Servicio '{servicio.nombre}' adquirido correctamente.",
        "registro": nueva_adquisicion
    }
