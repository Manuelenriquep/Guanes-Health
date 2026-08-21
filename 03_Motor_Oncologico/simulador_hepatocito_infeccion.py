# -*- coding: utf-8 -*-
"""
GUANES HEALTH - Simulador hepatocito / NTCP / HBV / Myrcludex (Capa B)

Toy model multiescala: zonacion por pO2, represion IL-6 de NTCP,
bloqueo competitivo Myrcludex B, carga viral de novo y veto redox GSH.

Instrumento de investigacion in silico — no evidencia clinica ni wet-lab.
Canonica: este archivo. El estudio SSoT apunta aqui; no duplicar logica.
"""

import numpy as np


class HepatocitoInmuneIntegrado:
    """
    Nodo hepatocito del modelo: O2 → NTCP, IL-6, Myrcludex B, HBV, MHC-I, GSH.
    """

    def __init__(self, gsh_nominal=8.0, o2_pp=60.0):
        self.ph_intracelular = 7.20
        self.potencial_membrana = -35.0  # mV (cotransporte Na+/taurocolato, modelo)
        self.gsh_pool = gsh_nominal  # mM
        self.gsh_nominal = gsh_nominal
        self.o2_presion_parcial = o2_pp  # mmHg

        self.ntcp_densidad_basal = 1.0
        self.ntcp_densidad_membrana = 1.0
        self.es_variante_S267F = False

        self.carga_viral_de_novo = 0.0
        self.mhc_i_presentacion = 1.0
        self.viabilidad = 1.0

        self.il6_concentracion = 0.0  # pg/mL
        self.lactato_extracelular = 1.5  # mM
        self.pHe = 7.40

        self.myrcludex_b_nM = 0.0

        self._aplicar_norma_zonacion()

    def _aplicar_norma_zonacion(self):
        """Jerarquia de zonacion por pO2 (parametros Capa B del estudio v3)."""
        if self.o2_presion_parcial < 20.0:
            self.ntcp_densidad_basal = 0.2
        elif self.o2_presion_parcial <= 35.0:
            self.ntcp_densidad_basal = 0.8
        else:
            self.ntcp_densidad_basal = 1.2
        self.ntcp_densidad_membrana = self.ntcp_densidad_basal

    def evaluar_regulacion_y_entrada_viral(self, inoculo_HBV, delta_t=1.0):
        """Cinetica NTCP + entrada HBV + riesgo colestasico (un paso)."""
        if self.viabilidad <= 0.0:
            return "NODE_INACTIVE: Apoptosis o Necrosis disparada"

        # 1. Represion IL-6 (Hill; techo 98% en el modelo)
        represion_il6 = 1.0
        if self.il6_concentracion > 0:
            represion_il6 = 1.0 - 0.98 * (
                self.il6_concentracion / (self.il6_concentracion + 50.0)
            )

        self.ntcp_densidad_membrana = self.ntcp_densidad_basal * represion_il6

        if self.es_variante_S267F:
            self.ntcp_densidad_membrana = 0.0

        # 2. Competencia Myrcludex: Ki viral 1 nM; Ki biliar 100 nM (modelo)
        fraccion_bloqueo_viral = 1.0 / (1.0 + (self.myrcludex_b_nM / 1.0))
        fraccion_bloqueo_biliar = 1.0 / (1.0 + (self.myrcludex_b_nM / 100.0))

        tasa_entrada = inoculo_HBV * self.ntcp_densidad_membrana * fraccion_bloqueo_viral
        self.carga_viral_de_novo += tasa_entrada * delta_t

        self.mhc_i_presentacion = min(10.0, 1.0 + (self.carga_viral_de_novo * 1.5))

        # 3. Aclaramiento biliar bajo umbral → deplecion GSH (riesgo del modelo)
        aclaramiento_sales_biliares = (
            self.ntcp_densidad_membrana * fraccion_bloqueo_biliar
        )
        if aclaramiento_sales_biliares < 0.15 and not self.es_variante_S267F:
            self.gsh_pool = max(0.0, self.gsh_pool - 0.5 * delta_t)

        # VETO FC-BIO-HEP-01: GSH < 30% nominal → viabilidad 0 (fail-closed modelo)
        if (self.gsh_pool / self.gsh_nominal) < 0.30:
            self.viabilidad = 0.0

        return {
            "NTCP_Membrana": self.ntcp_densidad_membrana,
            "Carga_Viral": self.carga_viral_de_novo,
            "MHC_I": self.mhc_i_presentacion,
            "GSH_Pool": self.gsh_pool,
            "Viabilidad_Hepatocito": self.viabilidad,
        }

    def evaluar_lisis_por_cd8(self, cd8_presente=False, anti_pd_1=False):
        """Lisis CD8 con veto por acidosis (FC-BIO-2.1) y PD-1 (modelo)."""
        if self.viabilidad <= 0.0 or not cd8_presente:
            return 0.0

        if self.pHe <= 6.50:
            return 0.0

        prob_reconocimiento = self.mhc_i_presentacion / 10.0
        pd_l1_expresion = min(1.0, self.carga_viral_de_novo * 0.2)
        pd1_interferencia = 0.0 if anti_pd_1 else pd_l1_expresion

        fuerza_litica = prob_reconocimiento * (1.0 - pd1_interferencia)
        fuerza_litica = max(0.0, min(1.0, fuerza_litica))

        self.viabilidad = max(0.0, self.viabilidad - fuerza_litica)
        return fuerza_litica


class SimuladorHepatitisB:
    """
    Perfiles temporales (72 h) bajo escenarios de control / IL-6 / Myrcludex.
    """

    def __init__(self):
        self.paso_tiempo = 0.5  # horas
        self.tiempo_total = 72.0
        self.puntos_tiempo = int(self.tiempo_total / self.paso_tiempo)

    def simular_escenario(self, escenario_id):
        tiempo = np.linspace(0, self.tiempo_total, self.puntos_tiempo)
        hep = HepatocitoInmuneIntegrado(gsh_nominal=8.0, o2_pp=60.0)
        inoculo_diario = 2.0

        if escenario_id == "Control":
            hep.il6_concentracion = 0.0
            hep.myrcludex_b_nM = 0.0
        elif escenario_id == "Inmunidad_Innata":
            hep.il6_concentracion = 100.0
            hep.myrcludex_b_nM = 0.0
        elif escenario_id == "Myrcludex_Optimo":
            hep.il6_concentracion = 0.0
            hep.myrcludex_b_nM = 10.0
        elif escenario_id == "Myrcludex_Toxico":
            hep.il6_concentracion = 0.0
            hep.myrcludex_b_nM = 1000.0
        else:
            raise ValueError(f"Escenario desconocido: {escenario_id}")

        ntcp_history = []
        carga_viral_history = []
        gsh_history = []
        viabilidad_history = []

        for _t in tiempo:
            res = hep.evaluar_regulacion_y_entrada_viral(
                inoculo_HBV=inoculo_diario, delta_t=self.paso_tiempo
            )

            if isinstance(res, str):
                ntcp_history.append(0.0)
                carga_viral_history.append(
                    carga_viral_history[-1] if carga_viral_history else 0.0
                )
                gsh_history.append(0.0)
                viabilidad_history.append(0.0)
            else:
                ntcp_history.append(res["NTCP_Membrana"])
                carga_viral_history.append(res["Carga_Viral"])
                gsh_history.append(res["GSH_Pool"])
                viabilidad_history.append(res["Viabilidad_Hepatocito"])

        return {
            "tiempo": tiempo,
            "ntcp": ntcp_history,
            "carga_viral": carga_viral_history,
            "gsh": gsh_history,
            "viabilidad": viabilidad_history,
        }


if __name__ == "__main__":
    print("=" * 69)
    print("GUANES HEALTH - SIMULADOR HEPATOCITO / HBV (Capa B, v1.1)")
    print("=" * 69)
    print()

    sim = SimuladorHepatitisB()
    escenarios = [
        "Control",
        "Inmunidad_Innata",
        "Myrcludex_Optimo",
        "Myrcludex_Toxico",
    ]

    for esc in escenarios:
        res = sim.simular_escenario(esc)
        print(f"-> [ESCENARIO: {esc.upper()}] t = 72.0 h (modelo):")
        print(f"   * NTCP membrana: {res['ntcp'][-1]:.4f}")
        print(f"   * Carga viral: {res['carga_viral'][-1]:.2f}")
        print(f"   * GSH: {res['gsh'][-1]:.2f} mM (basal modelo: 8.00)")
        print(f"   * Viabilidad: {res['viabilidad'][-1] * 100:.2f}%")

        if res["viabilidad"][-1] == 0.0:
            print("   [MODELO]: VETO FC-BIO-HEP-01 — apoptosis por colestasis simulada.")
        elif esc == "Myrcludex_Optimo":
            print("   [MODELO]: bloqueo viral con GSH preservado (ventana 10 nM).")
        elif esc == "Inmunidad_Innata":
            print("   [MODELO]: IL-6 reduce entrada viral via represion NTCP.")
        print("-" * 69)

    print("\n[OK] Simulacion de referencia completada (hipotesis in silico).")
