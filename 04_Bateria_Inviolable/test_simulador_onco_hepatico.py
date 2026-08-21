import unittest
import sys
import os

MOTOR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico")
)
sys.path.insert(0, MOTOR_DIR)

from simulador_onco_hepatico_v1 import SimuladorOncoHepatico, paridad_tumor_vs_v4


class TestSimuladorOncoHepaticoV1(unittest.TestCase):
    """Acoplamiento estroma Cohorte C → hepatocito HBV (Capa B)."""

    def test_paridad_tumor_con_v4(self):
        """Dinámica tumoral del acoplamiento = SimuladorTratamiento (sin feedback)."""
        for kwargs in (
            {"mutacion_mct2": False, "inhibicion_mct2": False},
            {"mutacion_mct2": True, "inhibicion_mct2": False},
            {"mutacion_mct2": True, "inhibicion_mct2": True},
        ):
            base, acoplado = paridad_tumor_vs_v4(**kwargs)
            for key in ("viabilidad", "pHi", "pHe", "atp", "eficiencia_cd8", "mct2"):
                self.assertAlmostEqual(
                    base[key][-1],
                    acoplado[key][-1],
                    places=6,
                    msg=f"Paridad fallida en {key} con {kwargs}",
                )

    def test_escape_mct2_veto_cd8_sobre_hepatocito(self):
        """Acidosis residual (pHe~6.65): FC-BIO-2.1 anula lisis; carga viral alta."""
        res = SimuladorOncoHepatico().ejecutar_acoplamiento(
            cohorte="C", mutacion_mct2=True, inoculo_HBV=2.0
        )
        self.assertAlmostEqual(res["pHe"][-1], 6.65, places=2)
        self.assertEqual(res["viabilidad_hepatocito"][-1], 1.0)
        self.assertEqual(sum(res["lisis_cd8_hepatocito"]), 0.0)
        self.assertGreater(res["carga_viral"][-1], 100.0)

    def test_cohorte_c_std_cd8_aclara_hepatocito_infectado(self):
        """pHe normalizado + anti-PD-1: lisis CD8 colapsa viabilidad del hepatocito."""
        res = SimuladorOncoHepatico().ejecutar_acoplamiento(
            cohorte="C", mutacion_mct2=False, inoculo_HBV=2.0
        )
        self.assertAlmostEqual(res["pHe"][-1], 7.35, places=2)
        self.assertEqual(res["viabilidad_hepatocito"][-1], 0.0)
        self.assertGreater(sum(res["lisis_cd8_hepatocito"]), 1.0)
        # Carga menor que en escape porque la célula muere y deja de acumular
        self.assertLess(res["carga_viral"][-1], 80.0)

    def test_myrcludex_reduce_carga_frente_a_control(self):
        """Myrcludex 10 nM reduce entrada viral bajo el mismo estroma Cohorte C."""
        sim = SimuladorOncoHepatico()
        control = sim.ejecutar_acoplamiento(
            cohorte="C", mutacion_mct2=False, inoculo_HBV=2.0, myrcludex_b_nM=0.0
        )
        myr = sim.ejecutar_acoplamiento(
            cohorte="C", mutacion_mct2=False, inoculo_HBV=2.0, myrcludex_b_nM=10.0
        )
        self.assertLess(myr["carga_viral"][-1], 10.0)
        self.assertLess(myr["carga_viral"][-1], control["carga_viral"][-1] * 0.2)


if __name__ == "__main__":
    unittest.main()
