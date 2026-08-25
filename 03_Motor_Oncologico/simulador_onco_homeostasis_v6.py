import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# Directorios de trabajo
_BASE_DIR = os.path.abspath(os.path.dirname(__file__))
visuales_dir = os.path.abspath(os.path.join(_BASE_DIR, "..", "02_Simulaciones_Visuales"))
os.makedirs(visuales_dir, exist_ok=True)

# =====================================================================
# CONSTANTES FÍSICAS E INMUTABLES DEL MOTOR (RESTRICCIONES BIOFÍSICAS - CAPA B)
# =====================================================================
POTENCIAL_REPOSO_MIN = -70.0       # mV
POTENCIAL_REPOSO_MAX = -90.0       # mV
FIDELIDAD_ADN_POLIMERASA = 1e-7    # Tasa basal de error de replicación
ATP_MINIMO_SOBREVIVENCIA = 0.5     # Umbral de energía relativa (~1.0 mM)
LIMITE_HAYFLICK_MAX = 70           # Límite mitótico fisiológico
UMBRAL_SENESCENCIA_TELOMEROS = 4000 # pb (Umbral de disparo de FC-BIO-02)

# Constantes de la Barrera Intestinal (Especialista en Akkermansia)
TEER_OPTIMO = 1500.0               # Ohm*cm^2
MUCUS_OPTIMO = 100.0               # micras
LPS_MAX_SEGURO = 50.0              # pg/mL

class CelulaHumana:
    """
    Representa el estado biofísico, iónico y genómico de una célula humana somática o tumoral.
    Diseñada como una herramienta de modelado conceptual in silico para la simulación de homeostasis celular.
    """
    def __init__(self, tipo_celular="Sana", atp_nivel=100.0, daño_genomico=0.0, telomeros=8000, divisiones=0):
        self.tipo_celular = tipo_celular
        self.atp_nivel = atp_nivel
        self.daño_genomico = daño_genomico
        self.telomeros = telomeros
        self.divisiones = divisiones
        self.viabilidad = 1.0

        # Concentraciones iónicas intracelulares y extracelulares (mM)
        self.k_out = 4.5
        self.k_in = 140.0
        self.na_out = 142.0
        self.na_in = 14.0
        self.cl_out = 103.0
        self.cl_in = 4.0

        # Coeficientes de permeabilidad relativos basales
        self.p_k = 1.0
        self.p_na = 0.04
        self.p_cl = 0.05

        # Variables de microambiente extracelular
        self.pHi = 7.20
        self.pHe = 7.40
        self.O2_saturacion = 100.0  # % de saturación

        # Estado de marcadores e inmuno-camuflaje
        self.p53_activo = True
        self.p21_WAF1 = 0.0
        self.Bcl2_expresion = 1.0   # Factor relativo (1.0 = basal, 25.0 = tumoral)
        self.Bax_Bak_libres = True
        self.fosfatidilserina_externa = False
        self.PD_L1_expresion = 0.0  # Nivel relativo en membrana

    def degradar_telomeros(self):
        """
        Simula el acortamiento de telómeros por división celular.
        """
        self.divisiones += 1
        self.telomeros = max(0, self.telomeros - 80)


class ReguladorRestricciones:
    """
    Herramienta de modelado de restricciones lógicas y transiciones de estado biológico.
    Valida las transiciones de estado celular en condiciones de frontera biofísica.
    """
    def __init__(self, celula: CelulaHumana):
        self.celula = celula

    def calcular_potencial_ghk(self):
        """
        Ecuación de Goldman-Hodgkin-Katz para el potencial transmembrana (V_m).
        Asume temperatura fisiológica de 37 °C (RT/F ≈ 26.7 mV).
        """
        numerator = (self.celula.p_k * self.celula.k_out +
                     self.celula.p_na * self.celula.na_out +
                     self.celula.p_cl * self.celula.cl_in)
        denominator = (self.celula.p_k * self.celula.k_in +
                       self.celula.p_na * self.celula.na_in +
                       self.celula.p_cl * self.celula.cl_out)

        if numerator <= 0 or denominator <= 0:
            return 0.0
        return 26.7 * math.log(numerator / denominator)

    def evaluar_homeostasis(self, phi_gut=1.0):
        """
        Auditoría de los mechanisms de regulación homeostática e inmutables biológicos.
        Retorna el estado de viabilidad de la célula y las alarmas activas.
        """
        alarmas = []
        V_m = self.calcular_potencial_ghk()

        # REG-I-01: Regulación de Ciclo por Daño Genómico (ATM/ATR -> p53)
        if self.celula.daño_genomico > 2.0:
            if self.celula.tipo_celular == "Sana":
                self.celula.p53_activo = True
                self.celula.p21_WAF1 = min(self.celula.daño_genomico * 10, 100.0)
                alarmas.append("Arresto de ciclo celular en G1/S activo (daño genómico)")
            else:
                self.celula.p53_activo = False
                self.celula.p21_WAF1 = 0.0
                alarmas.append("Evasión de auditoría genómica: p53 inactivo")

        # REG-I-02: Balance Bioenergético y Sensor AMPK
        if self.celula.atp_nivel < ATP_MINIMO_SOBREVIVENCIA:
            alarmas.append("Gatillo AMPK activo: Bloqueo de mTORC1 e inducción de autofagia")

        # REG-I-03: Potencial de Membrana (Na+/K+ ATPasa)
        if V_m > -55.0:
            demanda_bomba = abs(V_m + 55.0) * 1.5
            self.celula.atp_nivel = max(0.0, self.celula.atp_nivel - demanda_bomba)
            alarmas.append(f"Gasto energético de Bomba Na+/K+ ATPasa incrementado (V_m: {V_m:.2f} mV)")

        # VETO FC-BIO-01: Daño Genómico Irreparable (Apoptosis)
        if self.celula.daño_genomico > 8.0:
            if self.celula.tipo_celular == "Sana":
                self.celula.Bax_Bak_libres = True
                self.celula.viabilidad = 0.0
                alarmas.append("VETO FC-BIO-01 DETONADO: Muerte por Apoptosis (MMR Fallido)")
            else:
                if self.celula.Bcl2_expresion >= 25.0:
                    self.celula.Bax_Bak_libres = False
                    alarmas.append("VETO FC-BIO-01 BLOQUEADO: Resistencia apoptótica por taponamiento de Bcl-2")

        # VETO FC-BIO-02: Límite de Hayflick (Senescencia Replicativa)
        if self.celula.telomeros <= UMBRAL_SENESCENCIA_TELOMEROS or self.celula.telomeros <= 10:
            if self.celula.tipo_celular == "Sana":
                self.celula.viabilidad = 0.5  # Senescente
                alarmas.append("VETO FC-BIO-02 DETONADO: Arresto Replicativo Permanente (Senescencia de Hayflick)")
            else:
                alarmas.append("VETO FC-BIO-02 EVADIDO: Inmortalidad telomérica por reactivación de hTERT")

        # VETO FC-BIO-03: Colapso Crítico de Potencial o Energía
        if V_m > -15.0 or self.celula.atp_nivel < 0.2:
            self.celula.viabilidad = 0.0
            self.celula.fosfatidilserina_externa = True
            alarmas.append("VETO FC-BIO-03 DETONADO: Colapso del potencial de membrana / Translocación de Fosfatidilserina")

        # =====================================================================
        # EXCLUSIONES SEMÁNTICAS DE BARRERA INTESTINAL (ESPECIALISTA EN AKKERMANSIA)
        # =====================================================================
        teer = TEER_OPTIMO * phi_gut
        mucus = MUCUS_OPTIMO * phi_gut
        lps = 100.0 * (1.0 - phi_gut)

        # VETO FC-BAR-01: Hiperpermeabilidad Epitelial (TEER < 1000 Ohm*cm^2)
        if teer < 1000.0:
            alarmas.append(f"VETO FC-BAR-01 DETONADO: Hiperpermeabilidad Epitelial (TEER = {teer:.1f} Ohm*cm^2 < 1000.0)")
            if self.celula.tipo_celular == "Sana":
                self.celula.viabilidad = max(0.0, self.celula.viabilidad - 0.2) # Enterocitos sufren daño

        # VETO FC-BAR-02: Translocación Endotóxica Portal (LPS > 50 pg/mL)
        if lps > LPS_MAX_SEGURO:
            alarmas.append(f"VETO FC-BAR-02 DETONADO: Endotoxemia Portal Crítica (LPS = {lps:.1f} pg/mL > 50.0)")

        # VETO FC-BAR-03: Atrofia Extrema de Mucina (Mucus < 20 micras)
        if mucus < 20.0:
            alarmas.append(f"VETO FC-BAR-03 DETONADO: Atrofia de Mucosa Mucolítica (Mucus = {mucus:.1f} micras < 20.0)")

        return self.celula.viabilidad, alarmas


# =====================================================================
# SIMULADOR DE BARRERA INTESTINAL (ESPECIALISTA EN AKKERMANSIA)
# =====================================================================
class GutBarrierSimulator:
    """
    Modela la barrera intestinal y la cinética de translocación de LPS y liberación de IL-6.
    """
    def __init__(self, phi_gut=1.0):
        self.phi_gut = phi_gut

    def simular_eje_porta_hepatico(self, t):
        """
        Calcula la concentración de endotoxemia (LPS) y citoquina IL-6 sistémica
        que llega al hígado en función del tiempo.
        """
        IL6_physio = 5.0
        K_LPS_IL6 = 795.0
        # Simulación de la filtración del colon a lo largo del tiempo
        IL6_t = IL6_physio + K_LPS_IL6 * (1.0 - self.phi_gut) * (1.0 - 0.2 * np.exp(-t/50))
        LPS_t = 100.0 * (1.0 - self.phi_gut) * (1.0 - 0.1 * np.exp(-t/50))
        return IL6_t, LPS_t


# =====================================================================
# SIMULADOR MULTIESCALA ACOPLADO (v6)
# =====================================================================
class SimuladorTratamientoV6:
    """
    Ejecuta simulaciones de tratamiento combinando inhibición metabólica,
    estado de la barrera intestinal (Akkermansia) y blindaje celular de CAR-T.
    """
    def __init__(self):
        self.paso_tiempo = 0.1  # horas
        self.tiempo_total = 72.0 # horas
        self.puntos_tiempo = int(self.tiempo_total / self.paso_tiempo)

    def ejecutar_simulacion(self, cohorte="C", mutacion_mct2=False, inhibicion_mct2=False, phi_gut=1.0, has_shield=False):
        tiempo = np.linspace(0, self.tiempo_total, self.puntos_tiempo)

        # Inicializar perfiles
        sana = CelulaHumana(tipo_celular="Sana")
        tumor = CelulaHumana(tipo_celular="Tumor", atp_nivel=10000.0, telomeros=3920)
        tumor.Bcl2_expresion = 25.0
        tumor.pHe = 6.20
        tumor.mutacion_mct2_activa = mutacion_mct2

        # Simulador de barrera intestinal
        gut = GutBarrierSimulator(phi_gut=phi_gut)

        # Historial de variables
        pHi_history = []
        pHe_history = []
        atp_history = []
        viabilidad_history = []
        mct2_history = []
        il6_history = []
        pdl1_history = []
        h3k27me3_history = []
        viabilidad_cart_history = []
        citotox_history = []

        # Parámetros inmunológicos de la Capa B/C
        K_IL6_tumor = 300.0   # pg/mL
        alpha_IL6_PDL1 = 15.0
        k_TOX_activation = 0.005
        d_TOX_decay = 0.001

        current_TOX = 0.0
        current_epigenetic = 0.0

        t_metabolico = 12.0
        t_inmunoterapia = t_metabolico

        if cohorte == "A":
            t_inmunoterapia = t_metabolico
        elif cohorte == "B":
            t_inmunoterapia = t_metabolico + 6.0
        elif cohorte == "C":
            t_inmunoterapia = t_metabolico + 12.0
        elif cohorte == "D":
            t_inmunoterapia = t_metabolico + 24.0

        for t in tiempo:
            # 1. Simulación sistémica del colon (Akkermansia -> IL-6)
            IL6_sist, LPS_sist = gut.simular_eje_porta_hepatico(t)

            # 2. Expresión dinámica de PD-L1 regulada por el eje IL-6/STAT3
            PDL1_t = 1.0 * (1.0 + alpha_IL6_PDL1 * (IL6_sist / (IL6_sist + K_IL6_tumor)))
            tumor.PD_L1_expresion = PDL1_t

            # 3. Metabolismo tumoral basal y resistencia adaptativa (MCT2)
            if t < t_metabolico:
                tumor.pHe = 6.20
                tumor.pHi = 7.20
                tumor.mct2_expresion = 1.0
                eficiencia_cd8_basal = 0.0
            else:
                if tumor.mutacion_mct2_activa:
                    if inhibicion_mct2:
                        tumor.mct2_expresion = 0.5
                    else:
                        tumor.mct2_expresion = 1.0 + (15.0 - 1.0) * (1 - math.exp(-0.1 * (t - t_metabolico)))
                else:
                    tumor.mct2_expresion = 0.5 if inhibicion_mct2 else 1.0

                pHi_minimo = max(5.50, 5.75 + 0.85 * (1 - 1.0 / tumor.mct2_expresion))
                decay_pHi = (7.20 - pHi_minimo) * (1 - math.exp(-0.4 * (t - t_metabolico)))
                tumor.pHi = max(pHi_minimo, 7.20 - decay_pHi)

                pHe_maximo = min(7.35, 7.35 - 0.75 * (1 - 1.0 / tumor.mct2_expresion))
                lavado_pHe = (pHe_maximo - 6.20) * (1 - math.exp(-0.25 * (t - t_metabolico)))
                tumor.pHe = min(pHe_maximo, 6.20 + lavado_pHe)

                atp_minimo = max(10.0, 30.0 + 770.0 * (1 - 1.0 / tumor.mct2_expresion))
                atp_drop = (10000.0 - atp_minimo) * (1 - math.exp(-0.35 * (t - t_metabolico)))
                tumor.atp_nivel = max(atp_minimo, 10000.0 - atp_drop)

                # Eficiencia de migración de linfocitos según el pH extracelular local (parálisis ácida)
                if tumor.pHe > 6.50:
                    eficiencia_cd8_basal = (tumor.pHe - 6.50) / (7.35 - 6.50)
                else:
                    eficiencia_cd8_basal = 0.0

            eficiencia_cd8_basal = min(1.0, max(0.0, eficiencia_cd8_basal))

            # 4. Agotamiento Epigenético inducido por el camuflaje PD-L1 y la inflamación IL-6
            dTOX = k_TOX_activation * PDL1_t * (IL6_sist / (IL6_sist + K_IL6_tumor)) - d_TOX_decay * current_TOX
            current_TOX += dTOX * self.paso_tiempo
            
            dEpigenetic = 0.0015 * current_TOX
            current_epigenetic += dEpigenetic * self.paso_tiempo
            H3K27me3_val = min(current_epigenetic, 1.0)

            # 5. Viabilidad del linfocito CAR-T/CD8+ bajo acidez estromal profunda (pHe)
            # El blindaje NHE1-Shield protege la viabilidad del linfocito
            if has_shield:
                # Decaimiento lento por viabilidad protegida (vida media ~ 50 horas en ácido)
                viab_cart = 100.0 * math.exp(-t/50.0) * (1.0 - 0.5 * H3K27me3_val)
            else:
                # Colapso rápido convencional bajo acidez (vida media ~ 1 hora)
                viab_cart = 100.0 * math.exp(-t/1.0) * (1.0 - 0.8 * H3K27me3_val)
            viab_cart = np.clip(viab_cart, 0.0, 100.0)

            # 6. Sinergia Lítica e Inmunoterapia anti-PD-1
            if t >= t_inmunoterapia:
                efectividad_PD1 = 1.0 if tumor.pHe >= 7.30 else (tumor.pHe - 6.0) / (7.35 - 6.0)
                efectividad_PD1 = max(0.0, efectividad_PD1)
                
                # Capacidad citotóxica efectiva regulada por viabilidad, inmunoterapia y el freno de histonas
                fuerza_citotoxica = (viab_cart / 100.0) * eficiencia_cd8_basal * efectividad_PD1 * (1.0 - H3K27me3_val)
                fuerza_citotoxica = max(0.0, fuerza_citotoxica)

                # Depuración clonal tumoral
                depuracion = tumor.viabilidad * (1.0 - math.exp(-0.5 * fuerza_citotoxica * (t - t_inmunoterapia)))
                tumor.viabilidad = max(0.0, tumor.viabilidad - depuracion)
            else:
                fuerza_citotoxica = 0.0
                if tumor.pHi < 5.80:
                    tumor.viabilidad = max(0.2, tumor.viabilidad - 0.01 * (t - t_metabolico))
                else:
                    tumor.viabilidad = 1.0

            pHi_history.append(tumor.pHi)
            pHe_history.append(tumor.pHe)
            atp_history.append(tumor.atp_nivel)
            viabilidad_history.append(tumor.viabilidad)
            mct2_history.append(tumor.mct2_expresion)
            il6_history.append(IL6_sist)
            pdl1_history.append(PDL1_t)
            h3k27me3_history.append(H3K27me3_val * 100.0)
            viabilidad_cart_history.append(viab_cart)
            citotox_history.append(fuerza_citotoxica * 100.0)

        # Convertir todo a arreglos de numpy para evitar problemas al graficar
        return {
            "tiempo": np.array(tiempo),
            "pHi": np.array(pHi_history),
            "pHe": np.array(pHe_history),
            "atp": np.array(atp_history),
            "viabilidad": np.array(viabilidad_history),
            "mct2": np.array(mct2_history),
            "il6": np.array(il6_history),
            "pdl1": np.array(pdl1_history),
            "h3k27me3": np.array(h3k27me3_history),
            "viability_cart": np.array(viabilidad_cart_history),
            "citotox": np.array(citotox_history)
        }


if __name__ == "__main__":
    print("=====================================================================")
    print("INICIANDO MOTOR INTEGRADO DE BIOCONTROL Y BARRERA DE MUCOSA (v6.0)")
    print("=====================================================================\n")

    # 1. Validación de Exclusiones de Barrera (Regulador)
    sana = CelulaHumana(tipo_celular="Sana")
    regulador = ReguladorRestricciones(sana)

    print("-> Ejecutando Verificaciones de Exclusiones Semánticas (Doctrina Gut-Barrier):")
    # Caso eubiótico
    viab, alarmas_eub = regulador.evaluar_homeostasis(phi_gut=1.0)
    print(f"   * Saneado (phi=1.0) | Viabilidad: {viab*100:.1f}% | Alarmas: {len(alarmas_eub)}")
    
    # Caso Leaky Gut Severo
    viab_leak, alarmas_leak = regulador.evaluar_homeostasis(phi_gut=0.1)
    print(f"   * Leaky Gut (phi=0.1) | Viabilidad: {viab_leak*100:.1f}% | Alarmas detectadas:")
    for al in alarmas_leak:
        print(f"     - [ALERTA] {al}")
    print("-" * 69 + "\n")

    # 2. Simulación Multiescala Temporal de Co-Intervenciones
    sim = SimuladorTratamientoV6()

    print("-> Simulando Cohorte C (Tratamiento Combinado de 72 horas) bajo 4 Escenarios:")
    
    # Escenario 1: T Convencional + Leaky Gut
    res_1 = sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=True, phi_gut=0.20, has_shield=False)
    # Escenario 2: NHE1-Shield + Leaky Gut
    res_2 = sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=True, phi_gut=0.20, has_shield=True)
    # Escenario 3: T Convencional + Akkermansia
    res_3 = sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=True, phi_gut=0.92, has_shield=False)
    # Escenario 4: Sinergia Total (NHE1-Shield + Akkermansia)
    res_4 = sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=True, phi_gut=0.92, has_shield=True)

    print(f"   [1] T Convencional + Leaky Gut   | Viabilidad Tumoral Remanente: {res_1['viabilidad'][-1]*100:.2f}%")
    print(f"   [2] NHE1-Shield + Leaky Gut      | Viabilidad Tumoral Remanente: {res_2['viabilidad'][-1]*100:.2f}%")
    print(f"   [3] T Convencional + Akkermansia | Viabilidad Tumoral Remanente: {res_3['viabilidad'][-1]*100:.2f}%")
    print(f"   [4] Sinergia Total (NHE1 + Akker)| Viabilidad Tumoral Remanente: {res_4['viabilidad'][-1]*100:.2f}%")
    print("-" * 69 + "\n")

    # -------------------------------------------------------------------------
    # GENERACIÓN DE GRÁFICO CIENTÍFICO INTEGRADO
    # -------------------------------------------------------------------------
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 11))
    
    fig.suptitle("Ecosistema Acoplado v6.0: Sinergia de Barrera Intestinal (Akkermansia) y Escudo local (NHE1-Shield)",
                 fontsize=15, fontweight='bold', y=0.98)

    tiempo_h = res_1["tiempo"]

    # Panel 1: IL-6 Sistémica Portal (Eje de Alarma Hepática)
    ax1.plot(tiempo_h, res_1["il6"], color="#e7298a", lw=2.5, linestyle=":", label="Leaky Gut (phi_gut = 0.20)")
    ax1.plot(tiempo_h, res_4["il6"], color="#4daf4a", lw=2.5, linestyle="-", label="Akkermansia (phi_gut = 0.92)")
    ax1.axhline(y=500.0, color='red', linestyle='--', alpha=0.6, label="Umbral Inflamatorio Crítico")
    ax1.set_title("A. Dinámica de IL-6 en el Estroma Hepático", fontsize=11, fontweight='bold')
    ax1.set_xlabel("Tiempo (Horas)")
    ax1.set_ylabel("IL-6 (pg/mL)")
    ax1.legend(fontsize=9, loc="upper right")

    # Panel 2: Upregulation de PD-L1 en Hepatocarcinoma
    ax2.plot(tiempo_h, res_1["pdl1"], color="#e7298a", lw=2.5, linestyle=":", label="Leaky Gut (phi_gut = 0.20)")
    ax2.plot(tiempo_h, res_4["pdl1"], color="#4daf4a", lw=2.5, linestyle="-", label="Akkermansia (phi_gut = 0.92)")
    ax2.set_title("B. Upregulation de PD-L1 Inducida por STAT3", fontsize=11, fontweight='bold')
    ax2.set_xlabel("Tiempo (Horas)")
    ax2.set_ylabel("Expresión de PD-L1 (Relativa)")
    ax2.legend(fontsize=9, loc="upper right")

    # Panel 3: Agotamiento Epigenético de CAR-T (H3K27me3 en promotores IL2/IFNG)
    ax3.plot(tiempo_h, res_1["h3k27me3"], color="#e7298a", lw=2.5, linestyle=":", label="Convencional + Leaky Gut")
    ax3.plot(tiempo_h, res_2["h3k27me3"], color="#d95f02", lw=2.5, linestyle="--", label="NHE1-Shield + Leaky Gut")
    ax3.plot(tiempo_h, res_3["h3k27me3"], color="#377eb8", lw=2.5, linestyle="-.", label="Convencional + Akkermansia")
    ax3.plot(tiempo_h, res_4["h3k27me3"], color="#4daf4a", lw=2.5, linestyle="-", label="Sinergia Total")
    ax3.set_title("C. Bloqueo Epigenético de Linfocitos (H3K27me3 %)", fontsize=11, fontweight='bold')
    ax3.set_xlabel("Tiempo (Horas)")
    ax3.set_ylabel("% Promotores Silenciados")
    ax3.legend(fontsize=8, loc="upper left")

    # Panel 4: Depuración Clonal Tumoral (Viabilidad de Hepatocarcinoma)
    ax4.plot(tiempo_h, res_1["viabilidad"] * 100.0, color="#e7298a", lw=2.5, linestyle=":", label="T Conv + Leaky Gut")
    ax4.plot(tiempo_h, res_2["viabilidad"] * 100.0, color="#d95f02", lw=2.5, linestyle="--", label="NHE1-Shield + Leaky Gut")
    ax4.plot(tiempo_h, res_3["viabilidad"] * 100.0, color="#377eb8", lw=2.5, linestyle="-.", label="T Conv + Akkermansia")
    ax4.plot(tiempo_h, res_4["viabilidad"] * 100.0, color="#4daf4a", lw=2.5, linestyle="-", label="Sinergia Total (Lisis: 100%)")
    ax4.set_title("D. Viabilidad Remanente del Hepatocarcinoma (%)", fontsize=11, fontweight='bold')
    ax4.set_xlabel("Tiempo (Horas)")
    ax4.set_ylabel("Viabilidad del Tumor (%)")
    ax4.legend(fontsize=8, loc="lower left")

    plt.tight_layout(pad=2.0)
    grafico_v6_path = os.path.join(visuales_dir, "grafico_onco_homeostasis_v6.png")
    plt.savefig(grafico_v6_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[OK] Grafico multicapa v6 generado con exito en: {grafico_v6_path}")
