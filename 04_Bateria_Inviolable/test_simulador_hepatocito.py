import unittest
import numpy as np
import sys
import os

# Asegurar que el path incluya scratch para poder importar el módulo de simulación del hepatocito
sys.path.append("/workspace/scratch")

from simulador_hepatocito_infeccion import HepatocitoInmuneIntegrado, SimuladorHepatitisB

class TestSimuladorHepatocitoInfeccion(unittest.TestCase):
    """
    Suite de pruebas unitarias y de integración para validar el comportamiento
    del simulador de hepatocito e infección por HBV de referencia v1.1.
    """

    def test_zonacion_hepatica(self):
        """
        Prueba 1: Verificación de la Zonación Hepática (Nivel 4).
        Valida que el gradiente de oxígeno (presión parcial de O2) condicione de
        manera correcta la densidad de expresión basal del receptor NTCP.
        """
        # Caso A: Estado de Excepción por Isquemia (< 20 mmHg)
        hep_isquemia = HepatocitoInmuneIntegrado(o2_pp=15.0)
        self.assertEqual(hep_isquemia.ntcp_densidad_basal, 0.2)
        
        # Caso B: Zona 3 (Pericentral, <= 35 mmHg)
        hep_zona3 = HepatocitoInmuneIntegrado(o2_pp=30.0)
        self.assertEqual(hep_zona3.ntcp_densidad_basal, 0.8)
        
        # Caso C: Zona 1 (Periportal, > 35 mmHg)
        hep_zona1 = HepatocitoInmuneIntegrado(o2_pp=60.0)
        self.assertEqual(hep_zona1.ntcp_densidad_basal, 1.2)

    def test_represion_il6(self):
        """
        Prueba 2: Regulación e Interacción de la Inmunidad Innata (Eje IL-6).
        Valida que la exposición a la citoquina inflamatoria IL-6 reprima de forma
        dosis-dependiente la densidad de NTCP en la membrana sinusoidal.
        """
        hep = HepatocitoInmuneIntegrado(o2_pp=60.0)  # Densidad basal = 1.2
        hep.il6_concentracion = 50.0  # pg/mL
        
        # Evaluar regulación (inóculo = 0 para ver solo la regulación)
        res = hep.evaluar_regulacion_y_entrada_viral(inóculo_HBV=0.0)
        
        # Con IL-6 = 50 pg/mL, la represión es: 1.0 - 0.98 * (50 / (50 + 50)) = 1.0 - 0.49 = 0.51
        # NTCP final en membrana = 1.2 * 0.51 = 0.612
        self.assertAlmostEqual(res["NTCP_Membrana"], 0.612, places=3)

    def test_myrcludex_b_optimo_vs_toxico(self):
        """
        Prueba 3: Farmacodinámica del Myrcludex B y Veto Redox (VETO FC-HEP-01).
        Compara la ventana de seguridad de Myrcludex B:
        - Dosis óptima de 10 nM: Bloqueo viral sin depletar el GSH celular.
        - Dosis tóxica de 1000 nM: Bloqueo biliar extremo, depletación de GSH a <30%
          y detención biológica por apoptosis (viabilidad = 0.0).
        """
        sim = SimuladorHepatitisB()
        
        # Caso A: Myrcludex B Óptimo (10 nM)
        res_opt = sim.simular_escenario("Myrcludex_Optimo")
        self.assertEqual(res_opt["viabilidad"][-1], 1.0, "La viabilidad debe mantenerse intacta en dosis de 10 nM.")
        self.assertLess(res_opt["carga_viral"][-1], 20.0, "La carga viral debe mantenerse controlada por debajo de 20 viriones (reducción masiva).")
        self.assertEqual(res_opt["gsh"][-1], 8.0, "El pool de GSH debe preservarse en niveles nominales de 8.0 mM.")

        # Caso B: Myrcludex B Suprafisiológico (1000 nM)
        res_tox = sim.simular_escenario("Myrcludex_Toxico")
        self.assertEqual(res_tox["viabilidad"][-1], 0.0, "La viabilidad debe colapsar a 0.0 por apoptosis colestásica.")
        self.assertLess(res_tox["gsh"][-1], 2.4, "El pool de GSH debió depletarse por debajo del umbral crítico de 2.4 mM (30% de 8.0).")

if __name__ == "__main__":
    unittest.main()
