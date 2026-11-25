from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Header

app = FastAPI(title="API Consulta de Entradas Adquiridas - Subsonic Festival (US-007)")

class EntradaAdquirida(BaseModel):
    id_entrada: int
    usuario_id: int
    tipo_entrada: str
    precio: float
    fecha_adquisicion: str
    estado: str

# MODIFICACIÓN: BASE DE DATOS SIMULADA DE ENTRADAS ADQUIRIDAS EN EL SISTEMA
DB_ENTRADAS_ADQUIRIDAS = [
    EntradaAdquirida(id_entrada=101, usuario_id=2, tipo_entrada="General", precio=50.0, fecha_adquisicion="2026-06-01", estado="Valida"),
    EntradaAdquirida(id_entrada=102, usuario_id=2, tipo_entrada="VIP", precio=120.0, fecha_adquisicion="2026-06-02", estado="Valida"),
    # Nota: El usuario con ID 3 no tiene entradas para probar el caso de bandeja vacía
]

# --- SUBTAREA: TRATAR EL CASO DE ACCESO SIN SESIÓN INICIADA (US-007-AC-06) ---
def verificar_sesion_activa(x_usuario_id: Optional[int] = Header(None, description="ID del usuario en cabecera")):
    # MODIFICACIÓN: COMPROBAR SI SE HA PROPORCIONADO UNA IDENTIFICACIÓN DE SESIÓN VÁLIDA
    if x_usuario_id is None:
        raise HTTPException(
            status_code=401,
            detail="Acceso denegado: Los usuarios que no hayan iniciado sesión no pueden acceder a la consulta de entradas adquiridas."
        )
    return x_usuario_id

# --- SUBTAREA: OBTENER LAS ENTRADAS ADQUIRIDAS Y GESTIONAR CASO SIN ENTRADAS (US-007-AC-01, AC-02, AC-03, AC-05) ---
@app.get("/api/mis-entradas", response_model=dict)
def consultar_entradas_adquiridas(usuario_id: int = Header(..., alias="X-Usuario-ID")):
    # MODIFICACIÓN: VALIDAR QUE EL USUARIO HA INICIADO SESIÓN MEDIANTE LA CABECERA REQUERIDA
    if usuario_id is None:
        raise HTTPException(status_code=401, detail="Debe iniciar sesión para realizar esta consulta.")
        
    # MODIFICACIÓN: FILTRAR Y OBTENER EXCLUSIVAMENTE LAS ENTRADAS ASOCIADAS A LA CUENTA DEL USUARIO (US-007-AC-03)
    entradas_usuario = [entrada for entrada in DB_ENTRADAS_ADQUIRIDAS if entrada.usuario_id == usuario_id]
    
    # MODIFICACIÓN: GESTIONAR EL MENSAJE CLARO E INFORMATIVO CUANDO EL USUARIO NO TIENE ENTRADAS (US-007-AC-05)
    if not entradas_usuario:
        return {
            "mensaje": "No tienes entradas adquiridas actualmente en la plataforma.",
            "total_entradas": 0,
            "entradas": []
        }
        
    # MODIFICACIÓN: MOSTRAR LA INFORMACIÓN CORRESPONDIENTE AL LISTADO DE ENTRADAS ADQUIRIDAS (US-007-AC-01, AC-02)
    return {
        "mensaje": "Listado de entradas obtenido correctamente.",
        "total_entradas": len(entradas_usuario),
        "entradas": entradas_usuario
    }

# --- ENDPOINT COMPLEMENTARIO: CONSULTAR DETALLE DE UNA ENTRADA PROPIA ---
@app.get("/api/mis-entradas/{id_entrada}", response_model=EntradaAdquirida)
def consultar_detalle_entrada(id_entrada: int, usuario_id: int = Header(..., alias="X-Usuario-ID")):
    # MODIFICACIÓN: BUSCAR LA ENTRADA ESPECÍFICA Y GARANTIZAR LA PRIVACIDAD DE LOS DATOS (US-007-AC-03, AC-04)
    for entrada in DB_ENTRADAS_ADQUIRIDAS:
        if entrada.id_entrada == id_entrada:
            if entrada.usuario_id != usuario_id:
                raise HTTPException(
                    status_code=403,
                    detail="Acceso prohibido: Únicamente puedes acceder a tus propias entradas."
                )
            return entrada
            
    raise HTTPException(status_code=404, detail="La entrada seleccionada no se encuentra registrada.")