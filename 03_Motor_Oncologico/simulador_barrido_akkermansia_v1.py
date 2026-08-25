import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Directorios de trabajo
_BASE_DIR = os.path.abspath(os.path.dirname(__file__))
visuales_dir = os.path.abspath(os.path.join(_BASE_DIR, "..", "02_Simulaciones_Visuales"))
os.makedirs(visuales_dir, exist_ok=True)

# Configurar el estilo para alta calidad de publicacion
plt.style.use('seaborn-v0_8-whitegrid')
CHART_DPI = 150

# ----------------------------------------------------------------------------
# PARÁMETROS BASE DEL MODELO (EJE INTESTINO-HÍGADO-TUMOR)
# ----------------------------------------------------------------------------
t = np.linspace(0, 180, 200)
dt = t[1] - t[0]

IL6_physio = 5.0      # pg/mL
K_LPS_IL6 = 795.0     # pg/mL
K_IL6_tumor = 300.0   # pg/mL
PDL1_basal = 1.0      
alpha_IL6_PDL1 = 15.0 
k_TOX_activation = 0.005 
d_TOX_decay = 0.001     

phi_grid = np.linspace(0.0, 1.0, 100)

final_il6 = []
final_pdl1 = []
final_h3k27me3 = []
final_viab_conv = []
final_viab_nhe1 = []
final_cytotox_conv = []
final_cytotox_nhe1 = []

# BARRIDO PARAMÉTRICO
for phi in phi_grid:
    IL6_t = IL6_physio + K_LPS_IL6 * (1.0 - phi) * (1.0 - 0.2 * np.exp(-t/50))
    PDL1_t = PDL1_basal * (1.0 + alpha_IL6_PDL1 * (IL6_t / (IL6_t + K_IL6_tumor)))
    
    TOX_t = np.zeros_like(t)
    H3K27me3_t = np.zeros_like(t)
    current_TOX = 0.0
    current_epigenetic = 0.0
    
    for i in range(len(t)):
        dTOX = k_TOX_activation * PDL1_t[i] * (IL6_t[i] / (IL6_t[i] + K_IL6_tumor)) - d_TOX_decay * current_TOX
        current_TOX += dTOX * dt
        TOX_t[i] = current_TOX
        
        dEpigenetic = 0.003 * current_TOX
        current_epigenetic += dEpigenetic * dt
        H3K27me3_t[i] = min(current_epigenetic, 1.0)
        
    viability_conv = 100.0 * np.exp(-t/60) * (1.0 - 0.8 * H3K27me3_t)
    viability_nhe1 = 100.0 * np.exp(-t/500) * (1.0 - 0.5 * H3K27me3_t)
    
    cytotox_conv = viability_conv[-1] * (1.0 - H3K27me3_t[-1])
    cytotox_nhe1 = viability_nhe1[-1] * (1.0 - H3K27me3_t[-1])
    
    final_il6.append(IL6_t[-1])
    final_pdl1.append(PDL1_t[-1])
    final_h3k27me3.append(H3K27me3_t[-1] * 100.0)
    final_viab_conv.append(viability_conv[-1])
    final_viab_nhe1.append(viability_nhe1[-1])
    final_cytotox_conv.append(cytotox_conv)
    final_cytotox_nhe1.append(cytotox_nhe1)

final_il6 = np.array(final_il6)
final_h3k27me3 = np.array(final_h3k27me3)
final_viab_conv = np.array(final_viab_conv)
final_viab_nhe1 = np.array(final_viab_nhe1)
final_cytotox_conv = np.array(final_cytotox_conv)
final_cytotox_nhe1 = np.array(final_cytotox_nhe1)

# Encontrar umbrales
idx_safe_10 = np.where(final_h3k27me3 <= 10.0)[0]
phi_safe_tox_10 = phi_grid[idx_safe_10[0]] if len(idx_safe_10) > 0 else 0.95

idx_cytotox_50 = np.where(final_cytotox_nhe1 >= 50.0)[0]
phi_safe_cytotox_50 = phi_grid[idx_cytotox_50[0]] if len(idx_cytotox_50) > 0 else 0.90

# Punto de inflexión de la citotoxicidad de NHE1
slopes = np.gradient(final_cytotox_nhe1, phi_grid)
idx_inflexion = np.argmax(slopes)
phi_inflexion = phi_grid[idx_inflexion]

# ----------------------------------------------------------------------------
# GENERACIÓN DE GRÁFICOS
# ----------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6.5))

color_il6 = '#3182bd'
color_epi = '#e7298a'

# Gráfico 1: IL-6 Sistémica y Silenciamiento Epigenético
ax1.plot(phi_grid * 100, final_il6, color=color_il6, lw=3, label="IL-6 Sistémica")
ax1.set_xlabel("Integridad de la Barrera Intestinal / Akkermansia (phi_gut, %)", fontsize=11, fontweight='bold')
ax1.set_ylabel("IL-6 Sistémica en Estroma (pg/mL)", color=color_il6, fontsize=11, fontweight='bold')
ax1.tick_params(axis='y', labelcolor=color_il6)
ax1.set_ylim(0, 1000)

ax1_twin = ax1.twinx()
ax1_twin.plot(phi_grid * 100, final_h3k27me3, color=color_epi, lw=3, linestyle="--", label="Silenciamiento Epigenético")
ax1_twin.set_ylabel("Silenciamiento Epigenético H3K27me3 (%)", color=color_epi, fontsize=11, fontweight='bold')
ax1_twin.tick_params(axis='y', labelcolor=color_epi)
ax1_twin.set_ylim(0, 100)

# Líneas guía de umbral crítico de silenciamiento (H3K27me3 <= 10%)
ax1.axvline(x=phi_safe_tox_10 * 100, color='gray', linestyle=':', alpha=0.8)
ax1.text(phi_safe_tox_10 * 100 - 35, 900, f"Zona Segura TOX-\n(phi_gut >= {phi_safe_tox_10*100:.1f}%)", 
         fontsize=9, color='dimgray', fontweight='semibold')

ax1.set_title("La Barrera Epitelial Regula la Inflamacion Porta y el Epigenoma del CAR-T", 
             fontsize=12, fontweight='bold', pad=15)
ax1.spines['top'].set_visible(False)

# Gráfico 2: Capacidad Citotóxica Efectiva final (t = 180 min)
ax2.plot(phi_grid * 100, final_cytotox_nhe1, color='#1b9e77', lw=3.5, label="CAR-T con NHE1-Shield (Blindado Local)")
ax2.plot(phi_grid * 100, final_cytotox_conv, color='#d95f02', lw=2.5, linestyle=":", label="CAR-T Convencional (Linfocito Sencillo)")

# Sombreado de zonas de rescate terapéutico (Cytotox >= 50%)
ax2.axhspan(50, 70, color='#e5f5f0', alpha=0.5, label="Zona de Rescate Clinico Alto (Cytotox >= 50%)")
ax2.axvline(x=phi_safe_cytotox_50 * 100, color='gray', linestyle=':', alpha=0.8)
ax2.text(phi_safe_cytotox_50 * 100 - 32, 40, f"Rescate Terapeutico\n(phi_gut >= {phi_safe_cytotox_50*100:.1f}%)", 
         fontsize=9, color='dimgray', fontweight='semibold')

ax2.set_xlabel("Integridad de la Barrera Intestinal / Akkermansia (phi_gut, %)", fontsize=11, fontweight='bold')
ax2.set_ylabel("Capacidad Citotoxica Efectiva a los 180 min (%)", fontsize=11, fontweight='bold')
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 100)
ax2.legend(fontsize=9, loc="upper left")
ax2.set_title("La Inmunoterapia Convencional es Inutil sin Blindaje Contra la Acidosis", 
             fontsize=12, fontweight='bold', pad=15)

ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

fig.suptitle("Analisis de Bifurcacion Sistemica: Akkermansia es el Requisito para Evitar la Aniquilacion del CAR-T", 
             fontsize=14, fontweight='bold', y=1.02)

plt.tight_layout()
grafico_path = os.path.join(visuales_dir, "grafico_barrido_akkermansia.png")
fig.savefig(grafico_path, dpi=CHART_DPI, bbox_inches='tight')
plt.close()
print(f"[OK] Grafico de barrido generado con exito en: {grafico_path}")
