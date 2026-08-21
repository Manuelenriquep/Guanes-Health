"""Fronteras de inmuno_utils (Gated-6.50). No es evidencia clínica."""
import os
import sys
import unittest

MOTOR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico")
)
sys.path.insert(0, MOTOR_DIR)

from inmuno_utils import calcular_eficiencia_cd8


class TestInmunoUtils(unittest.TestCase):
    def test_gated_650_fronteras(self):
        self.assertEqual(calcular_eficiencia_cd8(6.50), 0.0)
        self.assertEqual(calcular_eficiencia_cd8(6.20), 0.0)
        self.assertEqual(calcular_eficiencia_cd8(6.65), 0.0)
        self.assertEqual(calcular_eficiencia_cd8(7.35), 1.0)
        self.assertGreaterEqual(calcular_eficiencia_cd8(6.67), 0.20)


if __name__ == "__main__":
    unittest.main()
