"""US-002: inicio, cierre de sesión y acceso protegido (demo académica)."""
import secrets
from typing import Literal
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(title='Subsonic Festival - Autenticación', version='1.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

class Credenciales(BaseModel):
    email: EmailStr
    password: str = Field(min_length=3)

class UsuarioLogueado(BaseModel):
    id: int
    nombre: str
    email: str
    rol: Literal['admin', 'cliente']
    token: str

# Datos de ejemplo de la subtarea de inicio de sesión. No usar en producción.
usuarios_db = [
    {'id': 1, 'nombre': 'Admin Subsonic', 'email': 'admin@subsonic.com', 'password': '123', 'rol': 'admin'},
    {'id': 2, 'nombre': 'Usuario Normal', 'email': 'usuario@gmail.com', 'password': '123', 'rol': 'cliente'},
]
# Tokens activos: al cerrar sesión se revoca el token en el servidor.
sesiones_activas: dict[str, int] = {}

def usuario_autenticado(authorization: str | None) -> dict:
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Debes iniciar sesión.')
    token = authorization.removeprefix('Bearer ').strip()
    usuario_id = sesiones_activas.get(token)
    usuario = next((u for u in usuarios_db if u['id'] == usuario_id), None)
    if usuario is None:
        raise HTTPException(status_code=401, detail='Sesión inválida o cerrada. Inicia sesión de nuevo.')
    return usuario

@app.post('/api/login', response_model=UsuarioLogueado)
def iniciar_sesion(creds: Credenciales):
    for user in usuarios_db:
        if user['email'].lower() == creds.email.lower() and user['password'] == creds.password:
            token = secrets.token_urlsafe(32)
            sesiones_activas[token] = user['id']
            return UsuarioLogueado(id=user['id'], nombre=user['nombre'], email=user['email'], rol=user['rol'], token=token)
    raise HTTPException(status_code=401, detail='Credenciales incorrectas. Verifica tu email y contraseña.')

@app.post('/api/logout')
def cerrar_sesion(authorization: str | None = Header(default=None)):
    usuario_autenticado(authorization)
    token = authorization.removeprefix('Bearer ').strip()
    del sesiones_activas[token]
    return {'mensaje': 'Sesión cerrada correctamente.'}

@app.get('/api/privado')
def consultar_area_privada(authorization: str | None = Header(default=None)):
    usuario = usuario_autenticado(authorization)
    return {'mensaje': 'Acceso autorizado.', 'id': usuario['id'], 'nombre': usuario['nombre'], 'rol': usuario['rol']}
