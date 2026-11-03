from typing import Literal
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Header, Depends

app = FastAPI(title="API Usuarios - Gestión Admin")

# --- PARTE 1 (Subtarea 1) ---
RolUsuario = Literal["admin", "cliente"]
EstadoUsuario = Literal["activo", "deshabilitado"]

class UsuarioBase(BaseModel):
    nombre: str = Field(min_length=2, description="Nombre completo del usuario")
    email: str = Field(pattern=r"^\S+@\S+\.\S+$")
    rol: RolUsuario
    estado: EstadoUsuario = "activo"

class Usuario(UsuarioBase):
    id: int