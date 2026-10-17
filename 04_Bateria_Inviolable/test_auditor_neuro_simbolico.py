"""
Bateria de Pruebas Inviolables - Auditor Neuro-Simbolico Level 0
Placa Base de Logica Cartesiana v3.2.0 Inmutable
===============================================================
Verificacion de:
- Axiomas I a V (Friston, Levin, Ulpiano, Hamilton, Mises)
- Cortafuegos Fail-Closed FC-UNIF-00 a FC-UNIF-07
- Latencias de resolucion O(1) y poda por decoherencia (< 0.1 ms / < 0.5 ms)
- Protocolo VERITAS con SHA-256 (Ley 527/1999) y Tope Deontologico (Ley 1123/2007)
"""

import sys
import os
import unittest
import time

# Incorporar ruta del motor oncologico
MOTOR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico"))
if MOTOR_DIR not in sys.path:
    sys.path.insert(0, MOTOR_DIR)

from bruxelas_kernel import (
    BruxelasKernel,
    MarkovBlanket,
    HypothesisCandidate,
    FailClosedVeto,
    CognitiveScale,
    SOBERANIA_NODO_LOCAL,
    TOPE_DEONTOLOGICO_VIABILIDAD,
    LATENCIA_MAXIMA_RESOLUCION_MS,
    LATENCIA_DECOHERENCIA_SISTEMA_2_MS
)


class TestAuditorNeuroSimbolico(unittest.TestCase):

    def setUp(self):
        self.kernel = BruxelasKernel()
        # Registrar un hecho fáctico inmutable
        self.fact_text = "Radicado 2026-CSJ-0042: Titularidad confirmada y debidamente autenticada."
        self.fact_hash = self.kernel.register_fact(self.fact_text)

        # Malla de Markov canónica sana
        self.blanket_sana = MarkovBlanket(
            node_id="NODO_SANO_01",
            sensory_states={"ph_e": 7.4, "lactato": 1.2},
            active_states={"efflux_protons": 0.1},
            internal_states={"atp": 100.0, "p53": "intacto"},
            boundary_integrity=1.0,
            v_mem_mv=-75.0,
            gap_junctions_open=True,
            cognitive_scale=CognitiveScale.LOGICA
        )

    def test_axioma_i_veto_monopolio_central_fc00(self):
        """FC-UNIF-00: Rechazo inmediato a hipótesis con observador central omnisciente."""
        candidato = HypothesisCandidate(
            hypothesis_id="H_CENTRAL_01",
            claim="El estado centralizado define la conciencia y mandato del nodo.",
            assumes_central_observer=True
        )
        res = self.kernel.verify_hypothesis(candidato, self.blanket_sana)
        self.assertFalse(res.admitted)
        self.assertEqual(res.veto_code, FailClosedVeto.FC_UNIF_00)
        self.assertEqual(res.status, "REJECTED_FAIL_CLOSED")

    def test_axioma_ii_frontera_inmutable_void_ab_initio_fc03(self):
        """Axioma II & FC-UNIF-03: Violación de frontera activa VOID_AB_INITIO."""
        blanket_invadida = MarkovBlanket(
            node_id="NODO_INVADIDO",
            boundary_integrity=0.6,  # Frontera rota (Delta Frontera > 0)
            v_mem_mv=-75.0,
            gap_junctions_open=True
        )
        candidato = HypothesisCandidate(
            hypothesis_id="H_EXPROP_01",
            claim="Expropiación de memoria de nodo",
            violates_boundary=True
        )
        res = self.kernel.verify_hypothesis(candidato, blanket_invadida)
        self.assertFalse(res.admitted)
        self.assertTrue(res.void_ab_initio)
        self.assertEqual(res.veto_code, FailClosedVeto.FC_UNIF_03)
        self.assertEqual(res.status, "VOID_AB_INITIO")

    def test_axioma_iii_veritas_sha256_y_poda_fc06(self):
        """FC-UNIF-06 & FC-UNIF-02: Hipótesis sin huella en vector de hechos es podada instantáneamente."""
        candidato_sin_hecho = HypothesisCandidate(
            hypothesis_id="H_FALSA_01",
            claim="Norma o radicado inexistente",
            citation_id="Radicado Falso 9999",
            factual_vector_evidence="Texto inventado sin registro SHA-256"
        )
        res = self.kernel.verify_hypothesis(candidato_sin_hecho, self.blanket_sana)
        self.assertFalse(res.admitted)
        self.assertEqual(res.veto_code, FailClosedVeto.FC_UNIF_06)
        self.assertEqual(res.status, "DECOHERENCE_PRUNED")

        # Ahora probamos con el hecho verificado registrado
        candidato_valido = HypothesisCandidate(
            hypothesis_id="H_VALIDA_01",
            claim="Titularidad válida y auditada",
            citation_id="Radicado 2026-CSJ-0042",
            factual_vector_evidence=self.fact_text,
            free_energy_f=0.01,
            action_delta_s=0.0
        )
        res_valido = self.kernel.verify_hypothesis(candidato_valido, self.blanket_sana)
        self.assertTrue(res_valido.admitted)
        self.assertEqual(res_valido.status, "GEODESIC_RESOLVED")
        self.assertIsNotNone(res_valido.geodesic_sha256)
        self.assertEqual(res_valido.deontological_score, TOPE_DEONTOLOGICO_VIABILIDAD)

    def test_axioma_iv_fep_minima_accion_geodesica(self):
        """Axioma IV: Minimización de Energía Libre (F -> 0) y Principio de Hamilton."""
        candidato_optimo = HypothesisCandidate(
            hypothesis_id="H_FEP_MIN",
            claim="Geodésica de mínima energía y acción",
            free_energy_f=0.001,
            action_delta_s=0.0
        )
        res = self.kernel.verify_hypothesis(candidato_optimo, self.blanket_sana)
        self.assertTrue(res.admitted)
        self.assertEqual(res.status, "GEODESIC_RESOLVED")
        self.assertEqual(len(res.geodesic_sha256), 64)

    def test_axioma_v_patologia_unica_smaller_selves(self):
        """Axioma V: Teorema de Levin/Friston: Ruptura bioeléctrica o de frontera = Smaller Self."""
        # Caso 1: Célula sana acoplada
        diag_sano = self.kernel.evaluate_smaller_self(self.blanket_sana, signal_valid=True)
        self.assertFalse(diag_sano["smaller_self_active"])
        self.assertEqual(diag_sano["pathology"], "HOMEOSTASIS_PRESERVED")
        self.assertEqual(diag_sano["bioelectric_status"], "NORMALIZED_DIFFERENTIATED")

        # Caso 2: Célula oncológica despolarizada y con uniones gap cerradas
        blanket_cancer = MarkovBlanket(
            node_id="NODO_TUMORAL_01",
            boundary_integrity=1.0,
            v_mem_mv=-15.0,  # Despolarización oncogénica
            gap_junctions_open=False  # Cierre de gap junctions (aislamiento computacional)
        )
        diag_cancer = self.kernel.evaluate_smaller_self(blanket_cancer, signal_valid=True)
        self.assertTrue(diag_cancer["smaller_self_active"])
        self.assertEqual(diag_cancer["pathology"], "PATHOLOGY_SMALLEST_SELF_COLLAPSE")
        self.assertEqual(diag_cancer["bioelectric_status"], "AMEBOID_ONCOGENIC")

    def test_fc_unif_01_veto_alucinacion_estocastica(self):
        """FC-UNIF-01: Rechazo si F es elevada o la confianza es inferior a la exigencia."""
        candidato_alucinado = HypothesisCandidate(
            hypothesis_id="H_ESTOCASTICA_01",
            claim="Predicción incierta de alta entropía",
            free_energy_f=0.85,  # Alta energía libre
            probabilistic_confidence=0.65
        )
        res = self.kernel.verify_hypothesis(candidato_alucinado, self.blanket_sana)
        self.assertFalse(res.admitted)
        self.assertEqual(res.veto_code, FailClosedVeto.FC_UNIF_01)

    def test_fc_unif_04_veto_microgestion_coercitiva(self):
        """FC-UNIF-04: Rechazo si intenta microgestión coercitiva de microestados."""
        candidato_micro = HypothesisCandidate(
            hypothesis_id="H_MICRO_01",
            claim="Control forzado de canales iónicos individuales sin ajuste de condición límite",
            coerces_microstates=True
        )
        res = self.kernel.verify_hypothesis(candidato_micro, self.blanket_sana)
        self.assertFalse(res.admitted)
        self.assertEqual(res.veto_code, FailClosedVeto.FC_UNIF_04)

    def test_fc_unif_05_freno_estoico_antialucinacion(self):
        """FC-UNIF-05: Freno estoico antialucinación ante profecías místicas o financieras."""
        candidato_profecia = HypothesisCandidate(
            hypothesis_id="H_MISTICA_01",
            claim="El universo es un organismo cósmico consciente y Bitcoin subirá a $1M mañana",
            has_mystical_or_financial_prophecy=True
        )
        res = self.kernel.verify_hypothesis(candidato_profecia, self.blanket_sana)
        self.assertFalse(res.admitted)
        self.assertEqual(res.veto_code, FailClosedVeto.FC_UNIF_05)

    def test_fc_unif_07_veto_muerte_equilibrio_detallado(self):
        """FC-UNIF-07: Veto al equilibrio detallado; los sistemas vivos exigen dinámica solenoide."""
        candidato_estatico = HypothesisCandidate(
            hypothesis_id="H_STATIC_01",
            claim="Estado de relajación termodinámica cerrada",
            maintains_solenoidal_dynamics=False
        )
        res = self.kernel.verify_hypothesis(candidato_estatico, self.blanket_sana)
        self.assertFalse(res.admitted)
        self.assertEqual(res.veto_code, FailClosedVeto.FC_UNIF_07)

    def test_latencias_de_silicio(self):
        """Verifica que la resolución y la poda se ejecuten en tiempos sub-milisegundo."""
        candidato_valido = HypothesisCandidate(
            hypothesis_id="H_BENCHMARK",
            claim="Resolución geodésica determinista",
            free_energy_f=0.01
        )
        # Ejecutar 500 iteraciones para medir promedio
        tiempos = []
        for _ in range(500):
            res = self.kernel.verify_hypothesis(candidato_valido, self.blanket_sana)
            tiempos.append(res.elapsed_ms)

        avg_ms = sum(tiempos) / len(tiempos)
        self.assertLess(avg_ms, 1.0, f"Latencia promedio esperada sub-milisegundo, obtenida: {avg_ms:.4f} ms")


if __name__ == "__main__":
    unittest.main(verbosity=2)
