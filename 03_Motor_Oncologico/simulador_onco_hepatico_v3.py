# -*- coding: utf-8 -*-
"""
Acoplamiento onco-hepático bidireccional v3 (Capa B).

Une homeostasis tumoral v5 (Gated-6.50 vía inmuno_utils) con hepatocito
NTCP/HBV. Instrumento in silico — no evidencia clínica.
"""

import math
import os
import sys

import numpy as np

_MOTOR_DIR = os.path.abspath(os.path.dirname(__file__))
if _MOTOR_DIR not in sys.path:
    sys.path.insert(0, _MOTOR_DIR)

from inmuno_utils import calcular_eficiencia_cd8
from simulador_hepatocito_infeccion import HepatocitoInmuneIntegrado as HepatocitoSano
from simulador_onco_homeostasis_v5 import CelulaHumana as CelulaTumor


class SimuladorOncoHepaticoBidireccional:
    """
    Acopla tumor (homeostasis v5) y hepatocito (Capa B).
    Modos: unidireccional (estroma → hepatocito) o feedback
    (hepatocito/IL-6 → PD-L1 tumoral).
    """

    def __init__(self):
        self.paso_tiempo = 0.1  # horas
        self.tiempo_total = 72.0  # horas
        self.puntos_tiempo = int(self.tiempo_total / self.paso_tiempo)

    def ejecutar_simulacion(
        self,
        cohorte="C",
        mutacion_mct2=False,
        inhibicion_mct2=False,
        infeccion_hbv=True,
        inóculo_tasa=10.0,
        myrcludex_nM=0.0,
        feedback_activo=False,
        beta_pd_l1=3.0,
    ):
        tiempo = np.linspace(0, self.tiempo_total, self.puntos_tiempo)

        tumor = CelulaTumor(tipo_celular="Tumor", atp_nivel=10000.0, telomeros=3920)
        tumor.Bcl2_expresion = 25.0
        tumor.pHe = 6.20
        tumor.PD_L1_expresion = 50.0
        tumor.mutacion_mct2_activa = mutacion_mct2

        hepatocito = HepatocitoSano(gsh_nominal=8.0, o2_pp=60.0)
        hepatocito.myrcludex_b_nM = myrcludex_nM

        pHi_history = []
        pHe_history = []
        atp_history = []
        viabilidad_tumor_history = []
        eficiencia_cd8_history = []
        mct2_history = []
        viral_load_history = []
        gsh_history = []
        viabilidad_hep_history = []
        il6_history = []
        pd_l1_tumor_history = []

        t_metabolico = 12.0
        t_inmunoterapia = t_metabolico
        if cohorte == "A":
            t_inmunoterapia = t_metabolico
        elif cohorte == "B":
            t_inmunoterapia = t_metabolico + 6.0
        elif cohorte == "C":
            t_inmunoterapia = t_metabolico + 12.0
        elif cohorte == "D":
            t_inmunoterapia = t_metabolico + 24.0

        for t in tiempo:
            if t < t_metabolico:
                tumor.pHe = 6.20
                tumor.pHi = 7.20
                tumor.mct2_expresion = 1.0
                eficiencia_cd8 = 0.0
            else:
                if tumor.mutacion_mct2_activa:
                    if inhibicion_mct2:
                        tumor.mct2_expresion = 0.5
                    else:
                        tumor.mct2_expresion = 1.0 + (15.0 - 1.0) * (
                            1 - math.exp(-0.1 * (t - t_metabolico))
                        )
                else:
                    tumor.mct2_expresion = 0.5 if inhibicion_mct2 else 1.0

                pHi_minimo = max(5.50, 5.75 + 0.85 * (1 - 1.0 / tumor.mct2_expresion))
                decay_pHi = (7.20 - pHi_minimo) * (
                    1 - math.exp(-0.4 * (t - t_metabolico))
                )
                tumor.pHi = max(pHi_minimo, 7.20 - decay_pHi)

                pHe_maximo = min(7.35, 7.35 - 0.75 * (1 - 1.0 / tumor.mct2_expresion))
                lavado_pHe = (pHe_maximo - 6.20) * (
                    1 - math.exp(-0.25 * (t - t_metabolico))
                )
                tumor.pHe = min(pHe_maximo, 6.20 + lavado_pHe)

                atp_minimo = max(10.0, 30.0 + 770.0 * (1 - 1.0 / tumor.mct2_expresion))
                atp_drop = (10000.0 - atp_minimo) * (
                    1 - math.exp(-0.35 * (t - t_metabolico))
                )
                tumor.atp_nivel = max(atp_minimo, 10000.0 - atp_drop)

                eficiencia_cd8_basal = calcular_eficiencia_cd8(tumor.pHe)
                if feedback_activo:
                    eficiencia_cd8 = min(
                        1.0,
                        eficiencia_cd8_basal
                        * (1.0 / (1.0 + (hepatocito.il6_concentracion / 10.0))),
                    )
                else:
                    eficiencia_cd8 = eficiencia_cd8_basal

            hepatocito.pHe = tumor.pHe
            inóculo_actual = (
                inóculo_tasa if (infeccion_hbv and hepatocito.viabilidad > 0.0) else 0.0
            )
            hepatocito.evaluar_regulacion_y_entrada_viral(
                inóculo_actual, delta_t=self.paso_tiempo
            )

            cd8_presente = eficiencia_cd8 > 0.1
            anti_pd_1_activo = t >= t_inmunoterapia
            hepatocito.evaluar_lisis_por_cd8(
                cd8_presente=cd8_presente, anti_pd_1=anti_pd_1_activo
            )

            if feedback_activo:
                liberacion_il6 = (
                    2.0 * hepatocito.carga_viral_de_novo
                    + 100.0 * (1.0 - hepatocito.viabilidad)
                )
                hepatocito.il6_concentracion = max(0.0, liberacion_il6)
                tumor.PD_L1_expresion = 50.0 + beta_pd_l1 * hepatocito.il6_concentracion
            else:
                hepatocito.il6_concentracion = 0.0
                tumor.PD_L1_expresion = 50.0

            if t >= t_inmunoterapia:
                if tumor.PD_L1_expresion >= 150.0:
                    efectividad_PD1 = 0.0
                else:
                    efectividad_PD1 = (
                        1.0
                        if tumor.pHe >= 7.30
                        else (tumor.pHe - 6.0) / (7.35 - 6.0)
                    )
                    efectividad_PD1 = max(0.0, efectividad_PD1) * (
                        50.0 / tumor.PD_L1_expresion
                    )

                fuerza_citotoxica = eficiencia_cd8 * efectividad_PD1
                depuracion = (tumor.viabilidad - 0.0) * (
                    1 - math.exp(-0.5 * fuerza_citotoxica * (t - t_inmunoterapia))
                )
                tumor.viabilidad = max(0.0, tumor.viabilidad - depuracion)
            else:
                if tumor.pHi < 5.80:
                    tumor.viabilidad = max(
                        0.2, tumor.viabilidad - 0.01 * (t - t_metabolico)
                    )
                else:
                    tumor.viabilidad = 1.0

            pHi_history.append(tumor.pHi)
            pHe_history.append(tumor.pHe)
            atp_history.append(tumor.atp_nivel)
            viabilidad_tumor_history.append(tumor.viabilidad)
            eficiencia_cd8_history.append(eficiencia_cd8 * 100.0)
            mct2_history.append(tumor.mct2_expresion)
            viral_load_history.append(hepatocito.carga_viral_de_novo)
            gsh_history.append(hepatocito.gsh_pool)
            viabilidad_hep_history.append(hepatocito.viabilidad)
            il6_history.append(hepatocito.il6_concentracion)
            pd_l1_tumor_history.append(tumor.PD_L1_expresion)

        return {
            "tiempo": tiempo,
            "pHi": pHi_history,
            "pHe": pHe_history,
            "atp": atp_history,
            "viabilidad_tumor": viabilidad_tumor_history,
            "eficiencia_cd8": eficiencia_cd8_history,
            "mct2": mct2_history,
            "carga_viral": viral_load_history,
            "gsh": gsh_history,
            "viabilidad_hepatocito": viabilidad_hep_history,
            "il6": il6_history,
            "pd_l1_tumor": pd_l1_tumor_history,
        }


if __name__ == "__main__":
    print("=== Simulador onco-hepatico v3 (Capa B; Gated-6.50) ===\n")
    sim = SimuladorOncoHepaticoBidireccional()
    res = sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=False, feedback_activo=False)
    print(
        f"[sin feedback] pHe={res['pHe'][-1]:.2f}  "
        f"viab_tumor={res['viabilidad_tumor'][-1] * 100:.2f}%  "
        f"viab_hep={res['viabilidad_hepatocito'][-1] * 100:.2f}%"
    )
