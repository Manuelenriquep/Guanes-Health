import math
import numpy as np
import sys
import os

_MOTOR_DIR = os.path.abspath(os.path.dirname(__file__))
if _MOTOR_DIR not in sys.path:
    sys.path.insert(0, _MOTOR_DIR)

from simulador_onco_homeostasis_v4 import CelulaHumana as CelulaTumor
from simulador_hepatocito_infeccion import HepatocitoInmuneIntegrado as HepatocitoSano

# =====================================================================
# SIMULADOR ACOPLADO BIDIRECCIONAL: ECOBISTEMA TUMOR-HEPATOCITO (v2.0)
# =====================================================================
class SimuladorOncoHepaticoBidireccional:
    """
    Simulador multiescala que acopla el modelo tumoral v2.4 (Capa B) y el modelo 
    del hepatocito v1.1 (Capa B), permitiendo evaluar tanto el acoplamiento
    unidireccional (estroma -> hepatocito) como el bucle de retroalimentación 
    recíproco (Hepatocito/IL-6 -> STAT3 -> PD-L1/EMT -> Tumor).
    """
    def __init__(self):
        self.paso_tiempo = 0.1  # horas
        self.tiempo_total = 72.0 # horas
        self.puntos_tiempo = int(self.tiempo_total / self.paso_tiempo)

    def ejecutar_simulacion(self, cohorte="C", mutacion_mct2=False, inhibicion_mct2=False,
                             infeccion_hbv=True, inóculo_tasa=10.0, myrcludex_nM=0.0,
                             feedback_activo=False, beta_pd_l1=3.0):
        tiempo = np.linspace(0, self.tiempo_total, self.puntos_tiempo)
        
        # 1. Inicializar componentes del microambiente hepático-tumoral
        tumor = CelulaTumor(tipo_celular="Tumor", atp_nivel=10000.0, telomeros=3920)
        tumor.Bcl2_expresion = 25.0
        tumor.pHe = 6.20
        tumor.PD_L1_expresion = 50.0  # Nivel basal
        tumor.mutacion_mct2_activa = mutacion_mct2
        
        # El hepatocito se localiza en el mismo microambiente sinusoidal adyacente
        hepatocito = HepatocitoSano(gsh_nominal=8.0, o2_pp=60.0) # Zona 1 (Periportal)
        hepatocito.myrcludex_b_nM = myrcludex_nM
        
        # Historial de variables acopladas
        pHi_history = []
        pHe_history = []
        atp_history = []
        viabilidad_tumor_history = []
        eficiencia_cd8_history = []
        mct2_history = []
        
        viral_load_history = []
        gsh_history = []
        viabilidad_hep_history = []
        il6_history = []
        pd_l1_tumor_history = []

        # Tiempos de dosificación
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
            # --- FASE 1: DINÁMICA DEL TUMOR (ESTROMA) ---
            if t < t_metabolico:
                tumor.pHe = 6.20
                tumor.pHi = 7.20
                tumor.mct2_expresion = 1.0
                eficiencia_cd8 = 0.0
            else:
                if tumor.mutacion_mct2_activa:
                    if inhibicion_mct2:
                        tumor.mct2_expresion = 0.5
                    else:
                        tumor.mct2_expresion = 1.0 + (15.0 - 1.0) * (1 - math.exp(-0.1 * (t - t_metabolico)))
                else:
                    if inhibicion_mct2:
                        tumor.mct2_expresion = 0.5
                    else:
                        tumor.mct2_expresion = 1.0
                
                pHi_minimo = max(5.50, 5.75 + 0.85 * (1 - 1.0 / tumor.mct2_expresion))
                decay_pHi = (7.20 - pHi_minimo) * (1 - math.exp(-0.4 * (t - t_metabolico)))
                tumor.pHi = max(pHi_minimo, 7.20 - decay_pHi)
                
                pHe_maximo = min(7.35, 7.35 - 0.75 * (1 - 1.0 / tumor.mct2_expresion))
                lavado_pHe = (pHe_maximo - 6.20) * (1 - math.exp(-0.25 * (t - t_metabolico)))
                tumor.pHe = min(pHe_maximo, 6.20 + lavado_pHe)
                
                atp_minimo = max(10.0, 30.0 + 770.0 * (1 - 1.0 / tumor.mct2_expresion))
                atp_drop = (10000.0 - atp_minimo) * (1 - math.exp(-0.35 * (t - t_metabolico)))
                tumor.atp_nivel = max(atp_minimo, 10000.0 - atp_drop)
                
                if tumor.pHe > 7.0:
                    eficiencia_cd8_basal = (tumor.pHe - 7.0) / (7.35 - 7.0)
                else:
                    eficiencia_cd8_basal = 0.0
                
                if feedback_activo:
                    # En feedback activo, la inflamación local por IL-6 también contribuye a atenuar CD8+
                    eficiencia_cd8 = min(1.0, eficiencia_cd8_basal * (1.0 / (1.0 + (hepatocito.il6_concentracion / 10.0))))
                else:
                    eficiencia_cd8 = min(1.0, eficiencia_cd8_basal)

            # --- FASE 2: ACOPLAMIENTO AL HEPATOCITO (UNIDIRECCIONAL) ---
            # El hepatocito comparte el pHe sinusoidal dictado por el estroma del tumor
            hepatocito.pHe = tumor.pHe
            
            # Cinética de infección viral de novo del hepatocito
            inóculo_actual = inóculo_tasa if (infeccion_hbv and hepatocito.viabilidad > 0.0) else 0.0
            hep_res = hepatocito.evaluar_regulacion_y_entrada_viral(inóculo_actual, delta_t=self.paso_tiempo)
            
            # Lisis del hepatocito mediada por inmunidad CD8+ (si el microambiente no está en parálisis)
            # El anti-PD-1 está presente si t >= t_inmunoterapia
            cd8_presente = (eficiencia_cd8 > 0.1)
            anti_pd_1_activo = (t >= t_inmunoterapia)
            
            # Evaluar lisis inmunitaria del hepatocito
            fuerza_lisis_hep = hepatocito.evaluar_lisis_por_cd8(cd8_presente=cd8_presente, anti_pd_1=anti_pd_1_activo)

            # --- FASE 3: RETROALIMENTACIÓN COMPLEJA (HEPATOCITO -> TUMOR) ---
            # En respuesta a la infección de novo y la lisis celular, el hepatocito secreta IL-6
            # La concentración local de IL-6 es directamente proporcional a la carga viral y a la lisis (DAMPs)
            if feedback_activo:
                # Secreción dinámica: proporcional a carga viral + liberación por lisis/daño de membrana (DAMPs)
                liberacion_il6 = 2.0 * hepatocito.carga_viral_de_novo + 100.0 * (1.0 - hepatocito.viabilidad)
                # Acumulación local en parénquima
                hepatocito.il6_concentracion = max(0.0, liberacion_il6)
                
                # RETROALIMENTACIÓN VÍA STAT3: IL-6 sobreexpresa PD-L1 en el tumor
                # Incremento del escudo inmunitario del tumor por encima del basal (50.0)
                tumor.PD_L1_expresion = 50.0 + beta_pd_l1 * hepatocito.il6_concentracion
            else:
                hepatocito.il6_concentracion = 0.0
                tumor.PD_L1_expresion = 50.0

            # --- FASE 4: DEPURAClÓN DEL TUMOR (CHECKPOINT ADAPTADO) ---
            if t >= t_inmunoterapia:
                # El tumor escapa por saturación de anticuerpos si PD-L1 supera el umbral terapéutico de 150.0
                if tumor.PD_L1_expresion >= 150.0:
                    efectividad_PD1 = 0.0
                else:
                    efectividad_PD1 = 1.0 if tumor.pHe >= 7.30 else (tumor.pHe - 6.0) / (7.35 - 6.0)
                    efectividad_PD1 = max(0.0, efectividad_PD1) * (50.0 / tumor.PD_L1_expresion)
                
                fuerza_citotoxica = eficiencia_cd8 * efectividad_PD1
                
                depuracion = (tumor.viabilidad - 0.0) * (1 - math.exp(-0.5 * fuerza_citotoxica * (t - t_inmunoterapia)))
                tumor.viabilidad = max(0.0, tumor.viabilidad - depuracion)
            else:
                if tumor.pHi < 5.80:
                    tumor.viabilidad = max(0.2, tumor.viabilidad - 0.01 * (t - t_metabolico))
                else:
                    tumor.viabilidad = 1.0

            # Guardar historiales
            pHi_history.append(tumor.pHi)
            pHe_history.append(tumor.pHe)
            atp_history.append(tumor.atp_nivel)
            viabilidad_tumor_history.append(tumor.viabilidad)
            eficiencia_cd8_history.append(eficiencia_cd8 * 100.0)
            mct2_history.append(tumor.mct2_expresion)
            
            viral_load_history.append(hepatocito.carga_viral_de_novo)
            gsh_history.append(hepatocito.gsh_pool)
            viabilidad_hep_history.append(hepatocito.viabilidad)
            il6_history.append(hepatocito.il6_concentracion)
            pd_l1_tumor_history.append(tumor.PD_L1_expresion)

        return {
            "tiempo": tiempo,
            "pHi": pHi_history,
            "pHe": pHe_history,
            "atp": atp_history,
            "viabilidad_tumor": viabilidad_tumor_history,
            "eficiencia_cd8": eficiencia_cd8_history,
            "mct2": mct2_history,
            "carga_viral": viral_load_history,
            "gsh": gsh_history,
            "viabilidad_hepatocito": viabilidad_hep_history,
            "il6": il6_history,
            "pd_l1_tumor": pd_l1_tumor_history
        }

if __name__ == "__main__":
    print("=====================================================================")
    print("INICIANDO EVALUACIÓN DEL BUCLE DE RETROALIMENTACIÓN RECÍPROCO (v2.0)")
    print("=====================================================================\n")
    
    sim = SimuladorOncoHepaticoBidireccional()
    
    # 1. Ejecutar Escenario Unireccional estándar (Sin feedback)
    res_uni = sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=False, feedback_activo=False)
    print("-> [ESCENARIO 1: UNIDIRECCIONAL ESTÁNDAR (Sin Feedback)]")
    print(f"   * pHe estromal terminal: {res_uni['pHe'][-1]:.2f}")
    print(f"   * Viabilidad tumoral terminal: {res_uni['viabilidad_tumor'][-1]*100:.2f}% (Aclaramiento Exitoso)")
    print(f"   * Viabilidad hepatocito terminal: {res_uni['viabilidad_hepatocito'][-1]*100:.2f}% (Aclaramiento Inmune de HBV)")
    print(f"   * Carga viral hepática terminal: {res_uni['carga_viral'][-1]:.2f} viriones")
    print("-" * 69)

    # 2. Ejecutar Escenario Unireccional con Escape MCT2 (Sin feedback)
    res_esc = sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=True, feedback_activo=False)
    print("-> [ESCENARIO 2: ESCAPE MCT2 UNIDIRECCIONAL (Santuario Viral)]")
    print(f"   * pHe estromal terminal: {res_esc['pHe'][-1]:.2f} (Acidosis persistente)")
    print(f"   * Viabilidad tumoral terminal: {res_esc['viabilidad_tumor'][-1]*100:.2f}% (Escape Tumoral por MCT2)")
    print(f"   * Viabilidad hepatocito terminal: {res_esc['viabilidad_hepatocito'][-1]*100:.2f}% (Protección de Infección)")
    print(f"   * Carga viral hepática terminal: {res_esc['carga_viral'][-1]:.2f} viriones (Santuario)")
    print("-" * 69)

    # 3. Ejecutar Escenario con Retroalimentación Activa (Opción A)
    res_bid = sim.ejecutar_simulacion(cohorte="C", mutacion_mct2=False, feedback_activo=True, beta_pd_l1=3.0)
    print("-> [ESCENARIO 3: RETROALIMENTACIÓN RECÍPROCA (Opción A - Bucle Activado)]")
    print(f"   * Concentración terminal de IL-6: {res_bid['il6'][-1]:.2f} pg/mL")
    print(f"   * Expresión inducida de PD-L1 tumoral: {res_bid['pd_l1_tumor'][-1]:.2f}x (Basal: 50.0x)")
    print(f"   * Viabilidad tumoral terminal: {res_bid['viabilidad_tumor'][-1]*100:.2f}% (Escape Tumoral inducido por Infección)")
    print(f"   * Viabilidad hepatocito terminal: {res_bid['viabilidad_hepatocito'][-1]*100:.2f}%")
    print(f"   * Carga viral hepática terminal: {res_bid['carga_viral'][-1]:.2f} viriones")
    print("-" * 69)
