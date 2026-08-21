import numpy as np
import matplotlib.pyplot as plt
import os
import math

# Configurar Matplotlib para guardado sin pantalla (Headless)
import matplotlib
matplotlib.use('Agg')

def simular_oxigeno_estocastico(mu, sigma, theta=0.5, dt=0.1, tiempo_total=72.0):
    """
    Simula la dinámica de saturación de O2 mediante un proceso de Ornstein-Uhlenbeck
    para representar fluctuaciones estocásticas en el tejido tumoral.
    """
    pasos = int(tiempo_total / dt)
    o2 = np.zeros(pasos)
    o2[0] = mu  # Inicia en el valor medio
    
    for t in range(1, pasos):
        # Ecuación de Ornstein-Uhlenbeck: dO2 = theta*(mu - O2)*dt + sigma*dWt
        dW = np.random.normal(0, math.sqrt(dt))
        o2[t] = o2[t-1] + theta * (mu - o2[t-1]) * dt + sigma * dW
        # Clampear a límites físicos mínimos (0% de saturación)
        o2[t] = max(0.0, o2[t])
        
    return o2

def calcular_acumulacion_hif1a(o2_profile, dt=0.1, k_syn=2.0, k_deg=0.8):
    """
    Modela la cinética de acumulación nuclear de HIF-1α.
    Se estabiliza progresivamente cuando O2 < 5.0% (hipoxia).
    """
    pasos = len(o2_profile)
    hif1a = np.zeros(pasos)
    
    for t in range(1, pasos):
        # Heaviside suave (Hill) para la tasa de estabilización por hipoxia
        o2_actual = o2_profile[t]
        factor_estabilizacion = 1.0 / (1.0 + math.exp(1.5 * (o2_actual - 5.0)))
        
        # dHIF1a/dt = k_syn * factor_estabilizacion - k_deg * HIF1a
        dHIF = (k_syn * factor_estabilizacion - k_deg * hif1a[t-1]) * dt
        hif1a[t] = max(0.0, hif1a[t-1] + dHIF)
        
    return hif1a

def evaluar_produccion_vegf(hif1a_profile, umbral_hre=0.8):
    """
    Calcula el porcentaje de tiempo acumulado donde HIF-1α supera el umbral HRE
    para activar la transcripción de VEGF (gatillando la angiogénesis).
    """
    tiempo_activo = np.sum(hif1a_profile >= umbral_hre)
    return (tiempo_activo / len(hif1a_profile)) * 100.0

def ejecutar_barrido_parametrico():
    print("[*] Iniciando barrido paramétrico estocástico de O2 vs Volatilidad...")
    
    # Definir grilla paramétrica (50x50)
    resolucion = 50
    mus = np.linspace(1.0, 12.0, resolucion)      # Saturación media de O2 (%)
    sigmas = np.linspace(0.1, 5.0, resolucion)    # Volatilidad / Amplitud del ruido (%)
    
    vegf_map = np.zeros((resolucion, resolucion))
    
    # Fijar semilla para reproductibilidad
    np.random.seed(42)
    
    for i, sigma in enumerate(sigmas):
        for j, mu in enumerate(mus):
            # Correr múltiples simulaciones de Monte Carlo por celda para promediar el ruido
            monte_carlo_runs = 5
            resultados_mc = []
            for _ in range(monte_carlo_runs):
                o2_profile = simular_oxigeno_estocastico(mu, sigma)
                hif1a_profile = calcular_acumulacion_hif1a(o2_profile)
                activacion_vegf = evaluar_produccion_vegf(hif1a_profile)
                resultados_mc.append(activacion_vegf)
            
            vegf_map[i, j] = np.mean(resultados_mc)
            
    print("[+] Barrido completado. Generando mapa de calor...")
    
    # Crear la visualización
    plt.figure(figsize=(10, 8))
    X, Y = np.meshgrid(mus, sigmas)
    
    # Contorno relleno
    cp = plt.contourf(X, Y, vegf_map, levels=20, cmap="YlOrRd")
    cbar = plt.colorbar(cp)
    cbar.set_label("Activación Transcripcional de VEGF (%)", fontsize=11, fontweight="bold")
    
    # Líneas de contorno clave
    contours = plt.contour(X, Y, vegf_map, levels=[10.0, 50.0, 90.0], colors="black", linewidths=1.2, linestyles="dashed")
    plt.clabel(contours, inline=True, fmt="%1.0f%%", fontsize=10, colors="black")
    
    # Anotaciones de las regiones fisiológicas
    plt.text(2.0, 1.0, "HIPOXIA\nPERMANENTE\n(VEGF > 90%)", color="darkred", fontsize=9, fontweight="bold", ha="center")
    plt.text(9.0, 4.0, "HIPOXIA\nINTERMITENTE\n(Bypass Estocástico)", color="orange", fontsize=9, fontweight="bold", ha="center")
    plt.text(9.5, 0.8, "NORMOXIA\nSEGURA", color="darkgreen", fontsize=9, fontweight="bold", ha="center")
    
    plt.title("MAPEO ESTOCÁSTICO DE RESISTENCIA: DINÁMICA HIF-1α / VEGF", fontsize=12, fontweight="bold", pad=15)
    plt.xlabel("Saturación Media de Oxígeno Intersticial ($\\mu$ - %)", fontsize=11, fontweight="bold")
    plt.ylabel("Amplitud de Fluctuaciones Estocásticas ($\\sigma$ - %)", fontsize=11, fontweight="bold")
    plt.grid(True, alpha=0.3, linestyle=":")
    
    # Guardar a scratch primero
    scratch_path = "/workspace/scratch/analisis_estocastico_oxigeno.png"
    plt.savefig(scratch_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    # Copiar a out
    out_path = "/workspace/out/analisis_estocastico_oxigeno.png"
    import shutil
    shutil.copy(scratch_path, out_path)
    print(f"[✔] ÉXITO: Visualización guardada en {out_path}")

if __name__ == "__main__":
    ejecutar_barrido_parametrico()
