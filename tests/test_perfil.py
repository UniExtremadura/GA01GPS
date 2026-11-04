import unittest
from fastapi.testclient import TestClient
from mainPerfil import app, DB_PERFILES, SESIONES


class PruebasPerfil(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        SESIONES.clear()
        DB_PERFILES[1].nombre = "Usuario Asistente"
        DB_PERFILES[1].email = "asistente@festival.com"

    def autorizacion(self, usuario_id=2):
        respuesta = self.client.post("/api/demo/login", json={"usuario_id": usuario_id})
        self.assertEqual(respuesta.status_code, 200)
        return {"Authorization": "Bearer " + respuesta.json()["access_token"]}

    def test_modifica_y_consulta_los_datos(self):
        headers = self.autorizacion()
        respuesta = self.client.put("/api/perfil", headers=headers, json={"nombre": "Nombre Nuevo", "email": "nuevo@festival.com"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(self.client.get("/api/perfil", headers=headers).json()["nombre"], "Nombre Nuevo")

    def test_rechaza_datos_invalidos(self):
        headers = self.autorizacion()
        respuesta = self.client.put("/api/perfil", headers=headers, json={"nombre": "X", "email": "correo-invalido"})
        self.assertEqual(respuesta.status_code, 422)

    def test_impide_modificar_otro_perfil(self):
        headers = self.autorizacion(2)
        respuesta = self.client.put("/api/perfil", headers=headers, json={"id": 3, "nombre": "Intruso", "email": "intruso@festival.com"})
        self.assertEqual(respuesta.status_code, 422)
        self.assertEqual(DB_PERFILES[2].nombre, "Otro Usuario")

    def test_requiere_autenticacion(self):
        respuesta = self.client.put("/api/perfil", json={"nombre": "Nuevo", "email": "nuevo@festival.com"})
        self.assertEqual(respuesta.status_code, 401)

    def test_no_permite_correo_duplicado(self):
        headers = self.autorizacion(2)
        respuesta = self.client.put("/api/perfil", headers=headers, json={"nombre": "Usuario", "email": "otro@festival.com"})
        self.assertEqual(respuesta.status_code, 409)


if __name__ == "__main__":
    unittest.main()