"""Pruebas de validación de productos (SCRUM-51).

Desde la raíz del repositorio:
    python -m unittest tests.test_merchandising_validaciones -v
"""
import copy
import unittest

from fastapi.testclient import TestClient

from Merchandising import main as merchandising


ADMIN = {"X-User-Role": "admin"}
USER = {"X-User-Role": "user"}


class ValidacionProductosTests(unittest.TestCase):
    def setUp(self):
        self.productos_originales = copy.deepcopy(merchandising.productos_db)
        self.siguiente_id_original = merchandising._siguiente_id
        self.client = TestClient(merchandising.app)
        self.addCleanup(self.client.close)

    def tearDown(self):
        merchandising.productos_db[:] = self.productos_originales
        merchandising._siguiente_id = self.siguiente_id_original

    @staticmethod
    def producto_valido(**cambios):
        producto = {
            "codigo": "MER-TEST-901",
            "nombre": "Producto de prueba",
            "descripcion": "Descripción de producto ficticio para pruebas.",
            "categoria": "ropa",
            "precio": 15.5,
            "stockDisponible": 10,
            "disponible": True,
            "icono": "🎁",
        }
        producto.update(cambios)
        return producto

    def comprobar_rechazo_con_error(self, respuesta, campo_esperado):
        self.assertEqual(respuesta.status_code, 400, respuesta.text)
        cuerpo = respuesta.json()
        self.assertIn("mensaje", cuerpo)
        self.assertTrue(cuerpo["errores"], cuerpo)
        campos = [error["campo"] for error in cuerpo["errores"]]
        self.assertIn(campo_esperado, campos)

    def test_creacion_rechaza_precio_negativo_y_no_guarda(self):
        antes = copy.deepcopy(merchandising.productos_db)
        respuesta = self.client.post(
            "/api/admin/productos",
            json=self.producto_valido(precio=-1),
            headers=ADMIN,
        )
        self.comprobar_rechazo_con_error(respuesta, "precio")
        self.assertEqual(merchandising.productos_db, antes)

    def test_creacion_rechaza_nombre_vacio_y_no_guarda(self):
        antes = copy.deepcopy(merchandising.productos_db)
        respuesta = self.client.post(
            "/api/admin/productos",
            json=self.producto_valido(nombre="   "),
            headers=ADMIN,
        )
        self.comprobar_rechazo_con_error(respuesta, "nombre")
        self.assertEqual(merchandising.productos_db, antes)

    def test_creacion_rechaza_stock_cero_disponible_y_no_guarda(self):
        antes = copy.deepcopy(merchandising.productos_db)
        respuesta = self.client.post(
            "/api/admin/productos",
            json=self.producto_valido(stockDisponible=0, disponible=True),
            headers=ADMIN,
        )
        self.comprobar_rechazo_con_error(respuesta, "disponible")
        self.assertEqual(merchandising.productos_db, antes)

    def test_creacion_rechaza_campos_extra_y_no_guarda(self):
        antes = copy.deepcopy(merchandising.productos_db)
        respuesta = self.client.post(
            "/api/admin/productos",
            json=self.producto_valido(id=99),
            headers=ADMIN,
        )
        self.comprobar_rechazo_con_error(respuesta, "id")
        self.assertEqual(merchandising.productos_db, antes)

    def test_codigo_duplicado_devuelve_conflicto_y_no_guarda(self):
        antes = copy.deepcopy(merchandising.productos_db)
        duplicado = merchandising.productos_db[0].codigo
        respuesta = self.client.post(
            "/api/admin/productos",
            json=self.producto_valido(codigo=duplicado),
            headers=ADMIN,
        )
        self.assertEqual(respuesta.status_code, 409)
        self.assertIn("código", respuesta.json()["detail"])
        self.assertEqual(merchandising.productos_db, antes)

    def test_edicion_invalida_no_altera_producto_existente(self):
        antes = merchandising.productos_db[0].model_copy(deep=True)
        payload = self.producto_valido(
            codigo=antes.codigo,
            nombre=antes.nombre,
            descripcion=antes.descripcion,
            categoria=antes.categoria,
            precio=-20,
            stockDisponible=antes.stockDisponible,
            disponible=antes.disponible,
            icono=antes.icono,
        )
        respuesta = self.client.put("/api/admin/productos/1", json=payload, headers=ADMIN)
        self.comprobar_rechazo_con_error(respuesta, "precio")
        self.assertEqual(merchandising.productos_db[0], antes)

    def test_rol_no_administrador_no_puede_crear_editar_ni_eliminar(self):
        antes = copy.deepcopy(merchandising.productos_db)
        payload = self.producto_valido()
        respuestas = [
            self.client.post("/api/admin/productos", json=payload, headers=USER),
            self.client.put("/api/admin/productos/1", json=payload, headers=USER),
            self.client.delete("/api/admin/productos/1", headers=USER),
        ]
        self.assertEqual([r.status_code for r in respuestas], [403, 403, 403])
        self.assertEqual(merchandising.productos_db, antes)


if __name__ == "__main__":
    unittest.main()
