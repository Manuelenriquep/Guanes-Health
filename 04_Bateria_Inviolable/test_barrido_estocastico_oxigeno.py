import unittest
import sys
import os

MOTOR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico")
)
sys.path.insert(0, MOTOR_DIR)

from barrido_estocastico_oxigeno import vegf_en_punto


class TestBarridoEstocasticoOxigeno(unittest.TestCase):
    """Aserciones de frontera del toy model O2 -> HIF -> VEGF (semilla fija)."""

    def test_hipoxia_permanente_alta_vegf(self):
        vegf = vegf_en_punto(mu=2.0, sigma=0.3, monte_carlo_runs=5, seed=1)
        self.assertGreater(vegf, 90.0)

    def test_normoxia_segura_baja_vegf(self):
        vegf = vegf_en_punto(mu=10.0, sigma=0.3, monte_carlo_runs=5, seed=2)
        self.assertLess(vegf, 10.0)

    def test_bypass_estocastico_eleva_vegf_en_normoxia_aparente(self):
        """Con mu ~8%, subir sigma debe aumentar activacion VEGF vs bajo ruido."""
        bajo_ruido = vegf_en_punto(mu=8.0, sigma=0.5, monte_carlo_runs=8, seed=3)
        alto_ruido = vegf_en_punto(mu=8.0, sigma=4.0, monte_carlo_runs=8, seed=3)
        self.assertLess(bajo_ruido, 25.0)
        self.assertGreater(alto_ruido, bajo_ruido + 15.0)


if __name__ == "__main__":
    unittest.main()
