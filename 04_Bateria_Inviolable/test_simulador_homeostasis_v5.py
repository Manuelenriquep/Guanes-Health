"""
Fronteras numéricas de simulador_onco_homeostasis_v5 (Capa B).
Cubre política CD8 Gated-6.50 y escenarios Cohorte C / MCT2.
No es evidencia clínica.
"""
import unittest
import sys
import os

MOTOR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico")
)
sys.path.insert(0, MOTOR_DIR)

from simulador_onco_homeostasis_v5 import SimuladorTratamiento


class TestSimuladorOncoHomeostasisV5(unittest.TestCase):
    """Regresión de la línea dinámica canónica (v5)."""

    def test_cohorte_c_sin_escape(self):
        resultados = SimuladorTratamiento().ejecutar_simulacion(
            cohorte="C", mutacion_mct2=False, inhibicion_mct2=False
        )
        self.assertAlmostEqual(resultados["viabilidad"][-1], 0.0, places=2)
        self.assertAlmostEqual(resultados["pHe"][-1], 7.35, places=2)
        self.assertAlmostEqual(resultados["eficiencia_cd8"][-1], 100.0, places=1)

    def test_cohorte_c_escape_mct2_anula_cd8(self):
        """pHe residual ~6.65 → cruda < anergy gate → CD8 0%."""
        resultados = SimuladorTratamiento().ejecutar_simulacion(
            cohorte="C", mutacion_mct2=True, inhibicion_mct2=False
        )
        self.assertAlmostEqual(resultados["pHe"][-1], 6.65, places=2)
        self.assertAlmostEqual(resultados["eficiencia_cd8"][-1], 0.0, places=1)
        self.assertAlmostEqual(resultados["viabilidad"][-1], 1.0, places=2)

    def test_cohorte_c_triple_inhibicion(self):
        resultados = SimuladorTratamiento().ejecutar_simulacion(
            cohorte="C", mutacion_mct2=True, inhibicion_mct2=True
        )
        self.assertAlmostEqual(resultados["pHe"][-1], 7.35, places=2)
        self.assertAlmostEqual(resultados["eficiencia_cd8"][-1], 100.0, places=1)
        self.assertAlmostEqual(resultados["viabilidad"][-1], 0.0, places=2)


if __name__ == "__main__":
    unittest.main()
