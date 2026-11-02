"""
Test unitario para BaseKernelLevel0 y la Matriz de Precisión Ponderada
======================================================================
"""
import os
import sys
import unittest
import numpy as np

MOTOR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico"))
if MOTOR_DIR not in sys.path:
    sys.path.insert(0, MOTOR_DIR)

from base_kernel_level0 import BaseKernelLevel0
from guanes_kernel_level0 import GuanesKernelLevel0


class TestBaseKernelLevel0(unittest.TestCase):
    def setUp(self):
        self.base = BaseKernelLevel0(kernel_id="TEST_BASE_L0")

    def test_precision_matrix_free_energy(self):
        current = np.array([-70.0, 7.30, 0.90, 80.0])
        target = np.array([-75.0, 7.40, 0.95, 100.0])
        weights = np.array([0.01, 5.0, 100.0, 0.01])

        f_weighted = self.base.compute_variational_free_energy(current, target, precision_weights=weights)
        self.assertGreater(f_weighted, 0.0)

        # Sin pesos
        f_unweighted = self.base.compute_variational_free_energy(current, target)
        self.assertNotEqual(f_weighted, f_unweighted)

    def test_short_circuit_firewalls(self):
        evaluated = []

        def rule_1(s):
            evaluated.append("R1")
            return s.get("x", 0) > 10, "x mayor a 10"

        def rule_2(s):
            evaluated.append("R2")
            return s.get("y", 0) > 10, "y mayor a 10"

        self.base.register_firewall("R1", "Regla 1", rule_1)
        self.base.register_firewall("R2", "Regla 2", rule_2)

        # Dispara R1 y no debe evaluar R2 (Short-Circuit)
        passed, rule, msg = self.base.evaluate_firewalls({"x": 20, "y": 20})
        self.assertFalse(passed)
        self.assertEqual(rule, "R1")
        self.assertEqual(evaluated, ["R1"])

    def test_inheritance_guanes_kernel(self):
        gk = GuanesKernelLevel0()
        self.assertIsInstance(gk, BaseKernelLevel0)
        self.assertEqual(gk.kernel_id, "GUANES_HEALTH_L0")
        self.assertGreater(len(gk.firewalls), 0)


if __name__ == "__main__":
    unittest.main()
