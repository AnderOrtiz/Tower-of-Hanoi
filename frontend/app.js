// app.js — interfaz. Solo dibuja y reacciona a clics;
// toda la lógica y validaciones las hace el backend (vía api.js).

const $ = (id) => document.getElementById(id);
const NOMBRES = ["origen", "auxiliar", "destino"];

const estado = {
  id: null,
  discos: 4,
  seleccion: null, // "origen" | "auxiliar" | "destino" | null
  ocupado: false,
  sonido: true,
};

/* ------------------------- Pantallas ------------------------- */

function mostrar(nombre) {
  document.querySelectorAll(".pantalla").forEach((p) => p.classList.remove("activa"));
  $("pantalla-" + nombre).classList.add("activa");
  if (nombre !== "victoria") detenerConfeti();
}

/* ------------------------- Sonido ------------------------- */

let audioCtx = null;
function tono(frecuencia, duracion = 0.12, tipo = "sine") {
  if (!estado.sonido) return;
  try {
    audioCtx = audioCtx || new (window.AudioContext || window.webkitAudioContext)();
    const osc = audioCtx.createOscillator();
    const gan = audioCtx.createGain();
    osc.type = tipo;
    osc.frequency.value = frecuencia;
    gan.gain.setValueAtTime(0.15, audioCtx.currentTime);
    gan.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duracion);
    osc.connect(gan).connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + duracion);
  } catch (e) { /* sin audio, no pasa nada */ }
}
const sonidoSeleccion = () => tono(520);
const sonidoMover = () => tono(330, 0.15, "triangle");
const sonidoError = () => tono(140, 0.25, "sawtooth");
const sonidoVictoria = () =>
  [523, 659, 784, 1046].forEach((f, i) => setTimeout(() => tono(f, 0.25, "triangle"), i * 150));

/* ------------------------- Mensajes ------------------------- */

function mensaje(texto, tipo = "") {
  const el = $("mensaje");
  el.textContent = texto;
  el.className = "mensaje " + tipo;
}

/* ------------------------- Dibujo ------------------------- */

function colorDisco(n) {
  const matiz = Math.round((n - 1) * (300 / (MAX_DISCOS - 1)));
  return `hsl(${matiz}, 80%, 62%)`;
}

function dibujar(datos) {
  $("contador").textContent = datos.movimientos;
  $("minimo").textContent = datos.minimo_teorico;
  $("cant-discos").textContent = estado.discos;

  NOMBRES.forEach((nombre) => {
    const cont = document.querySelector(`.torre[data-torre="${nombre}"] .discos`);
    cont.innerHTML = "";
    const lista = datos.torres[nombre]; // de base a tope
    lista.forEach((n, i) => {
      const d = document.createElement("div");
      d.className = "disco";
      d.style.width = 22 + (n / MAX_DISCOS) * 70 + "%";
      d.style.background = colorDisco(n);
      d.textContent = n;
      d.dataset.tope = i === lista.length - 1 ? "1" : "0";
      cont.appendChild(d);
    });
  });
  marcarSeleccion();
}

function marcarSeleccion() {
  document.querySelectorAll(".torre").forEach((t) => {
    const sel = t.dataset.torre === estado.seleccion;
    t.classList.toggle("seleccionada", sel);
    const tope = t.querySelector('.disco[data-tope="1"]');
    document.querySelectorAll(".disco.levantado").forEach((d) => d.classList.remove("levantado"));
    if (sel && tope) tope.classList.add("levantado");
  });
  // (el levantado se reaplica abajo para evitar que se borre en el bucle)
  if (estado.seleccion) {
    const tope = document.querySelector(
      `.torre[data-torre="${estado.seleccion}"] .disco[data-tope="1"]`
    );
    if (tope) tope.classList.add("levantado");
  }
}

function temblar(nombre) {
  const t = document.querySelector(`.torre[data-torre="${nombre}"]`);
  t.classList.remove("error");
  void t.offsetWidth; // reinicia la animación
  t.classList.add("error");
}

/* ------------------------- Flujo del juego ------------------------- */

async function nuevaPartida(discos) {
  const r = await api.nuevaPartida(discos);
  if (!r.ok) return r;
  estado.id = r.id ?? r.partida_id;
  estado.discos = r.cantidad_discos ?? discos;
  estado.seleccion = null;
  dibujar(r);
  mensaje("Elige una torre de origen.");
  mostrar("juego");
  return r;
}

async function alElegirTorre(nombre) {
  if (estado.ocupado) return;

  if (!estado.seleccion) {
    estado.seleccion = nombre;
    sonidoSeleccion();
    marcarSeleccion();
    mensaje(`Origen: ${nombre}. Ahora elige el destino.`);
    return;
  }

  const origen = estado.seleccion;
  estado.seleccion = null;
  estado.ocupado = true;
  const r = await api.mover(estado.id, origen, nombre);
  estado.ocupado = false;

  if (!r.ok) {
    mensaje(r.mensaje || "Movimiento inválido.", "error");
    sonidoError();
    temblar(origen);
    if (r.torres) dibujar(r); else marcarSeleccion();
    return;
  }

  mensaje(r.mensaje || "Movimiento realizado.", "ok");
  sonidoMover();
  dibujar(r);

  if (r.victoria) setTimeout(() => ganar(r), 500);
}

// Calificación (solo presentación): compara tus movimientos con el mínimo teórico
// que entrega el backend. 3 estrellas = perfecto.
function calificar(movimientos, minimo) {
  if (movimientos <= minimo) return { estrellas: 3, rango: "¡Perfecto!" };
  if (movimientos <= minimo * 1.5) return { estrellas: 2, rango: "¡Muy bien!" };
  return { estrellas: 1, rango: "¡Buen intento!" };
}

function ganar(r) {
  const nota = calificar(r.movimientos, r.minimo_teorico);
  $("estrellas").innerHTML = [1, 2, 3]
    .map((n) => `<span class="estrella ${n <= nota.estrellas ? "llena" : "vacia"}" style="--i:${n - 1}">★</span>`)
    .join("");
  $("rango-victoria").textContent = nota.rango;

  const extra =
    r.movimientos === r.minimo_teorico
      ? "¡Lo lograste con el mínimo posible!"
      : `El mínimo posible era ${r.minimo_teorico}.`;
  $("resumen-victoria").textContent =
    `Resolviste ${estado.discos} discos en ${r.movimientos} movimientos. ${extra}`;
  mostrar("victoria");
  sonidoVictoria();
  lanzarConfeti();
}

async function reiniciar() {
  const r = await api.reiniciar(estado.id);
  if (!r.ok) return mensaje(r.mensaje || "No se pudo reiniciar.", "error");
  estado.seleccion = null;
  dibujar(r);
  mensaje("Partida reiniciada. Elige una torre de origen.", "ok");
}

/* ------------------------- Confeti ------------------------- */

let animConfeti = null;
function lanzarConfeti() {
  const c = $("confeti");
  const ctx = c.getContext("2d");
  c.width = innerWidth;
  c.height = innerHeight;
  const piezas = Array.from({ length: 160 }, () => ({
    x: Math.random() * c.width,
    y: Math.random() * -c.height,
    r: 4 + Math.random() * 6,
    v: 2 + Math.random() * 4,
    h: Math.random() * 360,
    dx: (Math.random() - 0.5) * 2,
  }));
  (function paso() {
    ctx.clearRect(0, 0, c.width, c.height);
    piezas.forEach((p) => {
      p.y += p.v; p.x += p.dx;
      if (p.y > c.height) { p.y = -10; p.x = Math.random() * c.width; }
      ctx.fillStyle = `hsl(${p.h}, 90%, 60%)`;
      ctx.fillRect(p.x, p.y, p.r, p.r * 1.6);
    });
    animConfeti = requestAnimationFrame(paso);
  })();
}
function detenerConfeti() {
  if (animConfeti) cancelAnimationFrame(animConfeti);
  animConfeti = null;
}

/* ------------------------- Eventos ------------------------- */

// Fichas para elegir la cantidad de discos (el rango 3-8 lo valida el backend)
const NIVELES = { 3: "Aprendiz", 4: "Fácil", 5: "Normal", 6: "Difícil", 7: "Experto", 8: "Maestro" };

function marcarFicha() {
  document.querySelectorAll(".ficha").forEach((f) => {
    f.classList.toggle("activa", Number(f.dataset.n) === estado.discos);
  });
  $("nivel").textContent = `Nivel: ${NIVELES[estado.discos] || ""}`;
}

document.querySelectorAll(".ficha").forEach((f) => {
  f.addEventListener("click", () => {
    estado.discos = Number(f.dataset.n);
    sonidoSeleccion();
    marcarFicha();
  });
});

// Luciérnagas decorativas del fondo
(function crearLuciernagas() {
  const cont = $("luciernagas");
  for (let i = 0; i < 18; i++) {
    const l = document.createElement("span");
    l.className = "luciernaga";
    l.style.left = Math.random() * 100 + "%";
    l.style.top = 25 + Math.random() * 65 + "%";
    l.style.setProperty("--d", 5 + Math.random() * 7 + "s");
    l.style.setProperty("--dx", Math.random() * 80 - 40 + "px");
    l.style.setProperty("--dy", Math.random() * -70 + "px");
    l.style.animationDelay = Math.random() * -8 + "s";
    cont.appendChild(l);
  }
})();

$("btn-jugar").addEventListener("click", async () => {
  const msg = $("msg-menu");
  msg.classList.add("oculto");
  const r = await nuevaPartida(estado.discos);
  if (!r.ok) {
    msg.textContent = r.mensaje || r.error || "No se pudo crear la partida.";
    msg.classList.remove("oculto");
  }
});

$("btn-reglas").addEventListener("click", () => mostrar("reglas"));
$("btn-volver-reglas").addEventListener("click", () => mostrar("menu"));
$("btn-menu").addEventListener("click", () => { marcarFicha(); mostrar("menu"); });
$("btn-menu-victoria").addEventListener("click", () => { marcarFicha(); mostrar("menu"); });
$("btn-reiniciar").addEventListener("click", reiniciar);
$("btn-otra").addEventListener("click", () => nuevaPartida(estado.discos));
$("btn-sonido").addEventListener("click", () => {
  estado.sonido = !estado.sonido;
  $("btn-sonido").textContent = estado.sonido ? "🔊" : "🔇";
});

document.querySelectorAll(".torre").forEach((t) => {
  t.addEventListener("click", () => alElegirTorre(t.dataset.torre));
});

document.addEventListener("keydown", (e) => {
  if (!$("pantalla-juego").classList.contains("activa")) return;
  const idx = ["1", "2", "3"].indexOf(e.key);
  if (idx >= 0) alElegirTorre(NOMBRES[idx]);
  if (e.key === "Escape") { estado.seleccion = null; marcarSeleccion(); }
});

mostrar("menu");