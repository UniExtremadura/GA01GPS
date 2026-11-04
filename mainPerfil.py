from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Header, Depends

app = FastAPI(title="API Perfil de Usuario - Subsonic Festival (US-003)")

# --- MODELO DE DATOS DEL PERFIL ---
class PerfilUsuario(BaseModel):
    id: int = Field(..., description="Identificador único del usuario")
    nombre: str = Field(..., description="Nombre completo del usuario")
    email: str = Field(..., description="Correo electrónico asociado")
    rol: str = Field(..., description="Rol del usuario en la plataforma")
    estado: str = Field(..., description="Estado de la cuenta")

# MODIFICACIÓN: BASE DE DATOS EN MEMORIA SIMULADA DE PERFILES DE USUARIOS
DB_PERFILES = [
    PerfilUsuario(id=1, nombre="Admin Principal", email="admin@festival.com", rol="admin", estado="activo"),
    PerfilUsuario(id=2, nombre="Usuario Asistente", email="asistente@festival.com", rol="cliente", estado="activo"),
    PerfilUsuario(id=3, nombre="Otro Usuario", email="otro@festival.com", rol="cliente", estado="activo")
]

# --- SUBTAREA: COMPROBAR Y RECUPERAR DATOS DEL USUARIO AUTENTICADO (US-003-AC-01, AC-02, AC-07) ---
def obtener_usuario_autenticado(user_id: int = Header(..., description="ID del usuario que realiza la petición")):
    # MODIFICACIÓN: VERIFICAR Y RECUPERAR LOS DATOS DEL USUARIO AUTENTICADO MEDIANTE SU ID DE CABECERA
    for perfil in DB_PERFILES:
        if perfil.id == user_id:
            return perfil
            
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado o no autenticado correctamente."
    )

# --- SUBTAREA: ENDPOINT PARA CONSULTAR EL PROPIO PERFIL ---
@app.get("/api/perfil", response_model=PerfilUsuario)
def consultar_perfil(usuario_actual: PerfilUsuario = Depends(obtener_usuario_autenticado)):
    # MODIFICACIÓN: GARANTIZAR QUE EL USUARIO ÚNICAMENTE PUEDE CONSULTAR SUS PROPIOS DATOS (US-003-AC-07)
    # MODIFICACIÓN: VERIFICAR Y MOSTRAR CORRECTAMENTE LA INFORMACIÓN DEL PERFIL (US-003-AC-01, AC-02)
    return usuario_actual