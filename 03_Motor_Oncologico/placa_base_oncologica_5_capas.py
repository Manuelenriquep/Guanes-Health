# -*- coding: utf-8 -*-
"""
Guanes Health — Placa Base de Lógica: Motor Oncológico & Homeostasis Celular (5 Capas)
======================================================================================
Versión: 2026.6.0-STABLE | Standard: GUANES-HEALTH-2026 | Status: Production-Ready
SSoT: 01_Especificaciones_SSoT/Placa_Base_Oncologica_5_Capas.md

Instrumento biofísico in-silico para el modelado determinístico de restricciones
bioenergéticas, política inmune Gated-6.50, eje entero-hepático (phi_gut) y rescate homeostático.
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional, Tuple


# =============================================================================
# NIVEL III: CONSTANTES E INMUTABLES BIOFÍSICAS & FARMACOLÓGICAS (LEDGER 2026)
# =============================================================================
PH_ACIDO_TUMORAL: float = 6.20
PH_FISIOLOGICO_SANO: float = 7.35
PH_INTRACELULAR_BASAL: float = 7.20
PH_APOPTOSIS_CRITICO: float = 6.80
PH_INTRACELULAR_LETAL: float = 5.20
PH_VETO_CD8: float = 6.50
ANERGY_GATE_THRESHOLD: float = 0.20
PH_FISICO_MIN: float = 0.0
PH_FISICO_MAX: float = 14.0

ATP_WARBURG: int = 10000
ATP_BASAL_SANO: int = 5000
ATP_MINIMO_SOBREVIVENCIA: float = 20.0
ATP_COLAPSADO_PARCHE: int = 30
BCL2_FACTOR_TUMORAL: float = 25.0
BCL2_FACTOR_SANO: float = 1.0

PHI_GUT_OPTIMO: float = 1.0
PHI_GUT_CRITICO_RESCATE: float = 0.899
IL6_FISIOLOGICO: float = 5.0
IL6_TORMENTA_MAX: float = 800.0
K_LPS_IL6: float = 795.0
ALPHA_IL6_PDL1: float = 11.0
K_IL6_TUMOR: float = 50.0


# =============================================================================
# NIVEL IV: RED DE DEPENDENCIA MECANÍSTICA (MAPA KELSENIANO BIOFÍSICO)
# =============================================================================
MAPA_KELSENIANO_BIOFISICO = {
    "grado_1_leyes_fisicas_inmutables": [
        "Primera y Segunda Ley de la Termodinámica (Conservación y Entropía)",
        "Ecuación de Nernst y Potencial Electroquímico de Protones",
        "No Negatividad de Concentraciones y Ley de Acción de Masas"
    ],
    "grado_2_mecanismos_celulares": [
        "Vía Intrínseca Mitocondrial de Apoptosis (BCL-2 / MOMP / Caspasas)",
        "Eje de Extrusión Ácida Tumoral (MCT1, MCT4, NHE1)",
        "Eje Entero-Hepático-Tumoral (Barrera phi_gut -> LPS -> IL-6 -> STAT3)",
        "Punto de Control Inmunitario (PD-1 / PD-L1 / Gated-6.50)"
    ],
    "grado_3_intervenciones_terapeuticas": [
        "Política de Infiltración Inmune Gated-6.50 (inmuno_utils.py)",
        "Blindaje de Linfocitos T NHE1-Shield (S267F)",
        "Parche de Restauración Oncológica Guanes",
        "Terapia de Barrera Intestinal Mucorreguladora (Akkermansia)"
    ]
}


# =============================================================================
# NIVEL II: MATRIZ DE EXCLUSIONES SEMÁNTICAS & VETOS FAIL-CLOSED (FC-BIO-*)
# =============================================================================
class VetosBiofisicos:
    @staticmethod
    def validar_ph(ph: Any) -> float:
        """FC-BIO-02 y FC-BIO-03: Aborta si el pH es nulo, corrupto o fuera de rango."""
        if ph is None:
            raise ValueError("FC-BIO-02: pH nulo. Protocolo abortado (Fail-Closed).")
        try:
            val = float(ph)
        except (TypeError, ValueError) as exc:
            raise ValueError("FC-BIO-02: pH corrupto o no numérico. Protocolo abortado.") from exc

        if not (PH_FISICO_MIN < val < PH_FISICO_MAX):
            raise ValueError(f"FC-BIO-03: pH {val} fuera de rango físico real (0 < pH < 14).")
        return val

    @staticmethod
    def validar_phi_gut(phi_gut: Any) -> float:
        """FC-BIO-GUT: Aborta si la fracción de barrera mucosal está fuera de [0, 1]."""
        if phi_gut is None:
            raise ValueError("FC-BIO-GUT: phi_gut nulo.")
        try:
            val = float(phi_gut)
        except (TypeError, ValueError) as exc:
            raise ValueError("FC-BIO-GUT: phi_gut corrupto o no numérico.") from exc
        if not (0.0 <= val <= 1.0):
            raise ValueError(f"FC-BIO-GUT: phi_gut {val} fuera de intervalo físico [0, 1].")
        return val

    @staticmethod
    def validar_atp(atp: Any) -> int:
        """FC-BIO-04: No negatividad de ATP."""
        try:
            val = int(atp)
        except (TypeError, ValueError) as exc:
            raise ValueError("FC-BIO-04: ATP no numérico.") from exc
        if val < 0:
            raise ValueError(f"FC-BIO-04: Concentración de ATP negativa ({val}) físicamente imposible.")
        return val


# =============================================================================
# NIVEL I: MODELADO DE ESTADOS BIOFÍSICOS & POLÍTICA GATED-6.50
# =============================================================================
class EstadoCelular(str, Enum):
    HOMEOSTASIS = "HOMEOSTASIS"
    TUMORAL_WARBURG = "TUMORAL_WARBURG"
    APOPTOSIS_EN_CURSO = "APOPTOSIS_EN_CURSO"
    COLAPSO_ACIDO = "COLAPSO_ACIDO"
    ANERGIA_INMUNE = "ANERGIA_INMUNE"


def calcular_citotoxicidad_gated_650(pHe: float, nhe1_shield: bool = False) -> float:
    """
    Política Inmune Canónica Gated-6.50.
    - FC-BIO-2.1: pHe <= 6.50 -> 0.0
    - Rampa lineal: 6.50 a 7.35
    - Anergy Gate: < 0.20 -> 0.0
    """
    pHe_val = VetosBiofisicos.validar_ph(pHe)
    if nhe1_shield:
        return 0.947  # Blindaje NHE1-Shield mantiene resistencia a la acidosis
    if pHe_val <= PH_VETO_CD8:
        return 0.0

    fraccion_cruda = (pHe_val - PH_VETO_CD8) / (PH_FISIOLOGICO_SANO - PH_VETO_CD8)
    fraccion_cruda = min(1.0, max(0.0, fraccion_cruda))

    if fraccion_cruda < ANERGY_GATE_THRESHOLD:
        return 0.0
    return round(fraccion_cruda, 4)


def evaluar_eje_entero_hepatico(phi_gut: float) -> Dict[str, float]:
    """Transducción portal de LPS -> IL-6 -> STAT3 -> PD-L1 -> TOX."""
    phi = VetosBiofisicos.validar_phi_gut(phi_gut)
    il6_portal = IL6_FISIOLOGICO + K_LPS_IL6 * (1.0 - phi)
    pdl1_densidad = 1.0 + ALPHA_IL6_PDL1 * (il6_portal / (il6_portal + K_IL6_TUMOR))
    agotamiento_tox = round((1.0 - phi) * 82.3 + 1.2, 2)
    return {
        "phi_gut": phi,
        "il6_pg_ml": round(il6_portal, 2),
        "pdl1_densidad": round(pdl1_densidad, 2),
        "agotamiento_epigenetico_pct": min(100.0, agotamiento_tox)
    }


class CelulaTumoral5Capas:
    def __init__(self) -> None:
        self.pH_extracelular: float = PH_ACIDO_TUMORAL
        self.pH_intracelular: float = PH_INTRACELULAR_BASAL
        self.atp: int = ATP_WARBURG
        self.mct4_bloqueado: bool = False
        self.camuflaje_pd_l1: bool = True
        self.bcl2_expression: float = BCL2_FACTOR_TUMORAL
        self.apoptosis_activa: bool = False
        self.estado: EstadoCelular = EstadoCelular.TUMORAL_WARBURG

    def establecer_pH(self, ph: Any) -> None:
        val = VetosBiofisicos.validar_ph(ph)
        self.pH_extracelular = val
        self._recalcular_equilibrio()

    def bloquear_mct4(self) -> None:
        self.mct4_bloqueado = True
        if self.pH_extracelular <= PH_VETO_CD8:
            self.pH_intracelular = 6.60
        self._recalcular_equilibrio()

    def aplicar_parche_restauracion(self) -> None:
        self.establecer_pH(PH_FISIOLOGICO_SANO)
        self.pH_intracelular = PH_INTRACELULAR_BASAL
        self.bcl2_expression = BCL2_FACTOR_SANO
        self.camuflaje_pd_l1 = False
        self.mct4_bloqueado = False
        self.apoptosis_activa = True
        self.atp = ATP_BASAL_SANO
        self.estado = EstadoCelular.APOPTOSIS_EN_CURSO

    def _recalcular_equilibrio(self) -> None:
        if self.pH_intracelular < PH_APOPTOSIS_CRITICO and self.bcl2_expression > BCL2_FACTOR_SANO:
            self.estado = EstadoCelular.COLAPSO_ACIDO
        elif self.bcl2_expression <= BCL2_FACTOR_SANO:
            self.apoptosis_activa = True
            self.estado = EstadoCelular.APOPTOSIS_EN_CURSO
        else:
            self.apoptosis_activa = False
            self.estado = EstadoCelular.TUMORAL_WARBURG
