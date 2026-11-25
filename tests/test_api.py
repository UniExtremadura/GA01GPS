"""Pruebas HTTP: requieren las dependencias de Espacios/requirements.txt."""
import unittest

from fastapi.testclient import TestClient

from Espacios.main import app


class ApiEspaciosTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.addCleanup(self.client.close)

    def test_listado_y_filtros(self):
        respuesta = self.client.get("/api/espacios", params={"tipo": "escenario", "zona": "Sur", "capacidad_minima": 2000})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual([e["id"] for e in respuesta.json()], [2])

    def test_sin_coincidencias(self):
        respuesta = self.client.get("/api/espacios", params={"nombre": "inexistente"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json(), [])

    def test_filtros_invalidos(self):
        for parametros in ({"capacidad_minima": -1}, {"capacidad_minima": "abc"}, {"tipo": "otro"}, {"zona": "otra"}):
            with self.subTest(parametros=parametros):
                respuesta = self.client.get("/api/espacios", params=parametros)
                self.assertEqual(respuesta.status_code, 400)
                self.assertIn("mensaje", respuesta.json())

    def test_detalle_y_no_disponibles(self):
        self.assertEqual(self.client.get("/api/espacios/1").status_code, 200)
        for identificador in (6, 7, 999):
            self.assertEqual(self.client.get(f"/api/espacios/{identificador}").status_code, 404)

    def test_cors_frontend(self):
        respuesta = self.client.get("/api/espacios", headers={"Origin": "http://127.0.0.1:5500"})
        self.assertEqual(respuesta.headers["access-control-allow-origin"], "http://127.0.0.1:5500")


if __name__ == "__main__":
    unittest.main()
