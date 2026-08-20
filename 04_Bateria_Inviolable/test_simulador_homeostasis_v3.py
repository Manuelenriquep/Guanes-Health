import unittest
import sys
import os

# Asegurar que el path incluya scratch para poder importar el módulo de simulación v4
sys.path.append("/workspace/scratch")

from simulador_onco_homeostasis_v4 import CelulaHumana, ReguladorRestricciones, SimuladorTratamiento

class TestSimuladorOncoHomeostasisV3(unittest.TestCase):
    """
    Suite de pruebas unitarias v3.0 para validar la homeostasis, senescencia,
    resistencia de escape por MCT2 y la estrategia de triple inhibición (MCT1/4 + MCT2).
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
        Prueba 2: Validación de la respuesta temporal de la Cohorte C estándar
        Verifica que sin mutación de escape adaptativa, la viabilidad tumoral caiga a 0.00%
        con una restauración exitosa de CD8+ al 100.0%.
        """
        simulador = SimuladorTratamiento()
        resultados = simulador.ejecutar_simulacion(cohorte="C", mutacion_mct2=False, inhibicion_mct2=False)
        
        viabilidad_final = resultados["viabilidad"][-1]
        pHi_final = resultados["pHi"][-1]
        pHe_final = resultados["pHe"][-1]
        atp_final = resultados["atp"][-1]
        eficiencia_cd8_final = resultados["eficiencia_cd8"][-1]

        self.assertAlmostEqual(viabilidad_final, 0.0, places=2)
        self.assertAlmostEqual(pHi_final, 5.75, places=2)
        self.assertAlmostEqual(pHe_final, 7.35, places=2)
        self.assertAlmostEqual(atp_final, 30.0, places=1)
        self.assertAlmostEqual(eficiencia_cd8_final, 100.0, places=1)

    def test_kinetic_priming_cohorte_c_escape_mct2_resistencia(self):
        """
        Prueba 3: Verificación del bypass adaptativo por sobreexpresión de MCT2
        Valida que al activarse la mutación adaptativa, el tumor logre rescatar su pHi a 6.54,
        mantenga acidosis estromal (6.65) e inmunotolerancia adquirida (CD8+ = 0.0%, viabilidad = 100.0%).
        """
        simulador = SimuladorTratamiento()
        resultados = simulador.ejecutar_simulacion(cohorte="C", mutacion_mct2=True, inhibicion_mct2=False)
        
        viabilidad_final = resultados["viabilidad"][-1]
        pHi_final = resultados["pHi"][-1]
        pHe_final = resultados["pHe"][-1]
        atp_final = resultados["atp"][-1]
        eficiencia_cd8_final = resultados["eficiencia_cd8"][-1]
        mct2_final = resultados["mct2"][-1]

        self.assertAlmostEqual(mct2_final, 15.0, places=1)
        self.assertAlmostEqual(viabilidad_final, 1.0, places=2)
        self.assertAlmostEqual(pHi_final, 6.54, places=2)
        self.assertAlmostEqual(pHe_final, 6.65, places=2)
        self.assertAlmostEqual(atp_final, 748.5, places=1)
        self.assertAlmostEqual(eficiencia_cd8_final, 0.0, places=1)

    def test_kinetic_priming_cohorte_c_triple_inhibicion_neutralizacion(self):
        """
        Prueba 4: Validación de la triple inhibición (MCT1/4 + MCT2)
        Valida que al bloquear terapéuticamente el escape de MCT2 (inhibicion_mct2=True),
        se neutralice la mutación compensatoria, induciendo un colapso ácido profundo (pHi = 5.50),
        depleción bioenergética total (ATP = 10.0 u.), restauración inmune (CD8+ = 100.0%)
        y aclaramiento completo de la viabilidad (0.00%).
        """
        simulador = SimuladorTratamiento()
        resultados = simulador.ejecutar_simulacion(cohorte="C", mutacion_mct2=True, inhibicion_mct2=True)
        
        viabilidad_final = resultados["viabilidad"][-1]
        pHi_final = resultados["pHi"][-1]
        pHe_final = resultados["pHe"][-1]
        atp_final = resultados["atp"][-1]
        eficiencia_cd8_final = resultados["eficiencia_cd8"][-1]
        mct2_final = resultados["mct2"][-1]

        self.assertAlmostEqual(mct2_final, 0.5, places=1)
        self.assertAlmostEqual(viabilidad_final, 0.0, places=2)
        self.assertAlmostEqual(pHi_final, 5.50, places=2)
        self.assertAlmostEqual(pHe_final, 7.35, places=2)
        self.assertAlmostEqual(atp_final, 10.0, places=1)
        self.assertAlmostEqual(eficiencia_cd8_final, 100.0, places=1)

if __name__ == "__main__":
    unittest.main()
