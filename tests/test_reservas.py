"""Pruebas de aceptación US-010: disponibilidad y reservas de espacios."""
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient
from Espacios.main import app
from Espacios import reservas


class TestReservasUS010(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.parche_db = patch.object(reservas, 'RUTA_RESERVAS', Path(self.temporal.name) / 'reservas.sqlite3')
        self.parche_db.start()
        # Se simula la respuesta del servicio de autenticación únicamente
        # para las pruebas de reservas; el código de producción no se altera.
        app.dependency_overrides[reservas.identificar_usuario] = lambda: 2
        self.cliente = TestClient(app)
        self.fecha = (date.today() + timedelta(days=3)).isoformat()
        self.franja = {'fecha': self.fecha, 'horaInicio': '10:00', 'horaFin': '12:00'}

    def tearDown(self):
        app.dependency_overrides.clear()
        self.cliente.close()
        self.parche_db.stop()
        self.temporal.cleanup()

    def reservar(self, espacio=1, franja=None):
        return self.cliente.post(f'/api/espacios/{espacio}/reservas', json=franja or self.franja)

    def disponibilidad(self, espacio=1, franja=None):
        return self.cliente.get(f'/api/espacios/{espacio}/disponibilidad', params=franja or self.franja)

    def test_01_espacio_libre_antes_de_reservar(self):
        respuesta = self.disponibilidad()
        self.assertEqual(respuesta.status_code, 200)
        self.assertTrue(respuesta.json()['disponible'])

    def test_02_reserva_correcta_se_guarda(self):
        respuesta = self.reservar()
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(respuesta.json()['idUsuario'], 2)
        self.assertEqual(respuesta.json()['idEspacio'], 1)
        self.assertFalse(self.disponibilidad().json()['disponible'])

    def test_03_reserva_duplicada_rechazada(self):
        self.assertEqual(self.reservar().status_code, 201)
        respuesta = self.reservar()
        self.assertEqual(respuesta.status_code, 409)
        self.assertIn('reservado', respuesta.json()['mensaje'].lower())

    def test_04_franjas_solapadas_rechazadas(self):
        self.reservar()
        respuesta = self.reservar(franja={**self.franja, 'horaInicio': '11:00', 'horaFin': '13:00'})
        self.assertEqual(respuesta.status_code, 409)

    def test_05_franjas_contiguas_permitidas(self):
        self.assertEqual(self.reservar().status_code, 201)
        respuesta = self.reservar(franja={**self.franja, 'horaInicio': '12:00', 'horaFin': '13:00'})
        self.assertEqual(respuesta.status_code, 201)

    def test_06_espacios_distintos_no_se_bloquean(self):
        self.assertEqual(self.reservar(1).status_code, 201)
        self.assertEqual(self.reservar(2).status_code, 201)

    def test_07_sin_sesion_no_puede_reservar(self):
        app.dependency_overrides.clear()
        # Sin Authorization, la dependencia original debe rechazar la reserva.
        respuesta = self.reservar()
        self.assertEqual(respuesta.status_code, 401)

    def test_08_horario_invalido(self):
        respuesta = self.reservar(franja={**self.franja, 'horaInicio': '14:00', 'horaFin': '12:00'})
        self.assertEqual(respuesta.status_code, 400)

    def test_09_fecha_pasada(self):
        pasado = (date.today() - timedelta(days=1)).isoformat()
        respuesta = self.reservar(franja={**self.franja, 'fecha': pasado})
        self.assertEqual(respuesta.status_code, 400)

    def test_10_espacio_no_disponible(self):
        respuesta = self.reservar(999)
        self.assertEqual(respuesta.status_code, 404)

    def test_11_reserva_persiste_entre_consultas(self):
        self.assertEqual(self.reservar().status_code, 201)
        with self.cliente:
            respuesta = self.disponibilidad()
        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(respuesta.json()['disponible'])


if __name__ == '__main__':
    unittest.main()
