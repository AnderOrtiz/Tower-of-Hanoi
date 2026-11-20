import json

from django.test import TestCase

from hanoi import partida as almacen


class ApiPartidasTests(TestCase):
    def setUp(self):
        almacen.limpiar_partidas()

    def _post(self, url, cuerpo=None):
        return self.client.post(url, data=json.dumps(cuerpo or {}), content_type="application/json")

    def _crear(self, discos=3):
        r = self._post("/api/partidas/", {"discos": discos})
        return r, r.json()

    def test_crear_partida(self):
        r, d = self._crear(4)
        self.assertEqual(r.status_code, 201)
        self.assertTrue(d["ok"])
        self.assertEqual(d["torres"]["origen"], [4, 3, 2, 1])
        self.assertEqual(d["minimo_teorico"], 15)
        self.assertEqual(d["movimientos"], 0)
        self.assertFalse(d["victoria"])

    def test_crear_con_discos_invalidos(self):
        for malo in (2, 9, "abc", None):
            r = self._post("/api/partidas/", {"discos": malo})
            self.assertEqual(r.status_code, 400, malo)
            self.assertFalse(r.json()["ok"])

    def test_json_invalido(self):
        r = self.client.post("/api/partidas/", data="no es json", content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_movimiento_valido_e_invalido(self):
        _, d = self._crear(3)
        pid = d["id"]
        ok = self._post(f"/api/partidas/{pid}/mover/", {"origen": "origen", "destino": "destino"})
        self.assertEqual(ok.status_code, 200)
        self.assertEqual(ok.json()["movimientos"], 1)
        malo = self._post(f"/api/partidas/{pid}/mover/", {"origen": "origen", "destino": "destino"})
        self.assertEqual(malo.status_code, 400)
        self.assertFalse(malo.json()["ok"])
        self.assertEqual(malo.json()["movimientos"], 1)  # no suma
        self.assertIn("torres", malo.json())

    def test_entradas_invalidas_en_mover(self):
        _, d = self._crear(3)
        pid = d["id"]
        for cuerpo in ({}, {"origen": "x", "destino": "destino"}, {"origen": "origen", "destino": "origen"}):
            r = self._post(f"/api/partidas/{pid}/mover/", cuerpo)
            self.assertEqual(r.status_code, 400)
            self.assertFalse(r.json()["ok"])

    def test_partida_inexistente(self):
        for r in (
            self.client.get("/api/partidas/nada/"),
            self._post("/api/partidas/nada/mover/", {"origen": "origen", "destino": "destino"}),
            self._post("/api/partidas/nada/reiniciar/"),
        ):
            self.assertEqual(r.status_code, 404)
            self.assertFalse(r.json()["ok"])

    def test_partida_completa_y_reinicio(self):
        _, d = self._crear(3)
        pid = d["id"]
        jugadas = [("origen", "destino"), ("origen", "auxiliar"), ("destino", "auxiliar"),
                   ("origen", "destino"), ("auxiliar", "origen"), ("auxiliar", "destino"),
                   ("origen", "destino")]
        for o, de in jugadas:
            r = self._post(f"/api/partidas/{pid}/mover/", {"origen": o, "destino": de}).json()
            self.assertTrue(r["ok"])
        self.assertTrue(r["victoria"])
        self.assertEqual(r["movimientos"], 7)
        self.assertEqual(r["movimientos"], r["minimo_teorico"])
        e = self.client.get(f"/api/partidas/{pid}/").json()
        self.assertTrue(e["victoria"])
        rei = self._post(f"/api/partidas/{pid}/reiniciar/").json()
        self.assertEqual(rei["movimientos"], 0)
        self.assertEqual(rei["torres"]["origen"], [3, 2, 1])
        self.assertFalse(rei["victoria"])

    def test_metodo_no_permitido(self):
        self.assertEqual(self.client.get("/api/partidas/").status_code, 405)
