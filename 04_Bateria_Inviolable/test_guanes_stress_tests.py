"""
Guanes Health - Wrapper para TestGuanesStressTests
Permite la ejecución vía test_guanes_stress_tests.py y guanes_stress_tests.py
"""
import os
import sys
import unittest

BATERIA_DIR = os.path.dirname(os.path.abspath(__file__))
if BATERIA_DIR not in sys.path:
    sys.path.insert(0, BATERIA_DIR)

MOTOR_DIR = os.path.abspath(os.path.join(BATERIA_DIR, "..", "03_Motor_Oncologico"))
if MOTOR_DIR not in sys.path:
    sys.path.insert(0, MOTOR_DIR)

from guanes_stress_tests import TestGuanesStressTests

if __name__ == "__main__":
    unittest.main()
