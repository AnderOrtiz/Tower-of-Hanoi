from hanoi.estructuras import Pila, construir_torre_inicial, validar_cantidad_discos

NOMBRES_TORRES = ("origen", "auxiliar", "destino")


class JuegoHanoi:
    def __init__(self, discos):
        # Lanza ValueError si no está entre 3 y 8
        self.discos = validar_cantidad_discos(discos)
        self._construir()

    def _construir(self):
        """Arma las torres desde cero y pone el contador en 0."""
        self.origen = construir_torre_inicial(self.discos)
        self.auxiliar = Pila()
        self.destino = Pila()
        self._torres = {
            "origen": self.origen,
            "auxiliar": self.auxiliar,
            "destino": self.destino,
        }
        self.movimientos = 0

    # ---------- Control de partida ----------
    @property
    def minimo_teorico(self):
        return 2 ** self.discos - 1

    def esta_ganado(self):
        return self.destino.tamanio() == self.discos

    def reiniciar(self):
        self._construir()

    def resumen(self):
        """Estado de las torres + datos de la partida (para el JSON)."""
        return {
            "torres": self.estado(),
            "discos": self.discos,
            "movimientos": self.movimientos,
            "minimo_teorico": self.minimo_teorico,
            "victoria": self.esta_ganado(),
        }

    # ---------- Movimientos ----------
    def _resultado(self, ok, mensaje):
        return {"ok": ok, "mensaje": mensaje}

    def mover(self, origen, destino):
        # 1. Entrada válida
        if origen not in NOMBRES_TORRES or destino not in NOMBRES_TORRES:
            return self._resultado(
                False,
                "Error: torre inválida. Usa 'origen', 'auxiliar' o 'destino'.",
            )

        # 2. Origen distinto de destino
        if origen == destino:
            return self._resultado(
                False, "Error: la torre de origen y la de destino son la misma."
            )

        torre_origen = self._torres[origen]
        torre_destino = self._torres[destino]

        # 3. Origen no vacío
        if torre_origen.esta_vacia():
            return self._resultado(
                False, f"Error: la torre '{origen}' no tiene discos."
            )

        # 4. Disco grande sobre pequeño
        if not torre_destino.esta_vacia() and torre_origen.peek() > torre_destino.peek():
            return self._resultado(
                False, "Error: no puedes poner un disco grande sobre uno más pequeño."
            )

        # 5. Todo válido: recién ahora se modifica el estado
        torre_destino.push(torre_origen.pop())
        self.movimientos += 1  # solo suma si el movimiento fue válido

        if self.esta_ganado():
            return self._resultado(True, "¡Ganaste! Todos los discos están en destino.")
        return self._resultado(True, "Movimiento válido.")

    def estado(self):
        return {
            nombre: [disco.tamanio for disco in pila.a_lista()]
            for nombre, pila in self._torres.items()
        }