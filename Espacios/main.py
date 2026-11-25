"""API de consulta y administración de espacios - Subsonic Festival."""
import os
from threading import Lock
from typing import Literal

import httpx
from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator

<<<<<<< HEAD
from .catalogo import consultar_espacio, consultar_espacios, espacios, normalizar

app = FastAPI(
    title="API Espacios - Subsonic Festival",
    description="Consulta y administración de espacios del festival.",
    version="1.1.0",
=======
from .catalogo import consultar_espacio, consultar_espacios
from .reservas import router as reservas_router


# ==========================================
# CONFIGURACION DE FASTAPI
# ==========================================

app = FastAPI(
    title="API Espacios - Subsonic Festival",
    description="Consulta, filtrado y reserva de espacios - US-009 y US-010",
    version="1.0.0"
>>>>>>> origin/feature/SCRUM-31-US-010-Reserva-de-un-espacio
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080", "http://127.0.0.1:8080",
        "http://localhost:5500", "http://127.0.0.1:5500",
    ],
    allow_credentials=False,
<<<<<<< HEAD
    allow_methods=["*"],
=======
    allow_methods=["GET", "POST"],
>>>>>>> origin/feature/SCRUM-31-US-010-Reserva-de-un-espacio
    allow_headers=["*"],
)
app.include_router(reservas_router)

TipoEspacio = Literal["escenario", "camping", "zona_vip", "sala"]
ZonaEspacio = Literal["Norte", "Sur", "Este", "Oeste"]
_bloqueo = Lock()
_siguiente_id = max((espacio["id"] for espacio in espacios), default=0) + 1
URL_SESION = os.getenv("SUBSONIC_URL_SESION", "http://127.0.0.1:8000").rstrip("/")


class EspacioDatos(BaseModel):
    """Campos editables de un espacio; el identificador lo asigna la API."""

    model_config = ConfigDict(extra="forbid")

    nombre: str = Field(min_length=2, max_length=100)
    tipo: TipoEspacio
    zona: ZonaEspacio
    capacidad: int = Field(gt=0)
    descripcion: str = Field(min_length=5, max_length=500)
    habilitado: bool = True
    disponible: bool = True

    @field_validator("nombre", "descripcion", mode="before")
    @classmethod
    def normalizar_texto(cls, valor):
        if isinstance(valor, str):
            valor = valor.strip()
            if not valor:
                raise ValueError("Este campo es obligatorio y no puede estar vacío.")
        return valor


class Espacio(EspacioDatos):
    id: int = Field(gt=0)


def verificar_administrador(authorization: str | None = Header(default=None)):
    """Comprueba el rol con el servicio de sesión."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Inicia sesión para gestionar espacios.")
    try:
        respuesta = httpx.get(
            f"{URL_SESION}/api/privado", headers={"Authorization": authorization}, timeout=4,
        )
        if respuesta.status_code == 401:
            raise HTTPException(status_code=401, detail="Tu sesión no es válida. Inicia sesión de nuevo.")
        respuesta.raise_for_status()
        sesion = respuesta.json()
        if not isinstance(sesion, dict) or not isinstance(sesion.get("rol"), str):
            raise ValueError("Respuesta de sesión incompleta.")
    except (httpx.HTTPError, ValueError) as error:
        raise HTTPException(status_code=503, detail="No se pudo verificar la sesión.") from error
    if sesion["rol"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requieren permisos de administrador.",
        )


@app.exception_handler(RequestValidationError)
async def error_validacion(request, exc):
<<<<<<< HEAD
    errores = [
        {
            "campo": ".".join(str(parte) for parte in error.get("loc", ())[1:]) or "solicitud",
            "mensaje": error.get("msg", "Valor no válido."),
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=400,
        content={
            "codigo": 400,
            "mensaje": "Revisa los datos del espacio y corrige los campos indicados.",
            "errores": errores,
        },
    )
=======
    es_reserva = request.url.path.endswith(("/disponibilidad", "/reservas"))
    return JSONResponse(status_code=400, content={
        "codigo": 400,
        "mensaje": (
            "Revisa el espacio, la fecha y las horas de la reserva."
            if es_reserva else
            "Filtros no validos. Revisa el tipo, la zona y la capacidad minima."
        ),
    })
>>>>>>> origin/feature/SCRUM-31-US-010-Reserva-de-un-espacio


@app.exception_handler(HTTPException)
async def error_http(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"codigo": exc.status_code, "mensaje": exc.detail},
    )


def buscar_espacio_registrado(id_espacio: int) -> tuple[int, dict]:
    for indice, espacio in enumerate(espacios):
        if espacio["id"] == id_espacio:
            return indice, espacio
    raise HTTPException(status_code=404, detail="Espacio no encontrado.")


def comprobar_nombre_unico(nombre: str, excluir_id: int | None = None) -> None:
    clave = normalizar(nombre)
    if any(
        normalizar(espacio["nombre"]) == clave and espacio["id"] != excluir_id
        for espacio in espacios
    ):
        raise HTTPException(status_code=409, detail="Ya existe un espacio con ese nombre.")


@app.get("/")
def inicio():
    return {"mensaje": "Microservicio Espacios funcionando"}


# Consulta pública existente (US-009).
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


# Gestión administrativa (US-011 / SCRUM-66).
@app.get(
    "/api/admin/espacios",
    response_model=list[Espacio],
    dependencies=[Depends(verificar_administrador)],
)
def listar_espacios_admin():
    """Devuelve también espacios no disponibles para permitir su edición."""
    with _bloqueo:
        return [espacio.copy() for espacio in espacios]


@app.get(
    "/api/admin/espacios/{idEspacio}",
    response_model=Espacio,
    dependencies=[Depends(verificar_administrador)],
)
def obtener_espacio_admin(idEspacio: int):
    with _bloqueo:
        _, espacio = buscar_espacio_registrado(idEspacio)
        return espacio.copy()


@app.post(
    "/api/admin/espacios",
    response_model=Espacio,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verificar_administrador)],
)
def crear_espacio(datos: EspacioDatos):
    global _siguiente_id
    with _bloqueo:
        comprobar_nombre_unico(datos.nombre)
        nuevo = {"id": _siguiente_id, **datos.model_dump()}
        _siguiente_id += 1
        espacios.append(nuevo)
        return nuevo.copy()


@app.put(
    "/api/admin/espacios/{idEspacio}",
    response_model=Espacio,
    dependencies=[Depends(verificar_administrador)],
)
def modificar_espacio(idEspacio: int, datos: EspacioDatos):
    with _bloqueo:
        indice, existente = buscar_espacio_registrado(idEspacio)
        comprobar_nombre_unico(datos.nombre, excluir_id=idEspacio)
        actualizado = {"id": existente["id"], **datos.model_dump()}
        espacios[indice] = actualizado
        return actualizado.copy()


@app.delete(
    "/api/admin/espacios/{idEspacio}",
    response_model=Espacio,
    dependencies=[Depends(verificar_administrador)],
)
def deshabilitar_espacio(idEspacio: int):
    """Da de baja el espacio conservando su identificador y sus datos."""
    with _bloqueo:
        indice, espacio = buscar_espacio_registrado(idEspacio)
        actualizado = {**espacio, "habilitado": False, "disponible": False}
        espacios[indice] = actualizado
        return actualizado.copy()
