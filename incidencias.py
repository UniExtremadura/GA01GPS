"""US-019: registro y gestión de incidencias (proyecto académico Subsonic)."""
from datetime import datetime
from pathlib import Path
import os
import sqlite3
from contextlib import contextmanager
from typing import Literal

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from mainUsuario002 import usuario_autenticado

app = FastAPI(title="API Incidencias - Subsonic Festival")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DB_PATH = Path(os.environ.get("SUBSONIC_INCIDENCIAS_DB", str(Path(__file__).with_name("incidencias.sqlite3"))))


@contextmanager
def conectar():
    conexion = sqlite3.connect(DB_PATH, timeout=10)
    conexion.row_factory = sqlite3.Row
    try:
        with conexion:
            yield conexion
    finally:
        conexion.close()


def inicializar_bd():
    with conectar() as conexion:
        conexion.execute("""CREATE TABLE IF NOT EXISTS incidencias (
            idIncidencia INTEGER PRIMARY KEY AUTOINCREMENT,
            idUsuario INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            fechaRegistro TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'Pendiente'
            CHECK (estado IN ('Pendiente', 'Resuelta'))
        )""")


inicializar_bd()


class IncidenciaCreate(BaseModel):
    idUsuario: int = Field(gt=0)
    titulo: str = Field(min_length=5, max_length=100)
    descripcion: str = Field(min_length=10)


class Incidencia(IncidenciaCreate):
    idIncidencia: int
    fechaRegistro: str
    estado: Literal["Pendiente", "Resuelta"]


class EstadoUpdate(BaseModel):
    estado: Literal["Pendiente", "Resuelta"]


def requiere_admin(authorization: str | None = Header(default=None)):
    usuario = usuario_autenticado(authorization)
    if usuario["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Solo un administrador puede gestionar incidencias")
    return usuario


# Se conserva la ruta de registro utilizada por view/incidencias.html.
@app.post("/api/incidencias", status_code=201)
def registrar_incidencia(incidencia: IncidenciaCreate):
    try:
        with conectar() as conexion:
            cursor = conexion.execute(
                "INSERT INTO incidencias (idUsuario, titulo, descripcion, fechaRegistro, estado) VALUES (?, ?, ?, ?, ?)",
                (incidencia.idUsuario, incidencia.titulo.strip(), incidencia.descripcion.strip(),
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Pendiente"),
            )
            identificador = cursor.lastrowid
    except sqlite3.Error as error:
        raise HTTPException(status_code=500, detail="Error al guardar la incidencia") from error
    return {"mensaje": "Incidencia registrada correctamente. Nuestro equipo la revisará pronto.", "idIncidencia": identificador}


# Se conserva la ruta de consulta de la subtarea anterior.
@app.get("/api/incidencias/usuario/{id_usuario}", response_model=list[Incidencia])
def listar_incidencias_usuario(id_usuario: int):
    with conectar() as conexion:
        filas = conexion.execute("SELECT * FROM incidencias WHERE idUsuario = ? ORDER BY idIncidencia DESC", (id_usuario,)).fetchall()
    return [dict(fila) for fila in filas]


# Nuevas rutas administrativas. IMPORTANTE: rutas fijas antes de /{id_incidencia}.
@app.get("/api/admin/incidencias", response_model=list[Incidencia])
def listar_incidencias(estado: Literal["Pendiente", "Resuelta"] | None = None,
                       _admin=Depends(requiere_admin)):
    with conectar() as conexion:
        if estado is None:
            filas = conexion.execute("SELECT * FROM incidencias ORDER BY idIncidencia DESC").fetchall()
        else:
            filas = conexion.execute("SELECT * FROM incidencias WHERE estado = ? ORDER BY idIncidencia DESC", (estado,)).fetchall()
    return [dict(fila) for fila in filas]


@app.get("/api/admin/incidencias/{id_incidencia}", response_model=Incidencia)
def detalle_incidencia(id_incidencia: int, _admin=Depends(requiere_admin)):
    with conectar() as conexion:
        fila = conexion.execute("SELECT * FROM incidencias WHERE idIncidencia = ?", (id_incidencia,)).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail="Incidencia no encontrada")
    return dict(fila)


@app.patch("/api/admin/incidencias/{id_incidencia}")
def cambiar_estado(id_incidencia: int, datos: EstadoUpdate, _admin=Depends(requiere_admin)):
    try:
        with conectar() as conexion:
            cursor = conexion.execute("UPDATE incidencias SET estado = ? WHERE idIncidencia = ?",
                                      (datos.estado, id_incidencia))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Incidencia no encontrada")
            fila = conexion.execute("SELECT * FROM incidencias WHERE idIncidencia = ?", (id_incidencia,)).fetchone()
    except sqlite3.Error as error:
        raise HTTPException(status_code=500, detail="Error al actualizar la incidencia") from error
    return {"mensaje": "Estado actualizado correctamente", "incidencia": dict(fila)}