import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# Directorios de trabajo
_BASE_DIR = os.path.abspath(os.path.dirname(__file__))
visuales_dir = os.path.abspath(os.path.join(_BASE_DIR, "..", "02_Simulaciones_Visuales"))
os.makedirs(visuales_dir, exist_ok=True)

# -----------------------------------------------------------------------------
# PARÁMETROS DEL MODELO (EJE INTESTINO-HÍGADO-TUMOR)
# -----------------------------------------------------------------------------
# Tiempo de simulación (minutos)
t = np.linspace(0, 180, 200)

# Niveles basales y constantes
IL6_physio = 5.0      # pg/mL (nivel fisiológico sano)
K_LPS_IL6 = 795.0     # pg/mL (máxima elevación por endotoxemia portal)
K_IL6_tumor = 300.0   # pg/mL (afinidad de IL-6 por GP130)
PDL1_basal = 1.0      # Unidad relativa
alpha_IL6_PDL1 = 15.0 # Factor de amplificación de PD-L1 inducido por IL-6
k_TOX_activation = 0.005 # Tasa de inducción de TOX por señalización combinada
d_TOX_decay = 0.001     # Tasa de atenuación de TOX

# Scenarios de integridad de barrera intestinal (phi_gut)
scenarios = {
    "Akkermansia_Optima": {
        "phi_gut": 1.0, 
        "color": "#1b9e77", 
        "label": r"Akkermansia Optima (Saneado, $\phi_{gut} = 1.0$)"
    },
    "Endotoxemia_Moderada": {
        "phi_gut": 0.5, 
        "color": "#d95f02", 
        "label": r"Endotoxemia Moderada ($\phi_{gut} = 0.5$)"
    },
    "Leaky_Gut_Severo": {
        "phi_gut": 0.0, 
        "color": "#e7298a", 
        "label": r"Leaky Gut Severo (Inflamacion, $\phi_{gut} = 0.0$)"
    }
}

# -----------------------------------------------------------------------------
# SIMULACIÓN DINÁMICA DE LOS ESCENARIOS
# -----------------------------------------------------------------------------
results = {}

for name, sc in scenarios.items():
    phi = sc["phi_gut"]
    
    # 1. Concentración de IL-6 sistémica regulada por el colon
    IL6_t = IL6_physio + K_LPS_IL6 * (1.0 - phi) * (1.0 - 0.2 * np.exp(-t/50))
    
    # 2. Expresión de PD-L1 en las células tumorales
    PDL1_t = PDL1_basal * (1.0 + alpha_IL6_PDL1 * (IL6_t / (IL6_t + K_IL6_tumor)))
    
    # 3. Evolución del Factor de Transcripción TOX y Agotamiento Epigenético (H3K27me3)
    TOX_t = np.zeros_like(t)
    H3K27me3_t = np.zeros_like(t)
    
    current_TOX = 0.0
    current_epigenetic = 0.0
    dt = t[1] - t[0]
    
    for i in range(len(t)):
        dTOX = k_TOX_activation * PDL1_t[i] * (IL6_t[i] / (IL6_t[i] + K_IL6_tumor)) - d_TOX_decay * current_TOX
        current_TOX += dTOX * dt
        TOX_t[i] = current_TOX
        
        dEpigenetic = 0.003 * current_TOX
        current_epigenetic += dEpigenetic * dt
        H3K27me3_t[i] = min(current_epigenetic, 1.0)
        
    # 4. Viabilidad celular del CAR-T en el estroma ácido (pH = 6.20)
    viability_conv = 100.0 * np.exp(-t/60) * (1.0 - 0.8 * H3K27me3_t)
    viability_nhe1 = 100.0 * np.exp(-t/500) * (1.0 - 0.5 * H3K27me3_t)
    
    results[name] = {
        "IL6": IL6_t,
        "PDL1": PDL1_t,
        "TOX": TOX_t,
        "H3K27me3": H3K27me3_t * 100,
        "viability_conv": np.clip(viability_conv, 0, 100),
        "viability_nhe1": np.clip(viability_nhe1, 0, 100)
    }

# -----------------------------------------------------------------------------
# GENERACIÓN DE GRÁFICO CIENTÍFICO (MULTIPANEL)
# -----------------------------------------------------------------------------
plt.style.use('seaborn-v0_8-whitegrid')
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# Panel A: IL-6 Sistémica en el Hígado
for name, sc in scenarios.items():
    axs[0, 0].plot(t, results[name]["IL6"], color=sc["color"], lw=2.5, label=sc["label"])
axs[0, 0].axhline(y=500.0, color='red', linestyle='--', alpha=0.7, label="Umbral Critico Inflamatorio (500 pg/mL)")
axs[0, 0].set_title("A. Dinamica de IL-6 Sistemica (Eje Porta-Hepatico)", fontsize=12, fontweight='bold')
axs[0, 0].set_xlabel("Tiempo (minutos)", fontsize=10)
axs[0, 0].set_ylabel("IL-6 en Estroma (pg/mL)", fontsize=10)
axs[0, 0].legend(fontsize=9, loc="upper right")
axs[0, 0].set_ylim(0, 1000)

# Panel B: Expresión de PD-L1 en Hepatocarcinoma (GP130/STAT3)
for name, sc in scenarios.items():
    axs[0, 1].plot(t, results[name]["PDL1"], color=sc["color"], lw=2.5)
axs[0, 1].set_title("B. Upregulation de PD-L1 en Celulas de HCC", fontsize=12, fontweight='bold')
axs[0, 1].set_xlabel("Tiempo (minutos)", fontsize=10)
axs[0, 1].set_ylabel("Nivel Relativo de PD-L1 (basal = 1.0)", fontsize=10)

# Panel C: Bloqueo Epigenético (H3K27me3 en promotores IL2/IFNG)
for name, sc in scenarios.items():
    axs[1, 0].plot(t, results[name]["H3K27me3"], color=sc["color"], lw=2.5)
axs[1, 0].set_title("C. Silenciamiento Epigenetico por TOX (H3K27me3)", fontsize=12, fontweight='bold')
axs[1, 0].set_xlabel("Tiempo (minutos)", fontsize=10)
axs[1, 0].set_ylabel("% Promotores Silenciados ($IL2$ / $IFNG$)", fontsize=10)
axs[1, 0].set_ylim(0, 100)

# Panel D: Destino Poblacional de Células CAR-T en Estroma Ácido
for name, sc in scenarios.items():
    axs[1, 1].plot(t, results[name]["viability_nhe1"], color=sc["color"], lw=2.5, linestyle="-", label=f"NHE1-Shield ({sc['label'][:12]})")
    axs[1, 1].plot(t, results[name]["viability_conv"], color=sc["color"], lw=1.5, linestyle=":", alpha=0.7, label=f"Convencional ({sc['label'][:12]})")
axs[1, 1].set_title("D. Viabilidad de CAR-T bajo Acidosis Estromal (pH 6.20)", fontsize=12, fontweight='bold')
axs[1, 1].set_xlabel("Tiempo (minutos)", fontsize=10)
axs[1, 1].set_ylabel("% Viabilidad Celular Activa", fontsize=10)
axs[1, 1].legend(fontsize=8, loc="lower left", ncol=2)
axs[1, 1].set_ylim(0, 100)

plt.tight_layout()
grafico_path = os.path.join(visuales_dir, "comparativa_homeostasis_sistema_gut.png")
plt.savefig(grafico_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"[OK] Grafico generado en: {grafico_path}")
