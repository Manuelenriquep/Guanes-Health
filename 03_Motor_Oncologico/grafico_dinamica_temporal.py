import sys
import os
import numpy as np

# Asegurar importación de artifacts
sys.path.append("/workspace/artifacts")
sys.path.append("/workspace/scratch")

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from simulador_onco_hepatico_v2 import SimuladorOncoHepaticoBidireccional

def generar_analisis_grafico():
    print("[*] Iniciando simulación de retroalimentación acoplada para análisis dinámico...")
    sim = SimuladorOncoHepaticoBidireccional()
    
    # Ejecutar escenario con feedback activo (Opción A)
    res = sim.ejecutar_simulacion(
        cohorte="C", 
        mutacion_mct2=False, 
        inhibicion_mct2=False,
        infeccion_hbv=True, 
        inóculo_tasa=10.0, 
        myrcludex_nM=0.0,
        feedback_activo=True, 
        beta_pd_l1=3.0
    )
    
    tiempo = res["tiempo"]
    il6 = np.array(res["il6"])
    pd_l1 = np.array(res["pd_l1_tumor"])
    viab_tumor = np.array(res["viabilidad_tumor"])
    
    # Encontrar t_escape (donde PD-L1 >= 150.0x por primera vez)
    umbral_pd_l1 = 150.0
    idx_escape = np.where(pd_l1 >= umbral_pd_l1)[0]
    
    if len(idx_escape) > 0:
        t_escape = tiempo[idx_escape[0]]
        il6_escape = il6[idx_escape[0]]
        pd_l1_escape = pd_l1[idx_escape[0]]
        print(f"[+] Bifurcación temporal localizada a t = {t_escape:.2f} h")
        print(f"    * Concentración de IL-6 en escape: {il6_escape:.2f} pg/mL")
        print(f"    * Expresión de PD-L1 en escape: {pd_l1_escape:.2f}x")
    else:
        t_escape = None
        print("[-] Advertencia: No se detectó un cruce del umbral de escape en la ventana evaluada.")

    # Crear figura y ejes duales
    fig, ax1 = plt.subplots(figsize=(10, 6), dpi=150)
    
    # Eje Izquierdo: IL-6 (pg/mL)
    color_il6 = '#d9534f'
    line1 = ax1.plot(tiempo, il6, color=color_il6, linewidth=2.5, label=r'$[IL-6]$ Sinusoidal')
    ax1.set_xlabel('Tiempo de Simulación (horas)', fontsize=12, fontweight='bold', labelpad=10)
    ax1.set_ylabel(r'Concentración de $IL-6$ ($pg/mL$)', color=color_il6, fontsize=12, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=color_il6)
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    # Eje Derecho: PD-L1 Expresión en Tumor
    ax2 = ax1.twinx()
    color_pdl1 = '#337ab7'
    line2 = ax2.plot(tiempo, pd_l1, color=color_pdl1, linewidth=2.5, linestyle='--', label=r'$PD-L1$ Tumoral ($x$)')
    ax2.set_ylabel(r'Expresión Relativa de $PD-L1$ en Membrana ($x$)', color=color_pdl1, fontsize=12, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=color_pdl1)
    
    # Marcar umbral de saturación de anti-PD-1 (150x)
    ax2.axhline(y=umbral_pd_l1, color='purple', linestyle=':', alpha=0.75, linewidth=1.5, 
                label='Umbral de Saturación anti-PD-1 (150x)')
    
    # Resaltar la bifurcación temporal t_escape
    if t_escape is not None:
        # Línea vertical en t_escape
        ax1.axvline(x=t_escape, color='darkorange', linestyle='-.', alpha=0.9, linewidth=1.8)
        
        # Marcador en la curva de PD-L1
        ax2.scatter([t_escape], [pd_l1_escape], color='darkorange', s=100, zorder=5, edgecolor='black', linewidth=1.5)
        
        # Sombrear la Ventana de Co-Intervención (desde t_metabolico = 12.0h hasta t_escape)
        # Nota: Como t_escape ocurre a t=1.8h (antes de t_metabolico=12.0h debido a la velocidad de la infección),
        # esto demuestra la necesidad clínica de adelantar la terapia con Myrcludex B antes del inicio del inóculo.
        if t_escape > 12.0:
            ax1.axvspan(12.0, t_escape, color='green', alpha=0.1, label='Ventana de Co-Intervención')
            ax1.text(12.2, 350, 'Ventana\nTerapéutica\nÓptima', color='green', fontweight='bold', fontsize=9, alpha=0.85)
        else:
            # Si el escape ocurre prematuramente antes del tratamiento
            ax1.axvspan(0.0, t_escape, color='green', alpha=0.1, label='Fase Pre-escape Crítica')
            ax1.text(0.2, 350, 'Ventana\nPre-escape', color='green', fontweight='bold', fontsize=9, alpha=0.85)
        
        ax1.axvspan(t_escape, 72.0, color='red', alpha=0.08, label='Escape Inmune & Anergia')
        
        # Anotación del punto crítico de escape
        ax1.annotate(f'Punto de Escape\n$t_{{escape}} = {t_escape:.2f}\\ h$\n$[IL-6] = {il6_escape:.1f}\\ pg/mL$',
                     xy=(t_escape, il6_escape),
                     xytext=(t_escape + 5, il6_escape + 80),
                     arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
                     fontweight='bold', fontsize=9, bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.8))

    # Combinar leyendas de ejes distintos
    lines = line1 + line2 + [matplotlib.lines.Line2D([0], [0], color='purple', linestyle=':')]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', frameon=True, framealpha=0.9)
    
    plt.title('Dinámica Temporal Acoplada: Bucle de Retroalimentación HBV/IL-6 -> PD-L1', 
              fontsize=14, fontweight='bold', pad=15)
    
    # Guardar en scratch
    out_path_scratch = "/workspace/scratch/dinamica_temporal_il6_pdl1.png"
    plt.savefig(out_path_scratch, bbox_inches='tight', dpi=150)
    plt.close()
    
    # Copiar a out
    out_path_publish = "/workspace/out/dinamica_temporal_il6_pdl1.png"
    import shutil
    shutil.copy(out_path_scratch, out_path_publish)
    print(f"[✔] ÉXITO: Gráfico publicado correctamente en {out_path_publish}")

if __name__ == "__main__":
    generar_analisis_grafico()
