import math
import numpy as np

# Constantes del modelo (Capa B)
POTENCIAL_REPOSO_MIN = -70.0       # mV
POTENCIAL_REPOSO_MAX = -90.0       # mV
FIDELIDAD_ADN_POLIMERASA = 1e-7    # Tasa basal de error de replicación
ATP_MINIMO_SOBREVIVENCIA = 0.5     # Umbral de energía relativa (~1.0 mM)
LIMITE_HAYFLICK_MAX = 70           # Límite mitótico fisiológico
UMBRAL_SENESCENCIA_TELOMEROS = 4000 # pb (Umbral de disparo de FC-BIO-02)

class CelulaHumana:
    """Estado biofisico ionico/genomico sana o tumoral (modelo Capa B)."""
    def __init__(self, tipo_celular="Sana", atp_nivel=100.0, daño_genomico=0.0, telomeros=8000, divisiones=0):
        self.tipo_celular = tipo_celular
        self.atp_nivel = atp_nivel
        self.daño_genomico = daño_genomico
        self.telomeros = telomeros
        self.divisiones = divisiones
        
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
        self.viabilidad = 1.0       # 1.0 = viva, 0.0 = lisis/apoptosis
        
        # Parámetros del bypass metabólico adaptativo (MCT2) - Capa B
        self.mct2_expresion = 1.0   # Nivel basal de expresión (1.0)
        self.mutacion_mct2_activa = False

    def degradar_telomeros(self):
        """
        Modelado de replicación con desgaste del extremo 3'.
        Célula sana: tasa de acortamiento de 80 pb por división.
        Célula tumoral (hTERT+): tasa de acortamiento nula (0 pb) por actividad de telomerasa.
        """
        if self.tipo_celular == "Sana":
            self.telomeros -= 80
            self.divisiones += 1
        # hTERT mutado en el tumor compensa el acortamiento, manteniendo el telómero estable.

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

    def evaluar_homeostasis(self):
        """Evalua restricciones homeostaticas del modelo; retorna viabilidad y alarmas."""
        alarmas = []
        V_m = self.calcular_potencial_ghk()

        # REG-I-01: Regulación de Ciclo por Daño Genómico (ATM/ATR -> p53)
        if self.celula.daño_genomico > 2.0:
            if self.celula.tipo_celular == "Sana":
                self.celula.p53_activo = True
                self.celula.p21_WAF1 = min(self.celula.daño_genomico * 10, 100.0)
                alarmas.append("Arresto de ciclo celular en G1/S activo (daño genómico)")
            else:
                # El tumor evade REG-I-01 mediante MDM2 o mutación hotspot
                self.celula.p53_activo = False
                self.celula.p21_WAF1 = 0.0
                alarmas.append("Evasión de auditoría genómica: p53 inactivo")

        # REG-I-02: Balance Bioenergético y Sensor AMPK
        if self.celula.atp_nivel < ATP_MINIMO_SOBREVIVENCIA:
            alarmas.append("Gatillo AMPK activo: Bloqueo de mTORC1 e inducción de autofagia")
            
        # REG-I-03: Potencial de Membrana (Na+/K+ ATPasa)
        if V_m > -55.0:
            # Despolarización: requiere gasto acelerado de ATP para recargar el gradiente iónico
            demanda_bomba = abs(V_m + 55.0) * 1.5
            self.celula.atp_nivel = max(0.0, self.celula.atp_nivel - demanda_bomba)
            alarmas.append(f"Gasto energético de Bomba Na+/K+ ATPasa incrementado por despolarización (V_m: {V_m:.2f} mV)")

        # =====================================================================
        # Regulacion de muerte celular (Capa B)
        # =====================================================================
        
        # VETO FC-BIO-01: Daño Genómico Irreparable (Apoptosis)
        if self.celula.daño_genomico > 8.0:
            if self.celula.tipo_celular == "Sana":
                self.celula.Bax_Bak_libres = True
                self.celula.viabilidad = 0.0
                alarmas.append("VETO FC-BIO-01 activado: Muerte por Apoptosis (MMR Fallido)")
            else:
                # El tumor tiene Bcl-2 sobreexpresado x25 que secuestra Bax/Bak
                if self.celula.Bcl2_expresion >= 25.0:
                    self.celula.Bax_Bak_libres = False
                    alarmas.append("VETO FC-BIO-01 BLOQUEADO: Resistencia apoptótica por taponamiento de Bcl-2")

        # VETO FC-BIO-02: Límite de Hayflick (Senescencia Replicativa)
        # CORRECCIÓN DE FRONTERA: Usar <= para asegurar disparo en la división 50 exacta (8000 - 80 * 50 = 4000)
        if self.celula.telomeros <= UMBRAL_SENESCENCIA_TELOMEROS or self.celula.telomeros <= 10:
            if self.celula.tipo_celular == "Sana":
                self.celula.viabilidad = 0.5  # Senescente
                alarmas.append("VETO FC-BIO-02 activado: Arresto Replicativo Permanente (Senescencia de Hayflick)")
            else:
                alarmas.append("VETO FC-BIO-02 EVADIDO: Inmortalidad telomérica por reactivación de hTERT (Escala de salida: 3920 pb)")

        # VETO FC-BIO-03: Colapso Crítico de Potencial o Energía
        if V_m > -15.0 or self.celula.atp_nivel < 0.2:
            self.celula.viabilidad = 0.0
            self.celula.fosfatidilserina_externa = True
            alarmas.append("VETO FC-BIO-03 activado: Colapso del potencial de membrana. Translocación de Fosfatidilserina (Eat-Me)")

        return self.celula.viabilidad, alarmas

# Simulador de cohortes (modelo)
class SimuladorTratamiento:
    """Simula cohortes MCT/inmuno (Capa B); cronogramas y escape MCT2 segun version."""
    def __init__(self):
        self.paso_tiempo = 0.1  # horas
        self.tiempo_total = 72.0 # horas
        self.puntos_tiempo = int(self.tiempo_total / self.paso_tiempo)

    def ejecutar_simulacion(self, cohorte="C", mutacion_mct2=False, inhibicion_mct2=False):
        tiempo = np.linspace(0, self.tiempo_total, self.puntos_tiempo)
        
        # Inicializar perfiles de simulación
        sana = CelulaHumana(tipo_celular="Sana")
        tumor = CelulaHumana(tipo_celular="Tumor", atp_nivel=10000.0, telomeros=3920)
        tumor.Bcl2_expresion = 25.0  # Sobretaponamiento antiapoptótico
        tumor.pHe = 6.20             # Acidosis estromal basal del tumor
        tumor.PD_L1_expresion = 50.0  # Expresión de camuflaje inmunitario
        tumor.mutacion_mct2_activa = mutacion_mct2
        
        # Historial de variables
        pHi_history = []
        pHe_history = []
        atp_history = []
        viabilidad_history = []
        eficiencia_cd8_history = []
        mct2_history = []

        # Determinar retrasos de dosificación según cohorte
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
            # 1. Fase de Metabolismo basal del tumor o resistencia adaptativa
            if t < t_metabolico:
                tumor.pHe = 6.20
                tumor.pHi = 7.20
                tumor.mct2_expresion = 1.0
                eficiencia_cd8 = 0.0  # Parálisis por acidez estromal profunda
            else:
                # Si el bypass adaptativo MCT2 está activo, se sobreexpresa ante el estrés de protones
                if tumor.mutacion_mct2_activa:
                    if inhibicion_mct2:
                        # El inhibidor de MCT2 bloquea la sobreexpresión adaptativa y reduce la actividad basal a 0.5
                        tumor.mct2_expresion = 0.5
                    else:
                        # MCT2 se activa y sobreexpresa progresivamente hasta un factor de x15
                        tumor.mct2_expresion = 1.0 + (15.0 - 1.0) * (1 - math.exp(-0.1 * (t - t_metabolico)))
                else:
                    if inhibicion_mct2:
                        tumor.mct2_expresion = 0.5
                    else:
                        tumor.mct2_expresion = 1.0
                
                # Dinámica de pHi afectada por el eflujo protónico vía MCT2 (mayor afinidad Km L-lactato ≈ 1.0 mM)
                # Si MCT2 está sobreexpresado, rescata el pHi. Si está inhibido (0.5), exacerba la acidosis
                pHi_minimo = max(5.50, 5.75 + 0.85 * (1 - 1.0 / tumor.mct2_expresion))
                decay_pHi = (7.20 - pHi_minimo) * (1 - math.exp(-0.4 * (t - t_metabolico)))
                tumor.pHi = max(pHi_minimo, 7.20 - decay_pHi)
                
                # El eflujo de protones residual por MCT2 regula el pHe máximo alcanzable
                pHe_maximo = min(7.35, 7.35 - 0.75 * (1 - 1.0 / tumor.mct2_expresion))
                lavado_pHe = (pHe_maximo - 6.20) * (1 - math.exp(-0.25 * (t - t_metabolico)))
                tumor.pHe = min(pHe_maximo, 6.20 + lavado_pHe)
                
                # Colapso mitigado de ATP o colapso exacerbado por triple inhibición
                atp_minimo = max(10.0, 30.0 + 770.0 * (1 - 1.0 / tumor.mct2_expresion))
                atp_drop = (10000.0 - atp_minimo) * (1 - math.exp(-0.35 * (t - t_metabolico)))
                tumor.atp_nivel = max(atp_minimo, 10000.0 - atp_drop)
                
                # Recuperación pasiva de la eficiencia de linfocitos CD8+ TILs (atenuada por acidez estromal residual)
                if tumor.pHe > 7.0:
                    eficiencia_cd8_basal = (tumor.pHe - 7.0) / (7.35 - 7.0)
                else:
                    eficiencia_cd8_basal = 0.0
                eficiencia_cd8 = min(1.0, eficiencia_cd8_basal)

            # 2. Introducción de Inmunoterapia anti-PD-1
            if t >= t_inmunoterapia:
                # La efectividad del anti-PD-1 depende del pH extracelular (estabilidad Fab)
                efectividad_PD1 = 1.0 if tumor.pHe >= 7.30 else (tumor.pHe - 6.0) / (7.35 - 6.0)
                efectividad_PD1 = max(0.0, efectividad_PD1)
                
                # Sinergia lítica inmunitaria
                fuerza_citotoxica = eficiencia_cd8 * efectividad_PD1
                
                # Depuración clonal tumoral (colapso de viabilidad)
                depuracion = (tumor.viabilidad - 0.0) * (1 - math.exp(-0.5 * fuerza_citotoxica * (t - t_inmunoterapia)))
                tumor.viabilidad = max(0.0, tumor.viabilidad - depuracion)
            else:
                # Evade la inmunovigilancia por PD-L1 a pesar de pHe fisiológico
                if tumor.pHi < 5.80:
                    # Muerte parcial pasiva por autólisis ácida interna
                    tumor.viabilidad = max(0.2, tumor.viabilidad - 0.01 * (t - t_metabolico))
                else:
                    tumor.viabilidad = 1.0

            pHi_history.append(tumor.pHi)
            pHe_history.append(tumor.pHe)
            atp_history.append(tumor.atp_nivel)
            viabilidad_history.append(tumor.viabilidad)
            mct2_history.append(tumor.mct2_expresion)
            
            # Eficiencia de TILs CD8+ (Salida de modelo, no constituye evidencia clínica)
            actual_efficiency = eficiencia_cd8 * (1.0 if t >= t_inmunoterapia and tumor.pHe >= 7.30 else 0.1)
            eficiencia_cd8_history.append(min(1.0, actual_efficiency) * 100.0)

        return {
            "tiempo": tiempo,
            "pHi": pHi_history,
            "pHe": pHe_history,
            "atp": atp_history,
            "viabilidad": viabilidad_history,
            "eficiencia_cd8": eficiencia_cd8_history,
            "mct2": mct2_history
        }

if __name__ == "__main__":
    print("=== Homeostasis oncologica v2.4 (modelo) ===\n")

    sana = CelulaHumana(tipo_celular="Sana")
    regulador_sana = ReguladorRestricciones(sana)
    for _ in range(50):
        sana.degradar_telomeros()
    pot_sana = regulador_sana.calcular_potencial_ghk()
    viab_sana, alarmas_sanas = regulador_sana.evaluar_homeostasis()
    print(f"[SANA] gen={sana.divisiones}  tel={sana.telomeros} pb  "
          f"V_m={pot_sana:.2f} mV  viab={viab_sana * 100:.1f}%\n")

    sim = SimuladorTratamiento()

    res_std = sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=False, inhibicion_mct2=False)
    print(
        f"[C estandar] pHi={res_std['pHi'][-1]:.2f}  pHe={res_std['pHe'][-1]:.2f}  "
        f"ATP={res_std['atp'][-1]:.1f}  CD8={res_std['eficiencia_cd8'][-1]:.1f}%  "
        f"viab={res_std['viabilidad'][-1] * 100:.2f}%"
    )

    res_esc = sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=True, inhibicion_mct2=False)
    print(
        f"[C + MCT2] mct2={res_esc['mct2'][-1]:.1f}x  "
        f"pHi={res_esc['pHi'][-1]:.2f}  pHe={res_esc['pHe'][-1]:.2f}  "
        f"ATP={res_esc['atp'][-1]:.1f}  CD8={res_esc['eficiencia_cd8'][-1]:.1f}%  "
        f"viab={res_esc['viabilidad'][-1] * 100:.2f}%"
    )

    res_trip = sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=True, inhibicion_mct2=True)
    print(
        f"[C triple bloqueo] mct2={res_trip['mct2'][-1]:.2f}x  "
        f"pHi={res_trip['pHi'][-1]:.2f}  pHe={res_trip['pHe'][-1]:.2f}  "
        f"ATP={res_trip['atp'][-1]:.1f}  CD8={res_trip['eficiencia_cd8'][-1]:.1f}%  "
        f"viab={res_trip['viabilidad'][-1] * 100:.2f}%"
    )
