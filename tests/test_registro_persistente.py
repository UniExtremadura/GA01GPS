"""Pruebas de la subtarea US-001: persistencia y comprobación del registro."""
import importlib
import os
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient


class RegistroPersistenteTests(unittest.TestCase):
    def setUp(self):
        self.directorio = tempfile.TemporaryDirectory()
        os.environ['SUBSONIC_USUARIOS_DB'] = str(Path(self.directorio.name) / 'usuarios.sqlite3')
        import Usuarios.almacenamiento as almacenamiento
        import Usuarios.main as usuarios_api
        importlib.reload(almacenamiento)
        self.api = importlib.reload(usuarios_api)
        self.cliente = TestClient(self.api.app)
        self.datos = {
            'nombre': 'Ana', 'apellidos': 'Prueba', 'email': 'Ana@Ejemplo.com',
            'password': 'claveSegura123', 'tipo': 'cliente'
        }

    def tearDown(self):
        self.cliente.close()
        self.directorio.cleanup()
        os.environ.pop('SUBSONIC_USUARIOS_DB', None)

    def test_registro_correcto_y_comprobacion_en_listado(self):
        resultado = self.cliente.post('/api/usuarios', json=self.datos)
        self.assertEqual(resultado.status_code, 201)
        usuario = resultado.json()
        self.assertEqual(usuario['email'], 'ana@ejemplo.com')
        self.assertNotIn('password', usuario)
        self.assertEqual(self.cliente.get(f"/api/usuarios/{usuario['id']}").status_code, 200)
        self.assertTrue(any(x['id'] == usuario['id'] for x in self.cliente.get('/api/usuarios').json()))
        import Usuarios.almacenamiento as almacenamiento
        self.assertEqual(len(almacenamiento.cargar_registros()), 1)
        self.assertNotEqual(almacenamiento.cargar_registros()[0][1]['hash'], self.datos['password'])

    def test_correo_repetido_no_se_guarda(self):
        self.assertEqual(self.cliente.post('/api/usuarios', json=self.datos).status_code, 201)
        repetido = {**self.datos, 'email': ' ANA@EJEMPLO.COM '}
        self.assertEqual(self.cliente.post('/api/usuarios', json=repetido).status_code, 409)
        import Usuarios.almacenamiento as almacenamiento
        self.assertEqual(len(almacenamiento.cargar_registros()), 1)

    def test_datos_invalidos_no_se_guardan(self):
        invalido = {**self.datos, 'email': 'no-es-email'}
        self.assertEqual(self.cliente.post('/api/usuarios', json=invalido).status_code, 400)
        corto = {**self.datos, 'password': '123'}
        self.assertEqual(self.cliente.post('/api/usuarios', json=corto).status_code, 400)
        import Usuarios.almacenamiento as almacenamiento
        self.assertEqual(len(almacenamiento.cargar_registros()), 0)

    def test_registro_permanece_tras_reiniciar_modulo(self):
        creado = self.cliente.post('/api/usuarios', json=self.datos).json()
        self.cliente.close()
        import Usuarios.main as usuarios_api
        self.api = importlib.reload(usuarios_api)
        self.cliente = TestClient(self.api.app)
        self.assertEqual(self.cliente.get(f"/api/usuarios/{creado['id']}").status_code, 200)
        inicio = self.cliente.post('/api/usuarios/login', json={
            'email': self.datos['email'], 'password': self.datos['password']
        })
        self.assertEqual(inicio.status_code, 200)

    def test_eliminacion_tambien_es_persistente(self):
        creado = self.cliente.post('/api/usuarios', json=self.datos).json()
        self.assertEqual(self.cliente.delete(f"/api/usuarios/{creado['id']}").status_code, 204)
        self.cliente.close()
        import Usuarios.main as usuarios_api
        self.api = importlib.reload(usuarios_api)
        self.cliente = TestClient(self.api.app)
        self.assertEqual(self.cliente.get(f"/api/usuarios/{creado['id']}").status_code, 404)


if __name__ == '__main__':
    unittest.main()
