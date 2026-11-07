"""Comprobaciones de aceptación US-007 contra la API existente."""
import unittest
from fastapi.testclient import TestClient
from mainEntradasAdquiridas import app

class CriteriosAceptacionUS007(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_ac01_consulta_con_identificador(self):
        r = self.client.get('/api/mis-entradas', headers={'X-Usuario-ID': '2'})
        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.json()['entradas']), 0)

    def test_ac02_informacion_de_cada_entrada(self):
        r = self.client.get('/api/mis-entradas', headers={'X-Usuario-ID': '2'})
        for entrada in r.json()['entradas']:
            self.assertTrue({'tipo_entrada', 'fecha_adquisicion', 'estado'}.issubset(entrada))
            self.assertTrue(all(entrada[campo] for campo in ('tipo_entrada', 'fecha_adquisicion', 'estado')))

    def test_ac03_filtrado_por_identificador(self):
        r = self.client.get('/api/mis-entradas', headers={'X-Usuario-ID': '3'})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(all(e['usuario_id'] == 3 for e in r.json()['entradas']))

    def test_ac04_mensaje_si_no_hay_entradas(self):
        r = self.client.get('/api/mis-entradas', headers={'X-Usuario-ID': '3'})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['total_entradas'], 0)
        self.assertEqual(r.json()['entradas'], [])
        self.assertIn('No tienes entradas', r.json()['mensaje'])

    def test_acceso_sin_cabecera_no_autorizado(self):
        r = self.client.get('/api/mis-entradas')
        self.assertNotEqual(r.status_code, 200)

    @unittest.expectedFailure
    def test_seguridad_pendiente_no_suplantar_identidad(self):
        """Limitación conocida: X-Usuario-ID puede falsificarse sin sesión real."""
        r = self.client.get('/api/mis-entradas', headers={'X-Usuario-ID': '2'})
        self.assertNotEqual(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()
