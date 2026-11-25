import copy
import unittest
from fastapi.testclient import TestClient
from admin_entradas_api import app, ENTRADAS

client = TestClient(app)
ADMIN = {"Authorization": "Bearer demo-admin-token"}
USER = {"Authorization": "Bearer demo-user-token"}

class TestAdminEntradas(unittest.TestCase):
    def setUp(self):
        self.original = copy.deepcopy(ENTRADAS)
        self.valid = {"nombre": "vip", "descripcion": "VIP actualizado", "precio": 160,
                      "stockTotal": 120, "fechaInicioValidez": "2026-11-10", "fechaFinValidez": "2026-11-12"}

    def tearDown(self):
        ENTRADAS.clear()
        ENTRADAS.update(self.original)

    def test_sin_sesion(self):
        self.assertEqual(client.put('/api/entradas/1', json=self.valid).status_code, 401)

    def test_usuario_sin_permisos(self):
        self.assertEqual(client.put('/api/entradas/1', json=self.valid, headers=USER).status_code, 403)
        self.assertEqual(client.get('/api/entradas', headers=USER).status_code, 403)

    def test_token_falso(self):
        self.assertEqual(client.put('/api/entradas/1', json=self.valid, headers={"Authorization": "Bearer falso"}).status_code, 401)

    def test_administrador_actualiza(self):
        r = client.put('/api/entradas/1', json=self.valid, headers=ADMIN)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['stockDisponible'], 110)
        self.assertEqual(client.get('/api/entradas/1', headers=ADMIN).json()['descripcion'], 'VIP actualizado')

    def test_validaciones(self):
        for cambio in ({'precio': -1}, {'stockTotal': 0}, {'fechaFinValidez': '2026-11-09'}, {'nombre': 'otro'}):
            with self.subTest(cambio=cambio):
                self.assertEqual(client.put('/api/entradas/1', json={**self.valid, **cambio}, headers=ADMIN).status_code, 422)

    def test_no_reducir_stock_vendido(self):
        self.assertEqual(client.put('/api/entradas/1', json={**self.valid, 'stockTotal': 5}, headers=ADMIN).status_code, 409)

    def test_no_existe(self):
        self.assertEqual(client.put('/api/entradas/999', json=self.valid, headers=ADMIN).status_code, 404)

if __name__ == '__main__':
    unittest.main()
