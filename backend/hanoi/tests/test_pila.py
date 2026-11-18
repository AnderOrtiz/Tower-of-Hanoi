from django.test import SimpleTestCase

from hanoi.estructuras import (
    Disco,
    Pila,
    PilaVaciaError,
    construir_torre_inicial,
    validar_cantidad_discos,
)


class PilaTests(SimpleTestCase):
    def test_pila_nueva_esta_vacia(self):
        pila = Pila()
        self.assertTrue(pila.esta_vacia())
        self.assertEqual(pila.tamanio(), 0)

    def test_push_y_peek(self):
        pila = Pila()
        pila.push(1)
        pila.push(2)
        self.assertEqual(pila.peek(), 2)
        self.assertEqual(pila.tamanio(), 2)  # peek no quita

    def test_pop_respeta_lifo(self):
        pila = Pila()
        for n in (1, 2, 3):
            pila.push(n)
        self.assertEqual([pila.pop(), pila.pop(), pila.pop()], [3, 2, 1])
        self.assertTrue(pila.esta_vacia())

    def test_pop_en_pila_vacia_lanza_error(self):
        with self.assertRaises(PilaVaciaError):
            Pila().pop()

    def test_peek_en_pila_vacia_lanza_error(self):
        with self.assertRaises(PilaVaciaError):
            Pila().peek()

    def test_recorrido_no_modifica_la_pila(self):
        pila = Pila()
        for n in (1, 2, 3):
            pila.push(n)
        self.assertEqual(list(pila.recorrer_base_a_cima()), [1, 2, 3])
        self.assertEqual(list(pila.recorrer_cima_a_base()), [3, 2, 1])
        self.assertEqual(pila.tamanio(), 3)


class DiscoYTorreTests(SimpleTestCase):
    def test_disco_se_compara_por_tamanio(self):
        self.assertTrue(Disco(3) > Disco(1))

    def test_disco_invalido(self):
        with self.assertRaises(ValueError):
            Disco(0)

    def test_torre_inicial_ordenada_mayor_a_menor(self):
        torre = construir_torre_inicial(4)
        tamanios = [d.tamanio for d in torre.recorrer_base_a_cima()]
        self.assertEqual(tamanios, [4, 3, 2, 1])
        self.assertEqual(torre.peek(), Disco(1))  # el menor queda arriba

    def test_validar_cantidad_discos(self):
        self.assertEqual(validar_cantidad_discos("5"), 5)
        for invalido in (2, 9, "abc", None):
            with self.assertRaises(ValueError):
                validar_cantidad_discos(invalido)
