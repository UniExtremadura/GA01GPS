"""Modelo y conjunto inicial de productos ficticios de merchandising.

El conjunto es temporal y en memoria; no representa productos reales ni
realiza operaciones de compra o pago.
"""
from typing import Literal

from pydantic import BaseModel, Field, model_validator

CategoriaProducto = Literal["ropa", "accesorios", "bebida", "coleccion"]


class ProductoMerchandising(BaseModel):
    """Datos que identifican un producto y su disponibilidad en el catálogo."""

    id: int = Field(gt=0, description="Identificador interno del producto")
    codigo: str = Field(min_length=3, max_length=20, description="Código único de catálogo")
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: str = Field(min_length=5, max_length=500)
    categoria: CategoriaProducto
    precio: float = Field(ge=0, description="Precio expresado en euros; no inicia ningún cobro")
    stockDisponible: int = Field(ge=0)
    disponible: bool
    icono: str = Field(default="🎁", max_length=8, description="Emoji ilustrativo para la interfaz")

    @model_validator(mode="after")
    def validar_disponibilidad(self):
        if self.disponible and self.stockDisponible == 0:
            raise ValueError("Un producto sin stock no puede figurar como disponible")
        return self


# Datos completamente ficticios para desarrollo y demostración.
# Se incluyen productos disponibles y uno agotado para cubrir ambos estados.
PRODUCTOS_MOCK: list[ProductoMerchandising] = [
    ProductoMerchandising(
        id=1, codigo="MER-CAM-001", nombre="Camiseta Subsonic",
        descripcion="Camiseta oficial del festival, algodón cómodo y diseño edición 2026.",
        categoria="ropa", precio=22.50, stockDisponible=80, disponible=True, icono="👕",
    ),
    ProductoMerchandising(
        id=2, codigo="MER-TOT-002", nombre="Tote bag del festival",
        descripcion="Bolsa reutilizable con ilustración exclusiva de Subsonic Festival.",
        categoria="accesorios", precio=9.90, stockDisponible=120, disponible=True, icono="👜",
    ),
    ProductoMerchandising(
        id=3, codigo="MER-VAS-003", nombre="Vaso reutilizable",
        descripcion="Vaso oficial reutilizable para disfrutar de los conciertos.",
        categoria="bebida", precio=4.50, stockDisponible=250, disponible=True, icono="🥤",
    ),
    ProductoMerchandising(
        id=4, codigo="MER-SUD-004", nombre="Sudadera Subsonic",
        descripcion="Sudadera edición festival, ideal para las noches de conciertos.",
        categoria="ropa", precio=38.00, stockDisponible=35, disponible=True, icono="🧥",
    ),
    ProductoMerchandising(
        id=5, codigo="MER-POS-005", nombre="Póster edición festival",
        descripcion="Póster conmemorativo del cartel de Subsonic Festival 2026.",
        categoria="coleccion", precio=12.00, stockDisponible=0, disponible=False, icono="🎨",
    ),
]
