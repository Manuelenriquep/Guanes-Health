"""Ancla del demo estático vs Gated-6.50. No es evidencia clínica."""
import os
import sys
import unittest

MOTOR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico")
)
sys.path.insert(0, MOTOR_DIR)

from demo_divergencia_estatico_vs_placa import (
    barrido_pHe,
    clasificador_estatico,
    comparar_en_pHe,
    eficiencia_instrumento_placa,
)
from inmuno_utils import PH_VETO_CD8


class TestDivergenciaEstaticoVsPlaca(unittest.TestCase):
    def test_matcher_ignora_acido(self):
        self.assertEqual(clasificador_estatico(True), 1.0)
        self.assertEqual(clasificador_estatico(False), 0.0)

    def test_placa_anula_bajo_veto(self):
        self.assertEqual(eficiencia_instrumento_placa(6.20, True), 0.0)
        self.assertEqual(eficiencia_instrumento_placa(PH_VETO_CD8, True), 0.0)
        self.assertEqual(eficiencia_instrumento_placa(7.35, True), 1.0)

    def test_divergencia_en_estroma_acido(self):
        fila = comparar_en_pHe(6.20, firma_io_elegible=True)
        self.assertTrue(fila["diverge"])
        self.assertEqual(fila["eficacia_estatica"], 1.0)
        self.assertEqual(fila["eficacia_placa"], 0.0)

    def test_sin_divergencia_en_pHe_fisiologico(self):
        fila = comparar_en_pHe(7.35, firma_io_elegible=True)
        self.assertFalse(fila["diverge"])
        self.assertEqual(fila["eficacia_estatica"], 1.0)
        self.assertEqual(fila["eficacia_placa"], 1.0)

    def test_barrido_bajo_veto_siempre_diverge(self):
        filas = barrido_pHe(pHe_min=6.00, pHe_max=6.50, paso=0.10)
        self.assertGreaterEqual(len(filas), 2)
        for f in filas:
            self.assertEqual(f["eficacia_estatica"], 1.0)
            self.assertEqual(f["eficacia_placa"], 0.0)
            self.assertTrue(f["diverge"])


if __name__ == "__main__":
    unittest.main()
