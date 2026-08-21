import unittest
import sys
import os

MOTOR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico")
)
sys.path.insert(0, MOTOR_DIR)

from simulador_onco_hepatico_v2 import SimuladorOncoHepaticoBidireccional

class TestSimuladorOncoHepaticoCoupled(unittest.TestCase):
    """Regresion numerica del acoplamiento onco-hepatico v2 (Capa B)."""

    def setUp(self):
        self.sim = SimuladorOncoHepaticoBidireccional()

    def test_coupled_unidirectional_clearance(self):
        """Sin feedback, Cohorte C: viabilidades tumor/hepatocito -> 0 (modelo)."""
        res = self.sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=False, feedback_activo=False)
        
        self.assertAlmostEqual(res["pHe"][-1], 7.35, places=2)
        self.assertAlmostEqual(res["viabilidad_tumor"][-1], 0.00, places=2)
        self.assertAlmostEqual(res["viabilidad_hepatocito"][-1], 0.00, places=2)

    def test_coupled_mct2_sanctuary(self):
        """Escape MCT2: pHe acido, CD8 deprimidos, hepatocito/tumor viables."""
        res = self.sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=True, feedback_activo=False)
        
        self.assertAlmostEqual(res["pHe"][-1], 6.65, places=2)
        self.assertAlmostEqual(res["viabilidad_tumor"][-1], 1.00, places=2)
        self.assertAlmostEqual(res["viabilidad_hepatocito"][-1], 1.00, places=2)
        self.assertGreater(res["carga_viral"][-1], 800.0)

    def test_coupled_bidirectional_feedback_escape(self):
        """Feedback beta=3: IL-6/PD-L1 altos y escape tumoral parcial."""
        res = self.sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=False, feedback_activo=True, beta_pd_l1=3.0)
        
        self.assertGreater(res["il6"][-1], 300.0, "IL-6 modelo > 300")
        self.assertGreater(res["pd_l1_tumor"][-1], 1000.0, "PD-L1 modelo > 1000x")
        self.assertGreater(res["viabilidad_tumor"][-1], 0.15, "viabilidad tumoral > 15%")
        self.assertAlmostEqual(res["viabilidad_hepatocito"][-1], 1.00, places=2)

    def test_coupled_cointervention_clearance(self):
        """Co-intervencion: Myrcludex 10 nM + beta=0.1 -> viabilidad tumoral 0."""
        res = self.sim.ejecutar_simulacion(
            cohorte="C",
            mutacion_mct2=False,
            feedback_activo=True,
            myrcludex_nM=10.0,
            beta_pd_l1=0.1
        )
        
        self.assertAlmostEqual(res["viabilidad_tumor"][-1], 0.00, places=2)
        self.assertLess(res["carga_viral"][-1], 25.0, "carga viral < 25")
        self.assertLess(res["pd_l1_tumor"][-1], 150.0, "PD-L1 < umbral 150x")
        self.assertGreater(res["gsh"][-1], 5.0, "GSH > 5 mM")

if __name__ == "__main__":
    unittest.main()
