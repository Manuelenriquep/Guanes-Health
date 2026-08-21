import unittest
import sys
import os

MOTOR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico")
)
sys.path.insert(0, MOTOR_DIR)

from simulador_hepatocito_infeccion import HepatocitoInmuneIntegrado, SimuladorHepatitisB


class TestSimuladorHepatocitoInfeccion(unittest.TestCase):
    """Fronteras del toy model hepatocito / NTCP / HBV / Myrcludex (Capa B)."""

    def test_zonacion_hepatica(self):
        """Gradiente de O2 condiciona densidad basal de NTCP (modelo)."""
        hep_isquemia = HepatocitoInmuneIntegrado(o2_pp=15.0)
        self.assertEqual(hep_isquemia.ntcp_densidad_basal, 0.2)

        hep_zona3 = HepatocitoInmuneIntegrado(o2_pp=30.0)
        self.assertEqual(hep_zona3.ntcp_densidad_basal, 0.8)

        hep_zona1 = HepatocitoInmuneIntegrado(o2_pp=60.0)
        self.assertEqual(hep_zona1.ntcp_densidad_basal, 1.2)

    def test_represion_il6(self):
        """IL-6 reprime NTCP de forma dosis-dependiente (Hill, Capa B)."""
        hep = HepatocitoInmuneIntegrado(o2_pp=60.0)
        hep.il6_concentracion = 50.0

        res = hep.evaluar_regulacion_y_entrada_viral(inoculo_HBV=0.0)

        # IL-6=50 → 1 - 0.98*(50/(50+50)) = 0.51; NTCP = 1.2 * 0.51 = 0.612
        self.assertAlmostEqual(res["NTCP_Membrana"], 0.612, places=3)

    def test_myrcludex_b_optimo_vs_toxico(self):
        """Ventana modelo: 10 nM preserva GSH; 1000 nM dispara VETO FC-BIO-HEP-01."""
        sim = SimuladorHepatitisB()

        res_opt = sim.simular_escenario("Myrcludex_Optimo")
        self.assertEqual(res_opt["viabilidad"][-1], 1.0)
        self.assertLess(res_opt["carga_viral"][-1], 20.0)
        self.assertEqual(res_opt["gsh"][-1], 8.0)

        res_tox = sim.simular_escenario("Myrcludex_Toxico")
        self.assertEqual(res_tox["viabilidad"][-1], 0.0)
        self.assertLess(res_tox["gsh"][-1], 2.4)

    def test_veto_escudo_acido_cd8(self):
        """VETO FC-BIO-2.1: pHe <= 6.50 anula lisis CD8 en el modelo."""
        hep = HepatocitoInmuneIntegrado(o2_pp=60.0)
        hep.carga_viral_de_novo = 5.0
        hep.mhc_i_presentacion = 8.0
        hep.pHe = 6.50

        fuerza = hep.evaluar_lisis_por_cd8(cd8_presente=True, anti_pd_1=False)
        self.assertEqual(fuerza, 0.0)
        self.assertEqual(hep.viabilidad, 1.0)

    def test_variante_S267F_refractaria(self):
        """Polimorfismo S267F: NTCP nulo para entrada viral (modelo)."""
        hep = HepatocitoInmuneIntegrado(o2_pp=60.0)
        hep.es_variante_S267F = True
        res = hep.evaluar_regulacion_y_entrada_viral(inoculo_HBV=2.0, delta_t=1.0)
        self.assertEqual(res["NTCP_Membrana"], 0.0)
        self.assertEqual(res["Carga_Viral"], 0.0)


if __name__ == "__main__":
    unittest.main()
