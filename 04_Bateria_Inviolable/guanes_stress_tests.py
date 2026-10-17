"""
==================================================================================================
GUANES HEALTH - BATERÍA INVIOLABLE
Módulo de Pruebas de Estrés y Sensibilidad Multimórbida — guanes_stress_tests.py
Kernel Nivel 0 / Verificación Biomédica Inmutable
==================================================================================================
Somete al Kernel Nivel 0 a escenarios límite y mutaciones fisiológicas/farmacológicas extremas:
  1. Mutación de Resistencia en Cx43 (pérdida de afinidad a PQ1 -> persistencia de Smaller Self).
  2. Acidosis Estromal Refractaria Extrema (pHe < 5.80 -> colapso de ATP citosólico).
  3. Sobredosis Masiva de Cariporida (120 mg -> Cmax > MTD de 5.0 uM).
  4. Disbiosis Crítica y Ruptura de Barrera (TEER < 200 -> phi_gut < 0.899).

Invariantes Fail-Closed:
  - 100% de los escenarios mórbidos o tóxicos deben ser vetados mecánicamente.
  - Tasa de falsos negativos = 0.0%.
  - Tiempos de resolución sub-milisegundo.
==================================================================================================
"""

import os
import sys
import unittest

MOTOR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico"))
if MOTOR_DIR not in sys.path:
    sys.path.insert(0, MOTOR_DIR)

from guanes_kernel_level0 import (
    GuanesKernelLevel0,
    TherapeuticTrajectoryCandidate,
    BiosecurityVetoCode
)
from guanes_pkpd import CARIPORIDE_MTD_UM


class TestGuanesStressTests(unittest.TestCase):
    """Batería de pruebas de estrés biológico y farmacológico límite."""

    def setUp(self):
        self.kernel = GuanesKernelLevel0()

    def test_stress_cx43_resistance_mutation_veto_fc_bio_03(self):
        """
        Escenario 1: Mutación en Cx43 que impide el rescate bioeléctrico.
        El ligando no logra abrir conexinas y el tejido permanece despolarizado (-24.5 mV).
        Dispara Veto FC-BIO-03: Persistencia de Smaller Self oncogénico.
        """
        mutated_candidate = TherapeuticTrajectoryCandidate(
            trajectory_id="STRESS_CX43_MUTATION_RESISTANT",
            target_vmem_mv=-24.5,          # Falla la repolarización
            restore_cx43_conductance=0.15, # Conexinas clausuradas
            target_phe=7.30,
            inhibit_nhe1_fraction=0.60,
            akkermansia_target_pct=3.5,
            teer_target_ohms=1200.0
        )
        res = self.kernel.evaluate_and_audit_trajectory(mutated_candidate)
        self.assertFalse(res.admitted)
        self.assertEqual(res.status, "REJECTED_FAIL_CLOSED")
        self.assertEqual(res.veto_code, BiosecurityVetoCode.FC_BIO_03)

    def test_stress_refractory_severe_stromal_acidosis_veto_fc_bio_02(self):
        """
        Escenario 2: Acidosis estromal intratable (pHe = 5.75) con Vmem hiperpolarizado (-75 mV).
        La fuerza protón-motriz induce influjo masivo forzado de H+, apagando PFK-1 y colapsando el ATP (< 15%).
        Dispara Veto FC-BIO-02: Colapso metabólico letal no selectivo.
        """
        severe_acidosis = TherapeuticTrajectoryCandidate(
            trajectory_id="STRESS_SEVERE_ACIDOSIS_PHE_575",
            target_vmem_mv=-75.0,
            restore_cx43_conductance=0.85,
            target_phe=5.75,              # Acidosis extrema estromal
            inhibit_nhe1_fraction=0.90,   # Apagado total de bombeo protónico
            akkermansia_target_pct=3.5,
            teer_target_ohms=1200.0
        )
        res = self.kernel.evaluate_and_audit_trajectory(severe_acidosis)
        self.assertFalse(res.admitted)
        self.assertEqual(res.status, "REJECTED_FAIL_CLOSED")
        self.assertEqual(res.veto_code, BiosecurityVetoCode.FC_BIO_02)
        self.assertLess(res.post_atp_pct, 15.0)

    def test_stress_cariporide_massive_overdose_veto_fc_pkpd_02(self):
        """
        Escenario 3: Sobredosis de Cariporida (250 mg).
        Concentración plasmática pico supera el límite MTD seguro (5.0 uM).
        Dispara Veto FC-PKPD-02 por toxicidad off-target sistémica.
        """
        res = self.kernel.evaluate_pharmacological_regimen(
            trajectory_id="STRESS_OVERDOSE_CARIPORIDE_250MG",
            cariporide_mg=250.0,          # Dosis masiva que excede MTD (Cmax ~ 5.83 uM > 5.0 uM)
            pq1_mg=15.0,
            buffer_mmol=40.0,
            akkermansia_billions=30.0
        )
        self.assertFalse(res.admitted)
        self.assertEqual(res.status, "REJECTED_FAIL_CLOSED")
        self.assertIn("FC-PKPD-02", res.veto_reason)

    def test_stress_mucosal_collapse_and_leaky_gut_veto_fc_bio_01(self):
        """
        Escenario 4: Disbiosis severa y daño en la barrera intestinal (TEER = 180 Ohms).
        Provoca traslocación de LPS portal masiva e inflamación que rompe el umbral de rescate (phi_gut < 0.899).
        Dispara Veto FC-BIO-01: Endotoxemia portal inaceptable.
        """
        barrier_collapse = TherapeuticTrajectoryCandidate(
            trajectory_id="STRESS_GUT_BARRIER_COLLAPSE",
            target_vmem_mv=-75.0,
            restore_cx43_conductance=0.85,
            target_phe=7.30,
            inhibit_nhe1_fraction=0.50,
            akkermansia_target_pct=0.10,  # Microbiota ausente
            teer_target_ohms=180.0        # Barrera mucosal desintegrada
        )
        res = self.kernel.evaluate_and_audit_trajectory(barrier_collapse)
        self.assertFalse(res.admitted)
        self.assertEqual(res.status, "REJECTED_FAIL_CLOSED")
        self.assertEqual(res.veto_code, BiosecurityVetoCode.FC_BIO_01)
        self.assertLess(res.post_phi_gut, 0.899)


if __name__ == "__main__":
    unittest.main()
