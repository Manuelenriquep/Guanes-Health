# -*- coding: utf-8 -*-
"""
Batería Inviolable — Placa Base Oncológica (5 Capas v6.0)
=========================================================
Valida los 5 niveles biofísicos: Gated-6.50, Eje Gut-Liver, NHE1-Shield,
vetos Fail-Closed FC-BIO-* y restauración homeostática.
"""

import unittest
import sys
import os

# Asegurar path de importación
_HERE = os.path.abspath(os.path.dirname(__file__))
_PARENT = os.path.dirname(_HERE)
for p in [
    os.path.join(_PARENT, "03_Motor_Oncologico"),
    os.path.join(_PARENT, "motor"),
    _HERE
]:
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

from placa_base_oncologica_5_capas import (
    CelulaTumoral5Capas,
    EstadoCelular,
    VetosBiofisicos,
    calcular_citotoxicidad_gated_650,
    evaluar_eje_entero_hepatico
)


class TestPlacaBaseOncologica5Capas(unittest.TestCase):

    def test_politica_gated_650_anergia_inmune(self):
        """Valida que un CD8+ en pH ácido tumoral (6.20) tenga eficiencia 0.0 (FC-BIO-2.1)."""
        eficiencia_acida = calcular_citotoxicidad_gated_650(pHe=6.20, nhe1_shield=False)
        self.assertEqual(eficiencia_acida, 0.0)

        # En pH fisiológico (7.35) debe alcanzar 1.0
        eficiencia_fisiologica = calcular_citotoxicidad_gated_650(pHe=7.35, nhe1_shield=False)
        self.assertEqual(eficiencia_fisiologica, 1.0)

        # En pH 6.60 la fracción es (6.60-6.50)/0.85 = 0.1176 < 0.20 -> Anergy Gate cae a 0.0
        eficiencia_subumbral = calcular_citotoxicidad_gated_650(pHe=6.60, nhe1_shield=False)
        self.assertEqual(eficiencia_subumbral, 0.0)

    def test_blindaje_nhe1_shield_en_microambiente_acido(self):
        """Valida que el CAR-T acorazado con NHE1-Shield sostenga lisis activa a pH 6.20."""
        eficiencia_shield = calcular_citotoxicidad_gated_650(pHe=6.20, nhe1_shield=True)
        self.assertGreater(eficiencia_shield, 0.90)

    def test_veto_fail_closed_ph_corrupto_o_imposible(self):
        """FC-BIO-02 y FC-BIO-03: Abortar si el pH es None o fuera de rango físico."""
        with self.assertRaises(ValueError):
            VetosBiofisicos.validar_ph(None)
        with self.assertRaises(ValueError):
            VetosBiofisicos.validar_ph(-2.0)
        with self.assertRaises(ValueError):
            VetosBiofisicos.validar_ph(15.5)

    def test_veto_fail_closed_phi_gut_fuera_de_rango(self):
        """FC-BIO-GUT: Abortar si phi_gut no está en [0, 1]."""
        with self.assertRaises(ValueError):
            evaluar_eje_entero_hepatico(1.5)
        with self.assertRaises(ValueError):
            evaluar_eje_entero_hepatico(-0.1)

    def test_acoplamiento_eje_gut_liver_akkermansia(self):
        """Valida que Leaky Gut severo (phi=0.0) dispare IL-6 a 800 pg/mL y fatiga epigenética."""
        leaky_gut = evaluar_eje_entero_hepatico(phi_gut=0.0)
        self.assertEqual(leaky_gut["il6_pg_ml"], 800.0)
        self.assertGreater(leaky_gut["agotamiento_epigenetico_pct"], 80.0)

        gut_optimo = evaluar_eje_entero_hepatico(phi_gut=1.0)
        self.assertEqual(gut_optimo["il6_pg_ml"], 5.0)
        self.assertLess(gut_optimo["agotamiento_epigenetico_pct"], 2.0)

    def test_bloqueo_mct4_y_restauracion_homeostatica(self):
        """Valida la auto-acidificación citosólica tras bloqueo de MCT4 y apoptosis por parche."""
        celula = CelulaTumoral5Capas()
        self.assertEqual(celula.estado, EstadoCelular.TUMORAL_WARBURG)

        # Bloqueo de MCT4 en medio ácido provoca colapso ácido citosólico
        celula.bloquear_mct4()
        self.assertEqual(celula.estado, EstadoCelular.COLAPSO_ACIDO)
        self.assertEqual(celula.pH_intracelular, 6.60)

        # Aplicación de Parche Oncolítico activa apoptosis y neutraliza el estroma
        celula.aplicar_parche_restauracion()
        self.assertEqual(celula.estado, EstadoCelular.APOPTOSIS_EN_CURSO)
        self.assertTrue(celula.apoptosis_activa)
        self.assertEqual(celula.pH_extracelular, 7.35)
        self.assertEqual(celula.bcl2_expression, 1.0)


if __name__ == '__main__':
    unittest.main()
