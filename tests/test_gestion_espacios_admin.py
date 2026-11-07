"""Pruebas de alta y modificación de espacios (SCRUM-66)."""
import copy
import unittest

from fastapi.testclient import TestClient

from Espacios import main as espacios_api
from Espacios.catalogo import espacios

ADMIN = {"X-User-Role": "admin"}
USUARIO = {"X-User-Role": "user"}


class GestionEspaciosAdminTests(unittest.TestCase):
    def setUp(self):
        self.original = copy.deepcopy(espacios)
        self.next_id = espacios_api._siguiente_id
        self.client = TestClient(espacios_api.app)
        self.addCleanup(self.client.close)

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


if __name__ == "__main__":
    unittest.main()
