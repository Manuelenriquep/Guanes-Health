import unittest
import sys
import os

# Asegurar que Python pueda importar el motor local
MOTOR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico")
)
sys.path.append(MOTOR_DIR)

from placa_sana import CelulaSana
from placa_cancer import CelulaTumoral
from parche_restauracion import ParcheRestauracion

class TestGuanesHealthOncologia(unittest.TestCase):

    def setUp(self):
        """Inicializa las instancias base de prueba"""
        self.celula_sana = CelulaSana()
        self.celula_tumoral = CelulaTumoral()
        self.parche = ParcheRestauracion()

    def test_caso_A_homeostasis_sana(self):
        """Verifica que la célula sana mantenga su estado operativo nominal"""
        estado = self.celula_sana.obtener_estado()
        self.assertEqual(estado['pH_extracelular'], 7.35)
        self.assertEqual(estado['ATP'], 100)
        self.assertTrue(estado['apoptosis_habilitada'])

    def test_caso_B_fallo_monoterapia(self):
        """Verifica que la inmunoterapia sola (anti-PD1) falle en pH ácido (6.20)"""
        # Simulamos microambiente hostil sin parche metabólico
        self.celula_tumoral.establecer_pH(6.20)
        eficiencia_cd8 = self.parche.simular_inmunoterapia_aislada(self.celula_tumoral)
        # La acidez paraliza los linfocitos, eficiencia máxima del 10.0%
        self.assertLessEqual(eficiencia_cd8, 10.0)

    def test_caso_C_sinergia_determinista_total(self):
        """Verifica transiciones deterministas del protocolo combinado en el toy model"""
        # MCT4 bloqueado + anti-PD1 (estado modelado; no claim clínico)
        resultado = self.parche.aplicar_protocolo_combinado(self.celula_tumoral)

        self.assertEqual(resultado['pH_final'], 7.35)
        self.assertEqual(resultado['eficiencia_CD8'], 100.0)
        self.assertEqual(resultado['ATP_tumoral_restante'], 30)
        self.assertTrue(resultado['autolisis_acida_activada'])

    def test_caso_D_doctrina_fail_closed(self):
        """Garantiza que el sistema aborte si recibe variables corruptas (Fail-Closed)"""
        with self.assertRaises(ValueError):
            # Intentar pasar un pH físicamente imposible o una variable nula
            self.parche.aplicar_protocolo_combinado(None)

if __name__ == '__main__':
    unittest.main()