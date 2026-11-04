import unittest
from fastapi.testclient import TestClient
from mainUsuario002 import app, sesiones_activas

class TestSesion(unittest.TestCase):
    def setUp(self):
        sesiones_activas.clear()
        self.cliente = TestClient(app)

    def test_login_logout_y_bloqueo(self):
        respuesta = self.cliente.post('/api/login', json={'email':'usuario@gmail.com','password':'123'})
        self.assertEqual(respuesta.status_code, 200)
        token = respuesta.json()['token']
        cabecera = {'Authorization':f'Bearer {token}'}
        self.assertEqual(self.cliente.get('/api/privado',headers=cabecera).status_code,200)
        self.assertEqual(self.cliente.post('/api/logout',headers=cabecera).status_code,200)
        self.assertEqual(self.cliente.get('/api/privado',headers=cabecera).status_code,401)

    def test_acceso_sin_login(self):
        self.assertEqual(self.cliente.get('/api/privado').status_code,401)

    def test_login_incorrecto(self):
        self.assertEqual(self.cliente.post('/api/login',json={'email':'usuario@gmail.com','password':'incorrecta'}).status_code,401)

    def test_logout_repetido(self):
        token = self.cliente.post('/api/login',json={'email':'admin@subsonic.com','password':'123'}).json()['token']
        headers={'Authorization':f'Bearer {token}'}
        self.assertEqual(self.cliente.post('/api/logout',headers=headers).status_code,200)
        self.assertEqual(self.cliente.post('/api/logout',headers=headers).status_code,401)

if __name__=='__main__': unittest.main()
