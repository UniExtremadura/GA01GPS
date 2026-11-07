"""Pruebas del alta administrativa de servicios (SCRUM-69)."""
import copy
import unittest
from fastapi.testclient import TestClient

import serviciosUS013 as api

ADMIN = {"rol_usuario": "admin"}


class CrearServiciosTests(unittest.TestCase):
    def setUp(self):
        self.original = copy.deepcopy(api.servicios_db)
        self.client = TestClient(api.app)
        self.addCleanup(self.client.close)

    def tearDown(self):
        api.servicios_db[:] = self.original

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
        response = self.client.post("/api/admin/servicios", json=self.payload(), headers={"rol_usuario": "cliente"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(api.servicios_db, before)

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
