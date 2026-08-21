"""
Figura ilustrativa: dinámica IL-6 / PD-L1 (acoplamiento canónico v3).
Salida de modelo — no evidencia clínica.
"""
import os
import sys

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

_MOTOR_DIR = os.path.abspath(os.path.dirname(__file__))
if _MOTOR_DIR not in sys.path:
    sys.path.insert(0, _MOTOR_DIR)

from simulador_onco_hepatico_v3 import SimuladorOncoHepaticoBidireccional


def visuales_dir():
    path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "02_Simulaciones_Visuales")
    )
    os.makedirs(path, exist_ok=True)
    return path


def generar_analisis_grafico():
    print("[*] Dinamica IL-6/PD-L1 (modelo acoplado v3, Gated-6.50)...")
    sim = SimuladorOncoHepaticoBidireccional()

    res = sim.ejecutar_simulacion(
        cohorte="C",
        mutacion_mct2=False,
        inhibicion_mct2=False,
        infeccion_hbv=True,
        inóculo_tasa=10.0,
        myrcludex_nM=0.0,
        feedback_activo=True,
        beta_pd_l1=3.0,
    )

    tiempo = res["tiempo"]
    il6 = np.array(res["il6"])
    pd_l1 = np.array(res["pd_l1_tumor"])

    umbral_pd_l1 = 150.0
    idx_escape = np.where(pd_l1 >= umbral_pd_l1)[0]

    if len(idx_escape) > 0:
        t_escape = tiempo[idx_escape[0]]
        il6_escape = il6[idx_escape[0]]
        pd_l1_escape = pd_l1[idx_escape[0]]
        print(f"[+] t_escape modelado = {t_escape:.2f} h")
        print(f"    IL-6={il6_escape:.2f}  PD-L1={pd_l1_escape:.2f}x")
    else:
        t_escape = None
        il6_escape = None
        pd_l1_escape = None
        print("[-] Sin cruce del umbral PD-L1=150 en la ventana.")

    fig, ax1 = plt.subplots(figsize=(10, 6), dpi=150)

    color_il6 = "#d9534f"
    line1 = ax1.plot(
        tiempo, il6, color=color_il6, linewidth=2.5, label=r"$[IL-6]$ (modelo)"
    )
    ax1.set_xlabel("Tiempo (horas)", fontsize=12, fontweight="bold", labelpad=10)
    ax1.set_ylabel(
        r"$IL-6$ (pg/mL, modelo)", color=color_il6, fontsize=12, fontweight="bold"
    )
    ax1.tick_params(axis="y", labelcolor=color_il6)
    ax1.grid(True, linestyle="--", alpha=0.5)

    ax2 = ax1.twinx()
    color_pdl1 = "#337ab7"
    line2 = ax2.plot(
        tiempo,
        pd_l1,
        color=color_pdl1,
        linewidth=2.5,
        linestyle="--",
        label=r"$PD-L1$ tumoral ($x$)",
    )
    ax2.set_ylabel(
        r"$PD-L1$ relativo ($x$)", color=color_pdl1, fontsize=12, fontweight="bold"
    )
    ax2.tick_params(axis="y", labelcolor=color_pdl1)

    ax2.axhline(
        y=umbral_pd_l1,
        color="purple",
        linestyle=":",
        alpha=0.75,
        linewidth=1.5,
        label="Umbral anti-PD-1 (150x, modelo)",
    )

    if t_escape is not None:
        ax1.axvline(x=t_escape, color="darkorange", linestyle="-.", alpha=0.9, linewidth=1.8)
        ax2.scatter(
            [t_escape],
            [pd_l1_escape],
            color="darkorange",
            s=100,
            zorder=5,
            edgecolor="black",
            linewidth=1.5,
        )
        if t_escape > 12.0:
            ax1.axvspan(12.0, t_escape, color="green", alpha=0.1)
        else:
            ax1.axvspan(0.0, t_escape, color="green", alpha=0.1)
        ax1.axvspan(t_escape, 72.0, color="red", alpha=0.08)
        ax1.annotate(
            f"$t_{{escape}} = {t_escape:.2f}\\,h$\n$[IL-6] = {il6_escape:.1f}$",
            xy=(t_escape, il6_escape),
            xytext=(t_escape + 5, il6_escape + 80),
            arrowprops=dict(facecolor="black", shrink=0.05, width=1, headwidth=6),
            fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.9),
        )

    lines = line1 + line2 + [
        matplotlib.lines.Line2D([0], [0], color="purple", linestyle=":")
    ]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper left", frameon=True, framealpha=0.9)

    plt.title(
        "Dinamica temporal (modelo v3): IL-6 / PD-L1 y t_escape",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )

    out_path = os.path.join(visuales_dir(), "dinamica_temporal_il6_pdl1.png")
    plt.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close()
    print(f"[OK] Figura: {out_path}")


if __name__ == "__main__":
    generar_analisis_grafico()
