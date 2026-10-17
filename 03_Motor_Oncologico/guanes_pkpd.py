"""
==================================================================================================
GUANES HEALTH - MOTOR ONCOLÓGICO DETERMINISTA
Módulo Farmacocinético y Farmacodinámico (PK/PD) - guanes_pkpd.py
Kernel Nivel 0 / Verificación Biomédica Inmutable
==================================================================================================
Modela la farmacocinética (compartimental de primer orden) y farmacodinámica (Hill Emax / IC50)
de intervenciones terapéuticas dirigidas al microambiente tumoral y regenerativo:
  1. Inhibidores de NHE1 (Cariporida / Zoniporida): Cinética de clearance y reducción de extrusión H+.
  2. Moduladores / Apertura de Conexinas Cx43 (PQ1 / Tonabersat): Recuperación de acoplamiento.
  3. Probiótico Terapéutico Eje Intestinal (Akkermansia muciniphila + Inulina): Cinética luminal.
  4. Amortiguación Alcalinizante Estromal (Tris-Buffer / Bicarbonato): Neutralización de pHe.

Invariantes Fail-Closed:
  - FC-PKPD-01: Dosis o concentraciones negativas o NaN disparan ValueError / Veto inmediato.
  - FC-PKPD-02: Concentración máxima que exceda el margen de seguridad seguro (C_max > MTD) es vetada.
  - Sello Criptográfico SHA-256 de cada estado farmacocinético temporal.
==================================================================================================
"""

from dataclasses import dataclass, field
import hashlib
import json
import math
from typing import Dict, Any, Tuple


# ================================================================================================
# CONSTANTES FARMACOLÓGICAS Y BIOFÍSICAS (LITERATURA VERIFICADA)
# ================================================================================================

# 1. Cariporida (HOE-642) - Inhibidor selectivo de NHE1
CARIPORIDE_MW: float = 371.84         # g/mol
CARIPORIDE_IC50_UM: float = 0.05      # 50 nM afinidad por NHE1
CARIPORIDE_VD_L_KG: float = 1.4       # Volumen aparente de distribución (L/kg)
CARIPORIDE_T_HALF_H: float = 4.5      # Vida media de eliminación en humanos (horas)
CARIPORIDE_KE: float = math.log(2.0) / CARIPORIDE_T_HALF_H # Constante de eliminación (~0.154 h^-1)
CARIPORIDE_MTD_UM: float = 5.0        # Concentración plasmática máxima tolerable (seguridad)

# 2. PQ1 (Phenoxyalkyl-quinolina) - Modulador alostérico / activador de Conexina 43 (Cx43)
PQ1_EC50_UM: float = 0.12            # 120 nM para restauración de acoplamiento Cx43
PQ1_T_HALF_H: float = 6.0            # Vida media estimada (horas)
PQ1_KE: float = math.log(2.0) / PQ1_T_HALF_H
PQ1_E_MAX_GATING: float = 0.90       # Máxima restauración de conductancia uniones gap
PQ1_MTD_UM: float = 10.0

# 3. Akkermansia muciniphila (Biológico Luminal) + Inulina (Prebiótico)
AKKERMANSIA_GROWTH_RATE_MAX: float = 0.28 # Tasa máxima de crecimiento luminal (h^-1)
AKKERMANSIA_DEATH_RATE: float = 0.05      # Tasa de lavado / muerte basal (h^-1)
AKKERMANSIA_CARRYING_CAPACITY: float = 1.0 # Fracción de saturación óptima (1.0 = eubiosis)

# 4. Tris-Buffer / Bicarbonato Oral/IV - Amortiguador de pH extracelular
BUFFER_NEUTRALIZATION_RATE_UMOL: float = 0.45 # Capacidad de neutralización por micromol amortiguador
BUFFER_T_HALF_H: float = 2.0
BUFFER_KE: float = math.log(2.0) / BUFFER_T_HALF_H


@dataclass(frozen=True)
class DrugDose:
    """Especificación de una dosis unitaria de fármaco."""
    drug_id: str
    dose_amount_mg: float
    time_admin_h: float = 0.0

    def __post_init__(self):
        if self.dose_amount_mg < 0:
            raise ValueError(f"FC-PKPD-01: Dosis negativa {self.dose_amount_mg} rechazada.")
        if math.isnan(self.dose_amount_mg) or math.isinf(self.dose_amount_mg):
            raise ValueError("FC-PKPD-01: Dosis no numérica o infinita rechazada.")


@dataclass
class PKPDCompartmentState:
    """Estado temporal de concentraciones de fármacos y efectos biológicos."""
    time_h: float
    cariporide_conc_uM: float = 0.0
    pq1_conc_uM: float = 0.0
    akkermansia_density: float = 0.20 # Fracción inicial (0.0 a 1.0)
    buffer_conc_mM: float = 0.0
    
    # Efectos farmacodinámicos calculados (PD)
    nhe1_inhibition_fraction: float = 0.0 # 0.0 = sin inhibición, 1.0 = bloqueo total
    cx43_activation_boost: float = 0.0     # incremento de permeabilidad de uniones gap
    pHe_alkalization_delta: float = 0.0    # elevación de pH extracelular inducido
    gut_barrier_improvement: float = 0.0   # soporte a la integridad luminal phi_gut
    
    sha256_hash: str = ""

    def compute_sha256(self) -> str:
        payload = {
            "time_h": round(self.time_h, 4),
            "cariporide_conc_uM": round(self.cariporide_conc_uM, 6),
            "pq1_conc_uM": round(self.pq1_conc_uM, 6),
            "akkermansia_density": round(self.akkermansia_density, 6),
            "buffer_conc_mM": round(self.buffer_conc_mM, 6),
            "nhe1_inhibition_fraction": round(self.nhe1_inhibition_fraction, 6),
            "cx43_activation_boost": round(self.cx43_activation_boost, 6),
            "pHe_alkalization_delta": round(self.pHe_alkalization_delta, 6)
        }
        serialized = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


class PKPDSimulator:
    """
    Simulador Farmacocinético y Farmacodinámico Determinista.
    Integra perfiles temporales de fármacos y su traslación mecanicista al microambiente tumoral.
    """

    def __init__(self, patient_weight_kg: float = 70.0):
        if patient_weight_kg <= 0:
            raise ValueError("Peso de paciente inválido para PK/PD.")
        self.patient_weight_kg = patient_weight_kg

    def calculate_cariporide_cmax(self, dose_mg: float, bioavailability: float = 0.85) -> float:
        """
        Calcula la concentración plasmática inicial/máxima (C_max) en microMolar (uM).
        C_max = (Dose * F) / (Vd * Peso) convertido a uM.
        """
        vd_total_liters = CARIPORIDE_VD_L_KG * self.patient_weight_kg
        absorbed_mg = dose_mg * bioavailability
        conc_mg_l = absorbed_mg / vd_total_liters
        # Convertir mg/L a umol/L (uM) = (mg/L / MW_g_mol) * 1000
        conc_uM = (conc_mg_l / CARIPORIDE_MW) * 1000.0
        return conc_uM

    def simulate_regimen(
        self,
        cariporide_dose_mg: float,
        pq1_dose_mg: float,
        buffer_dose_mmol: float,
        akkermansia_cfu_billions: float,
        duration_hours: float = 24.0,
        time_step_h: float = 0.25,
        initial_akkermansia: float = 0.20
    ) -> list[PKPDCompartmentState]:
        """
        Simula la evolución temporal conjunta de la administración terapéutica.
        Retorna la trayectoria de estados con resolución temporal fina.
        """
        if duration_hours <= 0 or time_step_h <= 0:
            raise ValueError("Duración y paso temporal deben ser estrictamente positivos.")

        # Invariante FC-PKPD-01
        for val, name in [
            (cariporide_dose_mg, "cariporide_dose_mg"),
            (pq1_dose_mg, "pq1_dose_mg"),
            (buffer_dose_mmol, "buffer_dose_mmol"),
            (akkermansia_cfu_billions, "akkermansia_cfu_billions")
        ]:
            if val < 0 or math.isnan(val) or math.isinf(val):
                raise ValueError(f"FC-PKPD-01: Dosis no física en {name}: {val}")

        # Infección inicial de concentración (asumiendo absorción rápida de bolus oral/infusión)
        init_cariporide_uM = self.calculate_cariporide_cmax(cariporide_dose_mg)
        # Comprobar margen de seguridad MTD (Fail-Closed)
        if init_cariporide_uM > CARIPORIDE_MTD_UM:
            raise ValueError(
                f"FC-PKPD-02: Concentración estimada de Cariporida ({init_cariporide_uM:.2f} uM) "
                f"supera el límite de toxicidad MTD ({CARIPORIDE_MTD_UM} uM)."
            )

        # PQ1 farmacocinética aproximada
        init_pq1_uM = (pq1_dose_mg * 0.90) / (2.0 * self.patient_weight_kg * 0.350)
        if init_pq1_uM > PQ1_MTD_UM:
            raise ValueError(
                f"FC-PKPD-02: Concentración estimada de PQ1 ({init_pq1_uM:.2f} uM) "
                f"supera el límite de toxicidad MTD ({PQ1_MTD_UM} uM)."
            )

        # Buffer en compartimento extracelular (~14 Litros en 70 kg)
        ecf_liters = 0.20 * self.patient_weight_kg
        init_buffer_mM = buffer_dose_mmol / ecf_liters

        current_time = 0.0
        curr_cariporide = init_cariporide_uM
        curr_pq1 = init_pq1_uM
        curr_buffer = init_buffer_mM
        
        # El inóculo de Akkermansia aporta un salto inicial de biomasa luminal
        curr_akkermansia = min(
            AKKERMANSIA_CARRYING_CAPACITY,
            initial_akkermansia + (akkermansia_cfu_billions / 100.0) * 0.50
        )

        trajectory: list[PKPDCompartmentState] = []

        while current_time <= duration_hours + 1e-6:
            # 1. Farmacodinamia (PD): Efecto Hill Emax sobre NHE1 (inhibición)
            # E = C^n / (IC50^n + C^n) con n=1.0
            if curr_cariporide > 0:
                nhe1_inhibition = curr_cariporide / (CARIPORIDE_IC50_UM + curr_cariporide)
            else:
                nhe1_inhibition = 0.0

            # 2. Farmacodinamia de PQ1: Restauración de Cx43
            if curr_pq1 > 0:
                cx43_boost = PQ1_E_MAX_GATING * (curr_pq1 / (PQ1_EC50_UM + curr_pq1))
            else:
                cx43_boost = 0.0

            # 3. Efecto amortiguador sobre pHe (alcalinización estromal máxima de ~0.40 unidades)
            pHe_delta = min(0.45, curr_buffer * 0.08)

            # 4. Efecto de Akkermansia sobre la barrera intestinal
            gut_boost = curr_akkermansia * 0.15

            state = PKPDCompartmentState(
                time_h=current_time,
                cariporide_conc_uM=curr_cariporide,
                pq1_conc_uM=curr_pq1,
                akkermansia_density=curr_akkermansia,
                buffer_conc_mM=curr_buffer,
                nhe1_inhibition_fraction=nhe1_inhibition,
                cx43_activation_boost=cx43_boost,
                pHe_alkalization_delta=pHe_delta,
                gut_barrier_improvement=gut_boost
            )
            state.sha256_hash = state.compute_sha256()
            trajectory.append(state)

            # Integración de clearance farmacocinético (Euler de 1er orden sobre decaimiento exponencial)
            decay_cariporide = curr_cariporide * math.exp(-CARIPORIDE_KE * time_step_h)
            decay_pq1 = curr_pq1 * math.exp(-PQ1_KE * time_step_h)
            decay_buffer = curr_buffer * math.exp(-BUFFER_KE * time_step_h)

            # Dinámica de colonización logística para Akkermansia:
            # dN/dt = r * N * (1 - N / K) - death_rate * N
            logistic_growth = AKKERMANSIA_GROWTH_RATE_MAX * curr_akkermansia * (
                1.0 - (curr_akkermansia / AKKERMANSIA_CARRYING_CAPACITY)
            )
            washout = AKKERMANSIA_DEATH_RATE * curr_akkermansia
            next_akkermansia = curr_akkermansia + (logistic_growth - washout) * time_step_h
            next_akkermansia = max(0.01, min(AKKERMANSIA_CARRYING_CAPACITY, next_akkermansia))

            curr_cariporide = max(0.0, decay_cariporide)
            curr_pq1 = max(0.0, decay_pq1)
            curr_buffer = max(0.0, decay_buffer)
            curr_akkermansia = next_akkermansia
            current_time += time_step_h

        return trajectory
