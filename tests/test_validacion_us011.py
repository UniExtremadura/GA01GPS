"""US-011: permisos, validaciones y disponibilidad de espacios."""
import copy
import unittest
from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient
from Espacios import main as api
from Espacios.catalogo import espacios

ADMIN = {'Authorization': 'Bearer admin-test'}
CLIENTE = {'Authorization': 'Bearer cliente-test'}


def sesion_simulada(url, *, headers, timeout):
    roles = {'Bearer admin-test': 'admin', 'Bearer cliente-test': 'cliente'}
    rol = roles.get(headers.get('Authorization'))
    return httpx.Response(200 if rol else 401, json={'rol': rol}, request=httpx.Request('GET', url))


class ValidacionUS011(unittest.TestCase):
    def setUp(self):
        self.copia = copy.deepcopy(espacios)
        self.id_inicial = api._siguiente_id
        self.cliente = TestClient(api.app)
        self.addCleanup(self.cliente.close)
        parche = patch.object(api.httpx, 'get', side_effect=sesion_simulada)
        parche.start()
        self.addCleanup(parche.stop)

    def tearDown(self):
        espacios[:] = self.copia
        api._siguiente_id = self.id_inicial

    @staticmethod
    def datos(**cambios):
        datos = {'nombre': 'Nueva sala de pruebas', 'tipo': 'sala', 'zona': 'Este',
                 'capacidad': 100, 'descripcion': 'Sala para realizar pruebas de gestión.',
                 'habilitado': True, 'disponible': True}
        datos.update(cambios)
        return datos

    def test_01_sin_sesion_no_se_puede_gestionar(self):
        original = copy.deepcopy(espacios)
        for metodo, ruta, cuerpo in [('get','/api/admin/espacios',None),
                                     ('post','/api/admin/espacios',self.datos()),
                                     ('put','/api/admin/espacios/1',self.datos()),
                                     ('delete','/api/admin/espacios/1',None)]:
            respuesta = getattr(self.cliente, metodo)(ruta, headers={}, **({'json': cuerpo} if cuerpo else {}))
            self.assertEqual(respuesta.status_code, 401, (metodo, respuesta.text))
        self.assertEqual(espacios, original)

    def test_02_cliente_no_puede_gestionar(self):
        original = copy.deepcopy(espacios)
        for metodo, ruta, cuerpo in [('get','/api/admin/espacios',None),
                                     ('post','/api/admin/espacios',self.datos()),
                                     ('put','/api/admin/espacios/1',self.datos()),
                                     ('delete','/api/admin/espacios/1',None)]:
            respuesta = getattr(self.cliente, metodo)(ruta, headers=CLIENTE, **({'json': cuerpo} if cuerpo else {}))
            self.assertEqual(respuesta.status_code, 403, (metodo, respuesta.text))
        self.assertEqual(espacios, original)

    def test_03_token_falso_no_autoriza(self):
        respuesta = self.cliente.post('/api/admin/espacios', json=self.datos(), headers={'Authorization': 'Bearer falso'})
        self.assertEqual(respuesta.status_code, 401)

    def test_04_administrador_puede_crear_y_consultar(self):
        respuesta = self.cliente.post('/api/admin/espacios', json=self.datos(), headers=ADMIN)
        self.assertEqual(respuesta.status_code, 201, respuesta.text)
        id_espacio = respuesta.json()['id']
        detalle = self.cliente.get(f'/api/admin/espacios/{id_espacio}', headers=ADMIN)
        self.assertEqual(detalle.status_code, 200)
        self.assertEqual(detalle.json()['nombre'], self.datos()['nombre'])

    def test_05_capacidad_invalida_no_se_guarda(self):
        original = copy.deepcopy(espacios)
        respuesta = self.cliente.post('/api/admin/espacios', json=self.datos(capacidad=0), headers=ADMIN)
        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(espacios, original)

    def test_06_campos_obligatorios_y_tipos_invalidos(self):
        for cambios in [{'nombre': ' '}, {'tipo': 'inexistente'}, {'zona': 'Centro'},
                        {'descripcion': 'a'}, {'capacidad': -1}]:
            respuesta = self.cliente.post('/api/admin/espacios', json=self.datos(**cambios), headers=ADMIN)
            self.assertEqual(respuesta.status_code, 400, (cambios, respuesta.text))

    def test_07_nombre_repetido_no_se_guarda(self):
        original = copy.deepcopy(espacios)
        respuesta = self.cliente.post('/api/admin/espacios', json=self.datos(nombre='ESCENARIO PRINCIPAL'), headers=ADMIN)
        self.assertEqual(respuesta.status_code, 409)
        self.assertEqual(espacios, original)

    def test_08_actualizar_disponibilidad_se_refleja_en_catalogo(self):
        self.assertEqual(self.cliente.get('/api/espacios/1').status_code, 200)
        respuesta = self.cliente.put('/api/admin/espacios/1', json=self.datos(nombre='Escenario Principal', disponible=False), headers=ADMIN)
        self.assertEqual(respuesta.status_code, 200, respuesta.text)
        self.assertFalse(respuesta.json()['disponible'])
        self.assertEqual(self.cliente.get('/api/espacios/1').status_code, 404)
        self.assertFalse(self.cliente.get('/api/admin/espacios/1', headers=ADMIN).json()['disponible'])

    def test_09_deshabilitar_oculta_espacio_y_conserva_registro(self):
        respuesta = self.cliente.delete('/api/admin/espacios/1', headers=ADMIN)
        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(respuesta.json()['habilitado'])
        self.assertEqual(self.cliente.get('/api/espacios/1').status_code, 404)
        self.assertEqual(self.cliente.get('/api/admin/espacios/1', headers=ADMIN).status_code, 200)

    def test_10_espacio_inexistente_devuelve_404(self):
        respuesta = self.cliente.put('/api/admin/espacios/99999', json=self.datos(), headers=ADMIN)
        self.assertEqual(respuesta.status_code, 404)

    def test_11_si_falla_autenticacion_no_se_modifica(self):
        original = copy.deepcopy(espacios)
        with patch.object(api.httpx, 'get', side_effect=httpx.ConnectError('Sin servicio')):
            respuesta = self.cliente.delete('/api/admin/espacios/1', headers=ADMIN)
        self.assertEqual(respuesta.status_code, 503)
        self.assertEqual(espacios, original)


if __name__ == '__main__':
    unittest.main()
