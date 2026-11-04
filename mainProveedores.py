from threading import Lock
from typing import Literal
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="API Proveedores - Subsonic Festival", version="1.0.0")

CategoriaProveedor = Literal["sonido_iluminacion", "hosteleria", "seguridad", "logistica", "merchandising"]
EstadoProveedor = Literal["disponible", "inactivo"]

# ==========================================
# --- MODELOS DE DATOS ---
# ==========================================

# US-015-AC-02 y AC-04 (Público)
class Proveedor(BaseModel):
    id: int
    codigo: str
    nombre: str = Field(min_length=2)
    categoria: CategoriaProveedor
    descripcion: str
    emailContacto: str
    telefono: str
    servicioAsociado: str
    estado: EstadoProveedor

class RespuestaConsultaProveedores(BaseModel):
    total: int
    mensaje: str
    proveedores: list[Proveedor]

# US-016: Modelo para cuando el admin crea/edita (sin enviar el ID, que se autogenera)
class ProveedorBase(BaseModel):
    codigo: str
    nombre: str = Field(min_length=2)
    categoria: CategoriaProveedor
    descripcion: str
    emailContacto: str
    telefono: str
    servicioAsociado: str
    estado: EstadoProveedor

# ==========================================
# --- DATOS TEMPORALES EN MEMORIA ---
# ==========================================

proveedores_db: list[Proveedor] = [
    Proveedor(
        id=1,
        codigo="PROV-001",
        nombre="BassLine Audio Systems",
        categoria="sonido_iluminacion",
        descripcion="Suministro de sistemas de sonido line array e iluminación láser para escenarios.",
        emailContacto="tecnico@basslineaudio.es",
        telefono="+34 910 001 101",
        servicioAsociado="Escenarios Main y Underground",
        estado="disponible"
    ),
    Proveedor(
        id=2,
        codigo="PROV-002",
        nombre="NeonDrinks Catering & Bar",
        categoria="hosteleria",
        descripcion="Gestión integral de barras, bebidas y zona de restauración Food Trucks.",
        emailContacto="logistica@neondrinks.com",
        telefono="+34 910 002 202",
        servicioAsociado="Barras centrales y Zona VIP",
        estado="disponible"
    ),
    Proveedor(
        id=3,
        codigo="PROV-003",
        nombre="Aegis Security & Access",
        categoria="seguridad",
        descripcion="Control de accesos, validación de entradas y seguridad perimetral del recinto.",
        emailContacto="operaciones@aegissecurity.es",
        telefono="+34 910 003 303",
        servicioAsociado="Recinto completo y Accesos",
        estado="disponible"
    )
]

bloqueo = Lock()

# ==========================================
# --- FUNCIONES AUXILIARES ---
# ==========================================

def buscar_proveedor_disponible(id_proveedor: int) -> Proveedor:
    for prov in proveedores_db:
        if prov.id == id_proveedor and prov.estado == "disponible":
            return prov
    raise HTTPException(404, "El proveedor solicitado no existe o no se encuentra disponible actualmente.")

# US-016-AC-05: Seguridad para funciones de gestión (Administrador)
def verificar_admin(rol_usuario: str = Header("admin", description="Rol del usuario en la sesión")):
    if rol_usuario != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado. Se requieren permisos de administrador.")
    return rol_usuario

@app.exception_handler(RequestValidationError)
async def error_validacion(request, exc):
    return JSONResponse(status_code=400, content={"codigo": 400, "mensaje": "Datos o parametros de consulta no validos"})

@app.get("/")
def inicio():
    return {"mensaje": "Microservicio Proveedores funcionando"}


# ==========================================
# --- RUTAS PÚBLICAS (US-015) ---
# ==========================================

# US-015-AC-01, AC-02, AC-04 y AC-05: Consultar proveedores disponibles
@app.get("/api/proveedores", response_model=RespuestaConsultaProveedores)
def listar_proveedores_disponibles(categoria: CategoriaProveedor | None = None):
    with bloqueo:
        disponibles = [
            p for p in proveedores_db
            if p.estado == "disponible" and (categoria is None or p.categoria == categoria)
        ]

        if not disponibles:
            return RespuestaConsultaProveedores(
                total=0,
                mensaje="Actualmente no existen proveedores registrados y disponibles en la plataforma.",
                proveedores=[]
            )

        return RespuestaConsultaProveedores(
            total=len(disponibles),
            mensaje="Proveedores disponibles recuperados correctamente.",
            proveedores=disponibles
        )

# US-015-AC-03 y AC-04: Seleccionar un proveedor específico
@app.get("/api/proveedores/{idProveedor}", response_model=Proveedor)
def obtener_detalle_proveedor(idProveedor: int):
    with bloqueo:
        return buscar_proveedor_disponible(idProveedor)


# ==========================================
# --- RUTAS PRIVADAS DE ADMINISTRADOR (US-016) ---
# ==========================================

# US-016-AC-01: El administrador puede consultar todos los proveedores (incluyendo inactivos)
@app.get("/api/admin/proveedores", response_model=list[Proveedor], dependencies=[Depends(verificar_admin)])
def listar_todos_proveedores():
    with bloqueo:
        return proveedores_db

# US-016-AC-02: Registrar nuevo proveedor
@app.post("/api/admin/proveedores", response_model=Proveedor, dependencies=[Depends(verificar_admin)])
def crear_proveedor(prov: ProveedorBase):
    with bloqueo:
        nuevo_id = max([p.id for p in proveedores_db] + [0]) + 1
        nuevo = Proveedor(id=nuevo_id, **prov.dict())
        proveedores_db.append(nuevo)
        return nuevo

# US-016-AC-03: Modificar proveedor
@app.put("/api/admin/proveedores/{id_prov}", response_model=Proveedor, dependencies=[Depends(verificar_admin)])
def modificar_proveedor(id_prov: int, prov_actualizado: ProveedorBase):
    with bloqueo:
        for i, p in enumerate(proveedores_db):
            if p.id == id_prov:
                proveedores_db[i] = Proveedor(id=id_prov, **prov_actualizado.dict())
                return proveedores_db[i]
    raise HTTPException(status_code=404, detail="Proveedor no encontrado.")

# US-016-AC-04: Eliminar o deshabilitar proveedor
@app.delete("/api/admin/proveedores/{id_prov}", dependencies=[Depends(verificar_admin)])
def eliminar_proveedor(id_prov: int):
    with bloqueo:
        for i, p in enumerate(proveedores_db):
            if p.id == id_prov:
                prov_eliminado = proveedores_db.pop(i)
                return {"mensaje": f"Proveedor '{prov_eliminado.nombre}' eliminado correctamente."}
    raise HTTPException(status_code=404, detail="Proveedor no encontrado.")