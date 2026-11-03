from pydantic import BaseModel, Field, EmailStr
from fastapi import FastAPI, HTTPException
from typing import Literal

# --- MODELOS DE DATOS ---
class Credenciales(BaseModel):
    email: EmailStr = Field(description="Correo electrónico del usuario")
    password: str = Field(min_length=3, description="Contraseña del usuario")

class UsuarioLogueado(BaseModel):
    id: int
    nombre: str
    email: str
    rol: Literal["admin", "cliente"]
    token: str  # En un sistema real, aquí iría un JWT (JSON Web Token)

# --- BASE DE DATOS SIMULADA ---
# En un proyecto real esto saldría de una base de datos con contraseñas encriptadas.
usuarios_db = [
    {"id": 1, "nombre": "Admin Subsonic", "email": "admin@subsonic.com", "password": "123", "rol": "admin"},
    {"id": 2, "nombre": "Usuario Normal", "email": "usuario@gmail.com", "password": "123", "rol": "cliente"}
]

# --- ENDPOINT DE INICIO DE SESIÓN ---
@app.post("/api/login", response_model=UsuarioLogueado)
def iniciar_sesion(creds: Credenciales):
    """
    US-002-AC-02 y AC-03: Comprueba las credenciales. 
    Permite el acceso si son correctas o rechaza si son incorrectas.
    """
    for user in usuarios_db:
        if user["email"] == creds.email and user["password"] == creds.password:
            # Simulación de generación de token de sesión
            token_simulado = f"fake-jwt-token-{user['id']}" 
            
            return UsuarioLogueado(
                id=user["id"],
                nombre=user["nombre"],
                email=user["email"],
                rol=user["rol"],
                token=token_simulado
            )
            
    # US-002-AC-03: Mensaje comprensible si falla
    raise HTTPException(
        status_code=401, 
        detail="Credenciales incorrectas. Verifica tu email y contraseña."
    )