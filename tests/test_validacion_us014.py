"""US-014: permisos, validaciones y actualización del catálogo administrativo."""
import copy
import unittest
from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

import serviciosUS013 as api

ADMIN = {"Authorization": "Bearer token-admin"}
CLIENTE = {"Authorization": "Bearer token-cliente"}


class ValidacionServiciosUS014(unittest.TestCase):
    def setUp(self):
        self.original = copy.deepcopy(api.servicios_db)
        self.compras = copy.deepcopy(api.adquisiciones_db)
        self.client = TestClient(api.app)
        self.addCleanup(self.client.close)
        mocked = patch.object(api.httpx, "get", side_effect=self.verificar_sesion)
        mocked.start()
        self.addCleanup(mocked.stop)

    def tearDown(self):
        api.servicios_db[:] = self.original
        api.adquisiciones_db[:] = self.compras

    @staticmethod
    def verificar_sesion(url, *, headers, timeout):
        token = headers.get("Authorization")
        roles = {"Bearer token-admin": "admin", "Bearer token-cliente": "cliente"}
        request = httpx.Request("GET", url)
        if token not in roles:
            return httpx.Response(401, json={"detail": "No autorizado"}, request=request)
        return httpx.Response(200, json={"rol": roles[token]}, request=request)

    @staticmethod
    def datos(**cambios):
        servicio = {
            "nombre": "Zona de juegos", "categoria": "Ocio",
            "descripcion": "Acceso a actividades recreativas del festival.",
            "precio": 12.5, "disponible": True,
        }
        servicio.update(cambios)
        return servicio

    def test_01_sin_sesion_no_puede_gestionar(self):
        for metodo, ruta in [("GET", "/api/admin/servicios"),
                             ("POST", "/api/admin/servicios"),
                             ("PUT", "/api/admin/servicios/1"),
                             ("DELETE", "/api/admin/servicios/1")]:
            r = self.client.request(metodo, ruta, json=self.datos())
            self.assertEqual(r.status_code, 401, (metodo, r.text))
        self.assertEqual(api.servicios_db, self.original)

    def test_02_cliente_no_puede_gestionar(self):
        for metodo, ruta in [("GET", "/api/admin/servicios"),
                             ("POST", "/api/admin/servicios"),
                             ("PUT", "/api/admin/servicios/1"),
                             ("DELETE", "/api/admin/servicios/1")]:
            r = self.client.request(metodo, ruta, headers=CLIENTE, json=self.datos())
            self.assertEqual(r.status_code, 403, (metodo, r.text))
        self.assertEqual(api.servicios_db, self.original)

    def test_03_token_invalido_rechazado(self):
        r = self.client.get("/api/admin/servicios", headers={"Authorization": "Bearer falso"})
        self.assertEqual(r.status_code, 401)

    def test_04_rol_en_cabecera_no_concede_permisos(self):
        r = self.client.post("/api/admin/servicios", headers={"rol_usuario": "admin"}, json=self.datos())
        self.assertEqual(r.status_code, 401)

    def test_05_admin_puede_crear_y_consultar(self):
        r = self.client.post("/api/admin/servicios", headers=ADMIN, json=self.datos())
        self.assertEqual(r.status_code, 201, r.text)
        nuevo = r.json()
        self.assertEqual(nuevo["nombre"], "Zona de juegos")
        detalle = self.client.get(f'/api/admin/servicios/{nuevo["id"]}', headers=ADMIN)
        self.assertEqual(detalle.status_code, 200)
        self.assertEqual(detalle.json(), nuevo)

    def test_06_campos_vacios_rechazados_sin_guardar(self):
        r = self.client.post("/api/admin/servicios", headers=ADMIN, json=self.datos(nombre="  "))
        self.assertEqual(r.status_code, 400, r.text)
        self.assertEqual(api.servicios_db, self.original)

    def test_07_precio_negativo_rechazado_sin_guardar(self):
        r = self.client.post("/api/admin/servicios", headers=ADMIN, json=self.datos(precio=-3))
        self.assertEqual(r.status_code, 400, r.text)
        self.assertEqual(api.servicios_db, self.original)

    def test_08_nombre_duplicado_rechazado(self):
        r = self.client.post("/api/admin/servicios", headers=ADMIN,
                             json=self.datos(nombre=api.servicios_db[0].nombre))
        self.assertEqual(r.status_code, 409, r.text)
        self.assertEqual(api.servicios_db, self.original)

    def test_09_campos_no_permitidos_rechazados(self):
        r = self.client.post("/api/admin/servicios", headers=ADMIN,
                             json=self.datos(rol="admin"))
        self.assertEqual(r.status_code, 400, r.text)
        self.assertEqual(api.servicios_db, self.original)

    def test_10_admin_modifica_y_cambio_se_refleja(self):
        r = self.client.put("/api/admin/servicios/1", headers=ADMIN,
                            json=self.datos(nombre="Zona renovada", precio=30))
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(r.json()["precio"], 30)
        publico = self.client.get("/api/servicios")
        self.assertEqual(publico.status_code, 200)
        actualizado = next(s for s in publico.json() if s["id"] == 1)
        self.assertEqual(actualizado["nombre"], "Zona renovada")
        self.assertEqual(actualizado["precio"], 30)

    def test_11_modificacion_invalida_no_altera_registro(self):
        r = self.client.put("/api/admin/servicios/1", headers=ADMIN,
                            json=self.datos(descripcion="x"))
        self.assertEqual(r.status_code, 400, r.text)
        self.assertEqual(api.servicios_db, self.original)

    def test_12_admin_deshabilita_y_no_se_puede_adquirir(self):
        r = self.client.delete("/api/admin/servicios/1", headers=ADMIN)
        self.assertEqual(r.status_code, 200, r.text)
        self.assertFalse(r.json()["disponible"])
        publico = self.client.get("/api/servicios").json()
        self.assertFalse(next(s for s in publico if s["id"] == 1)["disponible"])
        compra = self.client.post("/api/servicios/adquirir", json={"idUsuario": 2, "idServicio": 1})
        self.assertEqual(compra.status_code, 400, compra.text)

    def test_13_servicio_inexistente_devuelve_404(self):
        r = self.client.put("/api/admin/servicios/99999", headers=ADMIN, json=self.datos())
        self.assertEqual(r.status_code, 404, r.text)

    def test_14_fallo_verificacion_sesion_deniega_acceso(self):
        with patch.object(api.httpx, "get", side_effect=httpx.ConnectError("Sin conexión")):
            r = self.client.post("/api/admin/servicios", headers=ADMIN, json=self.datos())
        self.assertEqual(r.status_code, 503, r.text)
        self.assertEqual(api.servicios_db, self.original)


if __name__ == "__main__":
    unittest.main()
