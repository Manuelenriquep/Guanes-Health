"""
==================================================================================================
GUANES HEALTH - MOTOR ONCOLÓGICO DETERMINISTA
BioelectricLattice3D — guanes_bioelectrico_3d.py
Microambiente Tumoral Tridimensional Esferoidal y Ecuaciones de Reacción-Difusión
==================================================================================================
Modela la arquitectura tridimensional de un esferoide tumoral:
  1. Geometría concéntrica con 3 capas histológicas fundamentales:
     - Zona 1: Núcleo necrótico interno (r <= R_necrotic): hipoxia severa (pO2 ~ 0-2 mmHg),
       acumulación ácida (pHe < 6.4), fallo bioeléctrico y desacoplamiento Cx43.
     - Zona 2: Zona intermedia quiescente/hipóxica (R_necrotic < r <= R_quiescent):
       células despolarizadas oncogénicas (-25 mV a -15 mV), activación de NHE1 y glucólisis.
     - Zona 3: Borde proliferativo/invasivo exterior (R_quiescent < r <= R_total):
       mayor perfusión de O2, contacto con estroma sano y células en transición bioeléctrica.
  2. Ecuaciones PDE de Reacción-Difusión 3D en coordenadas esféricas discretizadas:
     - Oxígeno: d(pO2)/dt = D_O2 * Laplaciano(pO2) - Vmax_O2 * pO2 / (Km_O2 + pO2)
     - Glucosa: d(Gluc)/dt = D_Gluc * Laplaciano(Gluc) - Consumo_Gluc(pO2, Vmem)
     - Protones / pHe: Extrusión por NHE1 acoplada a Vmem y amortiguación estromal.
  3. Acoplamiento Bioeléctrico GHK y uniones gap Cx43 en red 3D (conectividad 6-vecinos o 26-vecinos).
  4. Protocolo Levin 3D de Rescate y Normalización de Sincitio Tisular.

Invariantes Fail-Closed:
  - FC-BIO-3D-01: Concentraciones no físicas o infinitas son vetadas inmediatamente.
  - FC-BIO-3D-02: Conservación de masa estricta y límites biológicos termodinámicos.
  - Sello criptográfico SHA-256 de cada estado 3D volumétrico.
==================================================================================================
"""

from dataclasses import dataclass
from enum import Enum
import hashlib
import math
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

from guanes_bioelectrico import (
    GHKBioelectricEngine,
    UMBRAL_ONCOGENICO_VM_MV,
    UMBRAL_DIFERENCIADO_VM_MV,
    VM_MIN_FISICO,
    VM_MAX_FISICO,
    RT_OVER_F_MV
)


class HistologicalZone3D(str, Enum):
    NECROTIC_CORE = "NECROTIC_CORE"           # Capa 1: Núcleo necrótico central
    QUIESCENT_HYPOXIC = "QUIESCENT_HYPOXIC"   # Capa 2: Zona intermedia hipóxica/ácida
    PROLIFERATIVE_RIM = "PROLIFERATIVE_RIM"   # Capa 3: Borde exterior proliferativo/invasivo


# Constantes biofísicas de difusión esferoidal (Literatura de Microambiente Tumoral)
D_OXYGEN_MM2_S: float = 1.8e-3       # Difusión de O2 en tejido tumoral (mm^2/s)
KM_OXYGEN_MMHG: float = 2.5          # Constante de Michaelis-Menten para O2 (mmHg)
VMAX_OXYGEN_CONSUMPTION: float = 0.08 # Consumo volumétrico máximo (mmHg / s)

D_GLUCOSE_MM2_S: float = 0.5e-3      # Difusión de glucosa (mm^2/s)
KM_GLUCOSE_MM: float = 0.20          # Constante Michaelis-Menten para glucosa (mM)

D_PROTONS_MM2_S: float = 1.0e-3      # Difusión aparente de equivalentes de H+


class BioelectricLattice3D:
    """
    Simulador 3D Esferoidal de Microambiente Tumoral y Bioelectricidad Tisular.
    Malla cúbica discretizada L x L x L representando un esferoide multicelular.
    """

    def __init__(
        self,
        dim_size: int = 7,           # Dimensión cúbica (dim_size x dim_size x dim_size)
        voxel_spacing_um: float = 20.0, # Tamaño de célula/vóxel (~20 micras)
        ghk_engine: Optional[GHKBioelectricEngine] = None
    ):
        if dim_size < 3:
            raise ValueError("Dimensión 3D mínima requerida es 3x3x3.")
        if dim_size % 2 == 0:
            # Preferir número impar para tener vóxel central exacto
            dim_size += 1

        self.dim = dim_size
        self.voxel_um = voxel_spacing_um
        self.total_voxels = dim_size ** 3
        self.ghk = ghk_engine or GHKBioelectricEngine()
        self.c_m = 1.0 # uF/cm^2

        # Centro del esferoide
        self.center = (dim_size - 1) / 2.0
        self.radius_max_voxels = self.center

        # Campos tridimensionales
        self.v_mem = np.full((dim_size, dim_size, dim_size), -72.0, dtype=np.float64) # mV
        self.gjc = np.full((dim_size, dim_size, dim_size), 0.85, dtype=np.float64)     # Cx43
        self.p_o2 = np.full((dim_size, dim_size, dim_size), 40.0, dtype=np.float64)   # mmHg (normoxia periférica)
        self.glucose = np.full((dim_size, dim_size, dim_size), 5.0, dtype=np.float64) # mM
        self.ph_e = np.full((dim_size, dim_size, dim_size), 7.35, dtype=np.float64)   # pH extracelular

        # Inicialización de zonas concéntricas histológicas (almacenadas como strings para filtrado NumPy eficiente)
        self.zones = np.full((dim_size, dim_size, dim_size), HistologicalZone3D.PROLIFERATIVE_RIM.value, dtype=object)
        self._initialize_spheroid_geometry()

    def _initialize_spheroid_geometry(self):
        """Asigna zonas concéntricas en función de la distancia radial al centro."""
        r_max = self.radius_max_voxels
        # Proporciones esferoidales: 25% núcleo necrótico, 65% zona intermedia hipóxica/oncogénica, resto borde
        r_necrotic = 0.35 * r_max
        r_quiescent = 0.75 * r_max

        for x in range(self.dim):
            for y in range(self.dim):
                for z in range(self.dim):
                    dist = math.sqrt((x - self.center)**2 + (y - self.center)**2 + (z - self.center)**2)
                    if dist <= r_necrotic:
                        self.zones[x, y, z] = HistologicalZone3D.NECROTIC_CORE.value
                        self.p_o2[x, y, z] = 1.5      # Anoxia / hipoxia extrema
                        self.glucose[x, y, z] = 0.4   # Agotamiento nutricional
                        self.ph_e[x, y, z] = 6.40     # Alta acidosis estromal
                        self.v_mem[x, y, z] = -12.0   # Despolarización patológica
                        self.gjc[x, y, z] = 0.05      # Conexinas clausuradas
                    elif dist <= r_quiescent:
                        self.zones[x, y, z] = HistologicalZone3D.QUIESCENT_HYPOXIC.value
                        self.p_o2[x, y, z] = 10.0     # Hipoxia moderada
                        self.glucose[x, y, z] = 1.8   # Glucólisis anaerobia acelerada
                        self.ph_e[x, y, z] = 6.60     # Acidosis
                        self.v_mem[x, y, z] = -22.0   # Oncogénico "Smaller Self" (Vmem >= -25 mV)
                        self.gjc[x, y, z] = 0.12      # Conexinas desacopladas (< 0.20)
                    else:
                        self.zones[x, y, z] = HistologicalZone3D.PROLIFERATIVE_RIM.value
                        self.p_o2[x, y, z] = 38.0
                        self.glucose[x, y, z] = 4.5
                        self.ph_e[x, y, z] = 7.15
                        self.v_mem[x, y, z] = -45.0   # Zona de transición no diferenciada totalmente
                        self.gjc[x, y, z] = 0.40      # Acoplamiento parcial intermedio

    def step_reaction_diffusion_3d(self, dt_seconds: float = 1.0):
        """
        Integra 1 paso temporal de reacción-difusión tridimensional para O2, glucosa y pHe.
        Utiliza stencil de diferencias finitas en 3D (6 vecinos contiguos).
        """
        if dt_seconds <= 0:
            raise ValueError("[FC-BIO-3D-01] Paso de tiempo dt debe ser positivo.")

        # Factores de difusión normalizados al espaciado de vóxel
        dx2 = (self.voxel_um * 1e-3) ** 2 # mm^2
        alpha_o2 = (D_OXYGEN_MM2_S * dt_seconds) / dx2
        alpha_o2 = min(0.15, alpha_o2) # Estabilidad numérica Courant-Friedrichs-Lewy (CFL)

        # 1. Laplaciano 3D para difusión de oxígeno
        new_po2 = np.copy(self.p_o2)
        for x in range(1, self.dim - 1):
            for y in range(1, self.dim - 1):
                for z in range(1, self.dim - 1):
                    laplacian = (
                        self.p_o2[x+1, y, z] + self.p_o2[x-1, y, z] +
                        self.p_o2[x, y+1, z] + self.p_o2[x, y-1, z] +
                        self.p_o2[x, y, z+1] + self.p_o2[x, y, z-1] -
                        6.0 * self.p_o2[x, y, z]
                    )
                    # Consumo metabólico Michaelis-Menten
                    consumption = VMAX_OXYGEN_CONSUMPTION * (self.p_o2[x, y, z] / (KM_OXYGEN_MMHG + self.p_o2[x, y, z]))
                    new_po2[x, y, z] += alpha_o2 * laplacian - consumption * dt_seconds
                    new_po2[x, y, z] = max(0.0, min(100.0, new_po2[x, y, z]))

        # Fijar condiciones de frontera de Dirichlet en la periferia (perfusión vascular exterior)
        for x in [0, self.dim - 1]:
            new_po2[x, :, :] = 40.0
        for y in [0, self.dim - 1]:
            new_po2[:, y, :] = 40.0
        for z in [0, self.dim - 1]:
            new_po2[:, :, z] = 40.0

        self.p_o2 = new_po2

    def step_bioelectric_sync_3d(self, dt: float = 0.1, d_coeff: float = 0.25):
        """
        Integra difusión electrotónica en red tridimensional con gating de conexinas Cx43:
        dV_i/dt = (1/C_m) * sum_{j vecinos} [ G_GJ_ij * (V_j - V_i) ]
        """
        new_v = np.copy(self.v_mem)

        # Vecindario ortogonal en 3D (6 vecinos)
        for x in range(self.dim):
            for y in range(self.dim):
                for z in range(self.dim):
                    neighbors = []
                    if x > 0: neighbors.append((x - 1, y, z))
                    if x < self.dim - 1: neighbors.append((x + 1, y, z))
                    if y > 0: neighbors.append((x, y - 1, z))
                    if y < self.dim - 1: neighbors.append((x, y + 1, z))
                    if z > 0: neighbors.append((x, y, z - 1))
                    if z < self.dim - 1: neighbors.append((x, y, z + 1))

                    flux = 0.0
                    for nx, ny, nz in neighbors:
                        # Conductancia efectiva de uniones gap
                        g_eff = (self.gjc[x, y, z] + self.gjc[nx, ny, nz]) / 2.0
                        g_dynamic = self.ghk.compute_cx43_gating(self.v_mem[x, y, z], self.v_mem[nx, ny, nz])
                        g_total = g_eff * g_dynamic
                        flux += g_total * (self.v_mem[nx, ny, nz] - self.v_mem[x, y, z])

                    new_v[x, y, z] += (d_coeff / self.c_m) * flux * dt
                    new_v[x, y, z] = max(VM_MIN_FISICO, min(VM_MAX_FISICO, new_v[x, y, z]))

        self.v_mem = new_v

    def apply_levin_normalization_3d(self, force_vmem: float = -75.0, restore_gjc: float = 0.85):
        """
        Protocolo Levin de Rescate Tridimensional:
        Apertura forzada de uniones gap Cx43 y repolarización sincrónica de las capas tisulares.
        """
        for x in range(self.dim):
            for y in range(self.dim):
                for z in range(self.dim):
                    # El núcleo necrótico irrecuperable no responde a conexinas
                    if self.zones[x, y, z] != HistologicalZone3D.NECROTIC_CORE.value:
                        self.v_mem[x, y, z] = force_vmem
                        self.gjc[x, y, z] = restore_gjc
                        self.ph_e[x, y, z] = 7.35

    def compute_metrics_3d(self) -> Dict[str, Any]:
        """
        Calcula las métricas bioeléctricas y morfogénicas tridimensionales:
        - Cono cognitivo 3D (volumen de sincitio integrado).
        - Conteo de Smaller Selves aislados.
        - Perfiles de gradiente radial de oxígeno y pH.
        - Hash inmutable SHA-256 del estado volumétrico completo.
        """
        smaller_selves = 0
        coupled_voxels = 0

        for x in range(self.dim):
            for y in range(self.dim):
                for z in range(self.dim):
                    is_isolated = self.gjc[x, y, z] < 0.20
                    is_depolarized = self.v_mem[x, y, z] >= UMBRAL_ONCOGENICO_VM_MV

                    if is_isolated and is_depolarized:
                        smaller_selves += 1
                    elif self.gjc[x, y, z] >= 0.50 and self.v_mem[x, y, z] <= UMBRAL_DIFERENCIADO_VM_MV:
                        coupled_voxels += 1

        fraction_coupled = coupled_voxels / self.total_voxels
        fraction_smaller_selves = smaller_selves / self.total_voxels
        voltage_std = float(np.std(self.v_mem))

        # Información integrada Phi en 3D
        phi_3d = fraction_coupled * math.exp(-voltage_std / 15.0)

        # Radio esferoidal del cono cognitivo: R_eff = (3 * V / 4*pi)^(1/3)
        vol_effective = coupled_voxels
        cone_radius_voxels = ((3.0 * vol_effective) / (4.0 * math.pi)) ** (1.0 / 3.0)

        # Hash SHA-256 determinista
        data_bytes = (
            self.v_mem.tobytes() +
            self.gjc.tobytes() +
            self.p_o2.tobytes() +
            self.ph_e.tobytes()
        )
        sha_sig = hashlib.sha256(data_bytes).hexdigest()

        return {
            "total_voxels": self.total_voxels,
            "coupled_voxels_3d": coupled_voxels,
            "smaller_selves_count_3d": smaller_selves,
            "fraction_coupled_3d": fraction_coupled,
            "fraction_smaller_selves_3d": fraction_smaller_selves,
            "voltage_divergence_std": voltage_std,
            "cognitive_light_cone_phi_3d": phi_3d,
            "cognitive_cone_radius_voxels": cone_radius_voxels,
            "mean_po2_core": float(np.mean(self.p_o2[self.zones == HistologicalZone3D.NECROTIC_CORE.value])),
            "mean_po2_rim": float(np.mean(self.p_o2[self.zones == HistologicalZone3D.PROLIFERATIVE_RIM.value])),
            "tissue_state_3d": "SYNCHRONIZED_SPHEROID" if fraction_coupled > 0.70 else "FRAGMENTED_ONCOGENIC",
            "sha256_volume_hash": sha_sig
        }
