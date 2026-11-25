from typing import Literal, List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Header, Depends

app = FastAPI(title="API Usuarios - Gestión Admin (US-004)")

# --- PARTE 1: MODELOS Y TIPOS DE DATOS ---
RolUsuario = Literal["admin", "cliente"]
EstadoUsuario = Literal["activo", "deshabilitado"]

class UsuarioBase(BaseModel):
    nombre: str = Field(min_length=2, description="Nombre completo del usuario")
    email: str = Field(pattern=r"^\S+@\S+\.\S+$")
    rol: RolUsuario
    estado: EstadoUsuario = "activo"

class Usuario(UsuarioBase):
    id: int

# MODIFICACIÓN: BASE DE DATOS EN MEMORIA INICIALIZADA PARA PRUEBAS Y EVIDENCIA
DB_USUARIOS = [
    Usuario(id=1, nombre="Admin Principal", email="admin@festival.com", rol="admin", estado="activo"),
    Usuario(id=2, nombre="Cliente Ejemplo", email="cliente@festival.com", rol="cliente", estado="activo")
]
contador_id = 3

# SEGURIDAD: VERIFICACIÓN DE ROL DE ADMINISTRADOR (Criterio US-004-AC-06)
def verificar_admin(rol_usuario: str = Header(..., description="Rol del usuario que hace la petición")):
    # MODIFICACIÓN: RESTRINGIR ACCESO ÚNICAMENTE A USUARIOS CON ROL DE ADMINISTRADOR
    if rol_usuario != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Acceso denegado: Se requieren privilegios de administrador (US-004-AC-06)."
        )
    return True

# --- SUBTAREA 1: LISTADO DE USUARIOS CON ROL Y ESTADO (Criterio US-004-AC-01) ---
@app.get("/api/usuarios", response_model=List[Usuario], dependencies=[Depends(verificar_admin)])
def listar_usuarios():
    # MODIFICACIÓN: DEVUELVE EL LISTADO COMPLETO DE USUARIOS MOSTRANDO SU ROL Y ESTADO (US-004-AC-01)
    return DB_USUARIOS

# --- VALIDACIÓN Y VERIFICACIÓN DE CRITERIO US-004-AC-02 ---
@app.get("/api/usuarios/{usuario_id}", response_model=Usuario, dependencies=[Depends(verificar_admin)])
def consultar_usuario_concreto(usuario_id: int):
    # MODIFICACIÓN: PERMITE CONSULTAR LA INFORMACIÓN DETALLADA DE UN USUARIO CONCRETO (US-004-AC-02)
    for u in DB_USUARIOS:
        if u.id == usuario_id:
            return u
    raise HTTPException(status_code=404, detail="Usuario no encontrado.")

# --- SUBTAREA 2 Y 4: ALTA DE USUARIOS CON VALIDACIÓN DE DUPLICADOS (Criterios US-004-AC-03 y AC-04) ---
@app.post("/api/usuarios", response_model=dict, dependencies=[Depends(verificar_admin)])
def crear_usuario(usuario_nuevo: UsuarioBase):
    global contador_id
    
    # MODIFICACIÓN: VALIDAR CASO DE USUARIO DUPLICADO POR CORREO ELECTRÓNICO (US-004-AC-04)
    for u in DB_USUARIOS:
        if u.email.lower() == usuario_nuevo.email.lower():
            raise HTTPException(
                status_code=400, 
                detail="Error de validación: El correo electrónico ya está registrado en el sistema."
            )
    
    # MODIFICACIÓN: CREAR Y ALMACENAR EL NUEVO USUARIO
    nuevo_usuario = Usuario(id=contador_id, **usuario_nuevo.dict())
    DB_USUARIOS.append(nuevo_usuario)
    contador_id += 1
    
    # MODIFICACIÓN: RETORNAR CONFIRMACIÓN EXPLÍCITA DEL RESULTADO DE LA CREACIÓN (US-004-AC-03)
    return {
        "mensaje": "Usuario creado exitosamente",
        "resultado": "EXITO",
        "usuario": nuevo_usuario
    }

# --- SUBTAREA 2 Y 4: EDICIÓN DE USUARIOS CON VALIDACIÓN (Criterios US-004-AC-03 y AC-04) ---
@app.put("/api/usuarios/{usuario_id}", response_model=dict, dependencies=[Depends(verificar_admin)])
def editar_usuario(usuario_id: int, usuario_actualizado: UsuarioBase):
    # MODIFICACIÓN: VALIDAR DUPLICADOS EN LA EDICIÓN (QUE EL EMAIL NO PERTENEZCA A OTRO ID)
    for u in DB_USUARIOS:
        if u.email.lower() == usuario_actualizado.email.lower() and u.id != usuario_id:
            raise HTTPException(
                status_code=400, 
                detail="Error de validación: El correo ya pertenece a otro usuario registrado."
            )

    # MODIFICACIÓN: BUSCAR Y MODIFICAR LOS DATOS DEL USUARIO REGISTRADO (US-004-AC-03)
    for index, u in enumerate(DB_USUARIOS):
        if u.id == usuario_id:
            usuario_modificado = Usuario(id=usuario_id, **usuario_actualizado.dict())
            DB_USUARIOS[index] = usuario_modificado
            
            # MODIFICACIÓN: RETORNAR CONFIRMACIÓN DEL RESULTADO DE LA EDICIÓN
            return {
                "mensaje": f"Usuario con ID {usuario_id} modificado correctamente",
                "resultado": "EXITO",
                "usuario": usuario_modificado
            }
            
    raise HTTPException(status_code=404, detail="Usuario no encontrado para editar.")

# --- SUBTAREA 3: DESACTIVACIÓN DE USUARIOS (Criterio US-004-AC-05) ---
@app.patch("/api/usuarios/{usuario_id}/desactivar", response_model=dict, dependencies=[Depends(verificar_admin)])
def desactivar_usuario(usuario_id: int):
    # MODIFICACIÓN: BUSCAR AL USUARIO Y CAMBIAR SU ESTADO A 'deshabilitado' (US-004-AC-05)
    for index, u in enumerate(DB_USUARIOS):
        if u.id == usuario_id:
            datos_actualizados = u.dict()
            datos_actualizados["estado"] = "deshabilitado"
            usuario_deshabilitado = Usuario(**datos_actualizados)
            DB_USUARIOS[index] = usuario_deshabilitado
            
            # MODIFICACIÓN: RETORNAR CONFIRMACIÓN DEL RESULTADO DE LA DESACTIVACIÓN
            return {
                "mensaje": f"La cuenta del usuario con ID {usuario_id} ha sido desactivada correctamente.",
                "resultado": "EXITO",
                "usuario": usuario_deshabilitado
            }
            
    raise HTTPException(status_code=404, detail="Usuario no encontrado para desactivar.")
# Métodos de pago ficticios para la compra académica de entradas (sin cobros reales).
METODOS_PAGO = {
    1: [{"id": 1, "tipo": "tarjeta", "titular": "Admin Principal", "ultimosDigitos": "0001", "predeterminado": True}],
    2: [{"id": 2, "tipo": "tarjeta", "titular": "Cliente Ejemplo", "ultimosDigitos": "0002", "predeterminado": True}],
}

@app.get("/api/usuarios/{usuario_id}/metodos-pago")
def listar_metodos_pago(usuario_id: int):
    if not any(usuario.id == usuario_id for usuario in DB_USUARIOS):
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return METODOS_PAGO.get(usuario_id, [])
