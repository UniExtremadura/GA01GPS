"""Pruebas del flujo de adquisición simulada (SCRUM-92).

Ejecutar desde la raíz del repositorio:
    python -m unittest tests.test_adquisicion_simulada -v
"""
import copy
import unittest
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from Entradas import main as entradas


class AdquisicionSimuladaTests(unittest.TestCase):
    def setUp(self):
        self.original_tipos = copy.deepcopy(entradas.tipos_entrada)
        self.original_compras = copy.deepcopy(entradas.compras)
        self.original_usuarios = copy.deepcopy(entradas.entradas_usuarios)
        self.original_mapa = copy.deepcopy(entradas.entrada_a_compra)
        self.original_contadores = (
            entradas.contador_tipos,
            entradas.contador_compras,
            entradas.contador_entradas,
        )
        self.client = TestClient(entradas.app)
        self.addCleanup(self.client.close)
        self.metodos_pago = patch.object(entradas.httpx, "get", side_effect=self.respuesta_usuario)
        self.get_usuario = self.metodos_pago.start()
        self.addCleanup(self.metodos_pago.stop)
        self.cobro_real = patch.object(entradas.httpx, "post")
        self.post_externo = self.cobro_real.start()
        self.addCleanup(self.cobro_real.stop)

    def tearDown(self):
        entradas.tipos_entrada[:] = self.original_tipos
        entradas.compras[:] = self.original_compras
        entradas.entradas_usuarios[:] = self.original_usuarios
        entradas.entrada_a_compra.clear()
        entradas.entrada_a_compra.update(self.original_mapa)
        (entradas.contador_tipos, entradas.contador_compras,
         entradas.contador_entradas) = self.original_contadores

    @staticmethod
    def respuesta_usuario(url, timeout):
        """Simula el microservicio Usuarios; no contacta servicios externos."""
        if url.endswith("/usuarios/1/metodos-pago"):
            respuesta = Mock(status_code=200)
            respuesta.json.return_value = [{"id": 1, "tipo": "simulado"}]
            return respuesta
        return Mock(status_code=404)

    def datos_compra(self, **cambios):
        datos = {"idUsuario": 1, "idTipoEntrada": 1, "cantidad": 2, "idMetodoPago": 1}
        datos.update(cambios)
        return datos

    def test_compra_correcta_registra_compra_entradas_y_actualiza_stock(self):
        respuesta = self.client.post("/api/entradas/comprar", json=self.datos_compra())

        self.assertEqual(respuesta.status_code, 201, respuesta.text)
        compra = respuesta.json()
        self.assertEqual(compra["estado"], "completada")
        self.assertEqual(compra["cantidad"], 2)
        self.assertEqual(compra["precioTotal"], 300.0)
        self.assertEqual(entradas.tipos_entrada[0].stockDisponible, 998)
        self.assertEqual(len(entradas.entradas_usuarios), 2)
        self.assertTrue(all(e.idUsuario == 1 and e.estado == "valida" for e in entradas.entradas_usuarios))
        self.get_usuario.assert_called_once()

    def test_stock_insuficiente_no_crea_compra_ni_modifica_stock(self):
        respuesta = self.client.post(
            "/api/entradas/comprar",
            json=self.datos_compra(idTipoEntrada=1, cantidad=1001),
        )

        self.assertEqual(respuesta.status_code, 409)
        self.assertEqual(entradas.tipos_entrada[0].stockDisponible, 1000)
        self.assertEqual(entradas.compras, [])
        self.assertEqual(entradas.entradas_usuarios, [])

    def test_rechaza_cantidad_cero_sin_contactar_microservicio(self):
        respuesta = self.client.post(
            "/api/entradas/comprar", json=self.datos_compra(cantidad=0)
        )

        self.assertEqual(respuesta.status_code, 400)
        self.get_usuario.assert_not_called()
        self.assertEqual(entradas.compras, [])

    def test_rechaza_metodo_de_pago_que_no_pertenece_al_usuario(self):
        respuesta_http = Mock(status_code=200)
        respuesta_http.json.return_value = [{"id": 27}]
        self.get_usuario.side_effect = lambda url, timeout: respuesta_http

        respuesta = self.client.post(
            "/api/entradas/comprar", json=self.datos_compra(idMetodoPago=1)
        )

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(entradas.compras, [])
        self.assertEqual(entradas.tipos_entrada[0].stockDisponible, 1000)

    def test_adquisicion_no_invoca_ningun_cobro_externo(self):
        respuesta = self.client.post("/api/entradas/comprar", json=self.datos_compra())

        self.assertEqual(respuesta.status_code, 201, respuesta.text)
        self.post_externo.assert_not_called()
        self.assertTrue(all("metodos-pago" in llamada.args[0] for llamada in self.get_usuario.call_args_list))


if __name__ == "__main__":
    unittest.main()

