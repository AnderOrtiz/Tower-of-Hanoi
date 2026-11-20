// api.js — capa de comunicación con el backend.
// La interfaz (app.js) SOLO usa estas funciones; nunca hace fetch directo.
// Así la interfaz y la lógica no se mezclan.

const API_URL = "http://127.0.0.1:8000/api";

// true  = usa una lógica simulada en el navegador (para desarrollar sin backend)
// false = usa el backend Django real (cuando existan los endpoints de partidas)
const USAR_MOCK = false;

const MIN_DISCOS = 3;
const MAX_DISCOS = 8;

/* ---------------------------- API REAL ---------------------------- */

async function http(metodo, ruta, cuerpo) {
  try {
    const res = await fetch(API_URL + ruta, {
      method: metodo,
      headers: { "Content-Type": "application/json" },
      body: cuerpo ? JSON.stringify(cuerpo) : undefined,
    });
    return await res.json();
  } catch (e) {
    return {
      ok: false,
      mensaje: "No se pudo conectar con el servidor. ¿Está levantado el backend?",
    };
  }
}

const apiReal = {
  nuevaPartida: (discos) => http("POST", "/partidas/", { discos }),
  estado: (id) => http("GET", `/partidas/${id}/`),
  mover: (id, origen, destino) =>
    http("POST", `/partidas/${id}/mover/`, { origen, destino }),
  reiniciar: (id) => http("POST", `/partidas/${id}/reiniciar/`),
};

/* ---------------------------- API SIMULADA ---------------------------- */
// Misma forma de respuesta que el contrato:
// { ok, mensaje, id, torres, movimientos, minimo_teorico, victoria }

const partidasMock = {};
let contadorMock = 1;

function respuestaMock(p, ok = true, mensaje = "") {
  return {
    ok,
    mensaje,
    id: p.id,
    cantidad_discos: p.n,
    torres: JSON.parse(JSON.stringify(p.torres)),
    movimientos: p.movimientos,
    minimo_teorico: 2 ** p.n - 1,
    victoria: p.torres.destino.length === p.n,
  };
}

function torresIniciales(n) {
  const origen = [];
  for (let i = n; i >= 1; i--) origen.push(i);
  return { origen, auxiliar: [], destino: [] };
}

const apiMock = {
  async nuevaPartida(discos) {
    const n = Number(discos);
    if (!Number.isInteger(n) || n < MIN_DISCOS || n > MAX_DISCOS) {
      return {
        ok: false,
        mensaje: `La cantidad de discos debe estar entre ${MIN_DISCOS} y ${MAX_DISCOS}.`,
      };
    }
    const p = { id: contadorMock++, n, torres: torresIniciales(n), movimientos: 0 };
    partidasMock[p.id] = p;
    return respuestaMock(p);
  },

  async estado(id) {
    const p = partidasMock[id];
    if (!p) return { ok: false, mensaje: "La partida no existe." };
    return respuestaMock(p);
  },

  async mover(id, origen, destino) {
    const p = partidasMock[id];
    if (!p) return { ok: false, mensaje: "La partida no existe." };
    const validas = ["origen", "auxiliar", "destino"];
    if (!validas.includes(origen) || !validas.includes(destino))
      return respuestaMock(p, false, "Torre inexistente o entrada inválida.");
    if (origen === destino)
      return respuestaMock(p, false, "El origen y el destino no pueden ser la misma torre.");
    const desde = p.torres[origen];
    const hacia = p.torres[destino];
    if (desde.length === 0)
      return respuestaMock(p, false, "La torre de origen está vacía.");
    const disco = desde[desde.length - 1];
    if (hacia.length > 0 && hacia[hacia.length - 1] < disco)
      return respuestaMock(p, false, "No puedes poner un disco grande sobre uno más pequeño.");
    hacia.push(desde.pop());
    p.movimientos++;
    return respuestaMock(p, true, "Movimiento realizado.");
  },

  async reiniciar(id) {
    const p = partidasMock[id];
    if (!p) return { ok: false, mensaje: "La partida no existe." };
    p.torres = torresIniciales(p.n);
    p.movimientos = 0;
    return respuestaMock(p, true, "Partida reiniciada.");
  },
};

const api = USAR_MOCK ? apiMock : apiReal;
