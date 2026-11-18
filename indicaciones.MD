# Guía de indicaciones por integrante

## Integrante 1 (tú): Estructura de datos ✅
**Estado:** terminado. 10 pruebas pasando.

**Entregas para el equipo:**
- Repo con la carpeta `backend/` subida.
- Aviso de que pueden importar con `from hanoi.estructuras import Pila, Disco, PilaVaciaError, MIN_DISCOS, MAX_DISCOS, construir_torre_inicial`.
- Contrato JSON: las torres son listas **de base a tope**, por ejemplo `[4, 3, 2, 1]`.

---

## Integrante 2: Lógica y validaciones ✅
**Estado:** terminado. 10 pruebas propias pasando (20 en total con las del Integrante 1).

**Archivos:** `backend/hanoi/juego.py`, `backend/hanoi/tests/test_juego.py`

**Entregas para el equipo:**
- Importar con `from hanoi.juego import JuegoHanoi`.
- `JuegoHanoi(n)` expone `.origen`, `.auxiliar`, `.destino` (son `Pila`) y `.discos`.
- `mover(origen, destino)` acepta solo `"origen"`, `"auxiliar"`, `"destino"` y devuelve `{"ok": bool, "mensaje": str}`.
- `estado()` devuelve `{"origen": [3, 2, 1], "auxiliar": [], "destino": []}`: enteros, de base a tope.
- No incluye contador, victoria ni reinicio (Integrante 3).
- Un movimiento inválido nunca modifica las torres.

---

## Integrante 3: Control de partida y pruebas
**Archivos a crear:** `backend/hanoi/partida.py` (o ampliar `juego.py` junto con el Integrante 2), más `tests/test_juego.py`.

**Qué debe hacer:**
- Configurar la cantidad de discos con `validar_cantidad_discos` (rango 3 a 8).
- **Contador de movimientos:** solo suma cuando `mover()` fue válido.
- **Mínimo teórico:** `2**n - 1`.
- **Victoria:** todos los discos están en `destino`, es decir `destino.tamanio() == n`.
- **Reinicio:** reconstruir las torres y poner el contador en 0.
- **Guardar la partida entre peticiones:** Django no recuerda nada entre requests. Lo más simple es un diccionario en memoria `{partida_id: JuegoHanoi}`.
- Escribir las pruebas con `unittest`: movimientos válidos, inválidos, reinicio y partida completa. Con 3 discos se resuelve en 7 movimientos.
- Guardar las capturas con `python manage.py test -v 2`.



---

## Integrante 4: Interfaz e integración
**Carpeta:** `frontend/` en la raíz (HTML/JS, React u otra, a su elección).

**Qué debe hacer:**
- Consumir la API en `http://127.0.0.1:8000/api/` (CORS ya está habilitado).
- Hoy solo existe `GET /api/torres/?discos=N`. Para las demás pantallas debe acordar con los Integrantes 2 y 3 estos endpoints, que propongo como contrato:

| Acción | Endpoint |
|---|---|
| Nueva partida | `POST /api/partidas/` con `{"discos": 4}` |
| Ver estado | `GET /api/partidas/<id>/` |
| Mover | `POST /api/partidas/<id>/mover/` con `{"origen": "origen", "destino": "destino"}` |
| Reiniciar | `POST /api/partidas/<id>/reiniciar/` |

- Respuesta sugerida: `{"ok", "mensaje", "torres", "movimientos", "minimo_teorico", "victoria"}`.
- Dibujar las torres (los discos se ordenan por el número de la lista; mayor número, disco más ancho), mostrar el contador y el mínimo teórico, y mostrar `mensaje` tal cual cuando `ok` sea `false`.
- Incluir menú inicial, selector de discos (3 a 8), botón de reinicio y pantalla de victoria. Aquí está la parte de "sorprender al docente": animaciones, colores, sonidos.
- Redactar el documento técnico final con lo que aporte cada uno.



