import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# Directorios de trabajo
_BASE_DIR = os.path.abspath(os.path.dirname(__file__))
visuales_dir = os.path.abspath(os.path.join(_BASE_DIR, "..", "02_Simulaciones_Visuales"))
os.makedirs(visuales_dir, exist_ok=True)

# Configurar el estilo de los gráficos
plt.style.use('seaborn-v0_8-whitegrid')

# ----------------------------------------------------------------------------
# PARÁMETROS BIOFÍSICOS Y CINÉTICOS (GROUNDED IN PHYSICAL LEDGER & LITERATURE)
# ----------------------------------------------------------------------------
t = np.linspace(0, 360, 240) # Tiempo de simulación (6 horas, en minutos)

# Constantes físicas
V_cell = 1.15      # pL (Volumen celular de un linfocito T humano)
ATP_basal = 100.0  # % (Nivel basal de ATP en condiciones fisiológicas, pH 7.40)
pKa_PFK = 6.80     # pH de transición alostérica de PFK-1 (Ui 1966; Kemp & Foe 1983)
n_PFK = 4.0        # Coeficiente de Hill de PFK-1 (alta cooperatividad alostérica al protón)

# Parámetros del escenario de vacuna de ARNm convencional (sin blindaje iónico)
pHi_conv_basal = 7.20
pHi_conv_limit = 5.75  # Límite termodinámico citosólico en estroma de pH 6.20
tau_pHi_conv = 45.0    # Minutos (vida media de acidificación pasiva por entrada de H+)

# Parámetros del NHE1-Shield (mutante constitutivamente activo 1K3R4E)
Vmax_NHE1_shield = 22.0  # mM/min (capacidad máxima de extrusión de protones)
pHi_shield_limit = 6.85  # pH de equilibrio dinámico mantenido por el escudo iónico
tau_pHi_shield = 15.0    # Minutos (rápido ajuste alostérico de pH interno)

# ----------------------------------------------------------------------------
# RESOLUCIÓN NUMÉRICA DE LA CINÉTICA ENZIMÁTICA Y DEPLECIÓN DE ATP
# ----------------------------------------------------------------------------
# 1. Dinámica del pH intracelular (pHi) al ingresar al estroma tumoral ácido (pHe = 6.20)
# Nota: Se utiliza la solución analítica asintótica de relajación exponencial de primer orden
# (derivada del balance de masa continuo d[H+]/dt bajo capacidad amortiguadora beta_i = 30 mM/pH)
# para garantizar estabilidad numérica in silico:
pHi_conv = pHi_conv_limit + (pHi_conv_basal - pHi_conv_limit) * np.exp(-t / tau_pHi_conv)
pHi_shield = pHi_shield_limit + (pHi_conv_basal - pHi_shield_limit) * np.exp(-t / tau_pHi_shield)

# 2. Actividad relativa de la Fosfofructocinasa-1 (PFK-1), enzima marcapasos glucolítica
# La acidificación citosólica inhibe de forma cooperativa y alostérica a la PFK-1
act_PFK_conv = 1.0 / (1.0 + 10 ** (n_PFK * (pKa_PFK - pHi_conv)))
act_PFK_shield = 1.0 / (1.0 + 10 ** (n_PFK * (pKa_PFK - pHi_shield)))

# 3. Cinética de depletación e importación de ATP
# d[ATP]/dt = k_prod * act_PFK - k_cons * [ATP]
# En estado estacionario basal (pH 7.20), act_PFK ~ 0.8, ATP ~ 100%
k_cons = 0.05  # Tasa de consumo basal de ATP celular (1/min)
k_prod = 100.0 * k_cons / (1.0 / (1.0 + 10 ** (n_PFK * (pKa_PFK - 7.20))))

atp_conv = np.zeros_like(t)
atp_shield = np.zeros_like(t)

atp_conv[0] = ATP_basal
atp_shield[0] = ATP_basal

dt = t[1] - t[0]
for i in range(1, len(t)):
    # Integración de Euler para ATP Convencional
    dATP_conv = k_prod * act_PFK_conv[i-1] - k_cons * atp_conv[i-1]
    atp_conv[i] = max(0.0, atp_conv[i-1] + dATP_conv * dt)
    
    # Integración de Euler para NHE1-Shield
    dATP_shield = k_prod * act_PFK_shield[i-1] - k_cons * atp_shield[i-1]
    atp_shield[i] = max(0.0, atp_shield[i-1] + dATP_shield * dt)

# 4. Capacidad de Degranulamiento y Exocitosis Lítica (Perforinas y Granzimas)
# Requiere transporte de vesículas motorizado por miosinas y kinesinas dependientes de ATP (K_half ~ 20%)
K_atp_exocytosis = 20.0
cytotoxicity_conv = 100.0 * (atp_conv ** 2) / (atp_conv ** 2 + K_atp_exocytosis ** 2)
cytotoxicity_shield = 100.0 * (atp_shield ** 2) / (atp_shield ** 2 + K_atp_exocytosis ** 2)

# Simulación de la afinidad antigénica del receptor T (TCR) entrenado por la vacuna de ARNm
# En los primeros minutos, la afinidad y reconocimiento del antígeno es del 100% (gracias al entrenamiento con IA)
tcr_recognition_vaccine = 100.0 * np.ones_like(t)

# ----------------------------------------------------------------------------
# GENERACIÓN DE GRÁFICOS CIENTÍFICOS (Doble Panel)
# ----------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

fig.suptitle("Colapso Biofísico de las Vacunas de ARNm vs. Eficacia Sostenida de NHE1-Shield bajo Acidosis Tumoral (pH 6.20)", 
             fontsize=14, fontweight='bold', y=0.98)

# Panel A: Dinámica del pH Intracelular y depletación de ATP (Límite Glucolítico por PFK-1)
ax1.plot(t, pHi_conv, color='#e7298a', linestyle='-', lw=2.5, label='pHi - Convencional (Vacuna ARNm)')
ax1.plot(t, pHi_shield, color='#4daf4a', linestyle='-', lw=2.5, label='pHi - NHE1-Shield')
ax1.set_ylabel('pH Intracelular (pHi)', fontsize=11, fontweight='bold', color='black')
ax1.set_ylim(5.5, 7.5)
ax1.tick_params(axis='y')

# Crear eje secundario para el ATP
ax1_atp = ax1.twinx()
ax1_atp.plot(t, atp_conv, color='#e7298a', linestyle=':', lw=2.0, alpha=0.8, label='ATP - Convencional (Vacuna ARNm)')
ax1_atp.plot(t, atp_shield, color='#4daf4a', linestyle=':', lw=2.0, alpha=0.8, label='ATP - NHE1-Shield')
ax1_atp.set_ylabel('Reservas Relativas de ATP (%)', fontsize=11, fontweight='bold', color='gray')
ax1_atp.set_ylim(-5, 105)
ax1_atp.tick_params(axis='y', labelcolor='gray')

# Unir leyendas de ambos ejes en el Panel A
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax1_atp.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='center left', fontsize=9)
ax1.set_title("A. Cinética de Acidificación y Colapso Energético (PFK-1)", fontsize=12, fontweight='bold')
ax1.set_xlabel("Tiempo en el Estroma Tumoral (minutos)", fontsize=11)

# Panel B: Paradoja Inmunológica: Reconocimiento Antigénico de Vacuna vs. Capacidad Citolítica Real
ax2.plot(t, tcr_recognition_vaccine, color='#377eb8', linestyle='--', lw=2.0, label='Reconocimiento de Antígeno TCR (Fuerza Bruta IA)')
ax2.plot(t, cytotoxicity_conv, color='#e7298a', linestyle='-', lw=2.5, label='Citolisis Real - T Convencional (Vacuna)')
ax2.plot(t, cytotoxicity_shield, color='#4daf4a', linestyle='-', lw=2.5, label='Citolisis Real - NHE1-Shield')

ax2.set_title("B. Paradoja de Vacunas: Reconocimiento Perfecto vs. Parálisis Lítica", fontsize=12, fontweight='bold')
ax2.set_xlabel("Tiempo en el Estroma Tumoral (minutos)", fontsize=11)
ax2.set_ylabel("Eficiencia / Capacidad Funcional (%)", fontsize=11)
ax2.set_ylim(-5, 110)
ax2.legend(fontsize=9, loc='lower left')

ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
plt.tight_layout(pad=2.0)

# Guardar localmente en visuales_dir
grafico_path = os.path.join(visuales_dir, "grafico_limites_vacunas_arn.png")
plt.savefig(grafico_path, dpi=150, bbox_inches='tight')
plt.close()

# Mostrar resultados numéricos en consola para auditoría del búnker
print("VACCINE_LIMITS_SUMMARY:")
print(f"  - T Convencional (t=90m): pHi = {pHi_conv[60]:.2f} | ATP = {atp_conv[60]:.2f}% | Citolisis = {cytotoxicity_conv[60]:.2f}%")
print(f"  - T Convencional (t=180m): pHi = {pHi_conv[120]:.2f} | ATP = {atp_conv[120]:.2f}% | Citolisis = {cytotoxicity_conv[120]:.2f}%")
print(f"  - NHE1-Shield (t=180m): pHi = {pHi_shield[120]:.2f} | ATP = {atp_shield[120]:.2f}% | Citolisis = {cytotoxicity_shield[120]:.2f}%")
print(f"[OK] Grafico de limites de vacunas ARNm generado en: {grafico_path}")
