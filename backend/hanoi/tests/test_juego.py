import unittest

from hanoi import partida
from hanoi.juego import JuegoHanoi
from hanoi.partida import PartidaNoEncontrada

class TestJuegoHanoi(unittest.TestCase):
    def setUp(self):
        self.juego = JuegoHanoi(3)

    # Verifica base a tope, mayor abajo
    def test_estado_inicial(self):
        self.assertEqual(
            self.juego.estado(),
            {"origen": [3, 2, 1], "auxiliar": [], "destino": []},
        )

    # Evita que se cuelen objetos Disco, que romperían el JSON
    def test_estado_devuelve_enteros(self):
        for torre in self.juego.estado().values():
            for disco in torre:
                self.assertIsInstance(disco, int)

    def test_movimiento_valido(self):
        r = self.juego.mover("origen", "destino")
        self.assertTrue(r["ok"])
        self.assertEqual(
            self.juego.estado(),
            {"origen": [3, 2], "auxiliar": [], "destino": [1]},
        )

    def test_disco_pequeno_sobre_grande(self):
        self.juego.mover("origen", "destino")  # disco 1 a destino
        r = self.juego.mover("origen", "auxiliar")  # disco 2 a auxiliar vacia
        self.assertTrue(r["ok"])
        r = self.juego.mover("destino", "auxiliar")  # disco 1 sobre disco 2
        self.assertTrue(r["ok"])

    def test_torre_invalida(self):
        for origen, destino in [("torre1", "destino"), ("origen", "x"), (None, 5), (1, 2)]:
            r = self.juego.mover(origen, destino)
            self.assertFalse(r["ok"])
            self.assertIn("inválida", r["mensaje"])

    def test_origen_igual_a_destino(self):
        r = self.juego.mover("origen", "origen")
        self.assertFalse(r["ok"])
        self.assertIn("misma", r["mensaje"])

    def test_torre_origen_vacia(self):
        r = self.juego.mover("auxiliar", "destino")
        self.assertFalse(r["ok"])
        self.assertIn("no tiene discos", r["mensaje"])

    def test_disco_grande_sobre_pequeno(self):
        self.juego.mover("origen", "destino")        # disco 1 a destino
        # disco 2 sobre 1: inválido
        r = self.juego.mover("origen", "destino")
        self.assertFalse(r["ok"])
        self.assertIn("más pequeño", r["mensaje"])

    def test_movimiento_invalido_no_cambia_estado(self):
        self.juego.mover("origen", "destino")
        antes = self.juego.estado()
        self.juego.mover("origen", "destino")   # inválido
        self.juego.mover("auxiliar", "origen")  # inválido
        self.juego.mover("origen", "origen")    # inválido
        self.assertEqual(self.juego.estado(), antes)

    # Resuelve 3 discos en 7 movimientos (2^3 - 1) y comprueba que todos terminen en destino
    def test_partida_completa_3_discos(self):
        pasos = [
            ("origen", "destino"), ("origen", "auxiliar"), ("destino", "auxiliar"),
            ("origen", "destino"), ("auxiliar", "origen"), ("auxiliar", "destino"),
            ("origen", "destino"),
        ]
        for origen, destino in pasos:
            self.assertTrue(self.juego.mover(origen, destino)["ok"])
        self.assertEqual(
            self.juego.estado(),
            {"origen": [], "auxiliar": [], "destino": [3, 2, 1]},
        )

PASOS_3_DISCOS = [
    ("origen", "destino"), ("origen", "auxiliar"), ("destino", "auxiliar"),
    ("origen", "destino"), ("auxiliar", "origen"), ("auxiliar", "destino"),
    ("origen", "destino"),
]


def resolver(n, origen, destino, auxiliar, pasos):
    """Genera la solución óptima recursiva (para probar otras cantidades)."""
    if n == 0:
        return
    resolver(n - 1, origen, auxiliar, destino, pasos)
    pasos.append((origen, destino))
    resolver(n - 1, auxiliar, destino, origen, pasos)


class TestControlDePartida(unittest.TestCase):
    def setUp(self):
        self.juego = JuegoHanoi(3)

    def test_cantidad_de_discos_invalida(self):
        for invalido in (2, 9, "abc", None):
            with self.assertRaises(ValueError):
                JuegoHanoi(invalido)

    def test_cantidad_de_discos_en_los_limites(self):
        self.assertEqual(JuegoHanoi(3).discos, 3)
        self.assertEqual(JuegoHanoi(8).discos, 8)

    def test_contador_inicia_en_cero(self):
        self.assertEqual(self.juego.movimientos, 0)

    def test_contador_suma_solo_movimientos_validos(self):
        self.juego.mover("origen", "destino")      # válido
        self.assertEqual(self.juego.movimientos, 1)
        self.juego.mover("origen", "destino")      # inválido (grande sobre pequeño)
        self.juego.mover("auxiliar", "origen")     # inválido (origen vacío)
        self.juego.mover("origen", "origen")       # inválido (misma torre)
        self.juego.mover("x", "destino")           # inválido (torre inexistente)
        self.assertEqual(self.juego.movimientos, 1)

    def test_minimo_teorico(self):
        for n, esperado in [(3, 7), (4, 15), (5, 31), (8, 255)]:
            self.assertEqual(JuegoHanoi(n).minimo_teorico, esperado)

    def test_no_hay_victoria_al_inicio_ni_a_medias(self):
        self.assertFalse(self.juego.esta_ganado())
        self.juego.mover("origen", "destino")
        self.assertFalse(self.juego.esta_ganado())

    def test_victoria_3_discos_en_7_movimientos(self):
        for origen, destino in PASOS_3_DISCOS:
            self.assertTrue(self.juego.mover(origen, destino)["ok"])
        self.assertTrue(self.juego.esta_ganado())
        self.assertEqual(self.juego.movimientos, 7)
        self.assertEqual(self.juego.movimientos, self.juego.minimo_teorico)

    def test_victoria_con_otras_cantidades(self):
        for n in (4, 5, 8):
            juego = JuegoHanoi(n)
            pasos = []
            resolver(n, "origen", "destino", "auxiliar", pasos)
            for origen, destino in pasos:
                self.assertTrue(juego.mover(origen, destino)["ok"])
            self.assertTrue(juego.esta_ganado())
            self.assertEqual(juego.movimientos, 2 ** n - 1)

    def test_reiniciar(self):
        self.juego.mover("origen", "destino")
        self.juego.mover("origen", "auxiliar")
        self.juego.reiniciar()
        self.assertEqual(self.juego.movimientos, 0)
        self.assertEqual(
            self.juego.estado(),
            {"origen": [3, 2, 1], "auxiliar": [], "destino": []},
        )
        # Las torres reconstruidas siguen funcionando
        self.assertTrue(self.juego.mover("origen", "destino")["ok"])

    def test_reiniciar_tras_ganar(self):
        for origen, destino in PASOS_3_DISCOS:
            self.juego.mover(origen, destino)
        self.juego.reiniciar()
        self.assertFalse(self.juego.esta_ganado())
        self.assertEqual(self.juego.movimientos, 0)

    def test_resumen(self):
        self.juego.mover("origen", "destino")
        r = self.juego.resumen()
        self.assertEqual(r["movimientos"], 1)
        self.assertEqual(r["minimo_teorico"], 7)
        self.assertEqual(r["discos"], 3)
        self.assertFalse(r["victoria"])
        self.assertEqual(r["torres"]["destino"], [1])


class TestAlmacenDePartidas(unittest.TestCase):
    def setUp(self):
        partida.limpiar_partidas()

    def test_crear_y_obtener_la_misma_partida(self):
        pid, juego = partida.crear_partida(4)
        self.assertIs(partida.obtener_partida(pid), juego)

    def test_el_estado_persiste_entre_peticiones(self):
        pid, _ = partida.crear_partida(3)
        partida.obtener_partida(pid).mover("origen", "destino")   # "petición 1"
        self.assertEqual(partida.obtener_partida(pid).movimientos, 1)  # "petición 2"

    def test_partidas_independientes(self):
        pid_a, _ = partida.crear_partida(3)
        pid_b, _ = partida.crear_partida(3)
        self.assertNotEqual(pid_a, pid_b)
        partida.obtener_partida(pid_a).mover("origen", "destino")
        self.assertEqual(partida.obtener_partida(pid_b).movimientos, 0)

    def test_partida_inexistente(self):
        with self.assertRaises(PartidaNoEncontrada):
            partida.obtener_partida("no-existe")

    def test_crear_con_discos_invalidos(self):
        with self.assertRaises(ValueError):
            partida.crear_partida(10)

    def test_reiniciar_partida(self):
        pid, juego = partida.crear_partida(3)
        juego.mover("origen", "destino")
        partida.reiniciar_partida(pid)
        self.assertEqual(partida.obtener_partida(pid).movimientos, 0)

    def test_eliminar_partida(self):
        pid, _ = partida.crear_partida(3)
        partida.eliminar_partida(pid)
        with self.assertRaises(PartidaNoEncontrada):
            partida.obtener_partida(pid)

if __name__ == "__main__":
    unittest.main()
