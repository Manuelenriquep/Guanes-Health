import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# Directorios de trabajo
_BASE_DIR = os.path.abspath(os.path.dirname(__file__))
visuales_dir = os.path.abspath(os.path.join(_BASE_DIR, "..", "02_Simulaciones_Visuales"))
os.makedirs(visuales_dir, exist_ok=True)

# Configuración de estilo
plt.style.use('seaborn-v0_8-whitegrid')

# -----------------------------------------------------------------------------
# PARÁMETROS DE LA SIMULACIÓN DE CO-INTERVENCIÓN (EJE SISTÉMICO-LOCAL)
# -----------------------------------------------------------------------------
# Tiempo de simulación: 48 horas (en minutos)
t_max_min = 48 * 60  # 2880 minutos
t = np.linspace(0, t_max_min, 500)
t_hours = t / 60.0  # Convertido a horas para análisis clínico

# Parámetros biológicos (basados en physical_constants_ledger_v2.json)
IL6_physio = 5.0      # pg/mL (fisiológico sano)
K_LPS_IL6 = 795.0     # pg/mL (elevación por leaky gut)
K_IL6_tumor = 300.0   # pg/mL (afinidad gp130)
PDL1_basal = 1.0
alpha_IL6_PDL1 = 15.0
k_TOX_activation = 0.005
d_TOX_decay = 0.001

# Definición de Escenarios de Co-Intervención
# Comparamos 4 condiciones clínicas para evaluar la ganancia neta en horas de ataque activo
scenarios = {
    "1_Conv_LeakyGut": {
        "phi_gut": 0.20,       # Intestino inflamado (sin Akkermansia)
        "shield": False,      # CAR-T convencional
        "color": "#e7298a",
        "style": ":",
        "label": "T convencional + Leaky Gut (sin Akkermansia)"
    },
    "2_NHE1_LeakyGut": {
        "phi_gut": 0.20,       # Intestino inflamado (sin Akkermansia)
        "shield": True,       # CAR-T con NHE1-Shield
        "color": "#d95f02",
        "style": "--",
        "label": "NHE1-Shield + Leaky Gut (Inflamación Portal)"
    },
    "3_Conv_Akkermansia": {
        "phi_gut": 0.92,       # Intestino reparado (con Akkermansia)
        "shield": False,      # CAR-T convencional
        "color": "#377eb8",
        "style": "-.",
        "label": "T convencional + Akkermansia (Eje Saneado)"
    },
    "4_Sinergia_Total": {
        "phi_gut": 0.92,       # Intestino reparado (con Akkermansia)
        "shield": True,       # CAR-T con NHE1-Shield
        "color": "#4daf4a",
        "style": "-",
        "label": "Sinergia Total: NHE1-Shield + Akkermansia"
    }
}

# -----------------------------------------------------------------------------
# EJECUCIÓN DE LA SIMULACIÓN MULTIESCALA
# -----------------------------------------------------------------------------
results = {}

for key, sc in scenarios.items():
    phi = sc["phi_gut"]
    has_shield = sc["shield"]
    
    # 1. Cinética de IL-6 sistémica
    IL6_t = IL6_physio + K_LPS_IL6 * (1.0 - phi) * (1.0 - 0.3 * np.exp(-t/300))
    
    # 2. Expresión de PD-L1 inducida por IL-6/STAT3
    PDL1_t = PDL1_basal * (1.0 + alpha_IL6_PDL1 * (IL6_t / (IL6_t + K_IL6_tumor)))
    
    # 3. Evolución del factor de fatiga TOX y metilación epigenética
    TOX_t = np.zeros_like(t)
    H3K27me3_t = np.zeros_like(t)
    
    current_TOX = 0.0
    current_epigenetic = 0.0
    dt = t[1] - t[0]
    
    for i in range(len(t)):
        dTOX = k_TOX_activation * PDL1_t[i] * (IL6_t[i] / (IL6_t[i] + K_IL6_tumor)) - d_TOX_decay * current_TOX
        current_TOX += dTOX * dt
        TOX_t[i] = current_TOX
        
        dEpigenetic = 0.0015 * current_TOX  # Tasa de metilación a largo plazo (48h)
        current_epigenetic += dEpigenetic * dt
        H3K27me3_t[i] = min(current_epigenetic, 1.0)
        
    # 4. Viabilidad celular en el estroma ácido (pH = 6.20)
    # NHE1-Shield tolera la acidez (declinación lenta: vida media ~ 50 horas / 3000 min)
    # Convencional colapsa rápidamente (vida media ~ 1 hora / 60 min)
    if has_shield:
        viability_t = 100.0 * np.exp(-t/3000) * (1.0 - 0.5 * H3K27me3_t)
    else:
        viability_t = 100.0 * np.exp(-t/60) * (1.0 - 0.8 * H3K27me3_t)
        
    viability_t = np.clip(viability_t, 0.0, 100.0)
    
    # 5. Capacidad Citolítica Efectiva (%)
    # Depende de la viabilidad celular y es inversamente proporcional al cansancio epigenético (H3K27me3)
    cytol_power = viability_t * (1.0 - H3K27me3_t)
    
    # 6. Cálculo de Horas de Ataque Efectivo (ACT)
    # Definido como las horas acumuladas donde la capacidad citolítica efectiva se mantiene >= 30%
    active_mask = cytol_power >= 30.0
    active_time_hours = 0.0
    if np.any(active_mask):
        # Encontramos el último punto de tiempo continuo donde se cumple la condición
        active_time_hours = np.sum(active_mask) * (dt / 60.0)
        
    results[key] = {
        "time_hours": t_hours,
        "IL6": IL6_t,
        "PDL1": PDL1_t,
        "H3K27me3": H3K27me3_t * 100.0,
        "viability": viability_t,
        "cytol_power": cytol_power,
        "act_hours": active_time_hours
    }

# -----------------------------------------------------------------------------
# VISUALIZACIÓN CIENTÍFICA (Doble Panel)
# -----------------------------------------------------------------------------
plt.style.use('seaborn-v0_8-whitegrid')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

fig.suptitle("Sinergia Total: Co-Intervención de Akkermansia y NHE1-Shield Rescata la Citotoxicidad de Células T frente al HCC", 
             fontsize=14, fontweight='bold', y=0.98)

# Panel 1: Capacidad Citolítica Efectiva a lo largo de 48 Horas
for key, sc in scenarios.items():
    ax1.plot(results[key]["time_hours"], results[key]["cytol_power"], 
             color=sc["color"], linestyle=sc["style"], lw=2.5, 
             label=f"{sc['label']} (ACT: {results[key]['act_hours']:.1f}h)")

ax1.axhline(y=30.0, color='red', linestyle='--', alpha=0.5, label="Umbral Mínimo de Lisis Efectiva (30%)")
ax1.set_title("A. Evolución Temporal de la Capacidad Citolítica de las CAR-T", fontsize=12, fontweight='bold')
ax1.set_xlabel("Tiempo en el Tumor (Horas)", fontsize=11)
ax1.set_ylabel("Capacidad de Destrucción Tumoral (%)", fontsize=11)
ax1.set_xlim(0, 48)
ax1.set_ylim(0, 105)
ax1.legend(fontsize=9, loc="upper right")

# Panel 2: Comparativa de Horas de Ataque Continuo Ganas (ACT)
act_values = [results[key]["act_hours"] for key in scenarios.keys()]
bars_labels = ["T Convencional\n+ Leaky Gut", "NHE1-Shield\n+ Leaky Gut", "T Convencional\n+ Akkermansia", "Sinergia Total\n(NHE1 + Akker)"]
bars_colors = [scenarios[key]["color"] for key in scenarios.keys()]

bars = ax2.bar(bars_labels, act_values, color=bars_colors, edgecolor='black', alpha=0.85, width=0.5)
ax2.set_title("B. Horas Ganadas de Ataque Lítico Activo (ACT $\\geq$ 30%)", fontsize=12, fontweight='bold')
ax2.set_ylabel("Tiempo de Lisis Activo Acumulado (Horas)", fontsize=11)
ax2.set_ylim(0, max(act_values) * 1.2 if max(act_values) > 0 else 10)

for bar in bars:
    height = bar.get_height()
    ax2.annotate(f'{height:.1f} Horas',
                 xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3),  # 3 points vertical offset
                 textcoords="offset points",
                 ha='center', va='bottom', fontweight='bold', fontsize=10)

ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
plt.tight_layout(pad=2.0)

# Guardar localmente en visuales_dir
grafico_path = os.path.join(visuales_dir, "grafico_combinado_akkermansia_nhe1.png")
plt.savefig(grafico_path, dpi=150, bbox_inches='tight')
plt.close()

# Exportar resultados numéricos a la consola para reporte
print("SIMULATION_SUMMARY:")
for key, res in results.items():
    print(f"  - {key}: ACT = {res['act_hours']:.2f} horas")

print(f"[OK] Grafico generado con exito en: {grafico_path}")
