# -*- coding: utf-8 -*-
"""
Toy model Capa B: CAR-T / HCC.
RESOLVED-B-01: sGPC3. RESOLVED-B-02: η_mig (IFP/colágeno; esbozo, no PDE).
Instrumento in silico; no evidencia clínica.
"""

import math

UMBRAL_GPC3 = 1000.0
UMBRAL_ATP_NHE1 = 100.0
PH_IN_MIN = 7.10
KI_SGPC3_NOM = 2.5  # ng/mL — hipótesis Capa B (ledger)
IFP_UMBRAL_MMHG = 15.0
COLAGENO_UMBRAL_UG_MG = 50.0
IFP_ESCALA_MMHG = 10.0
COLAGENO_ESCALA_UG_MG = 25.0
OTR4120_BETA = 1.0  # alivio relativo de penalización por colágeno (Capa B)


class LinfocitoCART:
    def __init__(self, count_inicial=1.0e6, atp_nivel=500.0):
        self.count = count_inicial
        self.atp_nivel = atp_nivel
        self.ph_in = 7.20
        self.kd_neutro = 1200.0
        self.kd_acido = 1.0
        self.pka_histidinas = 6.70
        self.n_hill = 10.0
        self.k_casp = 2.5
        self.km_rimiducid = 10.0

    def evaluar_kd_gpc3(self, ph_e):
        exp = max(-20.0, min(20.0, self.n_hill * (self.pka_histidinas - ph_e)))
        return self.kd_acido + (self.kd_neutro - self.kd_acido) / (1.0 + 10.0 ** exp)

    def regular_ph_intracelular(self, ph_e, alfa_nhe1=0.2):
        if self.atp_nivel >= UMBRAL_ATP_NHE1:
            self.ph_in = 7.20 - 0.15 * max(0.0, 7.20 - ph_e) + alfa_nhe1 * max(0.0, 7.35 - ph_e)
            self.ph_in = max(PH_IN_MIN, min(7.35, self.ph_in))
        else:
            self.ph_in = max(5.0, min(7.20, ph_e + (7.20 - ph_e) * 0.3))
        return self.ph_in

    def simular_apoptosis_icasp9(self, rimiducid_nM, delta_t=0.1):
        if rimiducid_nM <= 0.0 or self.count <= 0.0:
            return self.count
        tasa = self.k_casp * (rimiducid_nM / (rimiducid_nM + self.km_rimiducid))
        self.count = max(0.0, self.count * math.exp(-tasa * delta_t))
        return self.count


class TumorHCC:
    def __init__(self, viabilidad=1.0, densidad_gpc3=5000.0):
        self.viabilidad = viabilidad
        self.densidad_gpc3 = densidad_gpc3

    def evaluar_veto_antigenico(self):
        if self.densidad_gpc3 <= UMBRAL_GPC3:
            return 0.0
        return max(0.0, min(1.0, 1.0 - UMBRAL_GPC3 / self.densidad_gpc3))


def factor_senuelo_sgpc3(sgpc3_ng_ml, ki_sgpc3=KI_SGPC3_NOM):
    """Atenuación competitiva 1/(1 + [sGPC3]/Ki). Capa B."""
    if ki_sgpc3 <= 0.0:
        return 1.0
    return 1.0 / (1.0 + max(0.0, sgpc3_ng_ml) / ki_sgpc3)


def factor_infiltracion_mig(
    ifp_mmhg=10.0,
    colageno_ug_mg=30.0,
    otr4120=0.0,
):
    """
    η_mig ∈ (0, 1]: fracción de encuentro efector–tumor (esbozo Capa B).
    Sin PDE ni heparanasa espacial. OTR4120>0 alivia solo la pena por colágeno.
    """
    pen_ifp = max(0.0, ifp_mmhg - IFP_UMBRAL_MMHG) / IFP_ESCALA_MMHG
    exceso_col = max(0.0, colageno_ug_mg - COLAGENO_UMBRAL_UG_MG)
    alivio = 1.0 + OTR4120_BETA * max(0.0, otr4120)
    pen_col = (exceso_col / COLAGENO_ESCALA_UG_MG) / alivio
    eta = 1.0 / ((1.0 + pen_ifp) * (1.0 + pen_col))
    return max(0.02, min(1.0, eta))


class SimuladorCARTInteraccion:
    def __init__(self, tiempo_total=72.0, paso_tiempo=0.1):
        self.paso_tiempo = paso_tiempo
        self.tiempo_total = tiempo_total
        self.puntos_tiempo = int(tiempo_total / paso_tiempo)

    def simular_intervalo(
        self,
        ph_e=6.20,
        rimiducid_nM=0.0,
        atp_linfocito=500.0,
        densidad_antigeno=5000.0,
        k_lisis=0.005,
        sgpc3_ng_ml=0.0,
        ki_sgpc3=KI_SGPC3_NOM,
        ifp_mmhg=10.0,
        colageno_ug_mg=30.0,
        otr4120=0.0,
        # alias del drop v2
        ph_e_sinusoidal=None,
        sgpc3_ngml=None,
    ):
        if ph_e_sinusoidal is not None:
            ph_e = ph_e_sinusoidal
        if sgpc3_ngml is not None:
            sgpc3_ng_ml = sgpc3_ngml

        cart = LinfocitoCART(atp_nivel=atp_linfocito)
        tumor = TumorHCC(densidad_gpc3=densidad_antigeno)
        eta = factor_infiltracion_mig(ifp_mmhg, colageno_ug_mg, otr4120)
        hist = {
            "tiempo": [],
            "cart_count": [],
            "ph_in": [],
            "kd_gpc3": [],
            "viabilidad_tumor": [],
            "eficiencia_reconocimiento": [],
            "factor_senuelo": [],
            "eta_mig": [],
        }

        t = 0.0
        for _ in range(self.puntos_tiempo):
            kd = cart.evaluar_kd_gpc3(ph_e)
            ph_in = cart.regular_ph_intracelular(ph_e)
            efi = tumor.evaluar_veto_antigenico()
            if ph_in < 6.80:
                efi *= 0.1

            f_sen = factor_senuelo_sgpc3(sgpc3_ng_ml, ki_sgpc3)
            efi *= f_sen * eta

            cart.simular_apoptosis_icasp9(rimiducid_nM, self.paso_tiempo)
            tasa = k_lisis * (cart.count / 1.0e6) * efi * (1.0 / (1.0 + kd / 10.0))
            tumor.viabilidad = max(0.0, tumor.viabilidad * math.exp(-tasa * self.paso_tiempo))

            hist["tiempo"].append(t)
            hist["cart_count"].append(cart.count)
            hist["ph_in"].append(ph_in)
            hist["kd_gpc3"].append(kd)
            hist["viabilidad_tumor"].append(tumor.viabilidad)
            hist["eficiencia_reconocimiento"].append(efi)
            hist["factor_senuelo"].append(f_sen)
            hist["eta_mig"].append(eta)
            t += self.paso_tiempo

        return hist


if __name__ == "__main__":
    sim = SimuladorCARTInteraccion()
    r0 = sim.simular_intervalo(ph_e=6.20, sgpc3_ng_ml=0.0)
    r5 = sim.simular_intervalo(ph_e=6.20, sgpc3_ng_ml=5.0)
    rb = sim.simular_intervalo(ph_e=6.20, ifp_mmhg=35.0, colageno_ug_mg=80.0)
    print(
        f"base viab={r0['viabilidad_tumor'][-1]*100:.2f}%  "
        f"sGPC3=5 viab={r5['viabilidad_tumor'][-1]*100:.2f}%  "
        f"barrera viab={rb['viabilidad_tumor'][-1]*100:.2f}% eta={rb['eta_mig'][-1]:.3f}"
    )
