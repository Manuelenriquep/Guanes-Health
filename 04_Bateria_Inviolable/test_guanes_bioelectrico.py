"""
Batería de Pruebas Inviolables — Motor Bioeléctrico y Redes Cx43
================================================================
Verifica formalmente:
1. Ecuación de Goldman-Hodgkin-Katz (GHK) en condiciones fisiológicas y patológicas.
2. Comportamiento Fail-Closed ante violación de barreras termodinámicas.
3. Conductancia dependiente de voltaje de conexinas Cx43.
4. Emergencia de 'Smaller Selves' y reversión por Normalización Bioeléctrica de Levin.
5. Cuantificación del Cono Cognitivo de Luz (Phi) y sellado SHA-256.
"""

import sys
import os
import unittest
import math
import numpy as np

MOTOR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico"))
if MOTOR_DIR not in sys.path:
    sys.path.insert(0, MOTOR_DIR)

from guanes_bioelectrico import (
    GHKBioelectricEngine,
    BioelectricLattice2D,
    IonConcentrations,
    UMBRAL_ONCOGENICO_VM_MV,
    UMBRAL_DIFERENCIADO_VM_MV,
    VM_MIN_FISICO,
    VM_MAX_FISICO
)


class TestGuanesBioelectrico(unittest.TestCase):

    def setUp(self):
        self.engine = GHKBioelectricEngine()
        self.lattice = BioelectricLattice2D(rows=8, cols=8, ghk_engine=self.engine)

    def test_ghk_healthy_vs_depolarized(self):
        """Verifica que GHK calcule Vmem diferenciado (-72 mV) y despolarizado (>= -25 mV)."""
        # Estado sano (P_Na / P_K = 0.04)
        v_sano = self.engine.compute_ghk_voltage(p_k=1.0, p_na=0.04, p_cl=0.45)
        self.assertLessEqual(v_sano, UMBRAL_DIFERENCIADO_VM_MV)
        self.assertAlmostEqual(v_sano, -72.0, delta=5.0)

        # Estado oncogénico despolarizado (P_Na / P_K = 0.70, P_K = 0.60, P_Cl = 0.30)
        v_onco = self.engine.compute_ghk_voltage(p_k=0.60, p_na=0.70, p_cl=0.30)
        self.assertGreaterEqual(v_onco, UMBRAL_ONCOGENICO_VM_MV)
        self.assertGreater(v_onco, v_sano)

    def test_ghk_fail_closed_limits(self):
        """FC-BIO-06: Verificación de rechazo inmediato si las concentraciones son no físicas."""
        with self.assertRaises(ValueError):
            IonConcentrations(k_in=-10.0)

    def test_cx43_voltage_gating(self):
        """Verifica que Delta_V = 0 mantenga alta conductancia y Delta_V alto cierre Cx43."""
        # Sin gradiente entre células contiguas -> acoplamiento máximo
        g_acoplado = self.engine.compute_cx43_gating(v_mem_a=-70.0, v_mem_b=-70.0)
        self.assertGreater(g_acoplado, 0.90)

        # Alto gradiente (ej. célula sana -75 mV vs tumoral -15 mV -> Delta_V = 60 mV)
        g_bloqueado = self.engine.compute_cx43_gating(v_mem_a=-75.0, v_mem_b=-15.0)
        self.assertLess(g_bloqueado, 0.20)
        self.assertGreaterEqual(g_bloqueado, 0.05)

    def test_smaller_selves_induction_and_normalization(self):
        """Verifica inducción de Smaller Selves y rescate completo mediante protocolo de Levin."""
        # 1. Estado inicial de tejido sano sincronizado
        m_inicial = self.lattice.compute_cognitive_light_cone_metrics()
        self.assertEqual(m_inicial["tissue_state"], "SYNCHRONIZED_ORGAN")
        self.assertEqual(m_inicial["smaller_selves_count"], 0)

        # 2. Inducción de foco despolarizado/oncogénico en el centro
        self.lattice.induce_oncogenic_depolarization(r=4, c=4, radius=2)
        m_onco = self.lattice.compute_cognitive_light_cone_metrics()
        self.assertGreater(m_onco["smaller_selves_count"], 0)
        self.assertLess(m_onco["cognitive_light_cone_phi"], m_inicial["cognitive_light_cone_phi"])

        # 3. Normalización bioeléctrica forzada (Levin)
        self.lattice.apply_levin_normalization(force_vmem=-75.0, restore_gjc=0.85)
        m_rescatado = self.lattice.compute_cognitive_light_cone_metrics()
        self.assertEqual(m_rescatado["smaller_selves_count"], 0)
        self.assertEqual(m_rescatado["tissue_state"], "SYNCHRONIZED_ORGAN")
        self.assertGreater(m_rescatado["fraction_coupled"], 0.90)

    def test_diffusion_step_and_sha256(self):
        """Verifica la integración por difusión y la firma criptográfica SHA-256."""
        m_antes = self.lattice.compute_cognitive_light_cone_metrics()
        self.assertEqual(len(m_antes["sha256_state"]), 64)

        # Paso de difusión
        self.lattice.step_diffusion(dt=0.05, d_coeff=0.20)
        m_despues = self.lattice.compute_cognitive_light_cone_metrics()
        self.assertEqual(len(m_despues["sha256_state"]), 64)
        # La dispersión debe ser suave y los valores mantenerse en rango físico
        self.assertTrue(np.all(self.lattice.v_mem >= VM_MIN_FISICO))
        self.assertTrue(np.all(self.lattice.v_mem <= VM_MAX_FISICO))


if __name__ == "__main__":
    unittest.main(verbosity=2)
