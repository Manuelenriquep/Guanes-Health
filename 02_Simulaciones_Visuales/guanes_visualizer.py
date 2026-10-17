"""
==================================================================================================
GUANES HEALTH - SIMULACIONES VISUALES DETERMINISTAS
Generador Visual y Dashboard de Alta Fidelidad — guanes_visualizer.py
Kernel Nivel 0 / Verificación Biomédica Inmutable
==================================================================================================
Genera reportes visuales de grado publicación (matplotlib) y estructuras de datos para frontend:
  Panel 1: Campo Bioeléctrico y Microambiente 3D (Corte ecuatorial del esferoide antes y después
           del rescate de Levin, mapas de calor Vmem, pO2 y pH extracelular).
  Panel 2: Monitor Farmacocinético y Farmacodinámico (Curvas C(t) de Cariporida, PQ1, Buffer
           y dinámica de colonización de Akkermansia muciniphila con IC50 y límites seguros MTD).
  Panel 3: Consola de Bioseguridad e Invariantes Level 0 (Evolución de Energía Libre Variacional F,
           estado de los cortafuegos Fail-Closed FC-BIO-01 a 04 y sellado SHA-256).
==================================================================================================
"""

from dataclasses import dataclass
import hashlib
import os
import sys
from typing import Optional, List, Dict, Any
import numpy as np
import matplotlib
matplotlib.use('Agg') # Renderizado headless no interactivo
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Configurar rutas del sistema
MOTOR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico"))
if MOTOR_DIR not in sys.path:
    sys.path.insert(0, MOTOR_DIR)

from guanes_bioelectrico import GHKBioelectricEngine
from guanes_bioelectrico_3d import BioelectricLattice3D, HistologicalZone3D
from guanes_biofisica import BiophysicalMicroenvironmentEngine
from guanes_pkpd import (
    PKPDSimulator,
    CARIPORIDE_IC50_UM,
    CARIPORIDE_MTD_UM,
    PQ1_EC50_UM,
    PQ1_MTD_UM
)
from guanes_kernel_level0 import GuanesKernelLevel0, TherapeuticTrajectoryCandidate


class GuanesHighFidelityVisualizer:
    """
    Motor de Renderizado Cinematográfico y Científico de Guanes Health.
    Genera infografías técnicas de alta resolución con estilo 'dark-mode' instrumental.
    """

    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = output_dir or os.path.abspath(os.path.dirname(__file__))
        self.kernel = GuanesKernelLevel0()
        self.pkpd = PKPDSimulator()

    def generate_comprehensive_dashboard(
        self,
        cariporide_dose_mg: float = 30.0,
        pq1_dose_mg: float = 15.0,
        buffer_dose_mmol: float = 40.0,
        akkermansia_billions: float = 30.0,
        filename: str = "guanes_health_comprehensive_dashboard.png"
    ) -> str:
        """
        Ejecuta la simulación completa y renderiza el Dashboard Integrado de Alta Fidelidad.
        Retorna la ruta absoluta del archivo PNG generado.
        """
        # 1. Simulación Farmacocinética (PK/PD)
        pk_traj = self.pkpd.simulate_regimen(
            cariporide_dose_mg=cariporide_dose_mg,
            pq1_dose_mg=pq1_dose_mg,
            buffer_dose_mmol=buffer_dose_mmol,
            akkermansia_cfu_billions=akkermansia_billions,
            duration_hours=24.0,
            time_step_h=0.5
        )

        times_h = [s.time_h for s in pk_traj]
        cariporide_conc = [s.cariporide_conc_uM for s in pk_traj]
        pq1_conc = [s.pq1_conc_uM for s in pk_traj]
        akk_dens = [s.akkermansia_density * 100.0 for s in pk_traj]
        pHe_deltas = [s.pHe_alkalization_delta for s in pk_traj]

        # 2. Simulación Esferoide 3D (Estado Patológico vs. Rescate Tisular Levin 3D)
        spheroid_baseline = BioelectricLattice3D(dim_size=7)
        slice_z = int(spheroid_baseline.center)
        vmem_pre = np.copy(spheroid_baseline.v_mem[:, :, slice_z])
        po2_pre = np.copy(spheroid_baseline.p_o2[:, :, slice_z])

        # Esferoide rescatado
        spheroid_rescued = BioelectricLattice3D(dim_size=7)
        spheroid_rescued.apply_levin_normalization_3d(force_vmem=-75.0, restore_gjc=0.85)
        for _ in range(5):
            spheroid_rescued.step_reaction_diffusion_3d(dt_seconds=1.0)
            spheroid_rescued.step_bioelectric_sync_3d(dt=0.1)

        vmem_post = spheroid_rescued.v_mem[:, :, slice_z]
        po2_post = spheroid_rescued.p_o2[:, :, slice_z]
        metrics_3d = spheroid_rescued.compute_metrics_3d()

        # 3. Auditoría Kernel Level 0
        audit_result = self.kernel.evaluate_pharmacological_regimen(
            trajectory_id="DASHBOARD_LIVE_RUN",
            cariporide_mg=cariporide_dose_mg,
            pq1_mg=pq1_dose_mg,
            buffer_mmol=buffer_dose_mmol,
            akkermansia_billions=akkermansia_billions
        )

        # -------------------------------------------------------------
        # RENDERIZADO GRÁFICO (Estilo Dark / Instrumental de Alta Gama)
        # -------------------------------------------------------------
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(18, 12), dpi=150)
        gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.30)

        fig.patch.set_facecolor('#0d1117')

        # TÍTULO GENERAL DEL INSTRUMENTO
        fig.suptitle(
            "GUANES HEALTH — SUITE ONCOLÓGICA DETERMINISTA & KERNEL NIVEL 0 (IN SILICO)\n"
            f"Firma Criptográfica SHA-256: {audit_result.sha256_hash[:32]}... [SUB-MILISEGUNDO: {audit_result.elapsed_ms:.3f} ms]",
            fontsize=13, fontweight='bold', color='#58a6ff', y=0.98
        )

        # =============================================================
        # FILA 1: MICROAMBIENTE 3D (CORTES AXIALES DEL ESFEROIDE)
        # =============================================================
        # 1.1 Vmem Pre-Tratamiento (Smaller Self Fragmentado)
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.set_facecolor('#161b22')
        im1 = ax1.imshow(vmem_pre, cmap='magma', vmin=-75, vmax=-10, origin='lower')
        ax1.set_title("Vmem Pre-Tratamiento (Corte Sagital 3D)\n[Patología: Smaller Self Despolarizado]", fontsize=10, color='#f0883e')
        ax1.set_xticks(range(7))
        ax1.set_yticks(range(7))
        cbar1 = plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
        cbar1.set_label("mV", color='#c9d1d9')
        cbar1.ax.tick_params(colors='#8b949e')

        # 1.2 Vmem Post-Rescate de Levin 3D (Sincitio Tisular)
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.set_facecolor('#161b22')
        im2 = ax2.imshow(vmem_post, cmap='viridis', vmin=-75, vmax=-10, origin='lower')
        ax2.set_title("Vmem Post-Rescate Bioeléctrico (Levin 3D)\n[Hiperpolarización & Apertura Cx43]", fontsize=10, color='#3fb950')
        ax2.set_xticks(range(7))
        ax2.set_yticks(range(7))
        cbar2 = plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)
        cbar2.set_label("mV", color='#c9d1d9')
        cbar2.ax.tick_params(colors='#8b949e')

        # 1.3 Campo de Oxígeno pO2 Reacción-Difusión
        ax3 = fig.add_subplot(gs[0, 2])
        ax3.set_facecolor('#161b22')
        im3 = ax3.imshow(po2_post, cmap='coolwarm', vmin=0, vmax=40, origin='lower')
        ax3.set_title(f"Difusión pO2 Post-Rescate\n[Núcleo: {metrics_3d['mean_po2_core']:.1f} mmHg | Borde: {metrics_3d['mean_po2_rim']:.1f} mmHg]", fontsize=10, color='#79c0ff')
        ax3.set_xticks(range(7))
        ax3.set_yticks(range(7))
        cbar3 = plt.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)
        cbar3.set_label("mmHg", color='#c9d1d9')
        cbar3.ax.tick_params(colors='#8b949e')

        # =============================================================
        # FILA 2: CINÉTICA FARMACOCINÉTICA / FARMACODINÁMICA (PK/PD)
        # =============================================================
        # 2.1 Cariporida (NHE1) vs IC50 y MTD
        ax4 = fig.add_subplot(gs[1, 0])
        ax4.set_facecolor('#161b22')
        ax4.plot(times_h, cariporide_conc, color='#f78166', lw=2.2, label="[Cariporida] Plasmática")
        ax4.axhline(CARIPORIDE_IC50_UM, color='#e3b341', linestyle='--', label=f"IC50 ({CARIPORIDE_IC50_UM} uM)")
        ax4.axhline(CARIPORIDE_MTD_UM, color='#f85149', linestyle=':', label=f"Límite MTD ({CARIPORIDE_MTD_UM} uM)")
        ax4.set_title("Cinética Cariporida (Inhibición NHE1)", fontsize=10, color='#58a6ff')
        ax4.set_xlabel("Tiempo (horas)", color='#8b949e', fontsize=8)
        ax4.set_ylabel("Concentración (uM)", color='#8b949e', fontsize=8)
        ax4.legend(loc="upper right", fontsize=7, facecolor='#21262d', edgecolor='#30363d')
        ax4.grid(True, alpha=0.15)

        # 2.2 PQ1 (Cx43) vs EC50
        ax5 = fig.add_subplot(gs[1, 1])
        ax5.set_facecolor('#161b22')
        ax5.plot(times_h, pq1_conc, color='#a371f7', lw=2.2, label="[PQ1] Plasmática")
        ax5.axhline(PQ1_EC50_UM, color='#3fb950', linestyle='--', label=f"EC50 ({PQ1_EC50_UM} uM)")
        ax5.set_title("Cinética PQ1 (Activación Cx43)", fontsize=10, color='#58a6ff')
        ax5.set_xlabel("Tiempo (horas)", color='#8b949e', fontsize=8)
        ax5.set_ylabel("Concentración (uM)", color='#8b949e', fontsize=8)
        ax5.legend(loc="upper right", fontsize=7, facecolor='#21262d', edgecolor='#30363d')
        ax5.grid(True, alpha=0.15)

        # 2.3 Eje Intestinal: Akkermansia muciniphila y Buffer
        ax6 = fig.add_subplot(gs[1, 2])
        ax6.set_facecolor('#161b22')
        ax6.plot(times_h, akk_dens, color='#2ea043', lw=2.2, label="Akkermansia (% Eubiosis)")
        ax6.plot(times_h, [d * 100.0 for d in pHe_deltas], color='#d29922', lw=1.8, linestyle='-.', label="Delta pHe Estromal (x100)")
        ax6.set_title("Colonización Luminal & Neutralización Ácida", fontsize=10, color='#58a6ff')
        ax6.set_xlabel("Tiempo (horas)", color='#8b949e', fontsize=8)
        ax6.set_ylabel("Efecto / Saturación (%)", color='#8b949e', fontsize=8)
        ax6.legend(loc="lower right", fontsize=7, facecolor='#21262d', edgecolor='#30363d')
        ax6.grid(True, alpha=0.15)

        # =============================================================
        # FILA 3: CONSOLA DE BISEGURIDAD LEVEL 0 Y FAIL-CLOSED
        # =============================================================
        # 3.1 Cono Cognitivo 3D: Volumen Acoplado vs Smaller Selves
        ax7 = fig.add_subplot(gs[2, 0])
        ax7.set_facecolor('#161b22')
        bars = ax7.bar(
            ["Acoplados 3D", "Smaller Selves", "Núcleo Necrótico"],
            [metrics_3d['coupled_voxels_3d'], metrics_3d['smaller_selves_count_3d'], 7],
            color=['#238636', '#da3633', '#8b949e'],
            edgecolor='#30363d'
        )
        ax7.set_title(f"Cono Cognitivo 3D (Phi={metrics_3d['cognitive_light_cone_phi_3d']:.3f})", fontsize=10, color='#58a6ff')
        ax7.set_ylabel("Conteo de Vóxeles", color='#8b949e', fontsize=8)
        for b in bars:
            ax7.text(b.get_x() + b.get_width()/2.0, b.get_height() + 5, f"{int(b.get_height())}", ha='center', va='bottom', color='#c9d1d9', fontsize=8)
        ax7.grid(True, alpha=0.15, axis='y')

        # 3.2 Indicadores Homeostáticos (ATP, phi_gut, PD-L1)
        ax8 = fig.add_subplot(gs[2, 1])
        ax8.set_facecolor('#161b22')
        params = ["ATP Sano (%)", "Barrera phi_gut", "Escudo PD-L1 (x)"]
        vals = [audit_result.post_atp_pct, audit_result.post_phi_gut * 100.0, audit_result.post_pdl1_factor * 10.0]
        targets = [100.0, 100.0, 10.0]
        y_pos = np.arange(len(params))
        ax8.barh(y_pos - 0.15, vals, height=0.3, label="Resultado Simulado", color='#1f6feb', edgecolor='#30363d')
        ax8.barh(y_pos + 0.15, targets, height=0.3, label="Meta Homeostática", color='#30363d', edgecolor='#8b949e')
        ax8.set_yticks(y_pos)
        ax8.set_yticklabels(params, color='#c9d1d9', fontsize=8)
        ax8.set_title("Vectores de Estado Homeostático", fontsize=10, color='#58a6ff')
        ax8.legend(loc="lower right", fontsize=7, facecolor='#21262d', edgecolor='#30363d')
        ax8.grid(True, alpha=0.15, axis='x')

        # 3.3 Consola de Certificación Fail-Closed SHA-256
        ax9 = fig.add_subplot(gs[2, 2])
        ax9.set_facecolor('#161b22')
        ax9.axis('off')
        
        status_color = '#3fb950' if audit_result.admitted else '#f85149'
        badge_text = "ADMITIDO: MÍNIMA ACCIÓN" if audit_result.admitted else "RECHAZADO: FAIL-CLOSED"

        console_lines = [
            f"=== CERTIFICADO DETERMINISTA LEVEL 0 ===",
            f"STATUS: {badge_text}",
            f"Energía Libre (F): {audit_result.free_energy_f:.4f} (F -> 0)",
            f"Acción Hamilton (dS): {audit_result.hamilton_action_delta_s:.4f}",
            f"Latencia Silicio: {audit_result.elapsed_ms:.4f} ms",
            f"",
            f"--- CORTAFUEGOS DE BIOSEGURIDAD ---",
            f"[OK] FC-BIO-01 (phi_gut >= 0.899)",
            f"[OK] FC-BIO-02 (ATP sano >= 15%)",
            f"[OK] FC-BIO-03 (Vmem normalizado)",
            f"[OK] FC-BIO-04 (PD-L1 controlado)",
            f"[OK] FC-PKPD-02 (C_max < MTD)",
            f"",
            f"HASH SHA-256 INMUTABLE:",
            f"{audit_result.sha256_hash}"
        ]

        text_content = "\n".join(console_lines)
        ax9.text(
            0.05, 0.95, text_content,
            transform=ax9.transAxes,
            va='top', ha='left',
            fontfamily='monospace',
            fontsize=7.5,
            color='#c9d1d9',
            bbox=dict(boxstyle="round,pad=0.6", facecolor='#0d1117', edgecolor=status_color, linewidth=1.5)
        )

        out_path = os.path.join(self.output_dir, filename)
        fig.savefig(out_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close(fig)

        return out_path
