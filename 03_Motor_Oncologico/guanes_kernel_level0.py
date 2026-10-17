"""
Guanes Health — Kernel Nivel 0 de Inferencia Activa y Bioseguridad (Level 0 Orchestrator)
========================================================================================
Orquestador maestro determinista en silicio:
1. Acopla el Frente Bioeléctrico (guanes_bioelectrico.py) con el Frente Biofísico (guanes_biofisica.py).
2. Ejecuta el descenso de gradiente de Energía Libre Variacional (F -> 0) bajo el Principio de Mínima Acción (delta S = 0).
3. Cortafuegos Fail-Closed de Bioseguridad:
   - FC-BIO-01: Veto si phi_gut < 0.899 (Translocación endotóxica LPS / Leaky Gut).
   - FC-BIO-02: Veto si ATP citosólico sano < 15.0% (Toxicidad metabólica sistémica).
   - FC-BIO-03: Veto si persiste el 'Smaller Self' oncogénico (Vmem >= -25 mV y GJC cerrada).
   - FC-BIO-04: Veto si el escudo tumoral PD-L1 > 5.0x o agotamiento TOX > 0.80.
4. Dictamen clínico-biológico inmutable con firmado SHA-256 en tiempo sub-milisegundo.
"""

from __future__ import annotations
import math
import hashlib
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from guanes_bioelectrico import (
    GHKBioelectricEngine,
    BioelectricLattice2D,
    UMBRAL_ONCOGENICO_VM_MV,
    UMBRAL_DIFERENCIADO_VM_MV
)
from guanes_biofisica import (
    BiophysicalMicroenvironmentEngine,
    PHI_GUT_UMBRAL_RESCATE,
    MicroenvironmentState,
    GutLiverImmuneState
)
from guanes_pkpd import (
    PKPDSimulator,
    CARIPORIDE_MTD_UM,
    PQ1_MTD_UM
)


class BiosecurityVetoCode(str, Enum):
    FC_BIO_01 = "FC-BIO-01: Ruptura de Barrera Intestinal (phi_gut < 0.899 -> Endotoxemia Portal)"
    FC_BIO_02 = "FC-BIO-02: Colapso Metabólico Severo (ATP sano < 15% -> Toxicidad Inaceptable)"
    FC_BIO_03 = "FC-BIO-03: Persistencia de Smaller Self (Vmem >= -25 mV -> Fracaso de Normalización)"
    FC_BIO_04 = "FC-BIO-04: Evasión Inmune Excesiva (PD-L1 > 5.0x o Agotamiento TOX > 0.80)"


@dataclass
class TherapeuticTrajectoryCandidate:
    """
    Candidato de intervención terapéutica explorado en el morfoespacio:
    - Normalización bioeléctrica forzada (Vmem target en mV y restauración de conexinas Cx43).
    - Modulación del microambiente estromal (objetivo de pHe y bloqueo de NHE1).
    - Intervención entero-hepática (suplementación de Akkermansia muciniphila y reparación TEER).
    """
    trajectory_id: str
    target_vmem_mv: float = -75.0
    restore_cx43_conductance: float = 0.85
    target_phe: float = 7.35
    inhibit_nhe1_fraction: float = 0.60
    akkermansia_target_pct: float = 3.5
    teer_target_ohms: float = 1200.0


@dataclass
class TrajectoryAuditResult:
    trajectory_id: str
    admitted: bool
    status: str
    free_energy_f: float
    hamilton_action_delta_s: float
    veto_code: Optional[BiosecurityVetoCode] = None
    veto_reason: Optional[str] = None
    post_vmem_mv: float = 0.0
    post_phi_gut: float = 0.0
    post_atp_pct: float = 0.0
    post_pdl1_factor: float = 0.0
    elapsed_ms: float = 0.0
    sha256_hash: str = ""


class GuanesKernelLevel0:
    """
    Núcleo Determinista Nivel 0 de Inferencia Activa y Bioseguridad.
    Supervisa la evolución dinámica de los tejidos y garantiza el principio Fail-Closed.
    """

    def __init__(self):
        self.bioelectric_engine = GHKBioelectricEngine()
        self.biophysical_engine = BiophysicalMicroenvironmentEngine()
        self.pkpd_simulator = PKPDSimulator()

        # Pesos bayesianos para el cálculo de la Energía Libre Variacional (F)
        # Representan la precisión esperada (inversa de la varianza) sobre cada parámetro homeostático
        self.w_vmem = 1.0 / (15.0 ** 2)       # Desviación típica admisible en Vmem: ~15 mV
        self.w_phi = 1.0 / (0.05 ** 2)        # Desviación típica admisible en barrera: ~0.05
        self.w_atp = 1.0 / (10.0 ** 2)        # Desviación típica admisible en ATP: ~10%
        self.w_pdl1 = 1.0 / (0.5 ** 2)        # Desviación admisible en PD-L1: ~0.5x

    def compute_variational_free_energy(
        self,
        v_mem: float,
        phi_gut: float,
        atp_pct: float,
        pdl1_factor: float,
        target_vmem: float = -75.0,
        target_phi: float = 1.0,
        target_atp: float = 100.0,
        target_pdl1: float = 1.0
    ) -> float:
        """
        Calcula la Energía Libre Variacional (F):
        F = Sum_i [ w_i * (estado_observado_i - estado_meta_i)^2 ]
        Representa el error de predicción cuadrático ponderado por precisión. F -> 0 implica homeostasis óptima.
        """
        err_v = (v_mem - target_vmem) ** 2 * self.w_vmem
        err_phi = (phi_gut - target_phi) ** 2 * self.w_phi
        err_atp = (atp_pct - target_atp) ** 2 * self.w_atp
        err_pdl1 = (pdl1_factor - target_pdl1) ** 2 * self.w_pdl1

        return float(err_v + err_phi + err_atp + err_pdl1)

    def evaluate_and_audit_trajectory(
        self,
        candidate: TherapeuticTrajectoryCandidate,
        initial_lattice: Optional[BioelectricLattice2D] = None
    ) -> TrajectoryAuditResult:
        """
        Auditoría determinista de una trayectoria terapéutica propuesta:
        1. Simula el impacto bioeléctrico y la respuesta del cono cognitivo.
        2. Simula el microambiente ácido y el eje Gut-Liver-Immune.
        3. Evalúa el gradiente de Energía Libre F.
        4. Aplica el cortafuegos Fail-Closed estricto.
        5. Emite certificado criptográfico SHA-256.
        """
        start_ns = time.perf_counter_ns()

        # 1. Simulación del Eje Gut-Liver-Immune
        gut_state = self.biophysical_engine.simulate_gut_liver_immune_axis(
            akkermansia_pct=candidate.akkermansia_target_pct,
            teer=candidate.teer_target_ohms
        )

        # 2. Simulación del Microambiente Estromal y ATP
        # pHi estimado a partir del Vmem target y la inhibición de NHE1
        ph_i_simulado = 7.20 if candidate.inhibit_nhe1_fraction < 0.8 else 6.65
        micro_state = self.biophysical_engine.evaluate_bioelectric_acid_trap(
            ph_i=ph_i_simulado,
            ph_e=candidate.target_phe,
            v_mem_mv=candidate.target_vmem_mv
        )

        # 3. Simulación Bioeléctrica (Lattice de prueba o proporcionado)
        lattice = initial_lattice or BioelectricLattice2D(rows=6, cols=6, ghk_engine=self.bioelectric_engine)
        lattice.apply_levin_normalization(
            force_vmem=candidate.target_vmem_mv,
            restore_gjc=candidate.restore_cx43_conductance
        )
        bio_metrics = lattice.compute_cognitive_light_cone_metrics()

        # 4. Cálculo de Energía Libre Variacional y Acción de Hamilton
        f_free_energy = self.compute_variational_free_energy(
            v_mem=candidate.target_vmem_mv,
            phi_gut=gut_state.phi_gut_barrier,
            atp_pct=micro_state.atp_availability_pct,
            pdl1_factor=gut_state.pdl1_tumor_shield_factor
        )
        # Acción delta S aproximada (costo de transición proporcional a F)
        delta_s = f_free_energy * 0.05

        elapsed_ms = (time.perf_counter_ns() - start_ns) / 1_000_000.0

        # =============================================================
        # CORTAFUEGOS FAIL-CLOSED DE BIOSEGURIDAD (FC-BIO-01 a 04)
        # =============================================================

        # FC-BIO-01: Veto a ruptura de barrera intestinal
        if gut_state.phi_gut_barrier < PHI_GUT_UMBRAL_RESCATE:
            return self._build_veto_result(
                candidate.trajectory_id,
                BiosecurityVetoCode.FC_BIO_01,
                f"Integridad mucosa ({gut_state.phi_gut_barrier:.4f}) inferior al umbral de rescate {PHI_GUT_UMBRAL_RESCATE}. Fuga portal de LPS inaceptable.",
                f_free_energy, delta_s, candidate.target_vmem_mv, gut_state.phi_gut_barrier, micro_state.atp_availability_pct, gut_state.pdl1_tumor_shield_factor, elapsed_ms
            )

        # FC-BIO-02: Veto a toxicidad sistémica por colapso de ATP
        if micro_state.atp_availability_pct < 15.0:
            return self._build_veto_result(
                candidate.trajectory_id,
                BiosecurityVetoCode.FC_BIO_02,
                f"Disponibilidad de ATP ({micro_state.atp_availability_pct:.2f}%) en zona de toxicidad irreversible (< 15%). Trampa de ácido no selectiva.",
                f_free_energy, delta_s, candidate.target_vmem_mv, gut_state.phi_gut_barrier, micro_state.atp_availability_pct, gut_state.pdl1_tumor_shield_factor, elapsed_ms
            )

        # FC-BIO-03: Veto a persistencia de Smaller Self oncogénico
        if candidate.target_vmem_mv >= UMBRAL_ONCOGENICO_VM_MV or bio_metrics["smaller_selves_count"] > 0:
            return self._build_veto_result(
                candidate.trajectory_id,
                BiosecurityVetoCode.FC_BIO_03,
                f"Fallo de normalización: Vmem ({candidate.target_vmem_mv:.1f} mV) en rango oncogénico o presencia de células aisladas ({bio_metrics['smaller_selves_count']}).",
                f_free_energy, delta_s, candidate.target_vmem_mv, gut_state.phi_gut_barrier, micro_state.atp_availability_pct, gut_state.pdl1_tumor_shield_factor, elapsed_ms
            )

        # FC-BIO-04: Veto a hiper-expresión de escudo PD-L1 o agotamiento T terminal
        if gut_state.pdl1_tumor_shield_factor > 5.0 or gut_state.tox_exhaustion_index > 0.80:
            return self._build_veto_result(
                candidate.trajectory_id,
                BiosecurityVetoCode.FC_BIO_04,
                f"Inmunosupresión crítica: Escudo PD-L1 ({gut_state.pdl1_tumor_shield_factor:.2f}x) o Factor TOX ({gut_state.tox_exhaustion_index:.2f}) en nivel letal.",
                f_free_energy, delta_s, candidate.target_vmem_mv, gut_state.phi_gut_barrier, micro_state.atp_availability_pct, gut_state.pdl1_tumor_shield_factor, elapsed_ms
            )

        # Aprobación: Trayectoria de Mínima Acción Validada
        sha_payload = (
            f"TRAJECTORY_PASS:{candidate.trajectory_id}:{f_free_energy:.4f}:{candidate.target_vmem_mv:.1f}:"
            f"{gut_state.phi_gut_barrier:.4f}:{micro_state.atp_availability_pct:.2f}:{gut_state.pdl1_tumor_shield_factor:.2f}"
        )
        sha_sig = hashlib.sha256(sha_payload.encode("utf-8")).hexdigest()

        return TrajectoryAuditResult(
            trajectory_id=candidate.trajectory_id,
            admitted=True,
            status="ADMITTED_MINIMAL_ACTION",
            free_energy_f=f_free_energy,
            hamilton_action_delta_s=delta_s,
            post_vmem_mv=candidate.target_vmem_mv,
            post_phi_gut=gut_state.phi_gut_barrier,
            post_atp_pct=micro_state.atp_availability_pct,
            post_pdl1_factor=gut_state.pdl1_tumor_shield_factor,
            elapsed_ms=elapsed_ms,
            sha256_hash=sha_sig
        )

    def _build_veto_result(
        self,
        traj_id: str,
        veto_code: BiosecurityVetoCode,
        veto_reason: str,
        f: float,
        delta_s: float,
        vmem: float,
        phi: float,
        atp: float,
        pdl1: float,
        elapsed_ms: float
    ) -> TrajectoryAuditResult:
        sha_payload = f"VETO:{traj_id}:{veto_code.name}:{f:.4f}:{elapsed_ms:.4f}"
        sha_sig = hashlib.sha256(sha_payload.encode("utf-8")).hexdigest()
        return TrajectoryAuditResult(
            trajectory_id=traj_id,
            admitted=False,
            status="REJECTED_FAIL_CLOSED",
            free_energy_f=f,
            hamilton_action_delta_s=delta_s,
            veto_code=veto_code,
            veto_reason=f"[{veto_code.value}] {veto_reason}",
            post_vmem_mv=vmem,
            post_phi_gut=phi,
            post_atp_pct=atp,
            post_pdl1_factor=pdl1,
            elapsed_ms=elapsed_ms,
            sha256_hash=sha_sig
        )

    def evaluate_pharmacological_regimen(
        self,
        trajectory_id: str,
        cariporide_mg: float,
        pq1_mg: float,
        buffer_mmol: float,
        akkermansia_billions: float,
        duration_hours: float = 24.0
    ) -> TrajectoryAuditResult:
        """
        Evalúa y audita un régimen farmacológico real acoplado a PK/PD:
        1. Simula concentraciones plasmáticas y efectos mecanicistas temporales.
        2. Mapea la farmacodinamia a una TherapeuticTrajectoryCandidate.
        3. Realiza la auditoría Fail-Closed de silicio bajo Mínima Acción.
        """
        # Ejecución del simulador PK/PD
        try:
            pk_traj = self.pkpd_simulator.simulate_regimen(
                cariporide_dose_mg=cariporide_mg,
                pq1_dose_mg=pq1_mg,
                buffer_dose_mmol=buffer_mmol,
                akkermansia_cfu_billions=akkermansia_billions,
                duration_hours=duration_hours
            )
        except ValueError as e:
            # Captura veto inmediato por dosis fuera de límites de seguridad (FC-PKPD-01 / FC-PKPD-02)
            return TrajectoryAuditResult(
                trajectory_id=trajectory_id,
                admitted=False,
                status="REJECTED_FAIL_CLOSED",
                free_energy_f=999.0,
                hamilton_action_delta_s=999.0,
                veto_code=BiosecurityVetoCode.FC_BIO_02,
                veto_reason=f"Veto Farmacológico PK/PD: {str(e)}",
                sha256_hash=hashlib.sha256(f"VETO_PKPD:{str(e)}".encode("utf-8")).hexdigest()
            )

        # Extraer estado pico farmacológico y estado sostenido a nivel intestinal
        peak_state = max(pk_traj, key=lambda s: s.nhe1_inhibition_fraction)
        sustained_state = pk_traj[-1]
        
        # Mapeo a parámetros de candidato biológico
        # - Vmem objetivo normalizado si PQ1 reactiva conexinas
        target_vmem = -75.0 if peak_state.cx43_activation_boost > 0.40 else -20.0
        gjc_target = min(0.95, 0.20 + peak_state.cx43_activation_boost)
        # Amortiguación de buffer estromal
        target_phe = min(7.40, 7.15 + peak_state.pHe_alkalization_delta)
        inhibit_nhe1 = min(0.75, peak_state.nhe1_inhibition_fraction)
        
        # Abundancia mucosal de Akkermansia alcanzada tras cinética sostenida
        # En eubiosis sana oscila entre 2.5% y 4.5%
        akkermansia_pct = 1.0 + sustained_state.akkermansia_density * 3.5

        candidate = TherapeuticTrajectoryCandidate(
            trajectory_id=trajectory_id,
            target_vmem_mv=target_vmem,
            restore_cx43_conductance=gjc_target,
            target_phe=target_phe,
            inhibit_nhe1_fraction=inhibit_nhe1,
            akkermansia_target_pct=akkermansia_pct,
            teer_target_ohms=1250.0 if akkermansia_pct >= 2.5 else 600.0
        )

        return self.evaluate_and_audit_trajectory(candidate)

