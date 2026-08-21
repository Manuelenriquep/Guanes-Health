"""Suite v2 (copia operativa). Canon: 04_Bateria_Inviolable/test_simulador_onco_hepatico-v2.py"""
import unittest
import sys
import os

_MOTOR_DIR = os.path.abspath(os.path.dirname(__file__))
if _MOTOR_DIR not in sys.path:
    sys.path.insert(0, _MOTOR_DIR)

from simulador_onco_hepatico_v2 import SimuladorOncoHepaticoBidireccional

class TestSimuladorOncoHepaticoCoupled(unittest.TestCase):
    """
    Suite de pruebas integradas para validar el comportamiento del simulador
    onco-hepático bidireccional v2.0 (Opción A).
    """

    def setUp(self):
        self.sim = SimuladorOncoHepaticoBidireccional()

    def test_coupled_unidirectional_clearance(self):
        """
        Prueba 1: Aclaramiento Inmune Exitoso (Unidireccional Estándar).
        Verifica que sin retroalimentación y bajo la Cohorte C, el estroma limpio (pHe 7.35)
        permita la reactivación lítica total de CD8+ tanto para el tumor (viabilidad -> 0%)
        como para el hepatocito infectado (viabilidad -> 0%).
        """
        res = self.sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=False, feedback_activo=False)
        
        self.assertAlmostEqual(res["pHe"][-1], 7.35, places=2)
        self.assertAlmostEqual(res["viabilidad_tumor"][-1], 0.00, places=2)
        self.assertAlmostEqual(res["viabilidad_hepatocito"][-1], 0.00, places=2)

    def test_coupled_mct2_sanctuary(self):
        """
        Prueba 2: Santuario Viral inducido por Escape del Tumor (MCT2).
        Verifica que el escape metabólico del tumor vía MCT2 (pHe ~ 6.65) deprima la eficiencia
        de CD8+ a 0%, protegiendo colateralmente al hepatocito infectado (viabilidad -> 100%)
        y permitiendo una alta carga viral (> 800 viriones) a las 72 horas.
        """
        res = self.sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=True, feedback_activo=False)
        
        self.assertAlmostEqual(res["pHe"][-1], 6.65, places=2)
        self.assertAlmostEqual(res["viabilidad_tumor"][-1], 1.00, places=2)
        self.assertAlmostEqual(res["viabilidad_hepatocito"][-1], 1.00, places=2)
        self.assertGreater(res["carga_viral"][-1], 800.0)

    def test_coupled_bidirectional_feedback_escape(self):
        """
        Prueba 3: Escape Tumoral inducido por Infección (Retroalimentación Opción A).
        Verifica que bajo el bucle bidireccional activo, la secreción de IL-6 por el hepatocito
        infectado (> 300 pg/mL) hiper-regule la expresión de PD-L1 en el tumor (> 1000x),
        saturando la inmunoterapia anti-PD-1 y provocando el escape terapéutico del tumor
        (viabilidad terminal > 15.0%) y del hepatocito.
        """
        res = self.sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=False, feedback_activo=True, beta_pd_l1=3.0)
        
        self.assertGreater(res["il6"][-1], 300.0, "La concentración de IL-6 debe superar los 300 pg/mL")
        self.assertGreater(res["pd_l1_tumor"][-1], 1000.0, "La expresión de PD-L1 tumoral debe superar las 1000x")
        self.assertGreater(res["viabilidad_tumor"][-1], 0.15, "El tumor debe escapar del aclaramiento (> 15% viabilidad)")
        self.assertAlmostEqual(res["viabilidad_hepatocito"][-1], 1.00, places=2)

if __name__ == "__main__":
    unittest.main()
