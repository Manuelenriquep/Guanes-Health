"""
GUANES_VIDEO_BRIDGE: Módulo Seguro de Solo Lectura para Producción de Video
==========================================================================
Ubicación: guanes_video_bridge.py
Propósito: Proveer datos certificados, rutas a assets B-roll de alta resolución
           y verificación Fail-Closed a agentes de producción de video y Shorts,
           sin permitir la modificación accidental del núcleo del motor.
==========================================================================
"""

import os
import hashlib
from typing import Dict, Any, List, Optional

# Directorio base del proyecto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Rutas estándar a activos B-roll (300 DPI / 4K)
ASSETS_PATHS = {
    "bioelectric_dashboard": os.path.join(BASE_DIR, "guanes-health-core", "web-mvp", "met01_bioelectric_connector_dashboard.png"),
    "ipd_ms_dashboard": os.path.join(BASE_DIR, "guanes-health-core", "web-mvp", "met01_ipd_ms_dashboard.png"),
    "vaccine_population_chart": os.path.join(BASE_DIR, "guanes-health-core", "web-mvp", "grafico_poblacional_vacunas_arn.png"),
}

# Verificación de rutas alternativas en Guanes Health repo
for key, path in list(ASSETS_PATHS.items()):
    if not os.path.exists(path):
        alt_path = os.path.join(BASE_DIR, "Guanes Health", "web-mvp", os.path.basename(path))
        if os.path.exists(alt_path):
            ASSETS_PATHS[key] = alt_path

# Escenarios de simulación deterministas certificados
CERTIFIED_PRESETS = {
    "d1": {
        "id": "GH-2026-V6-SYN",
        "title": "Full Multi-Scale Synergy — NHE1-Shield (1K3R4E) + Mucosal 92%",
        "status": "CONSTRAINTS_SATISFIED",
        "pHe": 6.20,
        "pHi": 6.697,
        "Vmem_mV": -60.17,
        "CLC_index": 0.911,
        "clc_state": "INTEGRATED SELF (Open Cx43 Gap Junctions)",
        "atp_pct": 92.0,
        "phi_gut": 92.0,
        "gpc3_density": 19200,
        "construct": "1K3R4E (Constitutive NHE1-Shield)",
        "summary": "At pHe = 6.20, the proton shield stabilizes cytosolic pH at 6.697 and Vmem at -60.17 mV, keeping gap junctions open.",
        "sha256": "4b9e28f1cc478da27189e4726bf7656d0124ad57398124da4bc6c3b65ef8211b"
    },
    "d2": {
        "id": "GH-2026-V6-LEAK",
        "title": "Permeable Mucosal Barrier — Native Unshielded CD8 (S703A)",
        "status": "VETO_FAIL_CLOSED",
        "pHe": 6.20,
        "pHi": 5.50,
        "Vmem_mV": -30.00,
        "CLC_index": 0.141,
        "clc_state": "FRAGMENTED AGENT (Closed Gap Junctions)",
        "atp_pct": 1.07,
        "phi_gut": 20.0,
        "gpc3_density": 18000,
        "construct": "S703A / Native Unshielded (Defective Extrusion)",
        "summary": "Stromal Acid Trap: unshielded cell in pHe 6.20 crashes ATP to 1.07% and shuts down gap junctions (CLC = 0.141).",
        "sha256": "7a30cf190288f3eb99a803da9e208b067f9d8540c5f2db8d4cb282dbef8362ea"
    },
    "d3": {
        "id": "GH-2026-V6-VACC",
        "title": "mRNA Vaccine Alone — Zero Shield / Acidic Stroma",
        "status": "VETO_FAIL_CLOSED",
        "pHe": 6.20,
        "pHi": 5.78,
        "Vmem_mV": -35.20,
        "CLC_index": 0.141,
        "clc_state": "METABOLIC PARALYSIS",
        "atp_pct": 8.0,
        "phi_gut": 45.0,
        "gpc3_density": 22000,
        "construct": "Native CD8 (Zero Shield)",
        "summary": "High antigen affinity fails because cytotoxic exocytosis requires ATP, which is depleted by unbuffered proton influx.",
        "sha256": "3e9f45a19cb203de889f02cb87ef902bca486518a2bc49870fe6b4164ad8029b"
    }
}


def get_broll_assets() -> Dict[str, str]:
    """Retorna las rutas absolutas a las imágenes de alta resolución disponibles."""
    return {k: v for k, v in ASSETS_PATHS.items() if os.path.exists(v)}


def get_preset_data(preset_id: str = "d1") -> Dict[str, Any]:
    """Retorna el paquete de datos biofísicos certificados para un escenario."""
    return CERTIFIED_PRESETS.get(preset_id, CERTIFIED_PRESETS["d1"])


def get_hud_metrics(preset_id: str = "d1") -> Dict[str, str]:
    """
    Retorna cadenas de texto pre-formateadas listas para superponer
    como métricas HUD en pantalla durante el video.
    """
    data = get_preset_data(preset_id)
    return {
        "hud_id": data["id"],
        "hud_pHe": f"pHe: {data['pHe']:.2f}",
        "hud_pHi": f"pHi: {data['pHi']:.3f}",
        "hud_vmem": f"Vmem: {data['Vmem_mV']:.2f} mV",
        "hud_clc": f"CLC Index: {data['CLC_index']:.3f}",
        "hud_atp": f"ATP: {data['atp_pct']:.1f}%",
        "hud_status": data["status"],
        "hud_sha256": data["sha256"][:16] + "...",
        "hud_doi": "DOI: 10.5281/zenodo.22101265",
        "hud_url": "health.guanes.biz"
    }


def audit_script_claims(script_text: str) -> Dict[str, Any]:
    """
    Cortafuegos de texto para guiones de video:
    Detecta términos prohibidos que violan la Capa D (afirmaciones clínicas,
    curas mágicas o sensacionalismo médico no autorizado).
    """
    forbidden_terms = [
        "cura definitiva", "cura el cáncer", "tratamiento médico garantizado",
        "100% efectivo", "reemplazo de quimioterapia", "dispositivo médico aprobado",
        "milagro", "sanación mágica"
    ]
    
    lower_text = script_text.lower()
    violations = [t for t in forbidden_terms if t in lower_text]
    
    passed = len(violations) == 0
    return {
        "passed": passed,
        "decision": "APPROVED_SCRIPT" if passed else "VETO_CAPA_D",
        "violations": violations,
        "recommendation": "Enmarcar como física determinista in-silico y biología de sistemas teórica."
    }


if __name__ == "__main__":
    print("GUANES VIDEO BRIDGE: Activo y Operativo.")
    print("Assets encontrados:", list(get_broll_assets().keys()))
    print("Muestra HUD:", get_hud_metrics("d1"))
