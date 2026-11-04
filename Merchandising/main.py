"""US-017: consulta del catalogo y de sus existencias ficticias."""
from threading import Lock

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field


app = FastAPI(title="API Merchandising - Subsonic Festival", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500", "http://127.0.0.1:5500",
        "http://localhost:8080", "http://127.0.0.1:8080",
    ],
    allow_methods=["GET"],
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


# Catalogo ficticio basado en los productos de la interfaz del equipo.
# Las cantidades son ejemplos para la demo, no existencias reales.
# Almacenamiento provisional: se reinicia al arrancar el proceso.
productos = [
    Producto(id=1, nombre="Camiseta Subsonic", descripcion="Camiseta oficial del festival, algodón cómodo y diseño edición 2026.", precio=22.5, categoria="Ropa", icono="👕", stockDisponible=25),
    Producto(id=2, nombre="Tote bag del festival", descripcion="Bolsa reutilizable con ilustración exclusiva de Subsonic Festival.", precio=9.9, categoria="Accesorios", icono="👜", stockDisponible=12),
    Producto(id=3, nombre="Vaso reutilizable", descripcion="Vaso oficial reutilizable para disfrutar de los conciertos.", precio=4.5, categoria="Accesorios", icono="🥤", stockDisponible=0),
    Producto(id=4, nombre="Sudadera Subsonic", descripcion="Sudadera edición festival, ideal para las noches de conciertos.", precio=38, categoria="Ropa", icono="🧥", stockDisponible=8),
]
bloqueo = Lock()


@app.exception_handler(HTTPException)
async def error_http(request, exc):
    return JSONResponse(status_code=exc.status_code, content={
        "codigo": exc.status_code, "mensaje": str(exc.detail)
    })


@app.exception_handler(RequestValidationError)
async def error_validacion(request, exc):
    return JSONResponse(status_code=400, content={
        "codigo": 400, "mensaje": "Identificador de producto no valido"
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
