# Guía de indicaciones por integrante

## Integrante 1 (tú): Estructura de datos ✅
**Estado:** terminado. 10 pruebas pasando.

**Entregas para el equipo:**
- Repo con la carpeta `backend/` subida.
- Aviso de que pueden importar con `from hanoi.estructuras import Pila, Disco, PilaVaciaError, MIN_DISCOS, MAX_DISCOS, construir_torre_inicial`.
- Contrato JSON: las torres son listas **de base a tope**, por ejemplo `[4, 3, 2, 1]`.

---

## Integrante 2: Lógica y validaciones
**Archivo a crear:** `backend/hanoi/juego.py` (más `tests/test_juego.py` si quiere).

**Qué debe hacer:**
- Crear la clase `JuegoHanoi` con tres `Pila`: `origen`, `auxiliar`, `destino`. Para la torre inicial debe usar `construir_torre_inicial(n)`.
- Implementar `mover(origen, destino)`, que valide y rechace con un mensaje claro en estos casos:
  - Torre inexistente o entrada inválida (aceptar solo `"origen"`, `"auxiliar"`, `"destino"`).
  - Origen igual a destino.
  - Torre de origen vacía.
  - Disco grande sobre uno pequeño (comparar `torre_origen.peek() > torre_destino.peek()`).
- Si el movimiento es válido: `pop()` del origen y `push()` en el destino.
- Devolver siempre un resultado uniforme, por ejemplo `{"ok": True/False, "mensaje": "..."}`.
- Exponer un método `estado()` que devuelva `{"origen": [...], "auxiliar": [...], "destino": [...]}`, usando `a_lista()` o `torre_a_lista`.

**No debe:** tocar `pila.py`, `disco.py` ni `torre.py`, ni poner contador o victoria (eso es del Integrante 3).



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



