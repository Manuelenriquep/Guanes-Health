import unittest
import sys
import os

MOTOR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico")
)
sys.path.insert(0, MOTOR_DIR)

from simulador_onco_homeostasis_v4 import (
    CelulaHumana,
    ReguladorRestricciones,
    SimuladorTratamiento,
)


class TestSimuladorOncoHomeostasisV3(unittest.TestCase):
    """Suite v2.4: Hayflick, Cohorte C, escape MCT2 y triple inhibición."""

    def setUp(self):
        self.sana = CelulaHumana(tipo_celular="Sana")
        self.tumor = CelulaHumana(tipo_celular="Tumor", atp_nivel=10000.0, telomeros=3920)
        self.tumor.Bcl2_expresion = 25.0
        self.tumor.pHe = 6.20
        self.tumor.PD_L1_expresion = 50.0

    def test_hayflick_senescencia_exacta(self):
        """VETO FC-BIO-02: 50 divisiones → 4000 pb y viabilidad 0.5."""
        regulador = ReguladorRestricciones(self.sana)

        for _ in range(50):
            self.sana.degradar_telomeros()

        viabilidad, alarmas = regulador.evaluar_homeostasis()

        self.assertEqual(self.sana.divisiones, 50)
        self.assertEqual(self.sana.telomeros, 4000)
        self.assertEqual(viabilidad, 0.5)
        self.assertTrue(any("VETO FC-BIO-02" in a for a in alarmas))

    def test_kinetic_priming_cohorte_c_eficacia_sin_escape(self):
        """Cohorte C estándar sin escape: aclaramiento completo a t=72 h."""
        resultados = SimuladorTratamiento().ejecutar_simulacion(
            cohorte="C", mutacion_mct2=False, inhibicion_mct2=False
        )

        self.assertAlmostEqual(resultados["viabilidad"][-1], 0.0, places=2)
        self.assertAlmostEqual(resultados["pHi"][-1], 5.75, places=2)
        self.assertAlmostEqual(resultados["pHe"][-1], 7.35, places=2)
        self.assertAlmostEqual(resultados["atp"][-1], 30.0, places=1)
        self.assertAlmostEqual(resultados["eficiencia_cd8"][-1], 100.0, places=1)

    def test_kinetic_priming_cohorte_c_escape_mct2_resistencia(self):
        """Escape MCT2: pHi rescatado, acidosis estromal y viabilidad 100%."""
        resultados = SimuladorTratamiento().ejecutar_simulacion(
            cohorte="C", mutacion_mct2=True, inhibicion_mct2=False
        )

        self.assertAlmostEqual(resultados["mct2"][-1], 15.0, places=1)
        self.assertAlmostEqual(resultados["viabilidad"][-1], 1.0, places=2)
        self.assertAlmostEqual(resultados["pHi"][-1], 6.54, places=2)
        self.assertAlmostEqual(resultados["pHe"][-1], 6.65, places=2)
        self.assertAlmostEqual(resultados["atp"][-1], 748.5, places=1)
        self.assertAlmostEqual(resultados["eficiencia_cd8"][-1], 0.0, places=1)

    def test_kinetic_priming_cohorte_c_triple_inhibicion_neutralizacion(self):
        """Triple inhibición MCT1/4 + MCT2: colapso ácido y aclaramiento."""
        resultados = SimuladorTratamiento().ejecutar_simulacion(
            cohorte="C", mutacion_mct2=True, inhibicion_mct2=True
        )

        self.assertAlmostEqual(resultados["mct2"][-1], 0.5, places=1)
        self.assertAlmostEqual(resultados["viabilidad"][-1], 0.0, places=2)
        self.assertAlmostEqual(resultados["pHi"][-1], 5.50, places=2)
        self.assertAlmostEqual(resultados["pHe"][-1], 7.35, places=2)
        self.assertAlmostEqual(resultados["atp"][-1], 10.0, places=1)
        self.assertAlmostEqual(resultados["eficiencia_cd8"][-1], 100.0, places=1)


if __name__ == "__main__":
    unittest.main()
