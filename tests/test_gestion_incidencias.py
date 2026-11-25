"""Pruebas de la subtarea US-019."""
import os
import tempfile
import unittest

# El fichero de pruebas debe poder ejecutarse sin alterar la BD real.
_archivo = tempfile.NamedTemporaryFile(suffix='.sqlite3', delete=False)
_archivo.close()
os.environ['SUBSONIC_INCIDENCIAS_DB'] = _archivo.name

from fastapi.testclient import TestClient
import incidencias
from mainUsuario002 import sesiones_activas, usuarios_db


class TestGestionIncidencias(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cliente = TestClient(incidencias.app)

    @classmethod
    def tearDownClass(cls):
        cls.cliente.close()
        try: os.unlink(_archivo.name)
        except OSError: pass

    def setUp(self):
        sesiones_activas['token-admin-test'] = 1
        sesiones_activas['token-cliente-test'] = 2
        with incidencias.conectar() as con:
            con.execute('DELETE FROM incidencias')
        self.datos = {'idUsuario': 2, 'titulo': 'Fallo en entrada', 'descripcion': 'No se puede descargar la entrada'}

    def headers(self, token):
        return {'Authorization': f'Bearer {token}'}

    def registrar(self):
        r = self.cliente.post('/api/incidencias', json=self.datos)
        self.assertEqual(r.status_code, 201)
        return r.json()['idIncidencia']

    def test_registro_y_listado_admin(self):
        identificador = self.registrar()
        r = self.cliente.get('/api/admin/incidencias', headers=self.headers('token-admin-test'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()[0]['idIncidencia'], identificador)

    def test_detalle(self):
        identificador = self.registrar()
        r = self.cliente.get(f'/api/admin/incidencias/{identificador}', headers=self.headers('token-admin-test'))
        self.assertEqual(r.json()['estado'], 'Pendiente')

    def test_cambio_estado_y_filtro(self):
        identificador = self.registrar()
        r = self.cliente.patch(f'/api/admin/incidencias/{identificador}', json={'estado': 'Resuelta'}, headers=self.headers('token-admin-test'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['incidencia']['estado'], 'Resuelta')
        listado = self.cliente.get('/api/admin/incidencias?estado=Resuelta', headers=self.headers('token-admin-test'))
        self.assertEqual(len(listado.json()), 1)
        self.assertEqual(len(self.cliente.get('/api/admin/incidencias?estado=Pendiente', headers=self.headers('token-admin-test')).json()), 0)

    def test_sin_token(self):
        self.registrar()
        self.assertEqual(self.cliente.get('/api/admin/incidencias').status_code, 401)

    def test_cliente_no_puede_gestionar(self):
        identificador = self.registrar()
        self.assertEqual(self.cliente.get('/api/admin/incidencias', headers=self.headers('token-cliente-test')).status_code, 403)
        self.assertEqual(self.cliente.patch(f'/api/admin/incidencias/{identificador}', json={'estado':'Resuelta'}, headers=self.headers('token-cliente-test')).status_code, 403)

    def test_estado_invalido_no_cambia_datos(self):
        identificador = self.registrar()
        r = self.cliente.patch(f'/api/admin/incidencias/{identificador}', json={'estado': 'Cerrada'}, headers=self.headers('token-admin-test'))
        self.assertEqual(r.status_code, 422)
        detalle = self.cliente.get(f'/api/admin/incidencias/{identificador}', headers=self.headers('token-admin-test'))
        self.assertEqual(detalle.json()['estado'], 'Pendiente')

    def test_incidencia_inexistente(self):
        r = self.cliente.patch('/api/admin/incidencias/999999', json={'estado':'Resuelta'}, headers=self.headers('token-admin-test'))
        self.assertEqual(r.status_code, 404)

    def test_persistencia_conexion_nueva(self):
        identificador = self.registrar()
        self.cliente.patch(f'/api/admin/incidencias/{identificador}', json={'estado':'Resuelta'}, headers=self.headers('token-admin-test'))
        with incidencias.conectar() as con:
            fila = con.execute('SELECT estado FROM incidencias WHERE idIncidencia = ?', (identificador,)).fetchone()
        self.assertEqual(fila['estado'], 'Resuelta')


if __name__ == '__main__': unittest.main()
