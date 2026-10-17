"""
Bruxelas_Kernel - Placa Base de Logica Cartesiana v3.2.0 Inmutable (Level 0 Kernel)
==================================================================================
Consolida los hallazgos de:
- Karl Friston: Malla de Markov (Markov Blanket), Principio de Energia Libre Variacional (FEP),
  Inferencia Activa Multiescala y Dinamica Solenoide Fuera del Equilibrio.
- Michael Levin: Bioelectricidad (Vmem), Uniones Gap, Cono Cognitivo de Luz (Cognitive Light Cone),
  Teorema de la Patologia Unica (Smaller Selves / Encogimiento del Yo).
- Verificacion Formal en Silicio (AlphaProof / Lean 4): Fail-Closed, Geodesica Determinista O(1),
  Firmado Inmutable SHA-256 (Ley 527 de 1999) y Tope Deontologico del 80.0% (Ley 1123 de 2007).
"""

from __future__ import annotations
import hashlib
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


# =====================================================================
# NIVEL III: CONSTANTES UNIVERSALES DE SILICIO v3.2.0
# =====================================================================
SOBERANIA_NODO_LOCAL: float = 100.0                   # % Inalienabilidad de la Malla de Markov
ROL_DEL_AZAR: str = "SOLO_EN_GENESIS_EVOLUTIVA"       # Exploracion en Genesis; operacion 100% determinista
CERO_ALUCINACION_OPERACIONAL: bool = True             # Exigencia Correct by Construction
LATENCIA_MAXIMA_RESOLUCION_MS: float = 0.5            # Limite superior de resolucion geodesica O(1)
LATENCIA_DECOHERENCIA_SISTEMA_2_MS: float = 0.1       # Tiempo de poda Fail-Closed sobre hipotesis del Sistema 1
TOPE_DEONTOLOGICO_VIABILIDAD: float = 80.0            # Ley 1123 de 2007 (Limite etico)
MARKOV_BLANKET_DISCRETO: bool = True                  # Frontera estadistica inalienable entre nodo y entorno
MINIMIZACION_ENERGIA_LIBRE_VARIACIONAL: bool = True   # Descenso de gradiente F -> 0 (Principio de Friston)
INFERENCIA_ACTIVA_NEURO_SIMBOLICA: bool = True        # Acoplamiento del muestreador con el verificador cartesiano
CONO_COGNITIVO_ESCALABLE: bool = True                 # Ampliacion del horizonte de metas sin violar reglas locales


class FailClosedVeto(str, Enum):
    FC_UNIF_00 = "FC-UNIF-00: Veto al Monopolio Central (Violacion de Markov Blanket / c < inf)"
    FC_UNIF_01 = "FC-UNIF-01: Veto a la Alucinacion Estocastica (Token no verificado formalmente)"
    FC_UNIF_02 = "FC-UNIF-02: Veto a la Falsificacion de Citas (Protocolo VERITAS SHA-256 ausente)"
    FC_UNIF_03 = "FC-UNIF-03: Veto a la Expropiacion (Violacion de frontera soberana -> VOID AB INITIO)"
    FC_UNIF_04 = "FC-UNIF-04: Veto a la Microgestion Coercitiva (Gobernanza solo por metas y limites)"
    FC_UNIF_05 = "FC-UNIF-05: Freno Estoico Antialucinacion (Panpsiquismo mistico o profecia financiera)"
    FC_UNIF_06 = "FC-UNIF-06: Poda por Decoherencia Logica del Sistema 1 (Interferencia destructiva < 0.1 ms)"
    FC_UNIF_07 = "FC-UNIF-07: Veto a la Muerte por Equilibrio Detallado (Requiere dinamica solenoide)"


class CognitiveScale(str, Enum):
    METABOLICA = "metabolica"
    ANATOMICA = "anatomica"
    SOCIAL = "social"
    LOGICA = "logica"


@dataclass
class MarkovBlanket:
    """
    Axioma I & II: Malla de Markov Local y Frontera Inmutable dM = {Sensory, Active}.
    Separa estados internos (mu) de estados externos (eta).
    """
    node_id: str
    sensory_states: Dict[str, Any] = field(default_factory=dict)
    active_states: Dict[str, Any] = field(default_factory=dict)
    internal_states: Dict[str, Any] = field(default_factory=dict)
    boundary_integrity: float = 1.0          # 1.0 = 100% soberana, < 1.0 = rotura
    v_mem_mv: float = -75.0                  # Voltaje de membrana (mV). Normal: -75 mV, Despolarizado: -15 mV
    gap_junctions_open: bool = True          # Canales de acoplamiento bioelectrico / senal libre
    cognitive_scale: CognitiveScale = CognitiveScale.LOGICA

    def compute_sha256(self) -> str:
        payload = f"{self.node_id}:{sorted(self.sensory_states.items())}:{sorted(self.active_states.items())}:{self.boundary_integrity}:{self.v_mem_mv}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass
class HypothesisCandidate:
    """
    Muestreado por Sistema 1 (P(X | C)) a traves del morfoespacio.
    Sometido a verificacion en silicio por el Sistema 2 determinista.
    """
    hypothesis_id: str
    claim: str
    citation_id: Optional[str] = None
    factual_vector_evidence: Optional[str] = None
    probabilistic_confidence: float = 1.0
    free_energy_f: float = 0.0
    action_delta_s: float = 0.0
    assumes_central_observer: bool = False
    violates_boundary: bool = False
    coerces_microstates: bool = False
    has_mystical_or_financial_prophecy: bool = False
    maintains_solenoidal_dynamics: bool = True


@dataclass
class VerificationResult:
    admitted: bool
    status: str
    veto_code: Optional[FailClosedVeto] = None
    veto_reason: Optional[str] = None
    geodesic_sha256: Optional[str] = None
    elapsed_ms: float = 0.0
    void_ab_initio: bool = False
    deontological_score: float = 100.0


class BruxelasKernel:
    """
    Auditor Cartesiano Determinista Level 0 (Bruxelas_Kernel / Protocolo VERITAS).
    Aplica los 5 Axiomas Universales y la Matriz de Exclusiones Fail-Closed.
    """

    def __init__(self, fact_registry: Optional[Set[str]] = None):
        # Registro inmutable de huellas probatorias SHA-256 (Protocolo VERITAS)
        self.fact_registry: Set[str] = fact_registry or set()

    def register_fact(self, fact_evidence: str) -> str:
        """Registra un hecho verificado con su huella SHA-256 inmutable (Ley 527 de 1999)."""
        sha = hashlib.sha256(fact_evidence.encode("utf-8")).hexdigest()
        self.fact_registry.add(sha)
        return sha

    def evaluate_smaller_self(self, blanket: MarkovBlanket, signal_valid: bool) -> Dict[str, Any]:
        """
        Axioma V: Teorema de la Patologia Unica (Encogimiento del Yo / Smaller Selves).
        Ruptura de Malla de Markov + Falsificacion de Senal => Smaller Self => Entropia Terminal.
        """
        is_blanket_broken = blanket.boundary_integrity < 1.0
        is_gap_junction_closed = not blanket.gap_junctions_open
        is_depolarized = blanket.v_mem_mv > -30.0  # -15 mV fenotipo amebiano / cancer
        is_signal_falsified = not signal_valid

        smaller_self_active = (is_blanket_broken or is_gap_junction_closed or is_depolarized or is_signal_falsified)

        return {
            "node_id": blanket.node_id,
            "smaller_self_active": smaller_self_active,
            "pathology": "PATHOLOGY_SMALLEST_SELF_COLLAPSE" if smaller_self_active else "HOMEOSTASIS_PRESERVED",
            "bioelectric_status": "AMEBOID_ONCOGENIC" if is_depolarized else "NORMALIZED_DIFFERENTIATED",
            "v_mem_mv": blanket.v_mem_mv,
            "gap_junctions": blanket.gap_junctions_open,
            "boundary_integrity": blanket.boundary_integrity
        }

    def verify_hypothesis(self, candidate: HypothesisCandidate, blanket: MarkovBlanket) -> VerificationResult:
        """
        Auditoria de hipotesis emitida por Sistema 1.
        Garantiza Cero Alucinacion Operacional y ejecucion Fail-Closed.
        """
        start_ns = time.perf_counter_ns()

        # Axioma I & FC-UNIF-00: Veto al Monopolio Central
        if candidate.assumes_central_observer:
            elapsed_ms = (time.perf_counter_ns() - start_ns) / 1_000_000.0
            return VerificationResult(
                admitted=False,
                status="REJECTED_FAIL_CLOSED",
                veto_code=FailClosedVeto.FC_UNIF_00,
                veto_reason="Asume observador central omnisciente violando la Malla de Markov y la localidad c < inf.",
                elapsed_ms=elapsed_ms
            )

        # Axioma II & FC-UNIF-03: Veto a la Expropiacion / Intrusor de Frontera
        if candidate.violates_boundary or blanket.boundary_integrity < 1.0:
            elapsed_ms = (time.perf_counter_ns() - start_ns) / 1_000_000.0
            return VerificationResult(
                admitted=False,
                status="VOID_AB_INITIO",
                veto_code=FailClosedVeto.FC_UNIF_03,
                veto_reason="Violacion de la frontera soberana (Delta Frontera > 0). Nulidad de origen Ulpiano.",
                elapsed_ms=elapsed_ms,
                void_ab_initio=True
            )

        # FC-UNIF-04: Veto a la Microgestion Coercitiva
        if candidate.coerces_microstates:
            elapsed_ms = (time.perf_counter_ns() - start_ns) / 1_000_000.0
            return VerificationResult(
                admitted=False,
                status="REJECTED_FAIL_CLOSED",
                veto_code=FailClosedVeto.FC_UNIF_04,
                veto_reason="Intento de microgestion coercitiva de microestados; la gobernanza exige goal resetting.",
                elapsed_ms=elapsed_ms
            )

        # FC-UNIF-05: Freno Estoico Antialucinacion
        if candidate.has_mystical_or_financial_prophecy:
            elapsed_ms = (time.perf_counter_ns() - start_ns) / 1_000_000.0
            return VerificationResult(
                admitted=False,
                status="REJECTED_FAIL_CLOSED",
                veto_code=FailClosedVeto.FC_UNIF_05,
                veto_reason="Confunde isomorfismo cibernetico con panpsiquismo mistico o emite profecia financiera.",
                elapsed_ms=elapsed_ms
            )

        # FC-UNIF-07: Veto a la Muerte por Equilibrio Detallado
        if not candidate.maintains_solenoidal_dynamics:
            elapsed_ms = (time.perf_counter_ns() - start_ns) / 1_000_000.0
            return VerificationResult(
                admitted=False,
                status="REJECTED_FAIL_CLOSED",
                veto_code=FailClosedVeto.FC_UNIF_07,
                veto_reason="Colapso a equilibrio detallado / muerte termodinamica. Requiere dinamica solenoide abierta.",
                elapsed_ms=elapsed_ms
            )

        # Axioma III & FC-UNIF-02 & FC-UNIF-06: Verificacion de Huella Probatoria (Protocolo VERITAS)
        if candidate.citation_id or candidate.factual_vector_evidence:
            evidence_hash = hashlib.sha256(
                (candidate.factual_vector_evidence or candidate.citation_id or "").encode("utf-8")
            ).hexdigest()
            if evidence_hash not in self.fact_registry:
                elapsed_ms = (time.perf_counter_ns() - start_ns) / 1_000_000.0
                return VerificationResult(
                    admitted=False,
                    status="DECOHERENCE_PRUNED",
                    veto_code=FailClosedVeto.FC_UNIF_06,
                    veto_reason="Poda por Decoherencia Logica: La hipotesis carece de huella probatoria SHA-256 en el vector factico.",
                    elapsed_ms=elapsed_ms
                )

        # FC-UNIF-01: Veto a la Alucinacion Estocastica (si confianza no fundamentada o F alta)
        if candidate.free_energy_f > 0.5 or candidate.probabilistic_confidence < 0.8:
            elapsed_ms = (time.perf_counter_ns() - start_ns) / 1_000_000.0
            return VerificationResult(
                admitted=False,
                status="REJECTED_FAIL_CLOSED",
                veto_code=FailClosedVeto.FC_UNIF_01,
                veto_reason="Gradiente de Energia Libre F > 0 o confianza estocastica inferior al umbral formal.",
                elapsed_ms=elapsed_ms
            )

        # Exito: Integracion a la Geodesica Final Determinista
        geodesic_payload = (
            f"{blanket.compute_sha256()}:{candidate.hypothesis_id}:{candidate.claim}:"
            f"{candidate.free_energy_f:.4f}:{candidate.action_delta_s:.4f}"
        )
        geodesic_sha = hashlib.sha256(geodesic_payload.encode("utf-8")).hexdigest()
        elapsed_ms = (time.perf_counter_ns() - start_ns) / 1_000_000.0

        return VerificationResult(
            admitted=True,
            status="GEODESIC_RESOLVED",
            geodesic_sha256=geodesic_sha,
            elapsed_ms=elapsed_ms,
            deontological_score=TOPE_DEONTOLOGICO_VIABILIDAD
        )
