# -*- coding: utf-8 -*-
"""
SUITE DE PRUEBAS UNITARIAS: BATERÍA DE CONTROL DE CALIDAD PARA CART-HCC
Guanes Health - División de Oncología Computacional e Inmunología de Sistemas

Pruebas de límites biofísicos de frontera con aserciones lógicas estrictas para
validar la consistencia matemática del esqueleto del simulador CAR-T.
"""

import unittest
import sys
import os

# Asegurar que el path incluya /workspace/scratch
sys.path.append("/workspace/scratch")

from simulador_cart_hcc_interaccion import LinfocitoCART, TumorHCC, SimuladorCARTInteraccion

class TestCARTInteraccionBiofisica(unittest.TestCase):
    """
    Conjunto de pruebas lógicas para el simulador simplificado CAR-T y HCC (Capa B).
    """

    def setUp(self):
        self.cart = LinfocitoCART()
        self.tumor = TumorHCC()
        self.sim = SimuladorCARTInteraccion()

    def test_ph_sensibility_limits(self):
        """
        Prueba 1: Sensibilidad al pH y límites de afinidad (Kd) de GPC3.
        Verifica que Kd transicione correctamente entre pH fisiológico y estroma ácido.
        """
        # A pH 7.4 (fisiológico neutro), la afinidad debe ser débil (Kd alto)
        kd_neutro = self.cart.evaluar_kd_gp3(7.40)
        self.assertGreater(kd_neutro, 900.0, "La constante Kd a pH neutro debe ser mayor a 900 nM (afinidad débil)")

        # A pH 6.0 (ácido estromal profundo), la afinidad debe ser fuerte (Kd bajo)
        kd_acido = self.cart.evaluar_kd_gp3(6.00)
        self.assertLess(kd_acido, 20.0, "La constante Kd a pH ácido debe ser menor a 20 nM (afinidad fuerte)")
        self.assertGreater(kd_acido, 0.0, "Kd debe ser estrictamente positivo")

        # El punto de inflexión en pKa (6.2) debe dar un valor intermedio
        kd_pka = self.cart.evaluar_kd_gp3(6.20)
        self.assertAlmostEqual(kd_pka, 500.5, places=1, msg="En el pKa, Kd debe rondar el valor medio (~500.5 nM)")

    def test_nhe1_exhaustion_atp(self):
        """
        Prueba 2: Fallo de la bomba NHE1 por deplesión energética (ATP).
        Verifica que el pH interno decae si no hay suficiente ATP para mantener la homeostasis.
        """
        # Con ATP saludable (e.g., 500), el pH interno debe resistir a pH estromal de 6.20
        self.cart.atp_nivel = 500.0
        ph_in_con_atp = self.cart.regular_ph_intracelular(6.20)
        self.assertGreaterEqual(ph_in_con_atp, 7.10, "El pH intracelular con ATP debe mantenerse homeostático (>= 7.10)")

        # Con ATP depletado (e.g., 50), el transportador NHE1 falla y el pH interno colapsa hacia el ácido
        self.cart.atp_nivel = 50.0
        ph_in_sin_atp = self.cart.regular_ph_intracelular(6.20)
        self.assertLess(ph_in_sin_atp, 6.80, "El pH intracelular sin ATP debe colapsar por debajo de 6.80")
        self.assertGreater(ph_in_sin_atp, 5.0, "El pH intracelular debe permanecer en un límite físicamente viable")

    def test_antigen_escape_veto(self):
        """
        Prueba 3: Veto por escape antigénico o baja densidad de antígenos.
        Verifica que la degranulación lítica cae a 0 si la densidad de GPC3 es menor a 1000 moléculas/célula.
        """
        # Densidad por encima del umbral (e.g., 5000 moléculas/célula) -> Eficiencia válida
        self.tumor.densidad_gpc3 = 5000.0
        eficiencia_alta = self.tumor.evaluar_veto_antigenico()
        self.assertEqual(eficiencia_alta, 0.8, "A 5000 moléculas, la eficiencia lítica debe ser de 0.8 (80%)")

        # Densidad en el límite estricto del umbral (1000 moléculas/célula) -> Lisis nula (Veto activo)
        self.tumor.densidad_gpc3 = 1000.0
        eficiencia_umbral = self.tumor.evaluar_veto_antigenico()
        self.assertEqual(eficiencia_umbral, 0.0, "En el umbral exacto de 1000, la eficiencia lítica debe ser 0.0")

        # Densidad por debajo de 1000 moléculas/célula -> Lisis vetada por completo
        self.tumor.densidad_gpc3 = 500.0
        eficiencia_vetada = self.tumor.evaluar_veto_antigenico()
        self.assertEqual(eficiencia_vetada, 0.0, "Por debajo de 1000 moléculas, la eficiencia lítica debe ser estrictamente 0.0")

    def test_icasp9_fuse_trigger(self):
        """
        Prueba 4: Fusible de seguridad iCasp9 inducido por rimiducid.
        Verifica que una dosis saturante de rimiducid reduce la población celular de CAR-T en más de un 95% en 4 horas.
        """
        poblacion_inicial = self.cart.count
        rimiducid_nM = 50.0 # Concentración saturante (Km = 10.0 nM)
        
        # Simular 4 horas con pasos de delta_t = 0.1h
        horas = 4.0
        pasos = int(horas / 0.1)
        for _ in range(pasos):
            self.cart.simular_apoptosis_icasp9(rimiducid_nM, delta_t=0.1)
            
        poblacion_final = self.cart.count
        fraccion_supervivencia = poblacion_final / poblacion_inicial
        
        # Verificar decaimiento drástico (>95% de mortalidad, es decir, <5% supervivencia)
        self.assertLess(fraccion_supervivencia, 0.05, "El fusible iCasp9 debe eliminar a más del 95% de los linfocitos en 4 horas")
        self.assertGreaterEqual(poblacion_final, 0.0, "La población celular no puede ser negativa")

if __name__ == "__main__":
    unittest.main()
