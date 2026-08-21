import sys
import os
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Asegurar importación de los módulos de simulación del workspace
sys.path.append("/workspace/artifacts")
sys.path.append("/workspace/scratch")

from simulador_onco_hepatico_v2 import SimuladorOncoHepaticoBidireccional

def generar_analisis_cointervencion():
    print("[*] Iniciando simulación comparativa de los 4 escenarios terapéuticos...")
    sim = SimuladorOncoHepaticoBidireccional()
    
    # Ejecutar las 4 simulaciones temporales
    # Escenario 1: Control (Secuencial Estándar Sin Feedback ni Myrcludex)
    res_esc1 = sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=False, feedback_activo=False, myrcludex_nM=0.0)
    
    # Escenario 2: Escape MCT2 Unidireccional (Sin feedback, con mutación de escape MCT2)
    res_esc2 = sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=True, feedback_activo=False, myrcludex_nM=0.0)
    
    # Escenario 3: Retroalimentación Activa (Con mutación, feedback activo, sin Myrcludex)
    res_esc3 = sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=False, feedback_activo=True, myrcludex_nM=0.0)
    
    # Escenario 4: Co-Intervención Estratégica (Con mutación, feedback activo, pre-tratamiento Myrcludex B 10 nM)
    res_esc4 = sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=False, feedback_activo=True, myrcludex_nM=10.0)
    
    tiempo = res_esc1["tiempo"]
    
    # Configurar gráficos comparativos de alta resolución (2x2 subplots)
    fig, axs = plt.subplots(2, 2, figsize=(14, 10), dpi=150)
    fig.suptitle("EVALUACIÓN MULTIESCALA DE LA CO-INTERVENCIÓN DE MYRCLUDEX B\nSinergia de Bloqueo Viral y Kinetic Priming de la Cohorte C", fontsize=14, fontweight="bold")
    
    colores = {
        "S1": "#2ca02c",  # Verde: Control exitoso
        "S2": "#d62728",  # Rojo: Escape MCT2
        "S3": "#ff7f0e",  # Naranja: Escape inducido por HBV (STAT3)
        "S4": "#1f77b4"   # Azul: Curación completa / Co-Intervención
    }
    
    estilos = {
        "S1": "-", 
        "S2": "--", 
        "S3": "-.", 
        "S4": "-"
    }
    
    # Subplot 1: Viabilidad Tumoral
    axs[0, 0].plot(tiempo, [v*100 for v in res_esc1["viabilidad_tumor"]], label="S1: Control (Lisis CD8+ Exitosa)", color=colores["S1"], linestyle=estilos["S1"], linewidth=2)
    axs[0, 0].plot(tiempo, [v*100 for v in res_esc2["viabilidad_tumor"]], label="S2: Escape MCT2 (Santuario Viral)", color=colores["S2"], linestyle=estilos["S2"], linewidth=2)
    axs[0, 0].plot(tiempo, [v*100 for v in res_esc3["viabilidad_tumor"]], label="S3: Feedback Activo (Escape STAT3)", color=colores["S3"], linestyle=estilos["S3"], linewidth=2)
    axs[0, 0].plot(tiempo, [v*100 for v in res_esc4["viabilidad_tumor"]], label="S4: Co-Intervención (Aclaramiento)", color=colores["S4"], linestyle=estilos["S4"], linewidth=2.5)
    axs[0, 0].set_title("Viabilidad Tumoral (%)", fontsize=11, fontweight="bold")
    axs[0, 0].set_xlabel("Tiempo (horas)")
    axs[0, 0].set_ylabel("Viabilidad (%)")
    axs[0, 0].grid(True, linestyle=":", alpha=0.6)
    axs[0, 0].axvline(12.0, color="gray", linestyle=":", label="Bloqueo MCT1/4 (t=12h)")
    axs[0, 0].axvline(24.0, color="purple", linestyle=":", label="Inmunoterapia (t=24h)")
    axs[0, 0].legend(fontsize=8, loc="lower left")
    
    # Subplot 2: Carga Viral Intracelular (HBV)
    axs[0, 1].plot(tiempo, res_esc1["carga_viral"], label="S1: Control (Depurada por CD8+)", color=colores["S1"], linestyle=estilos["S1"], linewidth=2)
    axs[0, 1].plot(tiempo, res_esc2["carga_viral"], label="S2: Escape MCT2 (Santuario Activo)", color=colores["S2"], linestyle=estilos["S2"], linewidth=2)
    axs[0, 1].plot(tiempo, res_esc3["carga_viral"], label="S3: Feedback Activo (Cronicidad)", color=colores["S3"], linestyle=estilos["S3"], linewidth=2)
    axs[0, 1].plot(tiempo, res_esc4["carga_viral"], label="S4: Co-Intervención (Bloqueo de Entrada)", color=colores["S4"], linestyle=estilos["S4"], linewidth=2.5)
    axs[0, 1].set_title("Carga Viral de HBV en Hepatocitos", fontsize=11, fontweight="bold")
    axs[0, 1].set_xlabel("Tiempo (horas)")
    axs[0, 1].set_ylabel("Viriones Intracelulares")
    axs[0, 1].grid(True, linestyle=":", alpha=0.6)
    axs[0, 1].legend(fontsize=8, loc="upper left")
    
    # Subplot 3: Concentración de IL-6 Sinusoidal
    axs[1, 0].plot(tiempo, res_esc1["il6"], label="S1: Control (Aclarado)", color=colores["S1"], linestyle=estilos["S1"], linewidth=2)
    axs[1, 0].plot(tiempo, res_esc2["il6"], label="S2: Escape MCT2 (Sin Daño)", color=colores["S2"], linestyle=estilos["S2"], linewidth=2)
    axs[1, 0].plot(tiempo, res_esc3["il6"], label="S3: Feedback Activo (Inundación)", color=colores["S3"], linestyle=estilos["S3"], linewidth=2)
    axs[1, 0].plot(tiempo, res_esc4["il6"], label="S4: Co-Intervención (Yugulación)", color=colores["S4"], linestyle=estilos["S4"], linewidth=2.5)
    axs[1, 0].set_title("Concentración de IL-6 Estromal (pg/mL)", fontsize=11, fontweight="bold")
    axs[1, 0].set_xlabel("Tiempo (horas)")
    axs[1, 0].set_ylabel("IL-6 (pg/mL)")
    axs[1, 0].grid(True, linestyle=":", alpha=0.6)
    axs[1, 0].legend(fontsize=8, loc="upper left")
    
    # Subplot 4: Expresión de PD-L1 en Células Tumorales
    axs[1, 1].plot(tiempo, res_esc1["pd_l1_tumor"], label="S1: Basal (50.0x)", color=colores["S1"], linestyle=estilos["S1"], linewidth=2)
    axs[1, 1].plot(tiempo, res_esc2["pd_l1_tumor"], label="S2: Basal (50.0x)", color=colores["S2"], linestyle=estilos["S2"], linewidth=2)
    axs[1, 1].plot(tiempo, res_esc3["pd_l1_tumor"], label="S3: Inducido STAT3 (>1200x)", color=colores["S3"], linestyle=estilos["S3"], linewidth=2)
    axs[1, 1].plot(tiempo, res_esc4["pd_l1_tumor"], label="S4: Bloqueado por Myrcludex", color=colores["S4"], linestyle=estilos["S4"], linewidth=2.5)
    axs[1, 1].axhline(150.0, color="red", linestyle=":", label="Umbral Saturación Checkpoint (150x)")
    axs[1, 1].set_title("Nivel de Expresión de PD-L1 Tumoral", fontsize=11, fontweight="bold")
    axs[1, 1].set_xlabel("Tiempo (horas)")
    axs[1, 1].set_ylabel("Densidad Superficial (Relativa)")
    axs[1, 1].grid(True, linestyle=":", alpha=0.6)
    axs[1, 1].legend(fontsize=8, loc="upper left")
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    out_img_path = "/workspace/scratch/cointervencion_curacion_grafico.png"
    plt.savefig(out_img_path, dpi=150, bbox_inches="tight")
    plt.close()
    
    print(f"[✔] ÉXITO: Imagen comparativa de 4 escenarios guardada en {out_img_path}")
    print(f"    * Escenario 4 Viabilidad Tumoral Terminal: {res_esc4['viabilidad_tumor'][-1]*100:.2f}%")
    print(f"    * Escenario 4 Carga Viral Terminal: {res_esc4['carga_viral'][-1]:.2f} viriones")
    print(f"    * Escenario 4 PD-L1 Terminal: {res_esc4['pd_l1_tumor'][-1]:.2f}x")

if __name__ == "__main__":
    generar_analisis_cointervencion()
