"""
GUANES KERNEL — NÚCLEO DE AUTOPOIESIS Y BIO-LOCI RELACIONALES
=============================================================================
Módulo: guanes_kernel/core/autopoiesis_biolocus.py
Fundamento Teórico:
  - Autopoiesis y Cierre Operacional (Maturana & Varela, 1973/1980).
  - Bioelectricidad y Cono de Luz Cognitivo (Levin, 2019/2025).
  - Termodinámica de Sistemas Fuera del Equilibrio: Ciclo Trabajo-Constricción (T-C)
    (Kauffman, 2000; Montévil & Mossio, 2015).
  - Información Semántica y Umbrales de Viabilidad (Kolchinsky & Wolpert, 2018).
  - Redes Relacionales, Bio-loci, Entropía de Flujo (H_flux) e Irreducibilidad (I).
  - Certificación Criptográfica Determinista Fail-Closed (Ley 527 de 1999).

CONFIDENCIALIDAD:
  Propiedad Intelectual y Secreto Industrial de Guanes Health.
  Aislamiento Hermético Local (Zero Cloud Leakage).
=============================================================================
"""

import math
import hashlib
import json
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple, Optional


# =============================================================================
# 1. CONSTANTES TERMODINÁMICAS Y BIOMÉDICAS INVARIANTES
# =============================================================================

DELTA_G_ATP = 50.0          # kJ / mol liberados por hidrólisis de ATP
K_B_BOLTZMANN = 1.380649e-23# J / K
T_FISIOLOGICA = 310.15      # 37°C en Kelvin
ATP_VETO_THRESHOLD = 20.0   # ATP < 20% activa Veto Fail-Closed irreversible
VMEM_DEPOL_THRESHOLD = -20.0# mV, umbral crítico de despolarización patológica
PHI_ACID_THRESHOLD = 6.60   # pKa alostérico de inactivación por protones


@dataclass
class EstadoCelular:
    """
    Vector de micro-estado fisiológico de una unidad celular dentro del bio-locus.
    """
    id_nodo: int
    v_mem: float            # mV (Potencial de membrana transcelular)
    ph_i: float             # pH citosólico interno
    atp: float              # % (0.0 a 100.0) de disponibilidad energética
    c_membrana: float = 1.0 # Densidad de constricciones funcionales C(t) (canales/bombas)

    def es_viable(self) -> bool:
        """Determina si la célula se encuentra dentro del atractor de viabilidad."""
        return self.atp >= ATP_VETO_THRESHOLD and self.v_mem <= VMEM_DEPOL_THRESHOLD and self.ph_i >= 6.50


# =============================================================================
# 2. CICLO TRABAJO-CONSTRICCIÓN (T-C): TERMODINÁMICA DE LA AUTOPOIESIS
# =============================================================================

class CicloTrabajoConstriccion:
    """
    Formaliza la causalidad circular termodinámica:
    'El trabajo genera constricciones que canalizan el trabajo'.
    
    Doble escala temporal:
    - Escala Rápida (Interactiva, tau ~ 10^-3 a 10^0 s): Bombeo iónico activo contra gradiente.
    - Escala Lenta (Constitutiva, tau ~ 10^3 a 10^5 s): Síntesis y reciclaje de compuertas C(t).
    """

    def __init__(
        self,
        eficiencia_sintesis: float = 0.05,
        tasa_degradacion: float = 0.02,
        k_m_bomba: float = 15.0
    ):
        self.eta_sintesis = eficiencia_sintesis
        self.gamma_deg = tasa_degradacion
        self.km_bomba = k_m_bomba

    def flujo_bombeo_interactivo(self, estado: EstadoCelular, ph_e: float) -> float:
        """
        Calcula el flujo cinético interactivo de bombeo de protones e iones.
        Depende no linealmente de [ATP] y de la constricción actual C(t).
        """
        if estado.atp < ATP_VETO_THRESHOLD:
            return 0.0  # Veto metabólico: cese de bombeo
        
        # Saturación Michaelis-Menten en ATP modulada por C(t)
        saturacion_atp = estado.atp / (self.km_bomba + estado.atp)
        gradiente_ph = max(0.0, ph_e - estado.ph_i)
        
        # Flujo de trabajo interactivo
        j_pump = estado.c_membrana * saturacion_atp * (1.0 + 0.5 * gradiente_ph)
        return float(j_pump)

    def calcular_trabajo_interactivo(self, estado: EstadoCelular, ph_e: float) -> float:
        """
        Trabajo interactivo (W_int) consumido en mantener el gradiente contra la crisis osmótica.
        W_int = Delta G_ATP * J_pump (kJ / s / unidad de volumen relativa).
        """
        j_pump = self.flujo_bombeo_interactivo(estado, ph_e)
        w_int = (DELTA_G_ATP / 100.0) * j_pump * (estado.atp / 100.0)
        return float(w_int)

    def evolucionar_constricciones_constitutivas(
        self,
        estado: EstadoCelular,
        dt_horas: float = 1.0
    ) -> float:
        """
        Evolución de la maquinaria constitutiva C(t):
        dC/dt = eta_sintesis * W_const - gamma_deg * C(t).
        W_const es trabajo metabólico desviado hacia transcripción/traducción de canales.
        """
        if estado.atp < ATP_VETO_THRESHOLD:
            # Sin ATP, no hay síntesis; solo degradación pasiva
            delta_c = - self.gamma_deg * estado.c_membrana * dt_horas
        else:
            w_const = (estado.atp / 100.0) * 0.8
            d_c_dt = (self.eta_sintesis * w_const) - (self.gamma_deg * estado.c_membrana)
            delta_c = d_c_dt * dt_horas

        nuevo_c = max(0.05, min(2.5, estado.c_membrana + delta_c))
        return float(nuevo_c)

    def verificar_cierre_operacional(self, estado: EstadoCelular, ph_e: float) -> Dict[str, Any]:
        """
        Verifica formalmente si el sistema mantiene cierre operacional:
        1. Produce trabajo interactivo suficiente para mantener el gradiente.
        2. Mantiene una tasa neta dC/dt >= 0 para regenerar su propio borde.
        """
        w_int = self.calcular_trabajo_interactivo(estado, ph_e)
        nuevo_c = self.evolucionar_constricciones_constitutivas(estado, dt_horas=0.1)
        regeneracion_positiva = nuevo_c >= estado.c_membrana

        cierre_operacional = (w_int > 0.05) and regeneracion_positiva and estado.es_viable()
        
        return {
            "cierre_operacional": cierre_operacional,
            "trabajo_interactivo_w_int": round(w_int, 4),
            "c_membrana_actual": round(estado.c_membrana, 4),
            "c_membrana_proyectado": round(nuevo_c, 4),
            "tasa_regenerativa_positiva": regeneracion_positiva,
            "viable": estado.es_viable()
        }


# =============================================================================
# 3. INFORMACIÓN SEMÁNTICA Y UMBRALES DE VIABILIDAD
# =============================================================================

class MedidorInformacionSemantica:
    """
    Cuantifica la Información Semántica (SI) procesada por el agente biológico
    como aquella correlación con el entorno que sostiene su viabilidad termodinámica.
    """

    @staticmethod
    def funcion_viabilidad(estado: EstadoCelular) -> float:
        """
        Función de viabilidad V(sigma) en [-1.0, 1.0].
        Valores > 0 indican mantenimiento dentro del cono de viabilidad homeostática.
        Valores <= 0 indican degradación entrópica terminal.
        """
        if estado.atp < ATP_VETO_THRESHOLD:
            return -1.0
        
        # Ponderación multiaxial de supervivencia
        v_atp = (estado.atp - ATP_VETO_THRESHOLD) / (100.0 - ATP_VETO_THRESHOLD)
        v_vmem = (-estado.v_mem - 20.0) / 70.0  # -90 mV -> 1.0, -20 mV -> 0.0
        v_phi = (estado.ph_i - 6.50) / (7.40 - 6.50)
        
        viabilidad = (0.4 * v_atp) + (0.35 * v_vmem) + (0.25 * v_phi)
        return float(max(-1.0, min(1.0, viabilidad)))

    def evaluar_informacion_semantica(
        self,
        estado_intacto: EstadoCelular,
        estado_perturbado: EstadoCelular
    ) -> Dict[str, Any]:
        """
        Calcula el valor de la Información Semántica:
        SI = max(0, V(intacto) - V(perturbado)).
        """
        v_intacto = self.funcion_viabilidad(estado_intacto)
        v_scrambled = self.funcion_viabilidad(estado_perturbado)
        si = max(0.0, v_intacto - v_scrambled)

        return {
            "viabilidad_intacta": round(v_intacto, 4),
            "viabilidad_perturbada": round(v_scrambled, 4),
            "informacion_semantica_bits": round(si * math.log2(math.e + 1), 4),
            "umbral_viabilidad_satisfecho": v_intacto > 0.0
        }


# =============================================================================
# 4. MATRIZ DE TRANSICIÓN Tk DEL BIO-LOCUS
# =============================================================================

class MatrizTransicionTk:
    """
    Matriz de Transición Markoviana/Ergódica de Microestados Bioeléctricos.
    Estados Discretos:
      S0: Homeostático Polarizado (Vmem <= -60 mV, G_GJ >= 0.8, ATP >= 60%)
      S1: Adaptativo / Estrés Leve (-60 < Vmem <= -45 mV, compensación activa)
      S2: Despolarizado / Ameboide / Neoplásico (Vmem > -45 mV, Cx43 cerrado)
      S3: Veto Metabólico / Lisis / Necrosis (ATP < 20% - Atractor Absorbente Fail-Closed)
    
    Invariantes formales:
      - Cada fila suma exactamente 1.0 (Conservación de probabilidad).
      - Probabilidades acotadas en [0.0, 1.0].
      - S3 es estado absorbente fail-closed: T_k(3, 3) = 1.0.
    """

    NOMBRES_ESTADOS = [
        "S0_HOMEOSTATICO_POLARIZADO",
        "S1_ADAPTATIVO_ESTRES",
        "S2_DESPOLARIZADO_AMEBOIDE",
        "S3_VETO_METABOLICO_LISIS"
    ]

    def __init__(
        self,
        v_mem: float,
        ph_i: float,
        atp: float,
        g_gj: float,
        phi_gut: float = 0.92,
        dosis_fda_repol: float = 0.0
    ):
        self.v_mem = v_mem
        self.ph_i = ph_i
        self.atp = atp
        self.g_gj = max(0.0, min(1.0, g_gj))
        self.phi_gut = max(0.0, min(1.0, phi_gut))
        self.fda_repol = max(0.0, min(1.0, dosis_fda_repol))
        
        self.matriz = self._construir_matriz_transicion()
        self._verificar_invariantes()

    def _construir_matriz_transicion(self) -> np.ndarray:
        T = np.zeros((4, 4), dtype=np.float64)

        # Regla Absoluta Fail-Closed: Si ATP < 20, colapso directo a S3
        if self.atp < ATP_VETO_THRESHOLD:
            for i in range(4):
                T[i, 3] = 1.0
            return T

        # Factores reguladores normalizados
        factor_acoplamiento = self.g_gj
        factor_inflamacion = (1.0 - self.phi_gut)
        factor_repol = self.fda_repol

        # FILA 0: Desde S0 (Homeostático)
        # Probabilidad de mantenerse en reposo polarizado
        t01 = 0.15 * factor_inflamacion + (0.10 if self.v_mem > -65.0 else 0.02)
        t02 = 0.08 * (1.0 - factor_acoplamiento) * (1.0 - factor_repol)
        t03 = 0.001
        t00 = max(0.0, 1.0 - (t01 + t02 + t03))
        T[0] = [t00, t01, t02, t03]

        # FILA 1: Desde S1 (Estrés)
        # Posibilidad de retorno a S0 si hay buen acoplamiento y rescate FDA
        t10 = 0.40 * factor_acoplamiento + 0.35 * factor_repol
        t12 = 0.30 * (1.0 - factor_acoplamiento) + 0.20 * factor_inflamacion
        t13 = 0.01 if self.atp < 40.0 else 0.002
        t10 = min(0.85, t10)
        t11 = max(0.0, 1.0 - (t10 + t12 + t13))
        T[1] = [t10, t11, t12, t13]

        # FILA 2: Desde S2 (Ameboide Neoplásico)
        # Salida hacia S0 / S1 fuertemente mediada por Repolarización FDA e Isotretinoína (G_GJ)
        t20 = 0.55 * factor_repol * factor_acoplamiento
        t21 = 0.25 * factor_repol + 0.10 * factor_acoplamiento
        t23 = 0.05 if self.atp < 30.0 else 0.01
        t22 = max(0.0, 1.0 - (t20 + t21 + t23))
        T[2] = [t20, t21, t22, t23]

        # FILA 3: Desde S3 (Lisis / Muerte - Atractor Absorbente)
        T[3] = [0.0, 0.0, 0.0, 1.0]

        # Normalización estricta por fila para garantizar estocasticidad exacta
        for i in range(4):
            suma = np.sum(T[i])
            if suma > 0:
                T[i] /= suma
            else:
                T[i, 3] = 1.0

        return T

    def _verificar_invariantes(self) -> None:
        """Verifica formalmente las invariantes de estocasticidad fail-closed."""
        for i in range(4):
            suma = float(np.sum(self.matriz[i]))
            if not math.isclose(suma, 1.0, rel_tol=1e-5, abs_tol=1e-5):
                raise ValueError(f"Violación de invariante estocástico en fila {i}: suma={suma} != 1.0")
            for j in range(4):
                val = self.matriz[i, j]
                if val < 0.0 or val > 1.0:
                    raise ValueError(f"Violación de probabilidad en T[{i},{j}] = {val}")

    def evolucionar(self, dist_inicial: np.ndarray, pasos: int = 1) -> np.ndarray:
        """
        Evoluciona la distribución de probabilidad de estados sobre 'pasos' temporales:
        p(t + pasos) = p(t) * (T_k)^pasos.
        """
        p = np.array(dist_inicial, dtype=np.float64)
        p = p / np.sum(p)
        T_pot = np.linalg.matrix_power(self.matriz, pasos)
        return p @ T_pot

    def calcular_distribucion_estacionaria(self) -> np.ndarray:
        """
        Calcula la distribución estacionaria pi tal que pi * T_k = pi.
        """
        evals, evecs = np.linalg.eig(self.matriz.T)
        idx_uno = np.argmin(np.abs(evals - 1.0))
        estacionaria = np.real(evecs[:, idx_uno])
        estacionaria = np.abs(estacionaria)
        return estacionaria / np.sum(estacionaria)

    def entropia_de_transicion(self) -> float:
        """
        Entropía media de las transiciones (tasa de incertidumbre Markoviana):
        H = - sum_i pi_i sum_j T_ij log(T_ij).
        """
        pi = self.calcular_distribucion_estacionaria()
        h_total = 0.0
        for i in range(4):
            h_fila = 0.0
            for j in range(4):
                p_ij = self.matriz[i, j]
                if p_ij > 1e-12:
                    h_fila -= p_ij * math.log(p_ij)
            h_total += pi[i] * h_fila
        return float(h_total)


# =============================================================================
# 5. RED RELACIONAL: BIO-LOCUS, ENTROPÍA DE FLUJO (H_flux) E IRREDUCIBILIDAD
# =============================================================================

class BioLocus:
    """
    Representa una comunidad o colectivo de células acopladas bioeléctrica y metabólicamente
    que actúan funcionalmente como un 'macro-agente' o 'individuo de segundo orden'.
    
    Implementa:
    - Grafo relacional ponderado de conductancias conexínicas (G_GJ).
    - Matriz de flujos intercelulares (corriente iónica + señalización metabólica).
    - Entropía de Flujo (H_flux) de Shreesha / Levin.
    - Métrica de Irreducibilidad I(bio-locus).
    - Índice de Integración Agencial Phi^r (Cono de Luz Cognitivo).
    - Simulación de Knockout (KO) in silico para medir centralidad funcional.
    """

    def __init__(self, id_locus: str, nodos: List[EstadoCelular]):
        if len(nodos) < 2:
            raise ValueError("Un Bio-locus requiere al menos 2 unidades celulares acopladas.")
        
        self.id_locus = id_locus
        self.nodos = {nodo.id_nodo: nodo for nodo in nodos}
        self.num_nodos = len(nodos)
        self.lista_ids = sorted(list(self.nodos.keys()))
        
        # Matrices dinámicas
        self.matriz_conductancia = np.zeros((self.num_nodos, self.num_nodos), dtype=np.float64)
        self.matriz_flujos = np.zeros((self.num_nodos, self.num_nodos), dtype=np.float64)
        
        self._recalcular_topologia_y_flujos()

    def _conductancia_gap_junction(self, nodo_a: EstadoCelular, nodo_b: EstadoCelular) -> float:
        """
        Conductancia transjuncional doble-Boltzmann modulada por diferencia de Vmem y pH_i.
        """
        delta_v = abs(nodo_a.v_mem - nodo_b.v_mem)
        # Gating por voltaje
        v_0 = 25.0
        k_v = 5.0
        g_v = 1.0 / (1.0 + math.exp((delta_v - v_0) / k_v))
        
        # Bloqueo por pH interno
        phi_medio = 0.5 * (nodo_a.ph_i + nodo_b.ph_i)
        g_ph = 1.0 / (1.0 + 10.0 ** (4.0 * (PHI_ACID_THRESHOLD - phi_medio)))
        
        # Modulación por constricción C(t) de membrana
        c_medio = 0.5 * (nodo_a.c_membrana + nodo_b.c_membrana)
        
        return float(g_v * g_ph * c_medio)

    def _recalcular_topologia_y_flujos(self) -> None:
        """Calcula la matriz de conductancias y los flujos intercelulares dirigidos."""
        for i, id_i in enumerate(self.lista_ids):
            nodo_i = self.nodos[id_i]
            for j, id_j in enumerate(self.lista_ids):
                if i == j:
                    self.matriz_conductancia[i, j] = 0.0
                    self.matriz_flujos[i, j] = 0.0
                    continue
                
                nodo_j = self.nodos[id_j]
                g_ij = self._conductancia_gap_junction(nodo_i, nodo_j)
                self.matriz_conductancia[i, j] = g_ij
                
                # Flujo electrometabólico: Corriente iónica de gradiente + difusión metabólica
                flujo_v = g_ij * abs(nodo_i.v_mem - nodo_j.v_mem)
                flujo_ph = 0.5 * abs(nodo_i.ph_i - nodo_j.ph_i)
                self.matriz_flujos[i, j] = flujo_v + flujo_ph

    def vector_flujo_saliente(self) -> np.ndarray:
        """Flujo acumulado emitido por cada nodo hacia el colectivo."""
        return np.sum(self.matriz_flujos, axis=1)

    def calcular_entropia_flujo(self) -> Tuple[float, float]:
        """
        Calcula la Entropía de Flujo Shannon:
        H_flux = - sum_i p_i ln(p_i)
        donde p_i es la fracción de flujo intercelular transmitida por el nodo i.
        
        Retorna (H_flux_absoluta, H_flux_normalizada en [0, 1]).
        """
        flujos = self.vector_flujo_saliente()
        flujo_total = np.sum(flujos)
        
        if flujo_total < 1e-12:
            return 0.0, 0.0
        
        p = flujos / flujo_total
        # Evitar log(0)
        p_safe = p[p > 1e-12]
        h_flux = -float(np.sum(p_safe * np.log(p_safe)))
        
        h_max = math.log(self.num_nodos)
        h_norm = h_flux / h_max if h_max > 0 else 0.0
        return h_flux, float(max(0.0, min(1.0, h_norm)))

    def calcular_irreducibilidad(self) -> float:
        """
        Métrica de Irreducibilidad I(bio-locus):
        Distancia en norma L1 entre la distribución real observada de flujo
        y la distribución uniforme esperada de células independientes desacopladas.
        
        I = 1/2 * sum_i | p_i_obs - 1/N |
        Valores cercanos a 1.0 implican alta especialización/integración no trivial.
        """
        flujos = self.vector_flujo_saliente()
        flujo_total = np.sum(flujos)
        
        if flujo_total < 1e-12:
            return 0.0
        
        p_obs = flujos / flujo_total
        p_exp = np.ones(self.num_nodos) / self.num_nodos
        
        distancia_l1 = 0.5 * float(np.sum(np.abs(p_obs - p_exp)))
        return float(max(0.0, min(1.0, distancia_l1)))

    def calcular_indice_integracion_agencial(self) -> float:
        """
        Índice de Integración Agencial Phi^r (Cono de Luz Cognitivo Colectivo):
        Phi^r = Irreducibilidad * Conductancia_Media * Factor_ATP_Homeostatico.
        
        Si el ATP cae por debajo de 20% en promedio, Phi^r colapsa deterministamente a 0.0.
        """
        atp_promedio = float(np.mean([nodo.atp for nodo in self.nodos.values()]))
        if atp_promedio < ATP_VETO_THRESHOLD:
            return 0.0  # Veto fail-closed
        
        irreducibilidad = self.calcular_irreducibilidad()
        # Media de conductancias sin la diagonal
        n = self.num_nodos
        suma_g = np.sum(self.matriz_conductancia)
        g_media = suma_g / (n * (n - 1)) if n > 1 else 0.0
        
        factor_atp = (atp_promedio - ATP_VETO_THRESHOLD) / (100.0 - ATP_VETO_THRESHOLD)
        
        phi_r = irreducibilidad * g_media * factor_atp
        return float(max(0.0, min(1.0, phi_r)))

    def simular_knockout(self, id_nodo_ko: int) -> Dict[str, Any]:
        """
        Experimento in silico de Knockout (KO):
        Elimina selectivamente un nodo de la red y mide la alteración del flujo informacional:
        Delta H_flux = | H_flux(WT) - H_flux(KO) |.
        Determina la centralidad crítica del nodo en el sostenimiento del bio-locus.
        """
        if id_nodo_ko not in self.nodos:
            raise KeyError(f"El nodo {id_nodo_ko} no pertenece a este bio-locus.")
        
        if self.num_nodos <= 2:
            raise ValueError("No se puede realizar KO con solo 2 nodos (destruye el locus).")
        
        h_wt, h_wt_norm = self.calcular_entropia_flujo()
        
        # Crear sub-red sobreviviente
        nodos_remanentes = [nodo for id_n, nodo in self.nodos.items() if id_n != id_nodo_ko]
        sub_locus = BioLocus(f"{self.id_locus}_KO_{id_nodo_ko}", nodos_remanentes)
        h_ko, h_ko_norm = sub_locus.calcular_entropia_flujo()
        
        delta_h = abs(h_wt - h_ko)
        delta_h_norm = abs(h_wt_norm - h_ko_norm)
        
        return {
            "nodo_eliminado": id_nodo_ko,
            "h_flux_wildtype": round(h_wt, 4),
            "h_flux_knockout": round(h_ko, 4),
            "delta_h_flux": round(delta_h, 4),
            "delta_h_flux_normalizada": round(delta_h_norm, 4),
            "centralidad_autopoietica": round(delta_h * 100.0, 2),
            "locus_viable_tras_ko": sub_locus.calcular_indice_integracion_agencial() > 0.05
        }

    def generar_certificado_forense(self) -> Dict[str, Any]:
        """
        Genera el dictamen de estado con sello inmutable SHA-256 (Ley 527 de 1999).
        """
        h_flux, h_norm = self.calcular_entropia_flujo()
        irred = self.calcular_irreducibilidad()
        phi_r = self.calcular_indice_integracion_agencial()
        atp_prom = float(np.mean([n.atp for n in self.nodos.values()]))
        vmem_prom = float(np.mean([n.v_mem for n in self.nodos.values()]))
        
        payload_datos = {
            "id_locus": self.id_locus,
            "total_celdas": self.num_nodos,
            "vmem_promedio_mv": round(vmem_prom, 2),
            "atp_promedio_pct": round(atp_prom, 2),
            "h_flux": round(h_flux, 4),
            "h_flux_normalizada": round(h_norm, 4),
            "irreducibilidad": round(irred, 4),
            "indice_integracion_phi_r": round(phi_r, 4),
            "estado_cono_cognitivo": "INTEGRATED_SELF" if phi_r >= 0.25 else "DECOUPLED_AMEBOID",
            "politica_imputacion": "FAIL_CLOSED_ZERO_HEURISTIC"
        }
        
        hash_sha256 = hashlib.sha256(
            json.dumps(payload_datos, sort_keys=True).encode("utf-8")
        ).hexdigest()
        
        payload_datos["sello_sha256"] = hash_sha256
        return payload_datos
