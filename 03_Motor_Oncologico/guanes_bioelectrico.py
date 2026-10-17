"""
Guanes Health — Motor Bioeléctrico y Redes Cx43 (Capa Lógica Morfogenética)
============================================================================
Frente Bioeléctrico:
- Ecuación de Goldman-Hodgkin-Katz (GHK) para el potencial de membrana (Vmem).
- Red de acoplamiento por uniones gap (conexinas Cx43 / GJC) en retícula celular.
- Teorema de la Patología Única de Levin & Friston: Detección y reversión de 'Smaller Selves'.
- Cuantificación formal del Cono Cognitivo de Luz (Escala espacial/temporal y coherencia Phi).
- Verificación determinista en silicio con firmado criptográfico SHA-256.
"""

from __future__ import annotations
import math
import hashlib
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

# =====================================================================
# CONSTANTES FÍSICAS UNIVERSALES Y BARRERAS BIOFÍSICAS (FAIL-CLOSED)
# =====================================================================
R_GAS_CONSTANT: float = 8.314462618        # J / (mol * K)
FARADAY_CONSTANT: float = 96485.33212       # C / mol
TEMP_PHYSIOLOGICAL_K: float = 310.15        # 37 °C en Kelvin
RT_OVER_F_MV: float = (R_GAS_CONSTANT * TEMP_PHYSIOLOGICAL_K / FARADAY_CONSTANT) * 1000.0  # ~26.725 mV

# Invariantes biofísicos termodinámicos
VM_MIN_FISICO: float = -100.0   # mV
VM_MAX_FISICO: float = 50.0     # mV
UMBRAL_ONCOGENICO_VM_MV: float = -25.0     # Vmem >= -25 mV indica despolarización oncogénica
UMBRAL_DIFERENCIADO_VM_MV: float = -50.0   # Vmem <= -50 mV fenotipo maduro / quiescente
UMBRAL_RESCATE_LEVIN_MV: float = -70.0     # Hiperpolarización forzada de rescate


class PhenotypeBioelectric(str, Enum):
    DIFFERENTIATED_HEALTHY = "DIFFERENTIATED_HEALTHY"
    DEPOLARIZED_ONCOGENIC = "DEPOLARIZED_ONCOGENIC"
    RESCUED_NORMALIZED = "RESCUED_NORMALIZED"
    ISOLATED_SMALLER_SELF = "ISOLATED_SMALLER_SELF"


@dataclass
class IonConcentrations:
    """Concentraciones fisiológicas en milimolar (mM)."""
    k_in: float = 140.0
    k_out: float = 4.5
    na_in: float = 12.0
    na_out: float = 145.0
    cl_in: float = 10.0
    cl_out: float = 110.0

    def __post_init__(self):
        for name, val in self.__dict__.items():
            if val <= 0.0:
                raise ValueError(f"[FC-BIO-GHK] Concentración iónica no física: {name} = {val} mM (debe ser > 0)")


@dataclass
class CellBioelectricState:
    cell_id: int
    v_mem_mv: float
    gjc_conductance: float       # Conductancia de conexina Cx43 [0.0 a 1.0]
    p_na_relative: float         # Permeabilidad relativa de Na+ frente a K+ (P_Na / P_K)
    p_cl_relative: float         # Permeabilidad relativa de Cl- frente a K+ (P_Cl / P_K)
    phenotype: PhenotypeBioelectric
    is_smaller_self: bool
    cognitive_light_cone_radius: float


class GHKBioelectricEngine:
    """
    Motor determinista para resolver el potencial transmembrana (Vmem)
    mediante la formulación analítica de Goldman-Hodgkin-Katz.
    """

    def __init__(self, ions: Optional[IonConcentrations] = None):
        self.ions = ions or IonConcentrations()

    def compute_ghk_voltage(
        self,
        p_k: float = 1.0,
        p_na: float = 0.04,
        p_cl: float = 0.45
    ) -> float:
        """
        Calcula Vmem analítico en mV según la ecuación GHK:
        V = (RT/F) * ln( (P_K*[K+]e + P_Na*[Na+]e + P_Cl*[Cl-]i) / (P_K*[K+]i + P_Na*[Na+]i + P_Cl*[Cl-]e) )
        """
        num = (p_k * self.ions.k_out) + (p_na * self.ions.na_out) + (p_cl * self.ions.cl_in)
        den = (p_k * self.ions.k_in) + (p_na * self.ions.na_in) + (p_cl * self.ions.cl_out)

        if num <= 0.0 or den <= 0.0:
            raise ValueError("[FC-BIO-GHK] Concentración o permeabilidad iónica no física (<= 0).")

        v_mem = RT_OVER_F_MV * math.log(num / den)

        # Validación Fail-Closed de límites físicos
        if v_mem < VM_MIN_FISICO or v_mem > VM_MAX_FISICO:
            raise ValueError(f"[FC-BIO-06] Potencial GHK fuera de frontera física: {v_mem:.2f} mV")

        return v_mem

    def compute_cx43_gating(
        self,
        v_mem_a: float,
        v_mem_b: float,
        g_min: float = 0.05,
        g_max: float = 1.00,
        v0: float = 25.0,
        a_sens: float = 0.15
    ) -> float:
        """
        Conductancia de conexinas homotípicas Cx43 según la diferencia de potencial transunión:
        G_GJ(Delta_V) = G_min + (G_max - G_min) / (1 + exp(a_sens * (|Delta_V| - V0)))
        """
        delta_v = abs(v_mem_a - v_mem_b)
        exponent = a_sens * (delta_v - v0)
        # Protección numérica contra desbordamiento
        exponent = max(-30.0, min(30.0, exponent))
        return g_min + (g_max - g_min) / (1.0 + math.exp(exponent))


class BioelectricLattice2D:
    """
    Simulador espacial en retícula de tejido celular para estudiar sincronización bioeléctrica,
    propagación de información y emergencia de 'Smaller Selves' oncológicos.
    """

    def __init__(self, rows: int = 10, cols: int = 10, ghk_engine: Optional[GHKBioelectricEngine] = None):
        self.rows = rows
        self.cols = cols
        self.n_cells = rows * cols
        self.ghk = ghk_engine or GHKBioelectricEngine()

        # Matrices de estado celular
        self.v_mem = np.full((rows, cols), -72.0, dtype=np.float64)  # Estado sano inicial
        self.gjc = np.full((rows, cols), 0.90, dtype=np.float64)     # Conexinas abiertas
        self.p_na = np.full((rows, cols), 0.04, dtype=np.float64)    # Permeabilidad basal
        self.c_m = 1.0  # Capacitancia de membrana específica [uF/cm^2]

    def induce_oncogenic_depolarization(self, r: int, c: int, radius: int = 2) -> None:
        """
        Simula una mutación o evento lesivo local que induce hiperexpresión de canales
        de sodio o bloqueo de canales de potasio (aumento de P_Na / P_K) y cierre de uniones gap.
        """
        for i in range(max(0, r - radius), min(self.rows, r + radius + 1)):
            for j in range(max(0, c - radius), min(self.cols, c + radius + 1)):
                dist = math.sqrt((i - r) ** 2 + (j - c) ** 2)
                if dist <= radius:
                    self.p_na[i, j] = 0.70   # Elevada permeabilidad a Na+
                    self.gjc[i, j] = 0.05    # Cierre de Cx43 (desacople celular)
                    self.v_mem[i, j] = self.ghk.compute_ghk_voltage(p_k=0.60, p_na=0.70, p_cl=0.30)

    def apply_levin_normalization(self, force_vmem: float = -75.0, restore_gjc: float = 0.85) -> None:
        """
        Protocolo de Normalización Bioeléctrica de Michael Levin & Chernet:
        Fuerza la hiperpolarización exógena (ej. vía optogenética o canalotropina)
        y reabre las uniones gap Cx43 para reintegrar las células al sincitio del tejido.
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if self.v_mem[i, j] >= UMBRAL_ONCOGENICO_VM_MV or self.gjc[i, j] < 0.20:
                    self.v_mem[i, j] = force_vmem
                    self.gjc[i, j] = restore_gjc
                    self.p_na[i, j] = 0.04

    def step_diffusion(self, dt: float = 0.1, d_coeff: float = 0.25) -> None:
        """
        Integra un paso de acoplamiento electrotónico y difusión por uniones gap:
        dV_i/dt = (1 / C_m) * sum_{j vecinos} [ g_gap_ij * (V_j - V_i) ]
        """
        new_v = np.copy(self.v_mem)
        for i in range(self.rows):
            for j in range(self.cols):
                flux = 0.0
                neighbors = []
                if i > 0: neighbors.append((i - 1, j))
                if i < self.rows - 1: neighbors.append((i + 1, j))
                if j > 0: neighbors.append((i, j - 1))
                if j < self.cols - 1: neighbors.append((i, j + 1))

                for ni, nj in neighbors:
                    # Conductancia media armónica de unión gap entre ambas células
                    g_eff = (self.gjc[i, j] + self.gjc[ni, nj]) / 2.0
                    g_dynamic = self.ghk.compute_cx43_gating(self.v_mem[i, j], self.v_mem[ni, nj])
                    g_total = g_eff * g_dynamic
                    flux += g_total * (self.v_mem[ni, nj] - self.v_mem[i, j])

                new_v[i, j] += (d_coeff / self.c_m) * flux * dt
                # Protección termodinámica
                new_v[i, j] = max(VM_MIN_FISICO, min(VM_MAX_FISICO, new_v[i, j]))

        self.v_mem = new_v

    def compute_cognitive_light_cone_metrics(self) -> Dict[str, Any]:
        """
        Cuantifica el Cono Cognitivo de Luz (Levin) del tejido:
        - Radio de integración espacial (células acopladas en sincitio).
        - Número de 'Smaller Selves' aislados.
        - Información integrada compartida (Phi).
        """
        smaller_selves_count = 0
        total_coupled_nodes = 0
        voltage_divergence = float(np.std(self.v_mem))

        for i in range(self.rows):
            for j in range(self.cols):
                is_isolated = self.gjc[i, j] < 0.20
                is_depolarized = self.v_mem[i, j] >= UMBRAL_ONCOGENICO_VM_MV

                if is_isolated and is_depolarized:
                    smaller_selves_count += 1
                elif self.gjc[i, j] >= 0.50 and self.v_mem[i, j] <= UMBRAL_DIFERENCIADO_VM_MV:
                    total_coupled_nodes += 1

        fraction_coupled = total_coupled_nodes / self.n_cells
        fraction_smaller_selves = smaller_selves_count / self.n_cells

        # Métrica de información compartida del cono cognitivo:
        # Alta cuando las células están acopladas con baja varianza de voltaje (tejido coordinado)
        phi_metric = fraction_coupled * math.exp(-voltage_divergence / 15.0)

        # Radio espacial efectivo del cono cognitivo
        spatial_cone_radius = math.sqrt(total_coupled_nodes / math.pi)

        # Hash SHA-256 de integridad determinista
        state_repr = f"{self.v_mem.tobytes()}:{self.gjc.tobytes()}"
        sha_sig = hashlib.sha256(state_repr.encode("latin-1")).hexdigest()

        return {
            "n_cells_total": self.n_cells,
            "total_coupled_nodes": total_coupled_nodes,
            "smaller_selves_count": smaller_selves_count,
            "fraction_coupled": fraction_coupled,
            "fraction_smaller_selves": fraction_smaller_selves,
            "voltage_divergence_std": voltage_divergence,
            "cognitive_light_cone_phi": phi_metric,
            "spatial_cone_radius": spatial_cone_radius,
            "tissue_state": "SYNCHRONIZED_ORGAN" if fraction_coupled > 0.8 else "ONCOGENIC_FRAGMENTATION",
            "sha256_state": sha_sig
        }
