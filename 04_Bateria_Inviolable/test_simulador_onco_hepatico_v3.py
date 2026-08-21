"""Regresión numérica del acoplamiento onco-hepático v3 (Capa B)."""
import os
import sys
import unittest

MOTOR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico")
)
sys.path.insert(0, MOTOR_DIR)

from simulador_onco_hepatico_v3 import SimuladorOncoHepaticoBidireccional


class TestSimuladorOncoHepaticoCoupledV3(unittest.TestCase):
    def setUp(self):
        self.sim = SimuladorOncoHepaticoBidireccional()

    def test_coupled_unidirectional_clearance(self):
        res = self.sim.ejecutar_simulacion(
            cohorte="C", mutacion_mct2=False, feedback_activo=False
        )
        self.assertAlmostEqual(res["pHe"][-1], 7.35, places=2)
        self.assertAlmostEqual(res["viabilidad_tumor"][-1], 0.00, places=2)
        self.assertAlmostEqual(res["viabilidad_hepatocito"][-1], 0.00, places=2)

    def test_coupled_mct2_sanctuary(self):
        """Escape MCT2: pHe~6.65 → Gated-6.50 anula CD8."""
        res = self.sim.ejecutar_simulacion(
            cohorte="C", mutacion_mct2=True, feedback_activo=False
        )
        self.assertAlmostEqual(res["pHe"][-1], 6.65, places=2)
        self.assertAlmostEqual(res["eficiencia_cd8"][-1], 0.0, places=1)
        self.assertAlmostEqual(res["viabilidad_tumor"][-1], 1.00, places=2)
        self.assertAlmostEqual(res["viabilidad_hepatocito"][-1], 1.00, places=2)
        self.assertGreater(res["carga_viral"][-1], 800.0)

    def test_coupled_bidirectional_feedback_escape(self):
        res = self.sim.ejecutar_simulacion(
            cohorte="C", mutacion_mct2=False, feedback_activo=True, beta_pd_l1=3.0
        )
        self.assertGreater(res["il6"][-1], 300.0)
        self.assertGreater(res["pd_l1_tumor"][-1], 1000.0)
        self.assertGreater(res["viabilidad_tumor"][-1], 0.15)
        self.assertAlmostEqual(res["viabilidad_hepatocito"][-1], 1.00, places=2)

    def test_coupled_cointervention_clearance(self):
        res = self.sim.ejecutar_simulacion(
            cohorte="C",
            mutacion_mct2=False,
            feedback_activo=True,
            myrcludex_nM=10.0,
            beta_pd_l1=0.1,
        )
        self.assertAlmostEqual(res["viabilidad_tumor"][-1], 0.00, places=2)
        self.assertLess(res["carga_viral"][-1], 25.0)
        self.assertLess(res["pd_l1_tumor"][-1], 150.0)
        self.assertGreater(res["gsh"][-1], 5.0)


if __name__ == "__main__":
    unittest.main()
