# -*- coding: utf-8 -*-
"""
Política CD8 compartida (Capa B) — Gated-6.50.

Fuente única para núcleo (`parche_restauracion`), dinámica (`…_v5`)
y acoplamiento (`…_hepatico_v3`). No es evidencia clínica.
"""

PH_VETO_CD8 = 6.50
PH_FISIOLOGICO = 7.35
ANERGY_GATE = 0.20


def calcular_eficiencia_cd8(
    pHe,
    ph_veto=PH_VETO_CD8,
    ph_fisio=PH_FISIOLOGICO,
    anergy_gate=ANERGY_GATE,
):
    """
    Eficiencia citotóxica CD8+ modelada (fracción 0–1).

    Rampa lineal ph_veto → ph_fisio; si la fracción cruda es < anergy_gate → 0.0.
    """
    pHe = float(pHe)
    if pHe <= ph_veto:
        return 0.0
    cruda = (pHe - ph_veto) / (ph_fisio - ph_veto)
    cruda = min(1.0, max(0.0, cruda))
    if cruda < anergy_gate:
        return 0.0
    return cruda
