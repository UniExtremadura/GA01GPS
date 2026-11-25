"""Pruebas de alta y modificación de espacios (SCRUM-66)."""
import copy
import unittest
from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

from Espacios import main as espacios_api
from Espacios.catalogo import espacios

ADMIN = {"Authorization": "Bearer token-admin"}
USUARIO = {"Authorization": "Bearer token-cliente"}


def consultar_sesion(url, *, headers, timeout):
    roles = {"Bearer token-admin": "admin", "Bearer token-cliente": "cliente"}
    rol = roles.get(headers["Authorization"])
    return httpx.Response(
        200 if rol else 401,
        json={"rol": rol},
        request=httpx.Request("GET", url),
    )


class GestionEspaciosAdminTests(unittest.TestCase):
    def setUp(self):
        self.original = copy.deepcopy(espacios)
        self.next_id = espacios_api._siguiente_id
        self.client = TestClient(espacios_api.app)
        self.addCleanup(self.client.close)
        servicio = patch.object(espacios_api.httpx, "get", side_effect=consultar_sesion)
        servicio.start()
        self.addCleanup(servicio.stop)

    def tearDown(self):
        espacios[:] = self.original
        espacios_api._siguiente_id = self.next_id

    @staticmethod
    def datos(**cambios):
        valores = {
            "nombre": "Zona de descanso nueva",
            "tipo": "sala",
            "zona": "Este",
            "capacidad": 120,
            "descripcion": "Espacio de descanso para asistentes del festival.",
            "habilitado": True,
            "disponible": True,
        }
        valores.update(cambios)
        return valores

    def test_administrador_crea_espacio(self):
        respuesta = self.client.post("/api/admin/espacios", json=self.datos(), headers=ADMIN)
        self.assertEqual(respuesta.status_code, 201, respuesta.text)
        creado = respuesta.json()
        self.assertEqual(creado["nombre"], "Zona de descanso nueva")
        self.assertGreater(creado["id"], 0)
        self.assertIn(creado["id"], [item["id"] for item in espacios])

    def test_administrador_modifica_espacio(self):
        respuesta = self.client.put(
            "/api/admin/espacios/1",
            json=self.datos(nombre="Escenario renovado", capacidad=6200),
            headers=ADMIN,
        )
        self.assertEqual(respuesta.status_code, 200, respuesta.text)
        self.assertEqual(respuesta.json()["nombre"], "Escenario renovado")
        self.assertEqual(respuesta.json()["capacidad"], 6200)
        self.assertEqual(respuesta.json()["id"], 1)

    def test_usuario_sin_rol_admin_no_puede_crear_ni_modificar(self):
        antes = copy.deepcopy(espacios)
        crear = self.client.post("/api/admin/espacios", json=self.datos(), headers=USUARIO)
        editar = self.client.put("/api/admin/espacios/1", json=self.datos(), headers=USUARIO)
        self.assertEqual(crear.status_code, 403)
        self.assertEqual(editar.status_code, 403)
        self.assertEqual(espacios, antes)

    def test_datos_invalidos_no_se_guardan_y_detallan_campo(self):
        antes = copy.deepcopy(espacios)
        respuesta = self.client.post(
            "/api/admin/espacios", json=self.datos(capacidad=0), headers=ADMIN
        )
        self.assertEqual(respuesta.status_code, 400)
        self.assertIn("capacidad", [e["campo"] for e in respuesta.json()["errores"]])
        self.assertEqual(espacios, antes)

    def test_nombre_duplicado_devuelve_conflicto(self):
        antes = copy.deepcopy(espacios)
        respuesta = self.client.post(
            "/api/admin/espacios", json=self.datos(nombre="escenario principal"), headers=ADMIN
        )
        self.assertEqual(respuesta.status_code, 409)
        self.assertEqual(espacios, antes)

    def test_id_inexistente_devuelve_404(self):
        respuesta = self.client.put(
            "/api/admin/espacios/999", json=self.datos(), headers=ADMIN
        )
        self.assertEqual(respuesta.status_code, 404)

    def test_listado_y_detalle_incluyen_espacios_no_publicos(self):
        listado = self.client.get("/api/admin/espacios", headers=ADMIN)
        self.assertEqual(listado.status_code, 200)
        self.assertEqual({e["id"] for e in listado.json()}, {e["id"] for e in espacios})
        detalle = self.client.get("/api/admin/espacios/7", headers=ADMIN)
        self.assertEqual(detalle.status_code, 200)
        self.assertFalse(detalle.json()["habilitado"])

    def test_baja_conserva_ficha_y_oculta_espacio_al_publico(self):
        ruta = "/api/admin/espacios/1"
        original = self.client.get(ruta, headers=ADMIN).json()
        respuesta = self.client.delete(ruta, headers=ADMIN)
        self.assertEqual(respuesta.status_code, 200)
        esperado = {**original, "habilitado": False, "disponible": False}
        self.assertEqual(self.client.get(ruta, headers=ADMIN).json(), esperado)
        self.assertEqual(self.client.delete(ruta, headers=ADMIN).json(), esperado)
        self.assertEqual(self.client.get("/api/espacios/1").status_code, 404)
        self.assertNotIn(1, [e["id"] for e in self.client.get("/api/espacios").json()])

    def test_baja_de_espacio_inexistente_devuelve_404(self):
        self.assertEqual(self.client.delete("/api/admin/espacios/999", headers=ADMIN).status_code, 404)

    def test_listado_detalle_y_baja_exigen_sesion_admin(self):
        antes = copy.deepcopy(espacios)
        base = "/api/admin/espacios"
        for metodo, ruta in [("GET", base), ("GET", f"{base}/1"), ("DELETE", f"{base}/1")]:
            self.assertEqual(self.client.request(metodo, ruta, headers=USUARIO).status_code, 403)
            self.assertEqual(self.client.request(metodo, ruta, headers={"X-User-Role": "admin"}).status_code, 401)
            self.assertEqual(self.client.request(metodo, ruta, headers={"Authorization": "Bearer falso"}).status_code, 401)
        self.assertEqual(espacios, antes)

    def test_fallo_del_servicio_de_sesion_no_autoriza_baja(self):
        antes = copy.deepcopy(espacios)
        with patch.object(espacios_api.httpx, "get", side_effect=httpx.ConnectError("Sin conexión")):
            respuesta = self.client.delete("/api/admin/espacios/1", headers=ADMIN)
        self.assertEqual(respuesta.status_code, 503)
        self.assertEqual(espacios, antes)


if __name__ == "__main__":
    unittest.main()
