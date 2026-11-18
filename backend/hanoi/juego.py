from hanoi.estructuras import Pila, construir_torre_inicial

NOMBRES_TORRES = ("origen", "auxiliar", "destino")


class JuegoHanoi:
    def __init__(self, discos):
        self.discos = discos
        self.origen = construir_torre_inicial(discos)
        self.auxiliar = Pila()
        self.destino = Pila()
        self._torres = {
            "origen": self.origen,
            "auxiliar": self.auxiliar,
            "destino": self.destino,
        }
        
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
        return self._resultado(True, "Movimiento válido.")

    def estado(self):
        return {
            nombre: [disco.tamanio for disco in pila.a_lista()]
            for nombre, pila in self._torres.items()
        }

