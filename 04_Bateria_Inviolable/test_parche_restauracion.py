import unittest
import sys
import os

MOTOR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico")
)
sys.path.append(MOTOR_DIR)

from placa_sana import CelulaSana
from placa_cancer import CelulaTumoral
from parche_restauracion import ParcheRestauracion


class TestGuanesHealthOncologia(unittest.TestCase):

    def setUp(self):
        self.celula_sana = CelulaSana()
        self.celula_tumoral = CelulaTumoral()
        self.parche = ParcheRestauracion()

    def test_caso_A_homeostasis_sana(self):
        """Célula sana: estado operativo nominal."""
        estado = self.celula_sana.obtener_estado()
        self.assertEqual(estado["pH_extracelular"], 7.35)
        self.assertEqual(estado["ATP"], 100)
        self.assertTrue(estado["apoptosis_habilitada"])

    def test_gated_650_fronteras(self):
        """Política Gated-6.50: piso, anergy gate (~6.65→0) y techo fisiológico."""
        self.assertEqual(ParcheRestauracion.calcular_eficiencia_cd8(6.50), 0.0)
        self.assertEqual(ParcheRestauracion.calcular_eficiencia_cd8(6.20), 0.0)
        # (6.65-6.50)/(7.35-6.50) ≈ 0.176 < 0.20 → truncado
        self.assertEqual(ParcheRestauracion.calcular_eficiencia_cd8(6.65), 0.0)
        self.assertEqual(ParcheRestauracion.calcular_eficiencia_cd8(7.35), 1.0)
        # Por encima del gate: pHe que da ≥20% crudo
        self.assertGreaterEqual(ParcheRestauracion.calcular_eficiencia_cd8(6.67), 0.20)

    def test_caso_B_fallo_monoterapia(self):
        """Anti-PD-1 sola en pHe tumoral 6.20 → CD8 modelado = 0%."""
        self.celula_tumoral.establecer_pH(6.20)
        eficiencia_cd8 = self.parche.simular_inmunoterapia_aislada(self.celula_tumoral)
        self.assertEqual(eficiencia_cd8, 0.0)

    def test_caso_C_sinergia_determinista_total(self):
        """Protocolo combinado: pHe restaurado → CD8 100% en el toy model."""
        resultado = self.parche.aplicar_protocolo_combinado(self.celula_tumoral)

        self.assertEqual(resultado["pH_final"], 7.35)
        self.assertEqual(resultado["eficiencia_CD8"], 100.0)
        self.assertEqual(resultado["ATP_tumoral_restante"], 30)
        self.assertTrue(resultado["autolisis_acida_activada"])

    def test_caso_D_doctrina_fail_closed(self):
        """Fail-closed ante célula nula."""
        with self.assertRaises(ValueError):
            self.parche.aplicar_protocolo_combinado(None)


if __name__ == "__main__":
    unittest.main()
