# -*- coding: utf-8 -*-
"""Fronteras numéricas del toy model CAR-T / HCC (Capa B)."""

import unittest
import sys
import os

MOTOR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico")
)
sys.path.insert(0, MOTOR_DIR)

from simulador_cart_hcc_interaccion import (
    LinfocitoCART,
    TumorHCC,
    SimuladorCARTInteraccion,
    UMBRAL_GPC3,
    factor_senuelo_sgpc3,
    factor_infiltracion_mig,
)


class TestCARTInteraccion(unittest.TestCase):
    def setUp(self):
        self.cart = LinfocitoCART()
        self.tumor = TumorHCC()
        self.sim = SimuladorCARTInteraccion()

    def test_kd_ph(self):
        self.assertGreater(self.cart.evaluar_kd_gpc3(7.40), 1000.0)
        self.assertLess(self.cart.evaluar_kd_gpc3(6.20), 10.0)

    def test_nhe1_atp(self):
        self.cart.atp_nivel = 500.0
        self.assertGreaterEqual(self.cart.regular_ph_intracelular(6.20), 7.10)
        self.cart.atp_nivel = 50.0
        self.assertLess(self.cart.regular_ph_intracelular(6.20), 6.80)

    def test_veto_gpc3(self):
        self.tumor.densidad_gpc3 = 5000.0
        self.assertAlmostEqual(self.tumor.evaluar_veto_antigenico(), 0.8, places=5)
        self.tumor.densidad_gpc3 = UMBRAL_GPC3
        self.assertEqual(self.tumor.evaluar_veto_antigenico(), 0.0)

    def test_icasp9(self):
        inicial = self.cart.count
        for _ in range(40):
            self.cart.simular_apoptosis_icasp9(50.0, delta_t=0.1)
        self.assertLess(self.cart.count / inicial, 0.01)

    def test_senuelo_sgpc3_resolved_b(self):
        """RESOLVED-B-01: frontera numérica del factor 1/(1+[s]/Ki)."""
        self.assertAlmostEqual(factor_senuelo_sgpc3(5.0, 2.5), 1.0 / 3.0, places=5)

        sin_s = self.sim.simular_intervalo(ph_e=6.20, sgpc3_ng_ml=0.0)
        con_s = self.sim.simular_intervalo(ph_e=6.20, sgpc3_ng_ml=5.0, ki_sgpc3=2.5)
        self.assertGreater(con_s["viabilidad_tumor"][-1], sin_s["viabilidad_tumor"][-1])
        self.assertAlmostEqual(
            con_s["eficiencia_reconocimiento"][-1],
            sin_s["eficiencia_reconocimiento"][-1] / 3.0,
            places=4,
        )

    def test_eta_mig_resolved_b02(self):
        """RESOLVED-B-02: η baja con IFP/colágeno altos; OTR alivia pena de colágeno."""
        eta_ok = factor_infiltracion_mig(ifp_mmhg=10.0, colageno_ug_mg=30.0)
        eta_bar = factor_infiltracion_mig(ifp_mmhg=35.0, colageno_ug_mg=80.0)
        eta_otr = factor_infiltracion_mig(ifp_mmhg=35.0, colageno_ug_mg=80.0, otr4120=1.0)
        self.assertGreaterEqual(eta_ok, 0.99)
        self.assertLess(eta_bar, 0.35)
        self.assertGreater(eta_otr, eta_bar)

        permeable = self.sim.simular_intervalo(ph_e=6.20, ifp_mmhg=10.0, colageno_ug_mg=30.0)
        barrera = self.sim.simular_intervalo(ph_e=6.20, ifp_mmhg=35.0, colageno_ug_mg=80.0)
        self.assertGreater(barrera["viabilidad_tumor"][-1], permeable["viabilidad_tumor"][-1])


if __name__ == "__main__":
    unittest.main()
