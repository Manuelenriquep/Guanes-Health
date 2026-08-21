# -*- coding: utf-8 -*-
"""
SIMULADOR DETERMINISTA DE CAPA B: INTERACCIÓN CAR-T Y HEPATOCARCINOMA (v1.0)
Guanes Health - División de Oncología Computacional e Inmunología de Sistemas

Este simulador modela la dinámica biofísica e inmunológica de un linfocito T
reprogramado (CAR-T) en el microambiente estromal del Carcinoma Hepatocelular (HCC).
Opera bajo un enfoque estrictamente conceptual y determinista (Capa B).
"""

import math

class LinfocitoCART:
    """
    Representa un linfocito T quimérico (CAR-T) con adaptaciones biofísicas
    para el microambiente ácido y un fusible de seguridad de caspasa inducida (iCasp9).
    """
    def __init__(self, count_inicial=1.0e6, atp_nivel=500.0):
        self.count = count_inicial          # Población de células CAR-T
        self.atp_nivel = atp_nivel          # ATP intracelular nominal
        self.ph_in = 7.20                  # pH intracelular basal
        
        # Parámetros del receptor pH-sensible (GPC3-CAR)
        self.kd_neutro = 1000.0            # nM (baja afinidad a pH fisiológico)
        self.kd_acido = 1.0                # nM (alta afinidad a pH estromal ácido)
        self.pka_histidinas = 6.2          # pKa teórico de los residuos de histidina modificados
        self.n_hill = 10.0                 # Coeficiente de Hill de protonación cooperativa (optimizado)
        
        # Parámetros del fusible iCasp9
        self.k_casp = 2.0                  # h^-1 (tasa máxima de inducción apoptótica)
        self.km_rimiducid = 10.0           # nM (afinidad del rimiducid por el dominio modificado)

    def evaluar_kd_gp3(self, ph_e):
        """
        Calcula la constante de disociación (Kd) para el antígeno GPC3 en función
        del pH extracelular (ph_e) sinusoidal/estromal.
        """
        # Ecuación sigmoidea basada en la protonación de histidinas
        exponente = self.n_hill * (self.pka_histidinas - ph_e)
        # Prevenir desbordamiento de punto flotante en exponents muy grandes
        exponente = max(-20.0, min(20.0, exponente))
        denominador = 1.0 + math.pow(10.0, exponente)
        
        kd = self.kd_acido + (self.kd_neutro - self.kd_acido) / denominador
        return kd

    def regular_ph_intracelular(self, ph_e, alfa_nhe1=0.2):
        """
        Calcula la homeostasis del pH intracelular (ph_in) mediada por el 
        transportador activo NHE1 en función de la acidez extracelular y el ATP.
        """
        ph_in_basal = 7.20
        
        # El transportador NHE1 requiere energía celular (ATP >= 100.0 unidades)
        if self.atp_nivel >= 100.0:
            # NHE1 compensa activamente el gradiente de protones
            factor_compensacion = alfa_nhe1 * max(0.0, 7.35 - ph_e)
            self.ph_in = max(7.10, ph_in_basal - 0.15 * max(0.0, 7.20 - ph_e) + factor_compensacion)
            # Acotar superiormente a rango fisiológico normal
            self.ph_in = min(7.35, self.ph_in)
        else:
            # Sin ATP, NHE1 falla y el pH citoplasmático colapsa hacia el pH externo (equilibrio pasivo)
            self.ph_in = ph_e + (ph_in_basal - ph_e) * 0.3
            self.ph_in = max(5.0, min(7.20, self.ph_in))
            
        return self.ph_in

    def simular_apoptosis_icasp9(self, rimiducid_nM, delta_t=0.1):
        """
        Simula el decaimiento cinético de la población CAR-T mediante la activación
        farmacológica del interruptor iCasp9 dependiente del inductor rimiducid.
        """
        if rimiducid_nM <= 0.0 or self.count <= 0.0:
            return self.count
            
        # Cinética de Michaelis-Menten para la dimerización del interruptor
        fraccion_activacion = rimiducid_nM / (rimiducid_nM + self.km_rimiducid)
        tasa_muerte = self.k_casp * fraccion_activacion
        
        # Integración determinista discreta de primer orden
        self.count = self.count * math.exp(-tasa_muerte * delta_t)
        self.count = max(0.0, self.count)
        return self.count


class TumorHCC:
    """
    Representa una población de Carcinoma Hepatocelular (HCC) que expresa el antígeno
    de membrana GPC3 y acidifica el microambiente.
    """
    def __init__(self, viabilidad=1.0, densidad_gpc3=5000.0):
        self.viabilidad = viabilidad        # Fracción de viabilidad del tumor (0.0 a 1.0)
        self.densidad_gpc3 = densidad_gpc3  # Moléculas de GPC3 por célula (antígeno diana)

    def evaluar_veto_antigenico(self):
        """
        Verifica el límite de degranulación del CAR-T dependiente de la densidad de antígeno.
        Si la densidad es menor al umbral estricto, la lisis se veta por completo.
        """
        umbral_critico = 1000.0 # Moléculas/célula
        if self.densidad_gpc3 < umbral_critico:
            return 0.0 # Veto activo (0% eficiencia de reconocimiento)
        
        # Si supera el umbral, la eficiencia se satura gradualmente
        eficiencia = 1.0 - (umbral_critico / self.densidad_gpc3)
        return max(0.0, min(1.0, eficiencia))


class SimuladorCARTInteraccion:
    """
    Orquesta la simulación determinista temporal de la interacción entre las células
    CAR-T y el microambiente estromal del Carcinoma Hepatocelular (HCC).
    """
    def __init__(self):
        self.paso_tiempo = 0.1  # horas
        self.tiempo_total = 72.0 # horas
        self.puntos_tiempo = int(self.tiempo_total / self.paso_tiempo)

    def simular_intervalo(self, ph_e_sinusoidal=6.20, rimiducid_nM=0.0,
                          atp_linfocito=500.0, densidad_antigeno=5000.0):
        """
        Ejecuta un ciclo temporal completo de 72 horas bajo parámetros constantes
        para evaluar el comportamiento final del sistema.
        """
        cart = LinfocitoCART(count_inicial=1.0e6, atp_nivel=atp_linfocito)
        tumor = TumorHCC(viabilidad=1.0, densidad_gpc3=densidad_antigeno)
        
        historial = {
            "tiempo": [],
            "cart_count": [],
            "ph_in": [],
            "kd_gpc3": [],
            "viabilidad_tumor": [],
            "eficiencia_reconocimiento": []
        }
        
        t = 0.0
        for _ in range(self.puntos_tiempo):
            # 1. Evaluar afinidad del CAR-T al pH del estroma
            kd = cart.evaluar_kd_gp3(ph_e_sinusoidal)
            
            # 2. Regular pH intracelular del CAR-T
            ph_in_t = cart.regular_ph_intracelular(ph_e_sinusoidal)
            
            # 3. Evaluar el veto antigénico en el tumor
            eficiencia_lisis = tumor.evaluar_veto_antigenico()
            
            # 4. Modulación de la lisis por pH intracelular del CAR-T
            # Si el pH celular interno cae por debajo de 6.80, la célula T entra en anergia metabólica
            if ph_in_t < 6.80:
                eficiencia_lisis_efectiva = eficiencia_lisis * 0.1  # Caída del 90%
            else:
                eficiencia_lisis_efectiva = eficiencia_lisis
                
            # 5. Ejecutar decaimiento de población si se activa iCasp9
            cart_prev = cart.count
            cart.simular_apoptosis_icasp9(rimiducid_nM, delta_t=self.paso_tiempo)
            
            # 6. Dinámica de depuración tumoral (cinética de aclaramiento)
            # Tasa de lisis proporcional al recuento de CAR-T activos y a la constante Kd
            factor_afinidad = 1.0 / (1.0 + (kd / 10.0))
            tasa_lisis = 0.005 * (cart.count / 1.0e6) * eficiencia_lisis_efectiva * factor_afinidad
            
            tumor.viabilidad = tumor.viabilidad * math.exp(-tasa_lisis * self.paso_tiempo)
            tumor.viabilidad = max(0.0, tumor.viabilidad)
            
            # Guardar registros de trayectoria
            historial["tiempo"].append(t)
            historial["cart_count"].append(cart.count)
            historial["ph_in"].append(ph_in_t)
            historial["kd_gpc3"].append(kd)
            historial["viabilidad_tumor"].append(tumor.viabilidad)
            historial["eficiencia_reconocimiento"].append(eficiencia_lisis_efectiva)
            
            t += self.paso_tiempo
            
        return historial

if __name__ == "__main__":
    print("==========================================================")
    print("GUANES HEALTH: INICIANDO DEMOSTRACIÓN DE COMPONENTES CAR-T")
    print("==========================================================\n")
    
    sim = SimuladorCARTInteraccion()
    # Ejecución base en estroma ácido (6.2) sin inductor iCasp9
    res = sim.simular_intervalo(ph_e_sinusoidal=6.20, rimiducid_nM=0.0)
    
    print(f"-> [TRAYECTORIA BASE] t = 72.0h (pH estromal: 6.20):")
    print(f"   * Afinidad final GPC3 (Kd): {res['kd_gpc3'][-1]:.4f} nM (Alta afinidad por acidez)")
    print(f"   * pH intracelular del CAR-T: {res['ph_in'][-1]:.4f} (Homeostasis mantenida por NHE1)")
    print(f"   * Viabilidad terminal del tumor: {res['viabilidad_tumor'][-1]*100:.2f}%")
    print(f"   * Población CAR-T remanente: {res['cart_count'][-1]:.2e} células")
    print("-" * 58)
