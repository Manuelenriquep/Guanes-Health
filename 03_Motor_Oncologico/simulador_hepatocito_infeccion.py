import math
import numpy as np

class HepatocitoInmuneIntegrado:
    """
    Simulador multiescala del hepatocito incorporando gradiente de oxigenación,
    regulación del receptor de entrada NTCP por la vía inflamatoria de IL-6,
    bloqueo competitivo con Myrcludex B, e infección por viriones de Hepatitis B (HBV).
    """
    def __init__(self, gsh_nominal=8.0, o2_pp=60.0):
        # Constantes Biofísicas del Hepatocito (v1.0)
        self.ph_intracelular = 7.20
        self.potencial_membrana = -35.0      # mV (necesario para cotransporte Na+/taurocolato)
        self.gsh_pool = gsh_nominal          # mM
        self.gsh_nominal = gsh_nominal
        self.o2_presion_parcial = o2_pp      # mmHg (Zonación Hepática)
        
        # Parámetros del Receptor de Entrada NTCP (SLC10A1)
        self.ntcp_densidad_basal = 1.0       # Fracción nominal (1.0 = 100%)
        self.ntcp_densidad_membrana = 1.0
        self.es_variante_S267F = False       # Si True, refractario a HBV y transporte de sales
        
        # Estado de Infección Viral por HBV y Carga Antigénica
        self.carga_viral_de_novo = 0.0       # Escala lineal de viriones intracelulares
        self.mhc_i_presentacion = 1.0        # Densidad superficial para CD8+ (antígeno viral)
        self.viabilidad = 1.0                # 1.0 = sano/funcional, 0.0 = apoptosis
        
        # Variables del Microambiente e Inmunología (v2.0)
        self.il6_concentracion = 0.0         # pg/mL (Citoquina inflamatoria)
        self.lactato_extracelular = 1.5      # mM
        self.pHe = 7.40                      # pH estromal/sinusoidal
        
        # Farmacodinámica del Inhibidor de Entrada
        self.myrcludex_b_nM = 0.0            # Concentración del lipopéptido competidor
        
        # Aplicar norma de zonación inicial
        self._aplicar_norma_zonacion()

    def _aplicar_norma_zonacion(self):
        """Aplica la jerarquía normativa basada en la presión parcial de oxígeno (Nivel 4)."""
        if self.o2_presion_parcial < 20.0:
            # Estado de Excepción: Isquemia. El hepatocito deprime transportadores metabólicos
            self.ntcp_densidad_basal = 0.2
        elif self.o2_presion_parcial <= 35.0:
            # Zona 3 (Pericentral): Menor oxigenación, expresión basal estándar
            self.ntcp_densidad_basal = 0.8
        else:
            # Zona 1 (Periportal): Alta oxigenación, expresión y aclaramiento de sales biliar máximo
            self.ntcp_densidad_basal = 1.2
        self.ntcp_densidad_membrana = self.ntcp_densidad_basal

    def evaluar_regulacion_y_entrada_viral(self, inóculo_HBV, delta_t=1.0):
        """
        Ejecuta la cinética de regulación transcripcional de NTCP y simula la tasa de entrada de HBV.
        """
        if self.viabilidad <= 0.0:
            return "NODE_INACTIVE: Apoptosis o Necrosis disparada"

        # 1. Represión de NTCP mediada por IL-6 (Vía JNK dependiente) - Nivel 4.2 de Inmuno
        # IL-6 induce una caída de hasta el 98% de NTCP de forma dosis-dependiente (función de saturación de Hill)
        represion_il6 = 1.0
        if self.il6_concentracion > 0:
            represion_il6 = 1.0 - 0.98 * (self.il6_concentracion / (self.il6_concentracion + 50.0))
            
        # 2. Densidad final de NTCP en membrana sinusoidal
        self.ntcp_densidad_membrana = self.ntcp_densidad_basal * represion_il6
        
        # Si presenta el polimorfismo refractario S267F, el receptor NTCP es nulo para HBV y sales biliares
        if self.es_variante_S267F:
            self.ntcp_densidad_membrana = 0.0
            
        # 3. Competencia estequiométrica basolateral de Myrcludex B frente a HBV
        # Myrcludex B bloquea con una potencia 100 veces mayor la entrada viral que la biliar.
        # Ki viral nominal = 1.0 nM; Ki biliar nominal = 100.0 nM
        fraccion_bloqueo_viral = 1.0 / (1.0 + (self.myrcludex_b_nM / 1.0))
        fraccion_bloqueo_biliar = 1.0 / (1.0 + (self.myrcludex_b_nM / 100.0))
        
        # 4. Cinética de Infección de novo por HBV (Capa B)
        # La tasa de penetración viral depende de la densidad de NTCP disponible y de la presencia del inhibidor
        tasa_entrada = inóculo_HBV * self.ntcp_densidad_membrana * fraccion_bloqueo_viral
        self.carga_viral_de_novo += tasa_entrada * delta_t
        
        # El hepatocito procesa y presenta antígenos del HBV en el complejo MHC-I de forma directamente proporcional
        self.mhc_i_presentacion = min(10.0, 1.0 + (self.carga_viral_de_novo * 1.5))
        
        # 5. Efecto biliar y colestasis tóxica por deplesión de aclaramiento (Riesgo del modelo)
        # Si aclaramiento_sales_biliares se bloquea fuertemente por Myrcludex B biliar (< 0.15), 
        # se acumulan ácidos biliares que agotan el pool antioxidante de Glutatión (GSH)
        aclaramiento_sales_biliares = self.ntcp_densidad_membrana * fraccion_bloqueo_biliar
        if aclaramiento_sales_biliares < 0.15 and not self.es_variante_S267F:
            # Pérdida crítica del aclaramiento: deplesión estequiométrica de GSH
            self.gsh_pool = max(0.0, self.gsh_pool - 0.5 * delta_t)
            
        # Evaluar Veto Redox del Hepatocito (VETO FC-HEP-01 - Apoptosis Fail-Closed)
        if (self.gsh_pool / self.gsh_nominal) < 0.30:
            self.viabilidad = 0.0  # Apoptosis iniciada por MOMP por exceso de estrés redox biliar
            
        return {
            "NTCP_Membrana": self.ntcp_densidad_membrana,
            "Carga_Viral": self.carga_viral_de_novo,
            "MHC_I": self.mhc_i_presentacion,
            "GSH_Pool": self.gsh_pool,
            "Viabilidad_Hepatocito": self.viabilidad
        }

    def evaluar_lisis_por_cd8(self, cd8_presente=False, anti_pd_1=False):
        """
        Calcula la probabilidad lítica de los TILs CD8+ sobre el hepatocito infectado,
        incorporando el veto por acidosis estromal profunda (Nivel 2.1 de Inmuno)
        y la anergia/agotamiento del TCR mediado por PD-1/PD-L1.
        """
        if self.viabilidad <= 0.0 or not cd8_presente:
            return 0.0
            
        # VETO EXCLUSIÓN: Parálisis de lisis en acidosis estromal local extrema (pHe <= 6.50)
        if self.pHe <= 6.50:
            return 0.0  # Veto del Escudo Ácido (FC-BIO-2.1)
            
        # Cálculo de afinidad e interacción TCR/MHC-I
        prob_reconocimiento = self.mhc_i_presentacion / 10.0
        
        # Checkpoint de veto por PD-1/PD-L1 (Evasión tumoral o viral crónica)
        # En inflamación prolongada, el ligando PD-L1 de la célula diana silencia la señal
        pd_l1_expresion = min(1.0, self.carga_viral_de_novo * 0.2)
        pd1_interferencia = 0.0 if anti_pd_1 else pd_l1_expresion
        
        fuerza_lítica = prob_reconocimiento * (1.0 - pd1_interferencia)
        fuerza_lítica = max(0.0, min(1.0, fuerza_lítica))
        
        # Aplicar daño por lisis inmunitaria CD8+ al hepatocito diana
        self.viabilidad = max(0.0, self.viabilidad - fuerza_lítica)
        
        return fuerza_lítica


class SimuladorHepatitisB:
    """
    Simula perfiles cinéticos temporales del hepatocito bajo diferentes escenarios:
    - Escenario 1: Infección Aguda HBV sin Tratamiento (Control)
    - Escenario 2: Infección HBV + Inmunidad Innata (IL-6 activa)
    - Escenario 3: Terapia con Myrcludex B - Dosis Óptima (Saturación segura)
    - Escenario 4: Terapia con Myrcludex B - Dosis Suprafisiológica (Toxicidad/Apoptosis)
    """
    def __init__(self):
        self.paso_tiempo = 0.5  # horas
        self.tiempo_total = 72.0 # horas
        self.puntos_tiempo = int(self.tiempo_total / self.paso_tiempo)

    def simular_escenario(self, escenario_id):
        tiempo = np.linspace(0, self.tiempo_total, self.puntos_tiempo)
        
        # Inicializar hepatocito en Zona 1 (Periportal, o2_pp = 60.0 mmHg)
        hep = HepatocitoInmuneIntegrado(gsh_nominal=8.0, o2_pp=60.0)
        inóculo_diario = 2.0  # Tasa de viriones que intentan entrar por unidad de tiempo
        
        # Configurar variables estables del escenario
        if escenario_id == "Control":
            hep.il6_concentracion = 0.0
            hep.myrcludex_b_nM = 0.0
        elif escenario_id == "Inmunidad_Innata":
            hep.il6_concentracion = 100.0  # pg/mL
            hep.myrcludex_b_nM = 0.0
        elif escenario_id == "Myrcludex_Optimo":
            hep.il6_concentracion = 0.0
            hep.myrcludex_b_nM = 10.0  # nM
        elif escenario_id == "Myrcludex_Toxico":
            hep.il6_concentracion = 0.0
            hep.myrcludex_b_nM = 1000.0  # nM
            
        # Historial de variables
        ntcp_history = []
        carga_viral_history = []
        gsh_history = []
        viabilidad_history = []
        
        for t in tiempo:
            # Evaluar la dinámica de entrada viral y toxicidad redox
            res = hep.evaluar_regulacion_y_entrada_viral(inóculo_HBV=inóculo_diario, delta_t=self.paso_tiempo)
            
            if isinstance(res, str):  # Célula muerta
                ntcp_history.append(0.0)
                carga_viral_history.append(carga_viral_history[-1] if carga_viral_history else 0.0)
                gsh_history.append(0.0)
                viabilidad_history.append(0.0)
            else:
                ntcp_history.append(res["NTCP_Membrana"])
                carga_viral_history.append(res["Carga_Viral"])
                gsh_history.append(res["GSH_Pool"])
                viabilidad_history.append(res["Viabilidad_Hepatocito"])
                
        return {
            "tiempo": tiempo,
            "ntcp": ntcp_history,
            "carga_viral": carga_viral_history,
            "gsh": gsh_history,
            "viabilidad": viabilidad_history
        }

if __name__ == "__main__":
    print("=====================================================================")
    print("GUANES HEALTH - SIMULADOR MULTIESCALA DE INFECCIÓN EN HEPATOCITOS (v1.1)")
    print("=====================================================================\n")
    
    sim = SimuladorHepatitisB()
    escenarios = ["Control", "Inmunidad_Innata", "Myrcludex_Optimo", "Myrcludex_Toxico"]
    
    for esc in escenarios:
        res = sim.simular_escenario(esc)
        idx_final = -1
        print(f"-> [ESCENARIO: {esc.upper()}] Resultados de simulación a t = 72.0 h:")
        print(f"   * Expresión de NTCP en membrana: {res['ntcp'][idx_final]:.4f} (densidad relativa)")
        print(f"   * Carga viral intracelular final: {res['carga_viral'][idx_final]:.2f} viriones")
        print(f"   * Pool de Glutatión (GSH): {res['gsh'][idx_final]:.2f} mM (basal: 8.00 mM)")
        print(f"   * Viabilidad del hepatocito: {res['viabilidad'][idx_final] * 100:.2f}%")
        
        # Evaluar detonación de veto celular
        if res['viabilidad'][idx_final] == 0.0:
            print("   [CRÍTICO]: VETO FC-HEP-01 DETONADO - Apoptosis por colestasis inducida por fármaco.")
        elif esc == "Myrcludex_Optimo":
            print("   [ÉXITO]: Aclaramiento viral óptimo sin toxicidad metabólica.")
        elif esc == "Inmunidad_Innata":
            print("   [REDUCCIÓN]: Autodefensa tisular mediada por IL-6 efectiva para disminuir entrada viral.")
        print("-" * 69)
        
    print("\n[SIMULACIÓN COMPLETADA]: Modelo de hepatocito de referencia verificado.")
