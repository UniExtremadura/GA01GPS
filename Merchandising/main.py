"""US-017 y US-018: Consulta de catálogo, existencias ficticias, adquisición simulada y gestión de merchandising."""
from threading import Lock
from typing import List

from fastapi import FastAPI, HTTPException, Header
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field


app = FastAPI(title="API Merchandising - Subsonic Festival", version="1.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500", "http://127.0.0.1:5500",
        "http://localhost:8080", "http://127.0.0.1:8080",
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


class Producto(BaseModel):
    id: int = Field(gt=0, strict=True)
    nombre: str
    descripcion: str
    precio: float = Field(ge=0, allow_inf_nan=False)
    categoria: str
    icono: str = "♫"
    stockDisponible: int = Field(ge=0, strict=True)
    habilitado: bool = True

    @computed_field
    @property
    def disponible(self) -> bool:
        # La disponibilidad se calcula desde el stock, no se guarda por separado.
        return self.habilitado and self.stockDisponible > 0


# MODIFICACIÓN: MODELOS DE DATOS PARA LA ADQUISICIÓN SIMULADA Y LA GESTIÓN ADMINISTRATIVA (US-018)
class CompraRequest(BaseModel):
    producto_id: int = Field(gt=0, strict=True)
    cantidad: int = Field(gt=0, strict=True, default=1)
    confirmado: bool = Field(..., description="AC-03: Permite confirmar o cancelar la operación")

class ProductoAdminSchema(BaseModel):
    nombre: str
    descripcion: str
    precio: float = Field(ge=0, allow_inf_nan=False)
    categoria: str
    icono: str = "♫"
    stockDisponible: int = Field(ge=0, strict=True)
    habilitado: bool = True


# Catalogo ficticio basado en los productos de la interfaz del equipo.
productos = [
    Producto(id=1, nombre="Camiseta Subsonic", descripcion="Camiseta oficial del festival, algodón cómodo y diseño edición 2026.", precio=22.5, categoria="Ropa", icono="👕", stockDisponible=25),
    Producto(id=2, nombre="Tote bag del festival", descripcion="Bolsa reutilizable con ilustración exclusiva de Subsonic Festival.", precio=9.9, categoria="Accesorios", icono="👜", stockDisponible=12),
    Producto(id=3, nombre="Vaso reutilizable", descripcion="Vaso oficial reutilizable para disfrutar de los conciertos.", precio=4.5, categoria="Accesorios", icono="🥤", stockDisponible=0),
    Producto(id=4, nombre="Sudadera Subsonic", descripcion="Sudadera edición festival, ideal para las noches de conciertos.", precio=38, categoria="Ropa", icono="🧥", stockDisponible=8),
]

# MODIFICACIÓN: ALMACENAMIENTO PROVISIONAL PARA LAS ADQUISICIONES SIMULADAS DE LOS USUARIOS (US-018)
adquisiciones = []
contador_transacciones = 1

bloqueo = Lock()


@app.exception_handler(HTTPException)
async def error_http(request, exc):
    return JSONResponse(status_code=exc.status_code, content={
        "codigo": exc.status_code, "mensaje": str(exc.detail)
    })


@app.exception_handler(RequestValidationError)
async def error_validacion(request, exc):
    return JSONResponse(status_code=400, content={
        "codigo": 400, "mensaje": "Error en los datos o identificador proporcionado"
    })


@app.get("/")
def inicio():
    return {"mensaje": "Microservicio Merchandising funcionando"}


@app.get("/api/productos", response_model=list[Producto])
def listar_productos():
    # Los agotados se muestran como tales; los deshabilitados se ocultan.
    with bloqueo:
        return [producto.model_copy(deep=True) for producto in productos if producto.habilitado]


@app.get("/api/productos/{idProducto}", response_model=Producto)
def consultar_producto(idProducto: int):
    with bloqueo:
        for producto in productos:
            if producto.id == idProducto and producto.habilitado:
                return producto.model_copy(deep=True)
    raise HTTPException(404, "Producto no encontrado o no habilitado")


# ==========================================
# ENDPOINTS IMPLEMENTADOS PARA LA US-018
# ==========================================

@app.post("/api/merch/comprar")
def realizar_compra_simulada(compra: CompraRequest, x_usuario_id: int = Header(..., alias="X-Usuario-ID")):
    global contador_transacciones
    with bloqueo:
        # MODIFICACIÓN: SELECCIONAR Y COMPROBAR DISPONIBILIDAD DEL PRODUCTO (US-018-AC-01, AC-02)
        prod_encontrado = None
        for p in productos:
            if p.id == compra.producto_id and p.habilitado:
                prod_encontrado = p
                break
        
        if not prod_encontrado:
            raise HTTPException(404, "El producto seleccionado no existe o no está disponible.")

        # MODIFICACIÓN: VALIDAR SI EL USUARIO HA CONFIRMADO O CANCELADO LA OPERACIÓN (US-018-AC-03)
        if not compra.confirmado:
            raise HTTPException(400, "Operación cancelada por el usuario antes de completarse.")

        if prod_encontrado.stockDisponible < compra.cantidad:
            raise HTTPException(400, "No hay suficiente stock disponible para completar la adquisición.")

        # MODIFICACIÓN: ACTUALIZAR LAS EXISTENCIAS FICTICIAS TRAS LA COMPRA
        prod_encontrado.stockDisponible -= compra.cantidad
        importe_total = prod_encontrado.precio * compra.cantidad

        # MODIFICACIÓN: REGISTRAR LA ADQUISICIÓN ASOCIADA AL USUARIO SIN PASARELAS DE PAGO REALES (US-018-AC-04, AC-05)
        nueva_adquisicion = {
            "id_transaccion": contador_transacciones,
            "usuario_id": x_usuario_id,
            "producto": prod_encontrado.nombre,
            "cantidad": compra.cantidad,
            "importe_total": importe_total,
            "estado": "EXITO_SIMULADO",
            "mensaje": "Adquisición realizada correctamente sin cargos bancarios reales."
        }
        adquisiciones.append(nueva_adquisicion)
        contador_transacciones += 1

        # MODIFICACIÓN: INFORMAR AL USUARIO DEL RESULTADO DE LA OPERACIÓN (US-018-AC-10)
        return {
            "mensaje": "La adquisición simulada de merchandising se ha completado con éxito.",
            "detalle": nueva_adquisicion
        }


@app.post("/api/admin/productos", response_model=Producto)
def crear_producto_admin(nuevo_prod: ProductoAdminSchema, x_rol: str = Header(..., alias="X-Rol")):
    # MODIFICACIÓN: RESTRINGIR EL ACCESO A FUNCIONES DE GESTIÓN SI NO ES ADMINISTRADOR (US-018-AC-06, AC-09)
    if x_rol != "admin":
        raise HTTPException(403, "Acceso denegado: Se requieren privilegios de administrador.")

    with bloqueo:
        nuevo_id = max([p.id for p in productos], default=0) + 1
        producto_creado = Producto(
            id=nuevo_id,
            nombre=nuevo_prod.nombre,
            descripcion=nuevo_prod.descripcion,
            precio=nuevo_prod.precio,
            categoria=nuevo_prod.categoria,
            icono=nuevo_prod.icono,
            stockDisponible=nuevo_prod.stockDisponible,
            habilitado=nuevo_prod.habilitado
        )
        productos.append(producto_creado)
        # MODIFICACIÓN: INFORMAR DEL RESULTADO DE LA CREACIÓN (US-018-AC-10)
        return producto_creado.model_copy(deep=True)


@app.put("/api/admin/productos/{idProducto}", response_model=Producto)
def modificar_producto_admin(idProducto: int, datos_act: ProductoAdminSchema, x_rol: str = Header(..., alias="X-Rol")):
    # MODIFICACIÓN: RESTRINGIR EL ACCESO A MODIFICACIONES SI NO ES ADMINISTRADOR (US-018-AC-07, AC-09)
    if x_rol != "admin":
        raise HTTPException(403, "Acceso denegado: Se requieren privilegios de administrador.")

    with bloqueo:
        for p in productos:
            if p.id == idProducto:
                p.nombre = datos_act.nombre
                p.descripcion = datos_act.descripcion
                p.precio = datos_act.precio
                p.categoria = datos_act.categoria
                p.icono = datos_act.icono
                p.stockDisponible = datos_act.stockDisponible
                p.habilitado = datos_act.habilitado
                # MODIFICACIÓN: INFORMAR DEL RESULTADO DE LA ACTUALIZACIÓN (US-018-AC-10)
                return p.model_copy(deep=True)
        raise HTTPException(404, "Producto no encontrado para modificar.")


@app.delete("/api/admin/productos/{idProducto}")
def deshabilitar_producto_admin(idProducto: int, x_rol: str = Header(..., alias="X-Rol")):
    # MODIFICACIÓN: RESTRINGIR EL ACCESO A DESHABILITACIÓN/ELIMINACIÓN SI NO ES ADMINISTRADOR (US-018-AC-08, AC-09)
    if x_rol != "admin":
        raise HTTPException(403, "Acceso denegado: Se requieren privilegios de administrador.")

    with bloqueo:
        for p in productos:
            if p.id == idProducto:
                p.habilitado = False
                # MODIFICACIÓN: INFORMAR CLARAMENTE DEL RESULTADO DE LA DESHABILITACIÓN (US-018-AC-10)
                return {"mensaje": f"El producto con ID {idProducto} ha sido deshabilitado correctamente del catálogo."}
        raise HTTPException(404, "Producto no encontrado para deshabilitar.")