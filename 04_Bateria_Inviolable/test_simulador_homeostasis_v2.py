import unittest
import sys
import os

# Asegurar que el path incluya scratch para poder importar el módulo de simulación
sys.path.append("/workspace/scratch")

from simulador_onco_homeostasis_v3 import CelulaHumana, ReguladorRestricciones, SimuladorTratamiento

class TestSimuladorOncoHomeostasis(unittest.TestCase):
    """
    Suite de pruebas unitarias y de integración para validar el comportamiento
    del simulador oncológico canónico v2.3 con y sin escape por MCT2.
    """

    def setUp(self):
        """Inicialización de perfiles de prueba estándar."""
        self.sana = CelulaHumana(tipo_celular="Sana")
        self.tumor = CelulaHumana(tipo_celular="Tumor", atp_nivel=10000.0, telomeros=3920)
        self.tumor.Bcl2_expresion = 25.0
        self.tumor.pHe = 6.20
        self.tumor.PD_L1_expresion = 50.0

    def test_hayflick_senescencia_exacta(self):
        """
        Prueba 1: Verificación del Límite de Hayflick (VETO FC-BIO-02)
        Valida que tras exactamente 50 divisiones, los telómeros de una célula sana
        se reduzcan de 8000 pb a 4000 pb, gatillando la senescencia (viabilidad = 0.5)
        en el paso de frontera exacto de la generación 50 (usando <= 4000).
        """
        regulador = ReguladorRestricciones(self.sana)
        
        # Simular 50 divisiones exactas (desgaste de 80 pb por ciclo)
        for _ in range(50):
            self.sana.degradar_telomeros()
            
        viabilidad, alarmas = regulador.evaluar_homeostasis()
        
        # Verificaciones del estado de frontera
        self.assertEqual(self.sana.divisiones, 50, "La célula debe registrar exactamente 50 divisiones.")
        self.assertEqual(self.sana.telomeros, 4000, "La longitud telomérica terminal debe ser de exactamente 4000 pb.")
        self.assertEqual(viabilidad, 0.5, "La viabilidad debe caer a 0.5 (Arresto Replicativo Permanente).")
        
        # Verificar que la alarma de senescencia se haya activado
        alarma_detectada = any("VETO FC-BIO-02" in alarma for alarma in alarmas)
        self.assertTrue(alarma_detectada, "La alarma VETO FC-BIO-02 de senescencia debe estar activa.")

    def test_kinetic_priming_cohorte_c_eficacia_sin_escape(self):
        """
        Prueba 2: Validación de la respuesta temporal de la Cohorte C (Sin Escape)
        Verifica que bajo el esquema estándar de Kinetic Priming, el modelo matemático simule
        un colapso completo de la viabilidad tumoral (0.00%) al final de la simulación (t=72h).
        """
        simulador = SimuladorTratamiento()
        resultados = simulador.ejecutar_simulacion(cohorte="C", mutacion_mct2=False)
        
        viabilidad_final = resultados["viabilidad"][-1]
        pHi_final = resultados["pHi"][-1]
        pHe_final = resultados["pHe"][-1]
        atp_final = resultados["atp"][-1]
        eficiencia_cd8_final = resultados["eficiencia_cd8"][-1]

        # Verificaciones de los límites del modelo (Veredicto Simulado)
        self.assertAlmostEqual(viabilidad_final, 0.0, places=2, 
                               msg="La viabilidad tumoral simulada al final de la Cohorte C debe aproximarse a 0.0.")
        self.assertAlmostEqual(pHi_final, 5.75, places=2, 
                               msg="El pHi final del tumor debe depletarse en el valor crítico de 5.75.")
        self.assertAlmostEqual(pHe_final, 7.35, places=2, 
                               msg="El pHe del microambiente tumoral debe normalizarse en el rango de 7.35.")
        self.assertAlmostEqual(atp_final, 30.0, places=1, 
                               msg="El balance energético de ATP del tumor debe depletarse hasta el valor límite de 30.0 u.")
        self.assertAlmostEqual(eficiencia_cd8_final, 100.0, places=1, 
                               msg="La eficiencia citotóxica simulada de los CD8+ debe alcanzar el 100.0%.")

    def test_kinetic_priming_cohorte_c_escape_mct2_resistencia(self):
        """
        Prueba 3: Validación del bypass adaptativo por sobreexpresión de MCT2
        Verifica que ante la mutación activa de MCT2, el tumor escape a la apoptosis ácida
        y a la depuración celular por linfocitos CD8+ a t=72h.
        """
        simulador = SimuladorTratamiento()
        resultados = simulador.ejecutar_simulacion(cohorte="C", mutacion_mct2=True)
        
        mct2_final = resultados["mct2"][-1]
        pHi_final = resultados["pHi"][-1]
        pHe_final = resultados["pHe"][-1]
        atp_final = resultados["atp"][-1]
        eficiencia_cd8_final = resultados["eficiencia_cd8"][-1]
        viabilidad_final = resultados["viabilidad"][-1]

        # Verificaciones del comportamiento de escape adaptativo
        self.assertAlmostEqual(mct2_final, 15.0, places=1, 
                               msg="La expresión de MCT2 debe aumentar hasta un factor de x15.")
        self.assertAlmostEqual(pHi_final, 6.54, places=2, 
                               msg="MCT2 debe rescatar el pHi tumoral hasta ~6.54, eludiendo la autólisis ácida.")
        self.assertAlmostEqual(pHe_final, 6.65, places=2, 
                               msg="La extrusión persistente de protones debe mantener el pHe estromal ácido en ~6.65.")
        self.assertAlmostEqual(atp_final, 748.5, places=1, 
                               msg="El tumor debe preservar su balance energético de ATP cerca de ~748.5 u.")
        self.assertAlmostEqual(eficiencia_cd8_final, 0.0, places=1, 
                               msg="La eficiencia citotóxica de los CD8+ debe colapsar a 0.0% por acidosis estromal remanente.")
        self.assertAlmostEqual(viabilidad_final, 1.0, places=2, 
                               msg="La viabilidad tumoral debe preservarse en 1.0 (100.0% de escape adaptativo).")

if __name__ == "__main__":
    unittest.main()
