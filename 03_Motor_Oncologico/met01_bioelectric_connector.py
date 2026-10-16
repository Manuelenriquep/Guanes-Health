"""
MET-01 Bioelectric Connector: Coupled Proton Dynamics (pHi/pHe),
Membrane Potential (Vmem), and Connexin Gap Junction Gating (Cognitive Light Cone).

Integrates Guanes Health MET-01 proton extrusion kinetics (wtNHE1, S703A, 1K3R4E)
with Dr. Michael Levin's somatic bioelectricity and Scale of the Self framework.
"""

import json
import math
import os
import csv
import numpy as np
import matplotlib.pyplot as plt


def compute_vmem(pHi: float) -> float:
    """
    Coupled Membrane Potential Equation (mV):
    Vmem(pHi) = -30.0 - 40.0 / (1.0 + 10^((6.60 - pHi) / 0.20))
    """
    exponent = (6.60 - pHi) / 0.20
    # Clamp exponent to avoid overflow
    exponent = max(-20.0, min(20.0, exponent))
    return -30.0 - (40.0 / (1.0 + (10.0 ** exponent)))


def compute_g_gj(vmem_cell: float, vmem_stroma: float = -70.0) -> float:
    """
    Homotypic Connexin (Cx43) Transjunctional Voltage Gating:
    G_GJ(Delta_Vmem) = G_min + (G_max - G_min) / (1 + exp(A * (|Delta_Vmem| - V0)))
    """
    g_min = 0.05
    g_max = 1.00
    v0 = 25.0
    a_sens = 0.15
    delta_vmem = abs(vmem_cell - vmem_stroma)
    return g_min + (g_max - g_min) / (1.0 + math.exp(a_sens * (delta_vmem - v0)))


def j_nhe1_flux(pHi: float, pHe: float, vmax: float, pka: float, n_hill: float) -> float:
    """
    Allosteric Hill proton extrusion flux (mM/min) modulated by extracellular proton backpressure.
    """
    # Extracellular acidosis backpressure factor f(pHe) at pHe = 6.20
    f_ext = 1.0 / (1.0 + (10.0 ** (5.991 - pHe)))
    hill_term = 1.0 / (1.0 + (10.0 ** (n_hill * (pHi - pka))))
    return vmax * f_ext * hill_term


def simulate_variant(
    variant_name: str,
    vmax: float,
    pka: float,
    n_hill: float,
    pHe: float = 6.20,
    q_met_pmol_min: float = 180.0,
    n_cells: float = 20000.0,
    v_cell_l: float = 1.15e-12,
    t_max_min: float = 60.0,
    dt: float = 0.05,
):
    """
    Integrates dpHi/dt = (-q_met_cyto + J_NHE1(pHi, pHe) - J_leak(pHi)) / beta_i(pHi)
    over t in [0, t_max_min] minutes.
    """
    q_met_cyto = (q_met_pmol_min * 1e-12) / (n_cells * v_cell_l) * 1e3  # mM/min (~7.8261)
    beta_i = 28.0  # Cytosolic buffering power (mM/pH)
    pHi_init = 7.20
    pHi_floor = 5.495  # Thermodynamic acid floor under uncompensated proton leak

    steps = int(t_max_min / dt) + 1
    times = np.linspace(0.0, t_max_min, steps)
    pHi_arr = np.zeros(steps)
    vmem_arr = np.zeros(steps)
    ggj_arr = np.zeros(steps)
    clc_arr = np.zeros(steps)

    pHi = pHi_init
    for idx, t in enumerate(times):
        vmem = compute_vmem(pHi)
        ggj = compute_g_gj(vmem)
        clc = ggj / 1.00

        pHi_arr[idx] = pHi
        vmem_arr[idx] = vmem
        ggj_arr[idx] = ggj
        clc_arr[idx] = clc

        if idx < steps - 1:
            j_pump = j_nhe1_flux(pHi, pHe, vmax, pka, n_hill)
            # Passive proton leak / thermodynamic floor stabilization near pHi 5.495
            j_floor_restore = max(0.0, (pHi_floor - pHi) * 18.0)
            dpHi_dt = (-q_met_cyto + j_pump + j_floor_restore) / beta_i
            pHi = max(pHi_floor, pHi + dpHi_dt * dt)

    return {
        "variant": variant_name,
        "time_min": times,
        "pHi": pHi_arr,
        "Vmem_mV": vmem_arr,
        "G_GJ": ggj_arr,
        "CLC_Index": clc_arr,
    }


def run_connector_suite():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Variants from met01_coupled_proton_ledger.json
    res_s703a = simulate_variant("S703A", vmax=10.0, pka=6.15, n_hill=3.0)
    res_1k3r4e = simulate_variant("1K3R4E", vmax=22.0, pka=6.75, n_hill=2.5)

    print("=======================================================================")
    print("BIOELECTRIC CONNECTOR SIMULATION SUMMARY (pHe = 6.20 Stromal Acidosis)")
    print("=======================================================================")
    for res, desc in [
        (res_s703a, "S703A (Mutante Defectivo / RSK-defective)"),
        (res_1k3r4e, "1K3R4E (Blindaje Constitutivo / Constitutively Active)"),
    ]:
        phi_f = res["pHi"][-1]
        vmem_f = res["Vmem_mV"][-1]
        ggj_f = res["G_GJ"][-1]
        clc_f = res["CLC_Index"][-1]
        state = (
            "INTEGRATED SELF (Functional)"
            if clc_f >= 0.70
            else "SHRUNK SELF (Physiological Disconnection / Anergy)"
        )
        print(f"Variant: {desc}")
        print(f"  Final pHi:       {phi_f:.3f}")
        print(f"  Final Vmem:      {vmem_f:.2f} mV")
        print(f"  Final G_GJ:      {ggj_f:.3f}")
        print(f"  Final CLC Index: {clc_f:.3f}")
        print(f"  Cognitive State: {state}")
        print("-----------------------------------------------------------------------")

    # Export time-series CSV
    csv_path = os.path.join(base_dir, "met01_bioelectric_connector.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "time_min",
            "S703A_pHi",
            "S703A_Vmem_mV",
            "S703A_G_GJ",
            "S703A_CLC",
            "1K3R4E_pHi",
            "1K3R4E_Vmem_mV",
            "1K3R4E_G_GJ",
            "1K3R4E_CLC",
        ])
        for i in range(0, len(res_s703a["time_min"]), 10):
            writer.writerow([
                f"{res_s703a['time_min'][i]:.2f}",
                f"{res_s703a['pHi'][i]:.4f}",
                f"{res_s703a['Vmem_mV'][i]:.3f}",
                f"{res_s703a['G_GJ'][i]:.4f}",
                f"{res_s703a['CLC_Index'][i]:.4f}",
                f"{res_1k3r4e['pHi'][i]:.4f}",
                f"{res_1k3r4e['Vmem_mV'][i]:.3f}",
                f"{res_1k3r4e['G_GJ'][i]:.4f}",
                f"{res_1k3r4e['CLC_Index'][i]:.4f}",
            ])

    # Generate 4-Panel Dashboard PNG
    fig, axes = plt.subplots(2, 2, figsize=(13, 9.5), dpi=220)
    fig.patch.set_facecolor("#0b0f19")
    for ax in axes.flat:
        ax.set_facecolor("#111827")
        ax.tick_params(colors="#cbd5e1")
        for spine in ax.spines.values():
            spine.set_color("#334155")
        ax.grid(True, linestyle="--", alpha=0.25, color="#64748b")

    t = res_s703a["time_min"]

    # Panel A: pHi Evolution
    ax = axes[0, 0]
    ax.plot(t, res_1k3r4e["pHi"], color="#a855f7", lw=2.6, label="1K3R4E (Constitutive NHE1-Shield)")
    ax.plot(t, res_s703a["pHi"], color="#f97316", lw=2.6, label="S703A (RSK-Defective Mutant)")
    ax.axhline(6.60, color="#ef4444", ls=":", lw=1.5, label="Gated-6.60 Anergy Threshold")
    ax.set_title("A. Cytosolic pHi Kinetics under Stromal Acidosis (pHe = 6.20)", color="#f8fafc", fontweight="bold")
    ax.set_xlabel("Time (min)", color="#94a3b8")
    ax.set_ylabel("Intracellular pHi", color="#94a3b8")
    ax.legend(facecolor="#1e293b", edgecolor="#475569", labelcolor="#f8fafc", fontsize=8.5)

    # Panel B: Vmem Coupling
    ax = axes[0, 1]
    ax.plot(t, res_1k3r4e["Vmem_mV"], color="#a855f7", lw=2.6, label="1K3R4E (-60.17 mV | Hyperpolarized)")
    ax.plot(t, res_s703a["Vmem_mV"], color="#f97316", lw=2.6, label="S703A (-30.00 mV | Depolarized)")
    ax.axhline(-70.0, color="#22c55e", ls="--", lw=1.3, label="Healthy Stroma Setpoint (-70 mV)")
    ax.set_title("B. Coupled Membrane Potential Vmem(t) Dynamics", color="#f8fafc", fontweight="bold")
    ax.set_xlabel("Time (min)", color="#94a3b8")
    ax.set_ylabel("Membrane Potential Vmem (mV)", color="#94a3b8")
    ax.legend(facecolor="#1e293b", edgecolor="#475569", labelcolor="#f8fafc", fontsize=8.5)

    # Panel C: Cognitive Light Cone Index (CLC)
    ax = axes[1, 0]
    ax.plot(t, res_1k3r4e["CLC_Index"], color="#a855f7", lw=2.6, label="1K3R4E (CLC = 0.911 | Integrated Self)")
    ax.plot(t, res_s703a["CLC_Index"], color="#f97316", lw=2.6, label="S703A (CLC = 0.141 | Shrunk Self / Anergy)")
    ax.axhline(0.70, color="#22c55e", ls=":", lw=1.4, label="Collective Integration Boundary (0.70)")
    ax.axhline(0.30, color="#ef4444", ls=":", lw=1.4, label="Cognitive Light Cone Collapse (0.30)")
    ax.set_ylim(0.0, 1.05)
    ax.set_title("C. Cognitive Light Cone Index (CLC = G_GJ / G_max)", color="#f8fafc", fontweight="bold")
    ax.set_xlabel("Time (min)", color="#94a3b8")
    ax.set_ylabel("CLC Index / Cx43 Conductance", color="#94a3b8")
    ax.legend(facecolor="#1e293b", edgecolor="#475569", labelcolor="#f8fafc", fontsize=8.5)

    # Panel D: Phase Space Vmem vs pHi
    ax = axes[1, 1]
    pHi_curve = np.linspace(5.40, 7.40, 200)
    vmem_curve = [compute_vmem(p) for p in pHi_curve]
    ax.plot(pHi_curve, vmem_curve, color="#38bdf8", lw=2.0, alpha=0.6, label="Sigmoidal Coupling Curve Vmem(pHi)")
    ax.scatter([res_1k3r4e["pHi"][-1]], [res_1k3r4e["Vmem_mV"][-1]], color="#a855f7", s=110, zorder=5, label="1K3R4E Equilibrium (pHi 6.70, -60.2 mV)")
    ax.scatter([res_s703a["pHi"][-1]], [res_s703a["Vmem_mV"][-1]], color="#f97316", s=110, zorder=5, label="S703A Equilibrium (pHi 5.50, -30.0 mV)")
    ax.set_title("D. Electro-Metabolic Phase Space: Vmem vs. pHi", color="#f8fafc", fontweight="bold")
    ax.set_xlabel("Cytosolic pHi", color="#94a3b8")
    ax.set_ylabel("Membrane Potential Vmem (mV)", color="#94a3b8")
    ax.legend(facecolor="#1e293b", edgecolor="#475569", labelcolor="#f8fafc", fontsize=8.5)

    plt.suptitle(
        "GUANES HEALTH × LEVIN FRAMEWORK: MET-01 Bioelectric Connector (pHe = 6.20, q_met = 180 pmol/min)",
        color="#f8fafc",
        fontsize=13,
        fontweight="bold",
        y=0.98,
    )
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    png_path = os.path.join(base_dir, "met01_bioelectric_connector_dashboard.png")
    plt.savefig(png_path, dpi=220, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Saved CSV: {csv_path}")
    print(f"Saved Dashboard PNG: {png_path}")


if __name__ == "__main__":
    run_connector_suite()
