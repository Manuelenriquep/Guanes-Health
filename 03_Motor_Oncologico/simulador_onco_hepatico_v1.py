# -*- coding: utf-8 -*-
"""
GUANES HEALTH - Acoplamiento onco-hepatico v1.0 (Capa B)

Une el microambiente de SimuladorTratamiento (v4 / Cohorte C) con el nodo
HepatocitoInmuneIntegrado (NTCP / HBV / Myrcludex / CD8).

Acoplamiento unidireccional estroma → hepatocito:
  - tumor.pHe → hep.pHe (veto FC-BIO-2.1)
  - escape MCT2 → zonacion pericentral (o2_pp=30)
  - anti-PD-1 segun cronograma de cohorte → lisis CD8 del hepatocito infectado

Sin feedback hepatocito→tumor (Capa C / UNRESOLVED).
Instrumento in silico — no evidencia clinica.
"""

import math

import numpy as np

from simulador_hepatocito_infeccion import HepatocitoInmuneIntegrado
from simulador_onco_homeostasis_v4 import CelulaHumana, SimuladorTratamiento


class SimuladorOncoHepatico:
    """
    Dinamica tumoral identica a SimuladorTratamiento + paso de hepatocito HBV.
    """

    def __init__(self):
        self.paso_tiempo = 0.1  # horas (mismo grid que v4)
        self.tiempo_total = 72.0
        self.puntos_tiempo = int(self.tiempo_total / self.paso_tiempo)

    def _tiempos_cohorte(self, cohorte):
        t_metabolico = 12.0
        if cohorte == "A":
            t_inmunoterapia = t_metabolico
        elif cohorte == "B":
            t_inmunoterapia = t_metabolico + 6.0
        elif cohorte == "C":
            t_inmunoterapia = t_metabolico + 12.0
        elif cohorte == "D":
            t_inmunoterapia = t_metabolico + 24.0
        else:
            raise ValueError(f"Cohorte desconocida: {cohorte}")
        return t_metabolico, t_inmunoterapia

    def ejecutar_acoplamiento(
        self,
        cohorte="C",
        mutacion_mct2=False,
        inhibicion_mct2=False,
        inoculo_HBV=2.0,
        myrcludex_b_nM=0.0,
        il6_pg_ml=0.0,
        variante_S267F=False,
    ):
        """
        Corre 72 h: tumor (logica v4) + hepatocito infectable en el mismo estroma.
        """
        tiempo = np.linspace(0, self.tiempo_total, self.puntos_tiempo)
        t_metabolico, t_inmunoterapia = self._tiempos_cohorte(cohorte)

        tumor = CelulaHumana(tipo_celular="Tumor", atp_nivel=10000.0, telomeros=3920)
        tumor.Bcl2_expresion = 25.0
        tumor.pHe = 6.20
        tumor.PD_L1_expresion = 50.0
        tumor.mutacion_mct2_activa = mutacion_mct2

        # Hipoxia peri-tumoral bajo escape MCT2 → Zona 3 (Capa B)
        o2_pp = 30.0 if mutacion_mct2 and not inhibicion_mct2 else 60.0
        hep = HepatocitoInmuneIntegrado(gsh_nominal=8.0, o2_pp=o2_pp)
        hep.il6_concentracion = il6_pg_ml
        hep.myrcludex_b_nM = myrcludex_b_nM
        hep.es_variante_S267F = variante_S267F

        pHi_history = []
        pHe_history = []
        atp_history = []
        viabilidad_tumor_history = []
        eficiencia_cd8_history = []
        mct2_history = []

        ntcp_history = []
        carga_viral_history = []
        gsh_history = []
        viabilidad_hep_history = []
        lisis_cd8_hep_history = []

        for t in tiempo:
            # --- Bloque tumoral (paridad con SimuladorTratamiento v4) ---
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

                if tumor.pHe > 7.0:
                    eficiencia_cd8_basal = (tumor.pHe - 7.0) / (7.35 - 7.0)
                else:
                    eficiencia_cd8_basal = 0.0
                eficiencia_cd8 = min(1.0, eficiencia_cd8_basal)

            if t >= t_inmunoterapia:
                efectividad_PD1 = (
                    1.0 if tumor.pHe >= 7.30 else (tumor.pHe - 6.0) / (7.35 - 6.0)
                )
                efectividad_PD1 = max(0.0, efectividad_PD1)
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

            actual_efficiency = eficiencia_cd8 * (
                1.0 if t >= t_inmunoterapia and tumor.pHe >= 7.30 else 0.1
            )

            # --- Acoplamiento estroma → hepatocito ---
            hep.pHe = tumor.pHe
            hep.lactato_extracelular = 1.5 + max(0.0, (7.40 - tumor.pHe) * 8.0)

            res_hep = hep.evaluar_regulacion_y_entrada_viral(
                inoculo_HBV=inoculo_HBV, delta_t=self.paso_tiempo
            )

            anti_pd_1 = t >= t_inmunoterapia
            cd8_presente = eficiencia_cd8 > 0.05
            fuerza_lisis = 0.0
            if not isinstance(res_hep, str) and hep.viabilidad > 0.0:
                # Lisis escalada por eficiencia TIL del estroma (sin doble conteo)
                viab_antes = hep.viabilidad
                fuerza_bruta = hep.evaluar_lisis_por_cd8(
                    cd8_presente=cd8_presente, anti_pd_1=anti_pd_1
                )
                hep.viabilidad = viab_antes
                fuerza_lisis = fuerza_bruta * eficiencia_cd8
                hep.viabilidad = max(0.0, hep.viabilidad - fuerza_lisis)

            # Historiales tumor
            pHi_history.append(tumor.pHi)
            pHe_history.append(tumor.pHe)
            atp_history.append(tumor.atp_nivel)
            viabilidad_tumor_history.append(tumor.viabilidad)
            mct2_history.append(tumor.mct2_expresion)
            eficiencia_cd8_history.append(min(1.0, actual_efficiency) * 100.0)

            # Historiales hepatocito
            if isinstance(res_hep, str):
                ntcp_history.append(0.0)
                carga_viral_history.append(
                    carga_viral_history[-1] if carga_viral_history else 0.0
                )
                gsh_history.append(0.0)
                viabilidad_hep_history.append(0.0)
            else:
                ntcp_history.append(res_hep["NTCP_Membrana"])
                carga_viral_history.append(res_hep["Carga_Viral"])
                gsh_history.append(res_hep["GSH_Pool"])
                viabilidad_hep_history.append(hep.viabilidad)
            lisis_cd8_hep_history.append(fuerza_lisis)

        return {
            "tiempo": tiempo,
            "pHi": pHi_history,
            "pHe": pHe_history,
            "atp": atp_history,
            "viabilidad": viabilidad_tumor_history,
            "eficiencia_cd8": eficiencia_cd8_history,
            "mct2": mct2_history,
            "ntcp": ntcp_history,
            "carga_viral": carga_viral_history,
            "gsh": gsh_history,
            "viabilidad_hepatocito": viabilidad_hep_history,
            "lisis_cd8_hepatocito": lisis_cd8_hep_history,
        }


def paridad_tumor_vs_v4(cohorte="C", mutacion_mct2=False, inhibicion_mct2=False):
    """Compara salidas tumorales del acoplamiento con SimuladorTratamiento puro."""
    base = SimuladorTratamiento().ejecutar_simulacion(
        cohorte=cohorte, mutacion_mct2=mutacion_mct2, inhibicion_mct2=inhibicion_mct2
    )
    acoplado = SimuladorOncoHepatico().ejecutar_acoplamiento(
        cohorte=cohorte,
        mutacion_mct2=mutacion_mct2,
        inhibicion_mct2=inhibicion_mct2,
        inoculo_HBV=0.0,
    )
    return base, acoplado


if __name__ == "__main__":
    print("=" * 69)
    print("GUANES HEALTH - ACOPLAMIENTO ONCO-HEPATICO v1.0 (Capa B)")
    print("=" * 69)
    print()

    sim = SimuladorOncoHepatico()

    casos = [
        ("C_STD_HBV", dict(cohorte="C", mutacion_mct2=False, inoculo_HBV=2.0)),
        (
            "C_ESCAPE_HBV",
            dict(cohorte="C", mutacion_mct2=True, inoculo_HBV=2.0),
        ),
        (
            "C_STD_MYR10",
            dict(cohorte="C", mutacion_mct2=False, inoculo_HBV=2.0, myrcludex_b_nM=10.0),
        ),
    ]

    for nombre, kwargs in casos:
        res = sim.ejecutar_acoplamiento(**kwargs)
        print(f"-> [{nombre}] t=72 h (modelo):")
        print(f"   * Tumor viabilidad: {res['viabilidad'][-1] * 100:.2f}%")
        print(f"   * pHe estromal: {res['pHe'][-1]:.2f}")
        print(f"   * Carga viral hep: {res['carga_viral'][-1]:.2f}")
        print(f"   * Viabilidad hep: {res['viabilidad_hepatocito'][-1] * 100:.2f}%")
        print(f"   * Lisis CD8 hep (ultimo paso): {res['lisis_cd8_hepatocito'][-1]:.3f}")
        print("-" * 69)

    print("\n[OK] Acoplamiento de referencia completado (hipotesis in silico).")
