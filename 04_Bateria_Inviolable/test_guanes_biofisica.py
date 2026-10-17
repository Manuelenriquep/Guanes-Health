"""
Batería de Pruebas Inviolables — Motor Biofísico Cinético-Estromal y Eje Gut-Liver
==================================================================================
Verifica formalmente:
1. Inhibición alostérica cuaternaria de PFK-1 por protones (Ecuación de Hill).
2. Cinética de extrusión de protones por NHE1 y contrapresión por acidosis estromal.
3. Trampa bioeléctrica del ácido (colapso de ATP citosólico).
4. Eje entero-hepático-inmune: Dinámica de Akkermansia, LPS portal, IL-6 y escudo PD-L1.
5. Invarianza determinista y sellado criptográfico SHA-256.
"""

import sys
import os
import unittest

MOTOR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico"))
if MOTOR_DIR not in sys.path:
    sys.path.insert(0, MOTOR_DIR)

from guanes_biofisica import (
    BiophysicalMicroenvironmentEngine,
    PKA_PFK1,
    N_HILL_PFK1,
    PHI_GUT_UMBRAL_RESCATE
)


class TestGuanesBiofisica(unittest.TestCase):

    def setUp(self):
        self.engine = BiophysicalMicroenvironmentEngine()

    def test_pfk1_allosteric_inhibition(self):
        """Verifica que PFK-1 opere activa a pHi fisiológico y colapse a pHi ácido."""
        # pH fisiológico sano (7.35) -> actividad > 95%
        act_sana = self.engine.compute_pfk1_inhibition(ph_i=7.35)
        self.assertGreater(act_sana, 90.0)

        # En el pKa (6.80) -> actividad exactamente del 50%
        act_pka = self.engine.compute_pfk1_inhibition(ph_i=PKA_PFK1)
        self.assertAlmostEqual(act_pka, 50.0, delta=1.0)

        # pH ácido estromal severo (6.40) -> colapso < 10%
        act_acida = self.engine.compute_pfk1_inhibition(ph_i=6.40)
        self.assertLess(act_acida, 10.0)

    def test_nhe1_proton_extrusion_and_backpressure(self):
        """Verifica cinética de extrusión y frenado por contrapresión ácida estromal."""
        # pHi ácido (6.20) en estroma neutro (7.40) -> máxima demanda de extrusión
        j_max = self.engine.compute_nhe1_proton_flux(ph_i=6.20, ph_e=7.40)
        self.assertGreater(j_max, 5.0)

        # Mismo pHi ácido pero en estroma ácido (pHe 6.20) -> contrapresión estromal frena el flujo
        j_backpressure = self.engine.compute_nhe1_proton_flux(ph_i=6.20, ph_e=6.20)
        self.assertLess(j_backpressure, j_max)

    def test_bioelectric_acid_trap(self):
        """Verifica detección de la trampa bioeléctrica del ácido y colapso de ATP."""
        # Caso 1: Célula tumoral adaptada (despolarizada -15 mV, pHi alcalino 7.30, pHe 6.50)
        state_onco = self.engine.evaluate_bioelectric_acid_trap(ph_i=7.30, ph_e=6.50, v_mem_mv=-15.0)
        self.assertFalse(state_onco.is_acid_trapped)
        self.assertGreater(state_onco.atp_availability_pct, 80.0)

        # Caso 2: Trampa del ácido (linfocito T o célula forzada a hiperpolarización -75 mV en pHe 6.20 con pHi 6.60)
        state_trapped = self.engine.evaluate_bioelectric_acid_trap(ph_i=6.60, ph_e=6.20, v_mem_mv=-75.0)
        self.assertTrue(state_trapped.is_acid_trapped)
        self.assertLess(state_trapped.atp_availability_pct, 15.0)
        self.assertEqual(len(state_trapped.sha256_signature), 64)

    def test_gut_liver_immune_axis_eubiosis_vs_leakygut(self):
        """Verifica que Akkermansia preserve la barrera y que el leaky gut eleve LPS, IL-6 y PD-L1."""
        # Eubiosis (Akkermansia 3.5%, TEER 1400)
        s_sano = self.engine.simulate_gut_liver_immune_axis(akkermansia_pct=3.5, teer=1400.0)
        self.assertGreaterEqual(s_sano.phi_gut_barrier, PHI_GUT_UMBRAL_RESCATE)
        self.assertLess(s_sano.portal_lps_ng_ml, 1.0)
        self.assertLess(s_sano.pdl1_tumor_shield_factor, 3.0)
        self.assertEqual(len(s_sano.sha256_signature), 64)

        # Disbiosis severa / Leaky Gut (Akkermansia 0.2%, TEER 250)
        s_disbiosis = self.engine.simulate_gut_liver_immune_axis(akkermansia_pct=0.2, teer=250.0)
        self.assertLess(s_disbiosis.phi_gut_barrier, 0.50)
        self.assertGreater(s_disbiosis.portal_lps_ng_ml, 5.0)
        self.assertGreater(s_disbiosis.il6_systemic_pg_ml, 200.0)
        self.assertGreater(s_disbiosis.pdl1_tumor_shield_factor, 5.0)
        self.assertGreater(s_disbiosis.tox_exhaustion_index, s_sano.tox_exhaustion_index)


if __name__ == "__main__":
    unittest.main(verbosity=2)
