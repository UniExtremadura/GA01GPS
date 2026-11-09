"""Consulta y registro de reservas de espacios para US-010."""

import os
import sqlite3
from contextlib import closing
from datetime import date
from pathlib import Path
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, Header, HTTPException, Query
from pydantic import BaseModel, Field

from .catalogo import consultar_espacio

router = APIRouter(prefix="/api/espacios", tags=["Reservas"])
URL_SESION = os.getenv("SUBSONIC_URL_SESION", "http://127.0.0.1:8000").rstrip("/")
RUTA_RESERVAS = Path(os.getenv(
    "SUBSONIC_RESERVAS_DB", str(Path.home() / ".subsonic" / "reservas.sqlite3")
))

Hora = Annotated[str, Field(pattern=r"^(?:[01][0-9]|2[0-3]):[0-5][0-9]$")]


class FranjaReserva(BaseModel):
    fecha: date
    horaInicio: Hora
    horaFin: Hora


class ReservaConfirmada(FranjaReserva):
    idReserva: int
    idEspacio: int
    nombreEspacio: str
    idUsuario: int


def identificar_usuario(authorization: str | None = Header(default=None)) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Inicia sesión para confirmar la reserva.")
    try:
        respuesta = httpx.get(
            f"{URL_SESION}/api/privado",
            headers={"Authorization": authorization},
            timeout=4,
        )
        if respuesta.status_code in (401, 403):
            raise HTTPException(401, "Tu sesión ha caducado. Vuelve a iniciar sesión.")
        respuesta.raise_for_status()
        usuario = respuesta.json()
    except (httpx.HTTPError, ValueError) as error:
        raise HTTPException(503, "No se ha podido comprobar tu sesión. Inténtalo de nuevo.") from error

    id_usuario = usuario.get("id") if isinstance(usuario, dict) else None
    if type(id_usuario) is not int or id_usuario <= 0:
        raise HTTPException(503, "El servicio de sesión no ha devuelto un usuario válido.")
    return id_usuario


def validar_franja(franja: FranjaReserva):
    if franja.fecha < date.today() or franja.horaInicio >= franja.horaFin:
        raise HTTPException(
            400, "Elige una fecha a partir de hoy y una hora de fin posterior a la de inicio."
        )


def espacio_reservable(id_espacio: int):
    espacio = consultar_espacio(id_espacio)
    if espacio is None:
        raise HTTPException(404, "El espacio no está disponible para reservar.")
    return espacio


def conectar():
    RUTA_RESERVAS.parent.mkdir(parents=True, exist_ok=True)
    conexion = sqlite3.connect(RUTA_RESERVAS)
    try:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY,
                id_espacio INTEGER NOT NULL,
                id_usuario INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                hora_inicio TEXT NOT NULL,
                hora_fin TEXT NOT NULL,
                CHECK (hora_inicio < hora_fin),
                UNIQUE (id_espacio, fecha, hora_inicio, hora_fin)
            )
        """)
    except sqlite3.Error:
        conexion.close()
        raise
    return conexion


def franja_ocupada(conexion, id_espacio: int, franja: FranjaReserva) -> bool:
    return conexion.execute(
        """
        SELECT 1 FROM reservas
        WHERE id_espacio = ? AND fecha = ? AND hora_inicio < ? AND hora_fin > ?
        LIMIT 1
        """,
        (id_espacio, franja.fecha.isoformat(), franja.horaFin, franja.horaInicio),
    ).fetchone() is not None


@router.get("/{idEspacio}/disponibilidad")
def consultar_disponibilidad(idEspacio: int, franja: Annotated[FranjaReserva, Query()]):
    validar_franja(franja)
    espacio_reservable(idEspacio)
    try:
        with closing(conectar()) as conexion:
            return {"disponible": not franja_ocupada(conexion, idEspacio, franja)}
    except (OSError, sqlite3.Error) as error:
        raise HTTPException(503, "No se ha podido consultar la disponibilidad.") from error


@router.post("/{idEspacio}/reservas", response_model=ReservaConfirmada, status_code=201)
def confirmar_reserva(
    idEspacio: int,
    franja: FranjaReserva,
    id_usuario: Annotated[int, Depends(identificar_usuario)],
):
    validar_franja(franja)
    try:
        with closing(conectar()) as conexion, conexion:
            # Reserva el turno de escritura antes de comprobar solapamientos.
            conexion.execute("BEGIN IMMEDIATE")
            espacio = espacio_reservable(idEspacio)
            if franja_ocupada(conexion, idEspacio, franja):
                raise HTTPException(409, "El espacio ya está reservado en parte o en toda esa franja.")
            resultado = conexion.execute(
                """
                INSERT INTO reservas (id_espacio, id_usuario, fecha, hora_inicio, hora_fin)
                VALUES (?, ?, ?, ?, ?)
                """,
                (idEspacio, id_usuario, franja.fecha.isoformat(), franja.horaInicio, franja.horaFin),
            )
            return ReservaConfirmada(
                **franja.model_dump(),
                idReserva=resultado.lastrowid,
                idEspacio=idEspacio,
                nombreEspacio=espacio["nombre"],
                idUsuario=id_usuario,
            )
    except (OSError, sqlite3.Error) as error:
        raise HTTPException(503, "No se ha podido guardar la reserva. Inténtalo de nuevo.") from error
