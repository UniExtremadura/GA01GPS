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

app = FastAPI(title="API Usuarios - Gestión Admin")

# Función de seguridad para restringir el acceso (Tu subtarea 2)
def verificar_admin(rol_usuario: str = Header(..., description="Rol del usuario que hace la petición")):
    """
    Verifica que el usuario que intenta acceder tenga permisos de administrador.
    Si no los tiene, deniega el acceso con un error 403.
    """
    if rol_usuario != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Acceso denegado: Se requieren privilegios de administrador para realizar esta accion."
        )
    return True

# Ejemplo de cómo se aplica la restricción a un endpoint (para que tus compañeros puedan seguir)
@app.get("/api/usuarios", dependencies=[Depends(verificar_admin)])
def listar_usuarios():
    # Aquí iría el código de tu compañero que hace la consulta
    return {"mensaje": "Lista de usuarios (Solo visible para admins)"}