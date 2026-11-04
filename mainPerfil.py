from secrets import token_urlsafe
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, Field, ConfigDict

app = FastAPI(title="API Perfil de Usuario - Subsonic Festival (US-003)")


# Modelo que ya utilizaba la consulta del perfil.
class PerfilUsuario(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: str
    estado: str


class ModificacionPerfil(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nombre: str = Field(min_length=2, max_length=100)
    email: EmailStr


class InicioSesionDemo(BaseModel):
    usuario_id: int


DB_PERFILES = [
    PerfilUsuario(id=1, nombre="Admin Principal", email="admin@festival.com", rol="admin", estado="activo"),
    PerfilUsuario(id=2, nombre="Usuario Asistente", email="asistente@festival.com", rol="cliente", estado="activo"),
    PerfilUsuario(id=3, nombre="Otro Usuario", email="otro@festival.com", rol="cliente", estado="activo"),
]

# Sesiones de demostración en memoria. Sustituir por el servicio de login de US-002 al integrar.
SESIONES: dict[str, int] = {}
seguridad = HTTPBearer(auto_error=False)


@app.post("/api/demo/login")
def iniciar_sesion_demo(datos: InicioSesionDemo):
    """Solo para pruebas locales; no utilizar como autenticación real."""
    usuario = next((u for u in DB_PERFILES if u.id == datos.usuario_id and u.estado == "activo"), None)
    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuario no disponible")
    token = token_urlsafe(32)
    SESIONES[token] = usuario.id
    return {"access_token": token, "token_type": "bearer"}


def obtener_usuario_autenticado(
    credenciales: Annotated[HTTPAuthorizationCredentials | None, Depends(seguridad)],
) -> PerfilUsuario:
    if credenciales is None:
        raise HTTPException(status_code=401, detail="Debes iniciar sesión")
    usuario_id = SESIONES.get(credenciales.credentials)
    usuario = next((u for u in DB_PERFILES if u.id == usuario_id and u.estado == "activo"), None)
    if usuario is None:
        raise HTTPException(status_code=401, detail="Sesión inválida")
    return usuario


# Consulta del perfil: se mantiene la ruta de la subtarea de tu compañero.
@app.get("/api/perfil", response_model=PerfilUsuario)
def consultar_perfil(usuario_actual: Annotated[PerfilUsuario, Depends(obtener_usuario_autenticado)]):
    return usuario_actual


# Tu subtarea: edición y guardado del perfil del usuario autenticado.
@app.put("/api/perfil", response_model=PerfilUsuario)
def modificar_perfil(
    cambios: ModificacionPerfil,
    usuario_actual: Annotated[PerfilUsuario, Depends(obtener_usuario_autenticado)],
):
    nombre = cambios.nombre.strip()
    if len(nombre) < 2:
        raise HTTPException(status_code=422, detail="El nombre debe tener al menos 2 caracteres")

    email = str(cambios.email).lower()
    if any(u.id != usuario_actual.id and str(u.email).lower() == email for u in DB_PERFILES):
        raise HTTPException(status_code=409, detail="Ese correo ya pertenece a otro usuario")

    # No se acepta id, rol ni estado en la petición; solo se modifica el usuario autenticado.
    usuario_actual.nombre = nombre
    usuario_actual.email = email
    return usuario_actual