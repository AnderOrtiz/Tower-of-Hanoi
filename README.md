# Reparto del Parcial 3 (Torre de Hanói) para 4 personas

La guía sugiere 5 roles, así que fusioné los dos más livianos (pruebas/documentación e integración/presentación) y los repartí para que nadie quede con una carga desigual. Todos deben defender su parte, así que cada rol incluye una pregunta que el docente podría hacerle.

## Arquitectura sugerida (para que trabajen en paralelo)

```
hanoi/
├── stack.py        # Clase Pila (Integrante 1)
├── juego.py        # Clase JuegoHanoi: reglas y validaciones (Integrante 2)
├── partida.py      # Contador, victoria, reinicio, mínimo teórico (Integrante 3)
├── interfaz.py     # Consola bonita o GUI (Integrante 4)
├── main.py         # Punto de entrada (Integrante 4)
├── tests/          # Pruebas (todos aportan, coordina el Integrante 3)
└── docs/           # Documento técnico y capturas
```

Esta separación cumple el requisito de **separar la lógica de la presentación**.

## Integrante 1: Estructura de datos (2.5 pts)
- Implementar la clase `Pila` (Stack): `push`, `pop`, `peek`, `esta_vacia`, `tamanio`, y recorrido para dibujar.
- Justificar por escrito por qué una pila es la estructura ideal (LIFO: solo se accede al disco superior).
- Cada torre es una `Pila` de discos (enteros o una clase `Disco`).
- **Defensa:** "¿Por qué pila y no lista o cola? ¿Qué complejidad tienen push/pop?"

## Integrante 2: Lógica y validaciones (2.5 pts)
- Clase `JuegoHanoi` con las tres torres (origen, auxiliar, destino).
- Método `mover(origen, destino)` que valide:
  - torre de origen vacía
  - disco mayor sobre menor
  - origen igual a destino
  - torre inexistente o entrada inválida
- Devolver mensajes de error claros (es lo que la rúbrica pide para el 100%).
- **Defensa:** "Muéstrame cómo evitas que un disco grande caiga sobre uno pequeño."

## Integrante 3: Control de partida y pruebas (2.0 pts + parte de 1.5 pts)
- Configurar la cantidad de discos (rango, por ejemplo 3 a 8).
- Contador de movimientos, mínimo teórico `2^n - 1`, detección automática de victoria y reinicio.
- Escribir las pruebas (`unittest` o `pytest`): movimientos válidos, inválidos, reinicio y partida completa.
- Guardar las capturas o registros de las pruebas.
- **Defensa:** "¿Cómo detectas la victoria? ¿De dónde sale 2^n - 1?"

## Integrante 4: Interfaz, integración y documento (parte de 1.5 pts + creatividad)
- Interfaz: es donde "sorprenden al docente". Opciones:
  - Consola con colores y discos dibujados en ASCII (librería `rich`)
  - GUI con `tkinter` o `pygame`
- `main.py` integrando todo, con menú, manejo de entradas inválidas y mensajes amigables.
- Redactar el documento técnico final (consolidando lo que cada uno aporte) y organizar la presentación.
- **Defensa:** "¿Cómo se comunica la interfaz con la lógica sin mezclarse?"

## Reparto transversal (para que todos aporten)

| Entregable | Responsable | Aportan |
|---|---|---|
| Código comentado | Cada quien en su módulo | Todos |
| Documento técnico | Integrante 4 | Cada uno escribe 1 párrafo de su módulo |
| Evidencias (capturas) | Integrante 3 | Todos prueban su parte |
| Demo en vivo | Integrante 4 | Todos presentan su módulo |

## Ideas creativas para destacar
- **Modo automático:** botón "Resolver" que ejecute el algoritmo recursivo animado (se lo asignaría al Integrante 2, ya que conoce la lógica).
- **Deshacer movimiento** usando otra pila de historial (excelente para mostrar otro uso de pilas).
- **Cronómetro y puntuación** (comparar movimientos hechos vs. mínimo).
- **Niveles de dificultad** y mensajes de victoria con un resumen de la partida.

## Consejos para la nota
1. Definan la interfaz de cada clase (nombres de métodos) **el primer día**, así trabajan en paralelo sin bloquearse.
2. Usen un repositorio de Git compartido con una rama por persona.
3. Antes de la defensa, hagan un ensayo donde cada uno explique el módulo de otro. La Defensa Individual vale 1.5 pts y es donde más suele fallar la nota.

Si quieres, puedo escribir el esqueleto del código (clase `Pila`, `JuegoHanoi` y las firmas de los métodos) para que cada integrante parta de una base común, o armarte una tabla con fechas por etapa. ¿Cuál prefieres?