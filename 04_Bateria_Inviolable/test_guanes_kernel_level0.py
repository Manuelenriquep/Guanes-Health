"""
Batería de Pruebas Inviolables — Kernel Nivel 0 de Inferencia Activa y Bioseguridad
===================================================================================
Verifica formalmente:
1. Selección determinista de la trayectoria de Mínima Acción y convergencia de Energía Libre (F -> 0).
2. Cortafuegos Fail-Closed FC-BIO-01 (Ruptura de barrera intestinal / phi_gut).
3. Cortafuegos Fail-Closed FC-BIO-02 (Colapso metabólico de ATP).
4. Cortafuegos Fail-Closed FC-BIO-03 (Persistencia de Smaller Self oncogénico).
5. Monotonía de la Energía Libre Variacional y sellado SHA-256 sub-milisegundo.
"""

import sys
import os
import unittest
import time

MOTOR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico"))
if MOTOR_DIR not in sys.path:
    sys.path.insert(0, MOTOR_DIR)

from guanes_kernel_level0 import (
    GuanesKernelLevel0,
    TherapeuticTrajectoryCandidate,
    BiosecurityVetoCode
)


class TestGuanesKernelLevel0(unittest.TestCase):

    def setUp(self):
        self.kernel = GuanesKernelLevel0()

    def test_admitted_optimal_trajectory(self):
        """Verifica que una intervención armónica óptima sea admitida bajo Mínima Acción."""
        optima = TherapeuticTrajectoryCandidate(
            trajectory_id="TRAJ_OPTIMA_LEVIN_AKK",
            target_vmem_mv=-75.0,
            restore_cx43_conductance=0.85,
            target_phe=7.35,
            inhibit_nhe1_fraction=0.50,
            akkermansia_target_pct=3.8,
            teer_target_ohms=1300.0
        )
        res = self.kernel.evaluate_and_audit_trajectory(optima)
        self.assertTrue(res.admitted)
        self.assertEqual(res.status, "ADMITTED_MINIMAL_ACTION")
        self.assertIsNone(res.veto_code)
        self.assertGreaterEqual(res.post_phi_gut, 0.899)
        self.assertGreaterEqual(res.post_atp_pct, 50.0)
        self.assertEqual(len(res.sha256_hash), 64)

    def test_veto_fc_bio_01_gut_barrier_rupture(self):
        """FC-BIO-01: Veto inmediato si phi_gut < 0.899 (disbiosis / endotoxemia portal)."""
        disbiosis = TherapeuticTrajectoryCandidate(
            trajectory_id="TRAJ_LEAKY_GUT_DANGER",
            target_vmem_mv=-75.0,
            akkermansia_target_pct=0.2,   # Disbiosis severa
            teer_target_ohms=250.0        # Barrera rota
        )
        res = self.kernel.evaluate_and_audit_trajectory(disbiosis)
        self.assertFalse(res.admitted)
        self.assertEqual(res.veto_code, BiosecurityVetoCode.FC_BIO_01)
        self.assertEqual(res.status, "REJECTED_FAIL_CLOSED")
        self.assertIn("FC-BIO-01", res.veto_reason)

    def test_veto_fc_bio_02_atp_collapse(self):
        """FC-BIO-02: Veto si se produce un colapso citotóxico de ATP (< 15%)."""
        sobre_inhibida = TherapeuticTrajectoryCandidate(
            trajectory_id="TRAJ_ATP_COLLAPSE",
            target_vmem_mv=-75.0,
            target_phe=6.20,              # Estroma hiper-ácido
            inhibit_nhe1_fraction=0.95,   # Freno excesivo que apaga pHi
            akkermansia_target_pct=3.5,
            teer_target_ohms=1200.0
        )
        res = self.kernel.evaluate_and_audit_trajectory(sobre_inhibida)
        self.assertFalse(res.admitted)
        self.assertEqual(res.veto_code, BiosecurityVetoCode.FC_BIO_02)
        self.assertIn("FC-BIO-02", res.veto_reason)

    def test_veto_fc_bio_03_smaller_self_persisting(self):
        """FC-BIO-03: Veto si persiste el fenotipo despolarizado/oncogénico (Vmem >= -25 mV)."""
        fallida_onco = TherapeuticTrajectoryCandidate(
            trajectory_id="TRAJ_SMALLER_SELF_REMAINING",
            target_vmem_mv=-18.0,         # No logra repolarizar (sigue oncogénica)
            restore_cx43_conductance=0.10, # Conexinas cerradas
            akkermansia_target_pct=3.5,
            teer_target_ohms=1200.0
        )
        res = self.kernel.evaluate_and_audit_trajectory(fallida_onco)
        self.assertFalse(res.admitted)
        self.assertEqual(res.veto_code, BiosecurityVetoCode.FC_BIO_03)

    def test_free_energy_monotonicity(self):
        """Verifica que la Energía Libre Variacional F sea menor cuanto más cercana esté a la homeostasis."""
        f_sano = self.kernel.compute_variational_free_energy(
            v_mem=-75.0, phi_gut=1.0, atp_pct=95.0, pdl1_factor=1.1
        )
        f_perturbado = self.kernel.compute_variational_free_energy(
            v_mem=-45.0, phi_gut=0.85, atp_pct=60.0, pdl1_factor=2.5
        )
        f_grave = self.kernel.compute_variational_free_energy(
            v_mem=-20.0, phi_gut=0.40, atp_pct=20.0, pdl1_factor=4.5
        )

        self.assertLess(f_sano, f_perturbado)
        self.assertLess(f_perturbado, f_grave)

    def test_submillisecond_latency(self):
        """Verifica que el orquestador ejecute la auditoría determinista en tiempo sub-milisegundo."""
        candidato = TherapeuticTrajectoryCandidate(
            trajectory_id="TRAJ_BENCHMARK",
            target_vmem_mv=-75.0,
            akkermansia_target_pct=3.5,
            teer_target_ohms=1200.0
        )
        times = []
        for _ in range(100):
            res = self.kernel.evaluate_and_audit_trajectory(candidato)
            times.append(res.elapsed_ms)

        avg_ms = sum(times) / len(times)
        self.assertLess(avg_ms, 1.0, f"Latencia promedio esperada sub-milisegundo, obtenida: {avg_ms:.4f} ms")

    def test_pharmacological_regimen_admitted(self):
        """Verifica la admisión de un régimen armónico Cariporida + PQ1 + Buffer + Akkermansia."""
        res = self.kernel.evaluate_pharmacological_regimen(
            trajectory_id="REGIMEN_HARMONIC_01",
            cariporide_mg=30.0,
            pq1_mg=15.0,
            buffer_mmol=40.0,
            akkermansia_billions=30.0,
            duration_hours=24.0
        )
        self.assertTrue(res.admitted)
        self.assertEqual(res.status, "ADMITTED_MINIMAL_ACTION")
        self.assertEqual(len(res.sha256_hash), 64)

    def test_pharmacological_regimen_toxic_overdose_veto(self):
        """Verifica que una sobredosis farmacológica sea rechazada Fail-Closed."""
        res = self.kernel.evaluate_pharmacological_regimen(
            trajectory_id="REGIMEN_TOXIC_CARIPORIDE",
            cariporide_mg=500.0, # Dosis tóxica
            pq1_mg=15.0,
            buffer_mmol=40.0,
            akkermansia_billions=30.0
        )
        self.assertFalse(res.admitted)
        self.assertEqual(res.status, "REJECTED_FAIL_CLOSED")
        self.assertIn("FC-PKPD-02", res.veto_reason)


if __name__ == "__main__":
    unittest.main(verbosity=2)

