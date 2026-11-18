import unittest

from hanoi.juego import JuegoHanoi

class TestJuegoHanoi(unittest.TestCase):
    def setUp(self):
        self.juego = JuegoHanoi(3)
    
    #Verifica base a tope, mayor abajo    
    def test_estado_inicial(self):
        self.assertEqual(
          self.juego.estado(),
          {"origen": [3, 2, 1], "auxiliar": [], "destino": []},  
        )
    
    #Evita que se cuelen objetos Disco, que romperían el JSON    
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
        self.juego.mover("origen", "destino") #disco 1 a destino
        r = self.juego.mover("origen", "auxiliar") #disco 2 a auxiliar vacia
        self.assertTrue(r["ok"])
        r = self.juego.mover("destino", "auxiliar") #disco 1 sobre disco 2
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
        r = self.juego.mover("origen", "destino")    # disco 2 sobre 1: inválido
        self.assertFalse(r["ok"])
        self.assertIn("más pequeño", r["mensaje"])
        
    def test_movimiento_invalido_no_cambia_estado(self):
        self.juego.mover("origen", "destino")
        antes = self.juego.estado()
        self.juego.mover("origen", "destino")   # inválido
        self.juego.mover("auxiliar", "origen")  # inválido
        self.juego.mover("origen", "origen")    # inválido
        self.assertEqual(self.juego.estado(), antes)
        
    #Resuelve 3 discos en 7 movimientos (2^3 - 1) y comprueba que todos terminen en destino    
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


if __name__ == "__main__":
    unittest.main()