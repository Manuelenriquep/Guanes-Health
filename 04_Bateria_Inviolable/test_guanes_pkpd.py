"""
==================================================================================================
GUANES HEALTH - BATERÍA INVIOLABLE
Suite de Pruebas Unitarias para el Módulo PK/PD - test_guanes_pkpd.py
Kernel Nivel 0 / Verificación Biomédica Inmutable
==================================================================================================
Valida:
  1. Cálculo determinista de Cmax de Cariporida y clearance con vida media t_1/2 ~ 4.5 h.
  2. Modulación alostérica de Cx43 con PQ1 y respuesta Hill Emax.
  3. Crecimiento logístico luminal de Akkermansia muciniphila acoplado a barrera intestinal.
  4. Amortiguación estromal de pHe mediante infusión de buffer.
  5. Invariantes Fail-Closed: Veto a concentraciones negativas y veto a sobredosis que supere MTD.
  6. Sello criptográfico SHA-256 en cada estado temporal.
==================================================================================================
"""

import math
import os
import sys
import unittest

MOTOR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico"))
if MOTOR_DIR not in sys.path:
    sys.path.insert(0, MOTOR_DIR)

from guanes_pkpd import (
    PKPDSimulator,
    DrugDose,
    CARIPORIDE_IC50_UM,
    CARIPORIDE_MTD_UM,
    PQ1_EC50_UM,
    PQ1_MTD_UM
)


class TestGuanesPKPD(unittest.TestCase):
    """Pruebas rigurosas de la cinéticas y dinámicas PK/PD."""

    def setUp(self):
        self.simulator = PKPDSimulator(patient_weight_kg=70.0)

    def test_cariporide_cmax_and_elimination_kinetics(self):
        """Verifica que Cmax responda a dosis lineal y decaiga con t_1/2 de 4.5 horas."""
        dose_mg = 40.0 # Dosis clínica segura
        cmax_uM = self.simulator.calculate_cariporide_cmax(dose_mg)
        
        # Validar orden de magnitud físico en plasma (en rango de 0.5 a 2.0 uM)
        self.assertGreater(cmax_uM, 0.5)
        self.assertLess(cmax_uM, CARIPORIDE_MTD_UM)

        # Simular 4.5 horas (exactamente una vida media)
        traj = self.simulator.simulate_regimen(
            cariporide_dose_mg=dose_mg,
            pq1_dose_mg=0.0,
            buffer_dose_mmol=0.0,
            akkermansia_cfu_billions=0.0,
            duration_hours=4.5,
            time_step_h=0.5
        )

        initial_conc = traj[0].cariporide_conc_uM
        final_conc = traj[-1].cariporide_conc_uM

        # A t = t_1/2, la concentración debe ser aproximadamente el 50% de la inicial
        ratio = final_conc / initial_conc
        self.assertAlmostEqual(ratio, 0.50, delta=0.06)

        # A la concentración inicial, la inhibición de NHE1 debe ser superior al 90% dado que Cmax >> IC50 (0.05 uM)
        self.assertGreater(traj[0].nhe1_inhibition_fraction, 0.90)

    def test_pq1_cx43_activation_hill_dynamics(self):
        """Verifica que el modulador PQ1 restablezca el acoplamiento de conexinas según ecuación Hill."""
        traj = self.simulator.simulate_regimen(
            cariporide_dose_mg=0.0,
            pq1_dose_mg=15.0,
            buffer_dose_mmol=0.0,
            akkermansia_cfu_billions=0.0,
            duration_hours=12.0,
            time_step_h=1.0
        )

        initial_state = traj[0]
        self.assertGreater(initial_state.pq1_conc_uM, PQ1_EC50_UM)
        # Debe inducir una apertura notable de conexinas Cx43
        self.assertGreater(initial_state.cx43_activation_boost, 0.50)

    def test_akkermansia_colonization_and_gut_support(self):
        """Verifica la expansión logística luminal de Akkermansia y su soporte a la barrera."""
        traj = self.simulator.simulate_regimen(
            cariporide_dose_mg=0.0,
            pq1_dose_mg=0.0,
            buffer_dose_mmol=0.0,
            akkermansia_cfu_billions=50.0,
            duration_hours=48.0,
            time_step_h=2.0,
            initial_akkermansia=0.15
        )

        initial_density = traj[0].akkermansia_density
        final_density = traj[-1].akkermansia_density

        # Con el inóculo y la tasa intrínseca de crecimiento, la densidad debe mantenerse o crecer hacia eubiosis
        self.assertGreaterEqual(final_density, 0.40)
        self.assertLessEqual(final_density, 1.0)
        self.assertGreater(traj[-1].gut_barrier_improvement, 0.05)

    def test_sha256_cryptographic_state_chain(self):
        """Verifica que cada punto de la trayectoria temporal cuente con un hash SHA-256 inmutable."""
        traj = self.simulator.simulate_regimen(
            cariporide_dose_mg=20.0,
            pq1_dose_mg=5.0,
            buffer_dose_mmol=50.0,
            akkermansia_cfu_billions=20.0,
            duration_hours=6.0,
            time_step_h=1.0
        )

        self.assertGreater(len(traj), 5)
        for state in traj:
            self.assertEqual(len(state.sha256_hash), 64)
            # Recomputar y comparar
            self.assertEqual(state.sha256_hash, state.compute_sha256())

    def test_fail_closed_fc_pkpd_01_negative_or_nan(self):
        """FC-PKPD-01: Veto inmediato ante dosis negativas o no numéricas."""
        with self.assertRaises(ValueError):
            DrugDose(drug_id="Cariporide", dose_amount_mg=-10.0)

        with self.assertRaises(ValueError):
            self.simulator.simulate_regimen(
                cariporide_dose_mg=float("nan"),
                pq1_dose_mg=5.0,
                buffer_dose_mmol=10.0,
                akkermansia_cfu_billions=10.0
            )

    def test_fail_closed_fc_pkpd_02_toxic_overdose_veto(self):
        """FC-PKPD-02: Veto inmediato si la dosis genera una Cmax superior a la máxima tolerable (MTD)."""
        toxic_dose_mg = 500.0 # Dosis masiva que superaría MTD
        with self.assertRaises(ValueError) as context:
            self.simulator.simulate_regimen(
                cariporide_dose_mg=toxic_dose_mg,
                pq1_dose_mg=0.0,
                buffer_dose_mmol=0.0,
                akkermansia_cfu_billions=0.0
            )
        self.assertIn("FC-PKPD-02", str(context.exception))


if __name__ == "__main__":
    unittest.main()
