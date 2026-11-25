"""US-008: API de demostración para validar permisos y operaciones administrativas.
Integrar con el almacenamiento y autenticación reales antes de desplegar.
"""
from datetime import date
from decimal import Decimal
from secrets import compare_digest
from typing import Literal

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, model_validator

app = FastAPI(title="Subsonic - US-008 Administración de entradas")
app.add_middleware(CORSMiddleware, allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
                   allow_methods=["GET", "PUT"], allow_headers=["Authorization", "Content-Type", "Accept"])

# Tokens ficticios SOLO para pruebas. En producción deben validarse con el servicio de usuarios.
DEMO_TOKENS = {"demo-admin-token": "admin", "demo-user-token": "usuario"}


def admin_required(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Debes iniciar sesión")
    token = authorization[7:]
    role = next((role for key, role in DEMO_TOKENS.items() if compare_digest(token, key)), None)
    if role is None:
        raise HTTPException(status_code=401, detail="Sesión no válida")
    if role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos de administrador")
    return role


class EntradaUpdate(BaseModel):
    nombre: Literal["vip", "abono_completo", "abono_un_dia"]
    descripcion: str = Field(default="", max_length=500)
    precio: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    stockTotal: int = Field(ge=1, le=1000000)
    fechaInicioValidez: date
    fechaFinValidez: date

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.fechaFinValidez < self.fechaInicioValidez:
            raise ValueError("La fecha final no puede ser anterior a la inicial")
        return self


# Catálogo simulado. Sustituir por el repositorio/BD del servicio de Entradas.
ENTRADAS = {
    1: {"id": 1, "nombre": "vip", "descripcion": "Abono VIP", "precio": 150.0,
        "stockTotal": 100, "stockDisponible": 90, "estado": "disponible",
        "fechaInicioValidez": "2026-11-10", "fechaFinValidez": "2026-11-12"},
    2: {"id": 2, "nombre": "abono_completo", "descripcion": "Festival completo", "precio": 80.0,
        "stockTotal": 200, "stockDisponible": 200, "estado": "disponible",
        "fechaInicioValidez": "2026-11-10", "fechaFinValidez": "2026-11-12"},
}


@app.get("/api/entradas")
def listar_entradas(_role: str = Depends(admin_required)):
    return list(ENTRADAS.values())


@app.get("/api/entradas/{entrada_id}")
def detalle_entrada(entrada_id: int, _role: str = Depends(admin_required)):
    entrada = ENTRADAS.get(entrada_id)
    if entrada is None:
        raise HTTPException(status_code=404, detail="Entrada no encontrada")
    return entrada


@app.put("/api/entradas/{entrada_id}")
def modificar_entrada(entrada_id: int, datos: EntradaUpdate, _role: str = Depends(admin_required)):
    entrada = ENTRADAS.get(entrada_id)
    if entrada is None:
        raise HTTPException(status_code=404, detail="Entrada no encontrada")
    vendidas = entrada["stockTotal"] - entrada["stockDisponible"]
    if datos.stockTotal < vendidas:
        raise HTTPException(status_code=409, detail=f"No puedes reducir el stock por debajo de las {vendidas} entradas vendidas")
    actualizada = {"id": entrada_id, **datos.model_dump(mode="json"),
                   "precio": float(datos.precio),
                   "stockDisponible": datos.stockTotal - vendidas,
                   "estado": "disponible" if datos.stockTotal > vendidas else "agotada"}
    ENTRADAS[entrada_id] = actualizada
    return actualizada
