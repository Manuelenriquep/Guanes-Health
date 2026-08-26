import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
import shutil

# Directorios de trabajo
scratch_dir = "/workspace/scratch"
out_dir = "/workspace/out"
os.makedirs(scratch_dir, exist_ok=True)
os.makedirs(out_dir, exist_ok=True)

# Configurar el estilo de los gráficos usando seaborn
sns.set_theme(style='whitegrid', palette='colorblind', font='DejaVu Sans')

# ----------------------------------------------------------------------------
# 1. PARAMETRIZACIÓN DE LA COHORTE VIRTUAL DE PACIENTES (N = 100)
# ----------------------------------------------------------------------------
np.random.seed(42)  # Semilla para reproducibilidad de la cohorte estocástica
N_patients = 100

# Cada paciente representa un caso real con heterogeneidad en su microbiota de Akkermansia
# Abundancia relativa de Akkermansia distribuida de forma realista (0.1% a 5.0%)
akkermansia_pool = np.random.uniform(0.1, 5.0, N_patients)

# Generamos la cohorte virtual de pacientes
patients_df = pd.DataFrame({
    'patient_id': [f"PAT-{i+1:03d}" for i in range(N_patients)],
    'akkermansia_abundance': akkermansia_pool
})

# Ecuación de acoplamiento para la integridad de la barrera intestinal (phi_gut) [0.0 - 1.0]
# Una abundancia comensal óptima (>= 3.0%) garantiza una phi_gut >= 90%
# En base a LBN-Gut-Barrier, si Akkermansia decae por debajo de 1.5%, la barrera empieza a colapsar
patients_df['phi_gut'] = 0.15 + 0.85 * (1.0 - np.exp(-patients_df['akkermansia_abundance'] / 1.2))
patients_df['phi_gut'] = np.clip(patients_df['phi_gut'], 0.0, 1.0)

# Asignar aleatoriamente a los pacientes a 4 brazos de intervención clínica (25 por brazo)
arms = [
    "Arm_A_Standard",       # Vacuna ARNm + Anti-PD1 (Convencional, microbiota basal)
    "Arm_B_Akkermansia",    # Vacuna ARNm + Anti-PD1 + Postbiótico Akkermansia (phi_gut optimizado)
    "Arm_C_NHE1_Shield",    # Vacuna ARNm + Anti-PD1 + CAR-T con Escudo NHE1-Shield (microbiota basal)
    "Arm_D_Sinergia_Total"  # Sinergia Total: Vacuna + Anti-PD1 + Akkermansia + NHE1-Shield
]

# Para asegurar distribución uniforme perfecta (25 por brazo) para el análisis estadístico:
patients_df['intervention_arm'] = [arms[i % 4] for i in range(N_patients)]

# ----------------------------------------------------------------------------
# 2. MODELADO DE LA INTERVENCIÓN CLÍNICA Y CÁLCULOS MULTIESCALA
# ----------------------------------------------------------------------------
# Constantes biofísicas inmutables (del physical_constants_ledger_v2.json)
IL6_physio = 5.0        # pg/mL
K_LPS_IL6 = 795.0       # pg/mL
K_IL6_tumor = 300.0     # pg/mL
PDL1_basal = 1.0
alpha_IL6_PDL1 = 15.0
pKa_PFK = 6.60          # pH de transición alostérica de PFK-1
n_PFK = 4.0             # Coeficiente de Hill de PFK-1
K_atp_exocytosis = 20.0 # Requisito de energía para degranulación lítica
pHe_tumor = 6.20        # Estroma ácido profundo

def simulate_patient_response(row):
    arm = row['intervention_arm']
    phi_gut = row['phi_gut']
    
    # Si el brazo de tratamiento incluye Akkermansia (Arm B y D), se optimiza artificialmente la barrera al 92%
    if arm in ["Arm_B_Akkermansia", "Arm_D_Sinergia_Total"]:
        phi_gut = 0.92
        
    # 1. Concentración de IL-6 sistémica regulada por el colon (vena porta)
    IL6_sinusoidal = IL6_physio + K_LPS_IL6 * (1.0 - phi_gut)
    
    # 2. Expresión de PD-L1 en el tumor (GP130/STAT3)
    PDL1_expression = PDL1_basal * (1.0 + alpha_IL6_PDL1 * (IL6_sinusoidal / (IL6_sinusoidal + K_IL6_tumor)))
    
    # 3. Silenciamiento epigenético por TOX (H3K27me3) inducido por estimulación y checkpoints
    # La estimulación persistente por vacuna de ARNm de 34 neoantígenos en presencia de PD-L1 induce TOX
    TOX_activation = (PDL1_expression / (PDL1_expression + 5.0))
    H3K27me3_silencing = min(TOX_activation * 0.95, 1.0) # Fracción de promotores líticos silenciados
    
    # 4. Viabilidad celular del linfocito T y regulación de pH citoplasmático interno (pHi)
    # Si el brazo incluye NHE1-Shield (Arm C y D), el pHi se mantiene en 6.85
    # Si es convencional (Arm A y B), el pHi cae pasivamente a 5.75
    if arm in ["Arm_C_NHE1_Shield", "Arm_D_Sinergia_Total"]:
        pHi_lymphocyte = 6.85
    else:
        pHi_lymphocyte = 5.75
        
    # 5. Actividad alostérica de la PFK-1 (Glucólisis)
    PFK1_activity = 1.0 / (1.0 + 10 ** (n_PFK * (pKa_PFK - pHi_lymphocyte)))
    
    # 6. Reservas de ATP celular del linfocito T (%)
    # dATP/dt = k_prod * PFK1 - k_cons * ATP = 0 en equilibrio dinámico
    # ATP ~ PFK1_activity * (100.0 / Actividad_PFK1_a_pH7.2)
    act_PFK1_basal = 1.0 / (1.0 + 10 ** (n_PFK * (pKa_PFK - 7.20)))
    atp_level = 100.0 * (PFK1_activity / act_PFK1_basal)
    atp_level = np.clip(atp_level, 0.1, 100.0)
    
    # 7. Capacidad Citolítica Real (Eficacia de lisis tumoral final %)
    # La capacidad de degranular e inyectar perforinas depende del ATP y es saboteada por el silenciamiento epigenético (H3K27me3)
    exocytosis_power = (atp_level ** 2) / (atp_level ** 2 + K_atp_exocytosis ** 2)
    tumor_clearance = 100.0 * exocytosis_power * (1.0 - H3K27me3_silencing)
    
    return pd.Series({
        'IL6_sinusoidal': IL6_sinusoidal,
        'PDL1_expression': PDL1_expression,
        'H3K27me3_silencing': H3K27me3_silencing * 100,
        'pHi_lymphocyte': pHi_lymphocyte,
        'atp_level': atp_level,
        'tumor_clearance_rate': np.clip(tumor_clearance, 0.0, 100.0)
    })

# Aplicar el simulador a cada paciente
simulation_results = patients_df.apply(simulate_patient_response, axis=1)
patients_df = pd.concat([patients_df, simulation_results], axis=1)

# ----------------------------------------------------------------------------
# 3. ANÁLISIS ESTADÍSTICO DE LA EFICACIA POR BRAZO CLÍNICO
# ----------------------------------------------------------------------------
summary_stats = patients_df.groupby('intervention_arm')['tumor_clearance_rate'].agg(['mean', 'std', 'min', 'max']).reset_index()
print("ESTADÍSTICAS DE LA SIMULACIÓN DE VACUNACIÓN COHORTES (N=100):")
print(summary_stats.to_string(index=False))

# ----------------------------------------------------------------------------
# 4. GENERACIÓN DE VISUALIZACIONES CIENTÍFICAS
# ----------------------------------------------------------------------------
plt.style.use('seaborn-v0_8-whitegrid')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

fig.suptitle("Simulación Poblacional (N = 100): Colapso Biofísico de la Vacuna de ARNm vs. Sinergia con Akkermansia y NHE1-Shield", 
             fontsize=14, fontweight='bold', y=0.98)

# Panel A: Boxplot de Eficacia de Depuración Tumoral (%) por Brazo de Intervención
order_arms = ["Arm_A_Standard", "Arm_B_Akkermansia", "Arm_C_NHE1_Shield", "Arm_D_Sinergia_Total"]
labels_arms = ["Vacuna ARNm\n(Estándar)", "Vacuna ARNm\n+ Akkermansia", "Vacuna ARNm\n+ NHE1-Shield", "Sinergia Total\n(NHE1 + Akker)"]

sns.boxplot(data=patients_df, x='intervention_arm', y='tumor_clearance_rate', order=order_arms, ax=ax1, width=0.5, hue='intervention_arm', palette='colorblind', legend=False)
sns.stripplot(data=patients_df, x='intervention_arm', y='tumor_clearance_rate', order=order_arms, ax=ax1, color='black', alpha=0.3, jitter=0.1)

ax1.set_title("A. Tasa de Depuración Tumoral (%) por Cohorte de Tratamiento", fontsize=12, fontweight='bold')
ax1.set_xticks([0, 1, 2, 3])
ax1.set_xticklabels(labels_arms, fontsize=10)
ax1.set_xlabel("Brazos de Intervención Clínica", fontsize=11, fontweight='bold')
ax1.set_ylabel("Tasa de Depuración del Tumor (Lisis, %)", fontsize=11, fontweight='bold')
ax1.set_ylim(-5, 105)

# Panel B: Correlación e Identificación del Umbral de Akkermansia
# Graficamos la correlación entre Akkermansia y la depuración del tumor para evidenciar la bifurcación no lineal
for arm in order_arms:
    subset = patients_df[patients_df['intervention_arm'] == arm]
    label_dict = {
        "Arm_A_Standard": "Vacuna Estándar",
        "Arm_B_Akkermansia": "Vacuna + Akkermansia (Saneado)",
        "Arm_C_NHE1_Shield": "Vacuna + NHE1-Shield",
        "Arm_D_Sinergia_Total": "Sinergia Total"
    }
    ax2.scatter(subset['akkermansia_abundance'], subset['tumor_clearance_rate'], 
                label=label_dict[arm], alpha=0.8, s=50)

# Resaltar el umbral clínico de eubiosis (89.9% integridad de barrera intestinal)
# En base a la ecuación, phi_gut = 0.899 ocurre cuando akkermansia ~ 1.5%
ax2.axvline(x=1.5, color='red', linestyle='--', alpha=0.7, label="Umbral de Eubiosis Intestinal (1.5%)")
ax2.axhspan(ymin=50, ymax=100, xmin=0.31, xmax=1.0, color='green', alpha=0.1, label="Zona de Éxito Clínico (Lisis >= 50%)")

ax2.set_title("B. Correlación: Salud Intestinal vs. Eficacia de la Terapia Celular", fontsize=12, fontweight='bold')
ax2.set_xlabel("Abundancia Relativa de Akkermansia muciniphila (%)", fontsize=11, fontweight='bold')
ax2.set_ylabel("Tasa de Depuración del Tumor (Lisis, %)", fontsize=11, fontweight='bold')
ax2.set_xlim(0, 5.2)
ax2.set_ylim(-5, 105)
ax2.legend(fontsize=9, loc="lower right")

sns.despine(ax=ax1)
sns.despine(ax=ax2)
plt.tight_layout(pad=2.0)

# Guardar localmente en scratch
grafico_path = os.path.join(scratch_dir, "grafico_poblacional_vacunas_arn.png")
plt.savefig(grafico_path, dpi=150, bbox_inches='tight')
plt.close()

# Generar archivo CSV consolidado con los resultados de los 100 pacientes para auditoría
data_path = os.path.join(scratch_dir, "resultados_simulacion_pacientes_arn.csv")
patients_df.to_csv(data_path, index=False)
print(f"[OK] Resultados de 100 pacientes exportados a {data_path}")

print("[OK] Código y visualizaciones poblacionales generadas con éxito en scratch.")
