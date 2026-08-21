# -*- coding: utf-8 -*-
"""Fronteras del barrido local CAR-T / HCC (Capa B)."""

import unittest
import sys
import os

MOTOR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico")
)
sys.path.insert(0, MOTOR_DIR)

from analisis_sensibilidad_local_cart import (
    viabilidad_terminal,
    barrido_phe,
    barrido_densidad,
    envolvente_asumida,
    UMBRAL_GPC3,
)


class TestSensibilidadLocalCART(unittest.TestCase):
    def test_veto_densidad_baja(self):
        self.assertGreaterEqual(viabilidad_terminal(densidad=UMBRAL_GPC3), 0.99)

    def test_phe_acido_vs_neutro(self):
        v_acido = viabilidad_terminal(ph_e=6.20)
        v_neutro = viabilidad_terminal(ph_e=7.40)
        self.assertLess(v_acido, v_neutro)

    def test_barridos_monotonos_forma(self):
        phe, v_phe = barrido_phe(n=9)
        self.assertEqual(len(phe), 9)
        self.assertGreater(v_phe[-1], v_phe[0])  # más neutro → más viabilidad

        dens, v_dens = barrido_densidad(n=9)
        self.assertEqual(len(dens), 9)
        # bajo veto: alta viab; sobre umbral: no mayor que en veto
        self.assertGreaterEqual(v_dens[0], v_dens[-1])

    def test_envolvente_ordenada(self):
        env = envolvente_asumida(n_grid=3)
        self.assertEqual(env["n"], 9)
        self.assertLessEqual(env["min"], env["mediana"])
        self.assertLessEqual(env["mediana"], env["max"])


if __name__ == "__main__":
    unittest.main()
