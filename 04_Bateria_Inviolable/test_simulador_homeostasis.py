import unittest
import sys
import os

MOTOR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico")
)
sys.path.insert(0, MOTOR_DIR)

from simulador_onco_homeostasis_v2 import (
    CelulaHumana,
    ReguladorRestricciones,
    SimuladorTratamiento,
)


class TestSimuladorOncoHomeostasis(unittest.TestCase):
    """Pruebas del simulador oncológico de referencia v2.2 (salidas de modelo)."""

    def setUp(self):
        self.sana = CelulaHumana(tipo_celular="Sana")
        self.tumor = CelulaHumana(tipo_celular="Tumor", atp_nivel=10000.0, telomeros=3920)
        self.tumor.Bcl2_expresion = 25.0
        self.tumor.pHe = 6.20
        self.tumor.PD_L1_expresion = 50.0

    def test_hayflick_senescencia_exacta(self):
        """VETO FC-BIO-02: a 50 divisiones, 8000→4000 pb y viabilidad 0.5 (umbral <= 4000)."""
        regulador = ReguladorRestricciones(self.sana)

        for _ in range(50):
            self.sana.degradar_telomeros()

        viabilidad, alarmas = regulador.evaluar_homeostasis()

        self.assertEqual(self.sana.divisiones, 50)
        self.assertEqual(self.sana.telomeros, 4000)
        self.assertEqual(viabilidad, 0.5)
        self.assertTrue(any("VETO FC-BIO-02" in a for a in alarmas))

    def test_kinetic_priming_cohorte_c_modelo(self):
        """Cohorte C a t=72 h: viabilidad→0 y pH/ATP/CD8 según salida del toy model."""
        resultados = SimuladorTratamiento().ejecutar_simulacion(cohorte="C")

        self.assertAlmostEqual(resultados["viabilidad"][-1], 0.0, places=2)
        self.assertAlmostEqual(resultados["pHi"][-1], 5.75, places=2)
        self.assertAlmostEqual(resultados["pHe"][-1], 7.35, places=2)
        self.assertAlmostEqual(resultados["atp"][-1], 30.0, places=1)
        self.assertAlmostEqual(resultados["eficiencia_cd8"][-1], 100.0, places=1)


if __name__ == "__main__":
    unittest.main()
