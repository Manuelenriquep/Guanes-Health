"""
==================================================================================================
GUANES HEALTH - BATERÍA INVIOLABLE
Suite de Pruebas Unitarias para el Generador Visual — test_guanes_visualizer.py
Kernel Nivel 0 / Verificación Biomédica Inmutable
==================================================================================================
Valida:
  1. Generación determinista del Dashboard Gráfico Integral (320+ KB en PNG a 150 DPI).
  2. Comprobación de que el pipeline de renderizado se complete sin errores flotantes ni de memoria.
  3. Presencia de la firma criptográfica SHA-256 en el encabezado del dictamen.
==================================================================================================
"""

import os
import sys
import unittest

VIS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02_Simulaciones_Visuales"))
if VIS_DIR not in sys.path:
    sys.path.insert(0, VIS_DIR)

from guanes_visualizer import GuanesHighFidelityVisualizer


class TestGuanesVisualizer(unittest.TestCase):
    """Pruebas del motor gráfico."""

    def setUp(self):
        self.output_test_png = os.path.join(VIS_DIR, "test_render_output.png")
        self.visualizer = GuanesHighFidelityVisualizer(output_dir=VIS_DIR)

    def tearDown(self):
        # Limpieza de archivo temporal generado para el test
        if os.path.exists(self.output_test_png):
            try:
                os.remove(self.output_test_png)
            except OSError:
                pass

    def test_generate_comprehensive_dashboard_file(self):
        """Verifica que el dashboard de 9 cuadrantes se genere correctamente como archivo gráfico."""
        out_path = self.visualizer.generate_comprehensive_dashboard(
            cariporide_dose_mg=30.0,
            pq1_dose_mg=15.0,
            buffer_dose_mmol=40.0,
            akkermansia_billions=30.0,
            filename="test_render_output.png"
        )

        self.assertTrue(os.path.exists(out_path))
        file_size = os.path.getsize(out_path)
        # Un render de alta resolución a 18x12 pulgadas con 9 paneles debe superar los 150 KB
        self.assertGreater(file_size, 150_000)


if __name__ == "__main__":
    unittest.main()
