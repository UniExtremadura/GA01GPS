"""Pruebas del listado de entradas adquiridas (US-007)."""
import unittest
from fastapi.testclient import TestClient
from mainEntradasAdquiridas import app


class TestListadoEntradas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_usuario_con_entradas(self):
        respuesta = self.client.get('/api/mis-entradas', headers={'X-Usuario-ID': '2'})
        self.assertEqual(respuesta.status_code, 200)
        datos = respuesta.json()
        self.assertEqual(datos['total_entradas'], 2)
        self.assertEqual(len(datos['entradas']), 2)

    def test_campos_visibles(self):
        respuesta = self.client.get('/api/mis-entradas', headers={'X-Usuario-ID': '2'})
        for entrada in respuesta.json()['entradas']:
            for campo in ('id_entrada', 'tipo_entrada', 'fecha_adquisicion', 'estado'):
                self.assertIn(campo, entrada)

    def test_usuario_sin_entradas(self):
        respuesta = self.client.get('/api/mis-entradas', headers={'X-Usuario-ID': '3'})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()['entradas'], [])
        self.assertEqual(respuesta.json()['total_entradas'], 0)

    def test_no_muestra_entradas_ajenas(self):
        respuesta = self.client.get('/api/mis-entradas', headers={'X-Usuario-ID': '3'})
        self.assertFalse(any(e['usuario_id'] == 2 for e in respuesta.json()['entradas']))

    def test_falta_identificador(self):
        respuesta = self.client.get('/api/mis-entradas')
        self.assertNotEqual(respuesta.status_code, 200)


if __name__ == '__main__':
    unittest.main()
