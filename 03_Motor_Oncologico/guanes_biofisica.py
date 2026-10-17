"""
Guanes Health — Motor Biofísico Cinético-Estromal y Eje Gut-Liver-Immune
========================================================================
Frente Biofísico:
- Cinética de transporte de protones por NHE1 y gradiente estromal (pHi vs. pHe).
- Inhibición alostérica cuaternaria de PFK-1 por protones y colapso de ATP glucolítico.
- Trampa bioeléctrica del ácido (interacción Vmem con gradiente electroquímico de H+).
- Eje entero-hepático-inmune: Akkermansia muciniphila -> integridad mucosa (phi_gut)
  -> endotoxemia portal (LPS) -> señalización IL-6 -> activación p-STAT3 -> escudo PD-L1.
- Verificación determinista en silicio y firmado criptográfico SHA-256.
"""

from __future__ import annotations
import math
import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import numpy as np


# =====================================================================
# CONSTANTES FISIOLÓGICAS Y CINÉTICAS DEL MICROAMBIENTE
# =====================================================================
PKA_PFK1: float = 6.80             # Constante de disociación alostérica para inhibición de PFK-1
N_HILL_PFK1: float = 4.0           # Coeficiente de Hill de cooperatividad cuaternaria de PFK-1
PKA_NHE1_WT: float = 6.45          # Set-point alostérico intracelular de NHE1 nativo
N_HILL_NHE1: float = 2.8           # Cooperatividad del sensor de protones de NHE1
VMAX_NHE1_MM_MIN: float = 12.5     # Flujo máximo de extrusión de H+ (mM/min)
PHE_ACIDOSIS_ESTROMAL: float = 6.50 # pH extracelular tumoral ácido de referencia
PHI_GUT_UMBRAL_RESCATE: float = 0.899 # Integridad de barrera mínima requerida (89.9%)


@dataclass
class MicroenvironmentState:
    ph_i: float                    # pH intracelular
    ph_e: float                    # pH extracelular estromal
    v_mem_mv: float                # Potencial de membrana (mV)
    j_nhe1_flux: float             # Flujo de protones NHE1 (mM/min)
    pfk1_activity_pct: float       # Actividad residual de PFK-1 (%)
    atp_availability_pct: float    # Nivel de ATP citosólico disponible (%)
    is_acid_trapped: bool          # ¿Está atrapada la célula en la trampa bioeléctrica?
    sha256_signature: str = ""


@dataclass
class GutLiverImmuneState:
    akkermansia_abundance_pct: float  # Abundancia relativa de Akkermansia (0.0% a 5.0%)
    teer_resistance: float            # Resistencia eléctrica transepitelial (Ohm * cm^2)
    phi_gut_barrier: float            # Coeficiente de integridad mucosa [0.0 a 1.0]
    portal_lps_ng_ml: float           # Endotoxina portal translocada (ng/mL)
    il6_systemic_pg_ml: float         # Concentración de IL-6 sistémica (pg/mL)
    p_stat3_activation_pct: float     # Nivel de fosforilación de STAT3 (%)
    pdl1_tumor_shield_factor: float   # Factor de expresión de PD-L1 tumoral
    tox_exhaustion_index: float       # Índice de agotamiento de linfocitos T (0.0 a 1.0)
    sha256_signature: str = ""


class BiophysicalMicroenvironmentEngine:
    """
    Simulador determinista de la cinética de protones, el microambiente ácido y el eje
    entero-hepático-inmune.
    """

    def __init__(self):
        pass

    def compute_pfk1_inhibition(self, ph_i: float) -> float:
        """
        Calcula la actividad enzimática relativa de PFK-1 (%) en función del pH intracelular:
        v_PFK / V_max = 1 / (1 + 10^(n_Hill * (pKa - pHi))) * 100%
        """
        exponent = N_HILL_PFK1 * (PKA_PFK1 - ph_i)
        exponent = max(-30.0, min(30.0, exponent))
        activity = 1.0 / (1.0 + (10.0 ** exponent))
        return activity * 100.0

    def compute_nhe1_proton_flux(
        self,
        ph_i: float,
        ph_e: float,
        v_mem_mv: float = -20.0,
        v_max: float = VMAX_NHE1_MM_MIN,
        pka: float = PKA_NHE1_WT,
        n_hill: float = N_HILL_NHE1
    ) -> float:
        """
        Calcula el flujo de extrusión de protones por NHE1 (mM/min):
        J_NHE1 = V_max * f_allosteric(pHi) * f_backpressure(pHe) * f_voltage(Vmem)
        """
        # Sensor alostérico intracelular (se activa si pHi < pKa)
        exp_allo = n_hill * (ph_i - pka)
        exp_allo = max(-20.0, min(20.0, exp_allo))
        f_allo = 1.0 / (1.0 + (10.0 ** exp_allo))

        # Contrapresión extracelular por acidosis estromal (frena la bomba si pHe es muy ácido)
        exp_back = 5.991 - ph_e
        exp_back = max(-20.0, min(20.0, exp_back))
        f_back = 1.0 / (1.0 + (10.0 ** exp_back))

        # Dependencia de voltaje (la despolarización facilita levemente la salida catiónica)
        # Factor normalizado centrado en -70 mV
        f_volt = 1.0 + 0.15 * ((v_mem_mv - (-70.0)) / 50.0)
        f_volt = max(0.5, min(1.5, f_volt))

        return float(v_max * f_allo * f_back * f_volt)

    def evaluate_bioelectric_acid_trap(
        self,
        ph_i: float,
        ph_e: float,
        v_mem_mv: float
    ) -> MicroenvironmentState:
        """
        Evalúa la Trampa Bioeléctrica del Ácido (Levin & Guanes Health):
        Si la célula se hiperpolariza (Vmem <= -60 mV) en un estroma muy ácido (pHe <= 6.50),
        la fuerza electromotriz protón-motriz empuja H+ hacia el interior, acidificando el
        citosol (pHi < 6.80), apagando PFK-1 y colapsando el ATP alostéricamente.
        """
        j_nhe1 = self.compute_nhe1_proton_flux(ph_i, ph_e, v_mem_mv)
        pfk_pct = self.compute_pfk1_inhibition(ph_i)

        # Si Vmem es muy negativo y pHe ácido, se produce influjo forzado
        is_trapped = (v_mem_mv <= -60.0) and (ph_e <= 6.50) and (ph_i <= PKA_PFK1)

        # En la trampa del ácido, el ATP colapsa severamente (< 10% del basal)
        if is_trapped:
            atp_pct = max(1.0, pfk_pct * 0.15)
        else:
            atp_pct = pfk_pct

        signature_payload = f"MICROENV:{ph_i:.3f}:{ph_e:.3f}:{v_mem_mv:.1f}:{j_nhe1:.3f}:{atp_pct:.2f}:{is_trapped}"
        sha_sig = hashlib.sha256(signature_payload.encode("utf-8")).hexdigest()

        return MicroenvironmentState(
            ph_i=ph_i,
            ph_e=ph_e,
            v_mem_mv=v_mem_mv,
            j_nhe1_flux=j_nhe1,
            pfk1_activity_pct=pfk_pct,
            atp_availability_pct=atp_pct,
            is_acid_trapped=is_trapped,
            sha256_signature=sha_sig
        )

    def simulate_gut_liver_immune_axis(
        self,
        akkermansia_pct: float = 3.0,
        teer: float = 1200.0,
        t_minutes: float = 60.0
    ) -> GutLiverImmuneState:
        """
        Modela el Eje Entero-Hepático-Inmune:
        1. phi_gut: integridad mucosa mediada por Akkermansia muciniphila y TEER.
        2. Fuga de LPS portal ante rotura de barrera (phi_gut < 0.899).
        3. IL-6 sistémica inducida por translocación de endotoxina.
        4. Activación p-STAT3 y expresión del escudo tumoral PD-L1.
        5. Agotamiento epigenético de linfocitos T infiltrantes (Factor TOX).
        """
        # Normalización de Akkermansia (rango fisiológico eubiótico: 1.0% a 5.0%)
        # Coeficiente sigmoidal de barrera intestinal phi_gut
        teer_factor = min(1.0, teer / 1000.0)
        akk_factor = 1.0 / (1.0 + math.exp(-2.0 * (akkermansia_pct - 1.5)))
        phi_gut = float(min(1.0, max(0.0, 0.3 * teer_factor + 0.7 * akk_factor)))

        # Translocación de LPS portal (ng/mL): se dispara si phi_gut decae
        lps_basal = 0.05
        lps_leak = 15.0 * (1.0 - phi_gut) ** 2
        portal_lps = float(lps_basal + lps_leak)

        # IL-6 sistémica (pg/mL)
        il6_physio = 5.0
        k_lps_il6 = 795.0
        il6_systemic = float(il6_physio + k_lps_il6 * (portal_lps / (portal_lps + 2.0)))

        # Fosforilación p-STAT3 (%)
        k_il6_tumor = 300.0
        p_stat3_pct = float(min(100.0, (il6_systemic / (il6_systemic + k_il6_tumor)) * 100.0))

        # Escudo tumoral PD-L1 (factor de sobreexpresión relativo a basal = 1.0)
        alpha_il6_pdl1 = 15.0
        pdl1_factor = float(1.0 + alpha_il6_pdl1 * (p_stat3_pct / 100.0))

        # Agotamiento de linfocitos T (Índice TOX) inducido por tiempo y sobreexpresión de PD-L1
        tox_induction_rate = 0.005
        tox_index = float(1.0 - math.exp(-tox_induction_rate * (pdl1_factor * (t_minutes / 30.0))))
        tox_index = max(0.0, min(1.0, tox_index))

        signature_payload = f"GUT_LIVER:{akkermansia_pct:.2f}:{phi_gut:.4f}:{portal_lps:.3f}:{il6_systemic:.1f}:{pdl1_factor:.2f}"
        sha_sig = hashlib.sha256(signature_payload.encode("utf-8")).hexdigest()

        return GutLiverImmuneState(
            akkermansia_abundance_pct=akkermansia_pct,
            teer_resistance=teer,
            phi_gut_barrier=phi_gut,
            portal_lps_ng_ml=portal_lps,
            il6_systemic_pg_ml=il6_systemic,
            p_stat3_activation_pct=p_stat3_pct,
            pdl1_tumor_shield_factor=pdl1_factor,
            tox_exhaustion_index=tox_index,
            sha256_signature=sha_sig
        )
