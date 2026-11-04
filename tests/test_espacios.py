import unittest
from unittest.mock import patch

from Espacios.catalogo import consultar_espacio, consultar_espacios, espacios


class ConsultaEspaciosTests(unittest.TestCase):
    def test_solo_habilitados_y_disponibles(self):
        self.assertEqual([e["id"] for e in consultar_espacios()], [1, 2, 3, 4, 5])

    def test_datos_para_identificar_cada_espacio(self):
        for espacio in consultar_espacios():
            for campo in ("id", "nombre", "tipo", "zona", "capacidad", "descripcion"):
                self.assertIn(campo, espacio)

    def test_nombre_parcial_sin_distinguir_tildes(self):
        self.assertEqual([e["id"] for e in consultar_espacios(nombre=" ELECTRONICA ")], [2])

    def test_tipo(self):
        self.assertEqual([e["id"] for e in consultar_espacios(tipo="camping")], [3])

    def test_zona(self):
        self.assertEqual([e["id"] for e in consultar_espacios(zona="Norte")], [1, 4])

    def test_capacidad_incluye_limite(self):
        self.assertEqual([e["id"] for e in consultar_espacios(capacidad_minima=2000)], [1, 2])

    def test_filtros_combinados(self):
        self.assertEqual([e["id"] for e in consultar_espacios(tipo="escenario", zona="Sur", capacidad_minima=100)], [2])

    def test_sin_coincidencias(self):
        self.assertEqual(consultar_espacios(nombre="inexistente"), [])
        self.assertEqual(consultar_espacios(tipo="camping", zona="Norte"), [])

    def test_detalle(self):
        self.assertEqual(consultar_espacio(3)["nombre"], "Camping Encinas")

    def test_detalle_inexistente_o_no_disponible(self):
        for identificador in (6, 7, 999):
            self.assertIsNone(consultar_espacio(identificador))

    def test_consulta_refleja_estado_actual(self):
        with patch.dict(espacios[0], disponible=False):
            self.assertIsNone(consultar_espacio(1))
            self.assertNotIn(1, [e["id"] for e in consultar_espacios()])

    def test_consulta_no_modifica_datos(self):
        resultado = consultar_espacios()
        resultado[0]["nombre"] = "Cambio externo"
        self.assertEqual(consultar_espacio(1)["nombre"], "Escenario Principal")


if __name__ == "__main__":
    unittest.main()
