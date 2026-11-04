from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .catalogo import consultar_espacio, consultar_espacios


# ==========================================
# CONFIGURACION DE FASTAPI
# ==========================================

app = FastAPI(
    title="API Espacios - Subsonic Festival",
    description="Consulta y filtrado de espacios disponibles - US-009",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080", "http://127.0.0.1:8080",
        "http://localhost:5500", "http://127.0.0.1:5500",
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


# ==========================================
# MODELOS DE DATOS
# ==========================================

TipoEspacio = Literal["escenario", "camping", "zona_vip", "sala"]
ZonaEspacio = Literal["Norte", "Sur", "Este", "Oeste"]


class Espacio(BaseModel):
    id: int
    nombre: str
    tipo: TipoEspacio
    zona: ZonaEspacio
    capacidad: int
    descripcion: str
    habilitado: bool
    disponible: bool


# ==========================================
# VALIDACION DE ERRORES
# ==========================================

@app.exception_handler(RequestValidationError)
async def error_validacion(request, exc):
    return JSONResponse(status_code=400, content={
        "codigo": 400,
        "mensaje": "Filtros no validos. Revisa el tipo, la zona y la capacidad minima."
    })


@app.exception_handler(HTTPException)
async def error_http(request, exc):
    return JSONResponse(status_code=exc.status_code, content={
        "codigo": exc.status_code, "mensaje": exc.detail
    })


@app.get("/")
def inicio():
    return {"mensaje": "Microservicio Espacios funcionando"}


# ==========================================
# CONSULTA Y FILTRADO DE ESPACIOS
# ==========================================

@app.get("/api/espacios", response_model=list[Espacio])
def listar_espacios(
    nombre: str = Query(default="", max_length=100),
    tipo: TipoEspacio | None = None,
    zona: ZonaEspacio | None = None,
    capacidad_minima: int = Query(default=0, ge=0),
):
    return consultar_espacios(nombre, tipo, zona, capacidad_minima)


@app.get("/api/espacios/{idEspacio}", response_model=Espacio)
def obtener_espacio(idEspacio: int):
    espacio = consultar_espacio(idEspacio)
    if espacio is None:
        raise HTTPException(status_code=404, detail="Espacio no encontrado o no disponible")
    return espacio
