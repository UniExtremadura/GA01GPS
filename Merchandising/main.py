"""API CRUD de administración de merchandising (US-018 / SCRUM-50)."""
from threading import Lock

from fastapi import Depends, FastAPI, Header, HTTPException, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .catalogo import CategoriaProducto, PRODUCTOS_MOCK, ProductoMerchandising

app = FastAPI(
    title="API Administración de Merchandising - Subsonic Festival",
    description="Alta, consulta, modificación y baja de productos para administradores.",
    version="1.0.0",
)

# Copia de trabajo en memoria inicializada con el catálogo ficticio SCRUM-49.
# Los cambios se conservan solo mientras el proceso esté activo.
productos_db: list[ProductoMerchandising] = [p.model_copy(deep=True) for p in PRODUCTOS_MOCK]
_siguiente_id = max((producto.id for producto in productos_db), default=0) + 1
_bloqueo = Lock()


class ProductoDatos(BaseModel):
    """Datos editables de producto; el identificador lo gestiona el servicio."""

    model_config = ConfigDict(extra="forbid")

    codigo: str = Field(min_length=3, max_length=20)
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: str = Field(min_length=5, max_length=500)
    categoria: CategoriaProducto
    precio: float = Field(ge=0, allow_inf_nan=False)
    stockDisponible: int = Field(ge=0)
    disponible: bool
    icono: str = Field(default="🎁", max_length=8)

    @field_validator("disponible")
    @classmethod
    def validar_disponibilidad(cls, disponible, info):
        if disponible and info.data.get("stockDisponible") == 0:
            raise ValueError("No se puede marcar como disponible un producto sin stock.")
        return disponible

    @field_validator("codigo", "nombre", "descripcion", mode="before")
    @classmethod
    def normalizar_y_exigir_texto(cls, valor):
        if isinstance(valor, str):
            valor = valor.strip()
            if not valor:
                raise ValueError("Este campo es obligatorio y no puede estar vacío.")
        return valor


def exigir_administrador(x_user_role: str = Header(default="", alias="X-User-Role")):
    """Permite las rutas de gestión únicamente para sesiones de rol admin."""
    if x_user_role.strip().casefold() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requieren permisos de administrador.",
        )


@app.exception_handler(RequestValidationError)
async def error_validacion(request, exc):
    errores = [
        {
            "campo": ".".join(str(parte) for parte in error.get("loc", ())[1:]) or "solicitud",
            "mensaje": error.get("msg", "Valor no válido."),
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "codigo": 400,
            "mensaje": "Revisa los datos del producto y corrige los campos indicados.",
            "errores": errores,
        },
    )


def buscar_producto(id_producto: int) -> ProductoMerchandising:
    producto = next((p for p in productos_db if p.id == id_producto), None)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    return producto


def comprobar_codigo_unico(codigo: str, excluir_id: int | None = None) -> None:
    if any(p.codigo.casefold() == codigo.casefold() and p.id != excluir_id for p in productos_db):
        raise HTTPException(status_code=409, detail="Ya existe un producto con ese código.")


@app.get("/", tags=["Estado"])
def inicio():
    return {"mensaje": "API de administración de merchandising funcionando"}


@app.get(
    "/api/admin/productos",
    response_model=list[ProductoMerchandising],
    dependencies=[Depends(exigir_administrador)],
    tags=["Administración de productos"],
)
def listar_productos_admin():
    """Consulta todos los productos, incluidos los agotados o deshabilitados."""
    with _bloqueo:
        return [p.model_copy(deep=True) for p in productos_db]


@app.get(
    "/api/admin/productos/{id_producto}",
    response_model=ProductoMerchandising,
    dependencies=[Depends(exigir_administrador)],
    tags=["Administración de productos"],
)
def obtener_producto_admin(id_producto: int):
    with _bloqueo:
        return buscar_producto(id_producto).model_copy(deep=True)


@app.post(
    "/api/admin/productos",
    response_model=ProductoMerchandising,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(exigir_administrador)],
    tags=["Administración de productos"],
)
def crear_producto(datos: ProductoDatos):
    global _siguiente_id
    with _bloqueo:
        comprobar_codigo_unico(datos.codigo)
        producto = ProductoMerchandising(id=_siguiente_id, **datos.model_dump())
        _siguiente_id += 1
        productos_db.append(producto)
        return producto.model_copy(deep=True)


@app.put(
    "/api/admin/productos/{id_producto}",
    response_model=ProductoMerchandising,
    dependencies=[Depends(exigir_administrador)],
    tags=["Administración de productos"],
)
def editar_producto(id_producto: int, datos: ProductoDatos):
    with _bloqueo:
        actual = buscar_producto(id_producto)
        comprobar_codigo_unico(datos.codigo, excluir_id=id_producto)
        actualizado = ProductoMerchandising(id=id_producto, **datos.model_dump())
        productos_db[productos_db.index(actual)] = actualizado
        return actualizado.model_copy(deep=True)


@app.delete(
    "/api/admin/productos/{id_producto}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(exigir_administrador)],
    tags=["Administración de productos"],
)
def eliminar_producto(id_producto: int):
    with _bloqueo:
        producto = buscar_producto(id_producto)
        productos_db.remove(producto)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


