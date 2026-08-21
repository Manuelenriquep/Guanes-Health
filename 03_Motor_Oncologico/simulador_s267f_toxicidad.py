import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

_MOTOR_DIR = os.path.abspath(os.path.dirname(__file__))
if _MOTOR_DIR not in sys.path:
    sys.path.insert(0, _MOTOR_DIR)

from simulador_hepatocito_infeccion import HepatocitoInmuneIntegrado


def visuales_dir():
    path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "02_Simulaciones_Visuales")
    )
    os.makedirs(path, exist_ok=True)
    return path

def correr_barrido(es_mutante=False):
    myr_concentraciones = [0.0, 1.0, 5.0, 10.0, 50.0, 100.0, 250.0, 500.0, 750.0, 1000.0]
    cargas_virales = []
    aclaramientos = []
    gsh_pools = []
    viabilidades = []
    
    tiempo_total = 72.0
    dt = 0.5
    pasos = int(tiempo_total / dt)
    inoculo_diario = 2.0
    
    for myr in myr_concentraciones:
        # Inicializar hepatocito en Zona 1 (Periportal, o2_pp = 60.0 mmHg)
        hep = HepatocitoInmuneIntegrado(gsh_nominal=8.0, o2_pp=60.0)
        hep.es_variante_S267F = es_mutante
        hep.myrcludex_b_nM = myr
        hep.il6_concentracion = 0.0
        
        # Simular 72 horas
        for _ in range(pasos):
            res = hep.evaluar_regulacion_y_entrada_viral(
                inoculo_HBV=inoculo_diario, delta_t=dt
            )
            if isinstance(res, str):  # Inactivo por muerte
                break
                
        # Registrar estados finales
        if hep.viabilidad <= 0.0:
            cargas_virales.append(hep.carga_viral_de_novo)
            aclaramientos.append(0.0)
            gsh_pools.append(0.0)
            viabilidades.append(0.0)
        else:
            cargas_virales.append(hep.carga_viral_de_novo)
            fraccion_bloqueo_biliar = 1.0 / (1.0 + (hep.myrcludex_b_nM / 100.0))
            aclaramientos.append(hep.ntcp_densidad_membrana * fraccion_bloqueo_biliar)
            gsh_pools.append(hep.gsh_pool)
            viabilidades.append(hep.viabilidad)
            
    return myr_concentraciones, cargas_virales, aclaramientos, gsh_pools, viabilidades

if __name__ == "__main__":
    print("[*] Ejecutando barrido de Myrcludex B para Wild-Type y Variante S267F...")
    
    myr, cv_wt, acl_wt, gsh_wt, viab_wt = correr_barrido(es_mutante=False)
    _, cv_mut, acl_mut, gsh_mut, viab_mut = correr_barrido(es_mutante=True)
    
    print("\nResultados Wild-Type (WT):")
    for i, m in enumerate(myr):
        print(f"Myr: {m:6.1f} nM | Viral: {cv_wt[i]:6.2f} | Biliar: {acl_wt[i]:5.2f} | GSH: {gsh_wt[i]:5.2f} | Viab: {viab_wt[i]*100:5.1f}%")
        
    print("\nResultados Variante S267F:")
    for i, m in enumerate(myr):
        print(f"Myr: {m:6.1f} nM | Viral: {cv_mut[i]:6.2f} | Biliar: {acl_mut[i]:5.2f} | GSH: {gsh_mut[i]:5.2f} | Viab: {viab_mut[i]*100:5.1f}%")
        
    # Graficar
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Estudio Comparativo Multiescala: Wild-Type vs. Variante S267F\n(Barrido de Myrcludex B a t = 72.0 h)", fontsize=16, fontweight='bold', y=0.96)
    
    # 1. Carga Viral
    axs[0, 0].plot(myr, cv_wt, 'o-', color='#e74c3c', label='Wild-Type (WT)', linewidth=2.5)
    axs[0, 0].plot(myr, cv_mut, 's--', color='#2ecc71', label='Variante S267F (Refractaria)', linewidth=2.5)
    axs[0, 0].set_xscale('symlog', linthresh=1.0)
    axs[0, 0].set_title("A. Carga Viral Final de HBV", fontsize=12, fontweight='bold')
    axs[0, 0].set_xlabel("Myrcludex B (nM) - Escala Logarítmica", fontsize=10)
    axs[0, 0].set_ylabel("Carga Viral (viriones)", fontsize=10)
    axs[0, 0].grid(True, which="both", ls="--", alpha=0.5)
    axs[0, 0].legend()
    
    # 2. Aclaramiento Biliar
    axs[0, 1].plot(myr, acl_wt, 'o-', color='#3498db', label='Wild-Type (WT)', linewidth=2.5)
    axs[0, 1].plot(myr, acl_mut, 's--', color='#2ecc71', label='Variante S267F', linewidth=2.5)
    axs[0, 1].set_xscale('symlog', linthresh=1.0)
    axs[0, 1].set_title("B. Aclaramiento Biliar Basolateral por NTCP", fontsize=12, fontweight='bold')
    axs[0, 1].set_xlabel("Myrcludex B (nM)", fontsize=10)
    axs[0, 1].set_ylabel("Fracción de Aclaramiento Biliar", fontsize=10)
    axs[0, 1].grid(True, which="both", ls="--", alpha=0.5)
    axs[0, 1].legend()
    
    # 3. GSH Pool
    axs[1, 0].plot(myr, gsh_wt, 'o-', color='#f39c12', label='Wild-Type (WT)', linewidth=2.5)
    axs[1, 0].plot(myr, gsh_mut, 's--', color='#2ecc71', label='Variante S267F', linewidth=2.5)
    axs[1, 0].axhline(y=2.4, color='red', linestyle=':', label='Umbral Crítico (30%)', linewidth=2)
    axs[1, 0].set_xscale('symlog', linthresh=1.0)
    axs[1, 0].set_title("C. Pool Redox de Glutatión Celular (GSH)", fontsize=12, fontweight='bold')
    axs[1, 0].set_xlabel("Myrcludex B (nM)", fontsize=10)
    axs[1, 0].set_ylabel("Concentración de GSH (mM)", fontsize=10)
    axs[1, 0].grid(True, which="both", ls="--", alpha=0.5)
    axs[1, 0].legend()
    
    # 4. Viabilidad
    axs[1, 1].plot(myr, [v*100 for v in viab_wt], 'o-', color='#9b59b6', label='Wild-Type (WT)', linewidth=2.5)
    axs[1, 1].plot(myr, [v*100 for v in viab_mut], 's--', color='#2ecc71', label='Variante S267F', linewidth=2.5)
    axs[1, 1].set_xscale('symlog', linthresh=1.0)
    axs[1, 1].set_title("D. Viabilidad Hepatocitaria", fontsize=12, fontweight='bold')
    axs[1, 1].set_xlabel("Myrcludex B (nM)", fontsize=10)
    axs[1, 1].set_ylabel("Viabilidad Celular (%)", fontsize=10)
    axs[1, 1].grid(True, which="both", ls="--", alpha=0.5)
    axs[1, 1].legend()
    
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    out_path = os.path.join(visuales_dir(), "analisis_toxicidad_s267f.png")
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\n[OK] Grafico guardado en: {out_path}")