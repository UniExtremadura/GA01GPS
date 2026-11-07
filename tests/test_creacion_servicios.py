"""Pruebas del alta administrativa de servicios (SCRUM-69)."""
import copy
import unittest
from unittest.mock import patch
import httpx
from fastapi.testclient import TestClient

import serviciosUS013 as api

ADMIN = {"Authorization": "Bearer admin"}
CLIENTE = {"Authorization": "Bearer cliente"}


class CrearServiciosTests(unittest.TestCase):
    def setUp(self):
        self.original = copy.deepcopy(api.servicios_db)
        self.client = TestClient(api.app)
        self.addCleanup(self.client.close)
        self.original_adquisiciones = copy.deepcopy(api.adquisiciones_db)
        sesion = patch.object(api.httpx, "get", side_effect=self.consultar_sesion)
        sesion.start()
        self.addCleanup(sesion.stop)

    def tearDown(self):
        api.servicios_db[:] = self.original
        api.adquisiciones_db[:] = self.original_adquisiciones

    @staticmethod
    def consultar_sesion(url, *, headers, timeout):
        rol = {"Bearer admin": "admin", "Bearer cliente": "cliente"}.get(headers["Authorization"])
        return httpx.Response(200 if rol else 401, json={"rol": rol}, request=httpx.Request("GET", url))

    @staticmethod
    def payload(**changes):
        data = {
            "nombre": "Servicio de prueba",
            "categoria": "Comodidad",
            "descripcion": "Servicio ficticio para verificar el alta.",
            "precio": 11.5,
            "disponible": True,
        }
        data.update(changes)
        return data

    def test_admin_crea_servicio_y_aparece_en_catalogo(self):
        response = self.client.post("/api/admin/servicios", json=self.payload(), headers=ADMIN)
        self.assertEqual(response.status_code, 201, response.text)
        service = response.json()
        self.assertEqual(service["nombre"], "Servicio de prueba")
        self.assertGreater(service["id"], 0)
        catalog = self.client.get("/api/admin/servicios", headers=ADMIN).json()
        self.assertIn(service["id"], [item["id"] for item in catalog])

    def test_rechaza_solicitud_sin_rol_admin(self):
        before = copy.deepcopy(api.servicios_db)
        response = self.client.post("/api/admin/servicios", json=self.payload(), headers=CLIENTE)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(api.servicios_db, before)

    def test_edicion_reflejada_en_listado_publico_y_detalle_admin(self):
        datos = self.payload(nombre="  Servicio actualizado  ", precio=20)
        respuesta = self.client.put("/api/admin/servicios/1", json=datos, headers=ADMIN)
        self.assertEqual(respuesta.status_code, 200, respuesta.text)
        esperado = {"id": 1, **datos, "nombre": "Servicio actualizado"}
        self.assertEqual(self.client.get("/api/admin/servicios/1", headers=ADMIN).json(), esperado)
        self.assertIn(esperado, self.client.get("/api/servicios").json())

    def test_edicion_invalida_o_duplicada_conserva_datos(self):
        original = self.client.get("/api/admin/servicios/1", headers=ADMIN).json()
        for datos, codigo in [(self.payload(precio=-1), 400), (self.payload(nombre=api.servicios_db[1].nombre), 409)]:
            self.assertEqual(self.client.put("/api/admin/servicios/1", json=datos, headers=ADMIN).status_code, codigo)
        self.assertEqual(self.client.get("/api/admin/servicios/1", headers=ADMIN).json(), original)

    def test_baja_preserva_adquisicion_previa_y_bloquea_otra(self):
        solicitud = {"idUsuario": 2, "idServicio": 1}
        self.assertEqual(self.client.post("/api/servicios/adquirir", json=solicitud).status_code, 200)
        anteriores = copy.deepcopy(api.adquisiciones_db)
        ruta = "/api/admin/servicios/1"
        baja = self.client.delete(ruta, headers=ADMIN)
        self.assertEqual(baja.status_code, 200)
        self.assertFalse(baja.json()["disponible"])
        self.assertEqual(self.client.delete(ruta, headers=ADMIN).json(), baja.json())
        self.assertEqual(self.client.get(ruta, headers=ADMIN).json(), baja.json())
        self.assertIn(baja.json(), self.client.get("/api/servicios").json())
        self.assertEqual(self.client.post("/api/servicios/adquirir", json=solicitud).status_code, 400)
        self.assertEqual(api.adquisiciones_db, anteriores)

    def test_gestion_rechaza_cliente_y_rol_declarado(self):
        for metodo, ruta in [("GET", "/api/admin/servicios"), ("GET", "/api/admin/servicios/1"),
                             ("PUT", "/api/admin/servicios/1"), ("DELETE", "/api/admin/servicios/1")]:
            self.assertEqual(self.client.request(metodo, ruta, headers=CLIENTE, json=self.payload()).status_code, 403)
            self.assertEqual(self.client.request(metodo, ruta, headers={"rol_usuario": "admin"}).status_code, 401)
        self.assertEqual(api.servicios_db, self.original)

    def test_servicio_inexistente(self):
        for metodo in ("GET", "PUT", "DELETE"):
            self.assertEqual(self.client.request(
                metodo, "/api/admin/servicios/999", json=self.payload(), headers=ADMIN,
            ).status_code, 404)

    def test_rechaza_campos_obligatorios_vacios_sin_guardar(self):
        before = copy.deepcopy(api.servicios_db)
        response = self.client.post("/api/admin/servicios", json=self.payload(nombre="   "), headers=ADMIN)
        self.assertEqual(response.status_code, 400)
        self.assertIn("errores", response.json())
        self.assertEqual(api.servicios_db, before)

    def test_rechaza_precio_negativo_sin_guardar(self):
        before = copy.deepcopy(api.servicios_db)
        response = self.client.post("/api/admin/servicios", json=self.payload(precio=-1), headers=ADMIN)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(api.servicios_db, before)

    def test_rechaza_nombre_duplicado(self):
        before = copy.deepcopy(api.servicios_db)
        response = self.client.post("/api/admin/servicios", json=self.payload(nombre=api.servicios_db[0].nombre), headers=ADMIN)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(api.servicios_db, before)


if __name__ == "__main__":
    unittest.main()
