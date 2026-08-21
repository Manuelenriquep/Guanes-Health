import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
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

def generar_analisis_cointervencion():
    print("[*] Comparativa de 4 escenarios (modelo acoplado v3)...")
    sim = SimuladorOncoHepaticoBidireccional()
    
    # Ejecutar las 4 simulaciones temporales
    # Escenario 1: Control (Secuencial Estándar Sin Feedback ni Myrcludex)
    res_esc1 = sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=False, feedback_activo=False, myrcludex_nM=0.0)
    
    # Escenario 2: Escape MCT2 Unidireccional (Sin feedback, con mutación de escape MCT2)
    res_esc2 = sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=True, feedback_activo=False, myrcludex_nM=0.0)
    
    # Escenario 3: Retroalimentación Activa (feedback activo, sin Myrcludex)
    res_esc3 = sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=False, feedback_activo=True, myrcludex_nM=0.0)
    
    # Escenario 4: Co-intervención (Myrcludex 10 nM + atenuación IL-6/STAT3 via beta_pd_l1)
    res_esc4 = sim.ejecutar_simulacion(
        cohorte="C",
        mutacion_mct2=False,
        feedback_activo=True,
        myrcludex_nM=10.0,
        beta_pd_l1=0.1,
    )
    
    tiempo = res_esc1["tiempo"]
    
    fig, axs = plt.subplots(2, 2, figsize=(14, 10), dpi=150)
    fig.suptitle(
        "Comparativa de escenarios (modelo onco-hepatico v3)\n"
        "Myrcludex B, feedback IL-6/PD-L1 y Cohorte C (Gated-6.50)",
        fontsize=14,
        fontweight="bold",
    )
    
    colores = {
        "S1": "#2ca02c",
        "S2": "#d62728",
        "S3": "#ff7f0e",
        "S4": "#1f77b4",
    }
    
    estilos = {
        "S1": "-",
        "S2": "--",
        "S3": "-.",
        "S4": "-",
    }
    
    axs[0, 0].plot(tiempo, [v*100 for v in res_esc1["viabilidad_tumor"]], label="S1: Control", color=colores["S1"], linestyle=estilos["S1"], linewidth=2)
    axs[0, 0].plot(tiempo, [v*100 for v in res_esc2["viabilidad_tumor"]], label="S2: Escape MCT2", color=colores["S2"], linestyle=estilos["S2"], linewidth=2)
    axs[0, 0].plot(tiempo, [v*100 for v in res_esc3["viabilidad_tumor"]], label="S3: Feedback activo", color=colores["S3"], linestyle=estilos["S3"], linewidth=2)
    axs[0, 0].plot(tiempo, [v*100 for v in res_esc4["viabilidad_tumor"]], label="S4: Co-intervencion", color=colores["S4"], linestyle=estilos["S4"], linewidth=2.5)
    axs[0, 0].set_title("Viabilidad tumoral (%)", fontsize=11, fontweight="bold")
    axs[0, 0].set_xlabel("Tiempo (horas)")
    axs[0, 0].set_ylabel("Viabilidad (%)")
    axs[0, 0].grid(True, linestyle=":", alpha=0.6)
    axs[0, 0].axvline(12.0, color="gray", linestyle=":", label="MCT1/4 (t=12h)")
    axs[0, 0].axvline(24.0, color="purple", linestyle=":", label="Inmunoterapia (t=24h)")
    axs[0, 0].legend(fontsize=8, loc="lower left")
    
    axs[0, 1].plot(tiempo, res_esc1["carga_viral"], label="S1: Control", color=colores["S1"], linestyle=estilos["S1"], linewidth=2)
    axs[0, 1].plot(tiempo, res_esc2["carga_viral"], label="S2: Escape MCT2", color=colores["S2"], linestyle=estilos["S2"], linewidth=2)
    axs[0, 1].plot(tiempo, res_esc3["carga_viral"], label="S3: Feedback activo", color=colores["S3"], linestyle=estilos["S3"], linewidth=2)
    axs[0, 1].plot(tiempo, res_esc4["carga_viral"], label="S4: Co-intervencion", color=colores["S4"], linestyle=estilos["S4"], linewidth=2.5)
    axs[0, 1].set_title("Carga viral HBV (hepatocito)", fontsize=11, fontweight="bold")
    axs[0, 1].set_xlabel("Tiempo (horas)")
    axs[0, 1].set_ylabel("Viriones (modelo)")
    axs[0, 1].grid(True, linestyle=":", alpha=0.6)
    axs[0, 1].legend(fontsize=8, loc="upper left")
    
    axs[1, 0].plot(tiempo, res_esc1["il6"], label="S1: Control", color=colores["S1"], linestyle=estilos["S1"], linewidth=2)
    axs[1, 0].plot(tiempo, res_esc2["il6"], label="S2: Escape MCT2", color=colores["S2"], linestyle=estilos["S2"], linewidth=2)
    axs[1, 0].plot(tiempo, res_esc3["il6"], label="S3: Feedback activo", color=colores["S3"], linestyle=estilos["S3"], linewidth=2)
    axs[1, 0].plot(tiempo, res_esc4["il6"], label="S4: Co-intervencion", color=colores["S4"], linestyle=estilos["S4"], linewidth=2.5)
    axs[1, 0].set_title("IL-6 estromal (pg/mL, modelo)", fontsize=11, fontweight="bold")
    axs[1, 0].set_xlabel("Tiempo (horas)")
    axs[1, 0].set_ylabel("IL-6 (pg/mL)")
    axs[1, 0].grid(True, linestyle=":", alpha=0.6)
    axs[1, 0].legend(fontsize=8, loc="upper left")
    
    axs[1, 1].plot(tiempo, res_esc1["pd_l1_tumor"], label="S1: Basal", color=colores["S1"], linestyle=estilos["S1"], linewidth=2)
    axs[1, 1].plot(tiempo, res_esc2["pd_l1_tumor"], label="S2: Basal", color=colores["S2"], linestyle=estilos["S2"], linewidth=2)
    axs[1, 1].plot(tiempo, res_esc3["pd_l1_tumor"], label="S3: Feedback (PD-L1 alto)", color=colores["S3"], linestyle=estilos["S3"], linewidth=2)
    axs[1, 1].plot(tiempo, res_esc4["pd_l1_tumor"], label="S4: beta atenuado", color=colores["S4"], linestyle=estilos["S4"], linewidth=2.5)
    axs[1, 1].axhline(150.0, color="red", linestyle=":", label="Umbral saturacion anti-PD-1 (150x)")
    axs[1, 1].set_title("PD-L1 tumoral (relativo)", fontsize=11, fontweight="bold")
    axs[1, 1].set_xlabel("Tiempo (horas)")
    axs[1, 1].set_ylabel("Densidad relativa")
    axs[1, 1].grid(True, linestyle=":", alpha=0.6)
    axs[1, 1].legend(fontsize=8, loc="upper left")
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    out_img_path = os.path.join(visuales_dir(), "cointervencion_escenarios.png")
    plt.savefig(out_img_path, dpi=150, bbox_inches="tight")
    plt.close()
    
    print(f"[OK] Figura: {out_img_path}")
    print(f"    S4 viabilidad tumoral terminal: {res_esc4['viabilidad_tumor'][-1]*100:.2f}%")
    print(f"    S4 carga viral terminal: {res_esc4['carga_viral'][-1]:.2f}")
    print(f"    S4 PD-L1 terminal: {res_esc4['pd_l1_tumor'][-1]:.2f}x")


if __name__ == "__main__":
    generar_analisis_cointervencion()
