"""
GUANES HEALTH — SUITE DE PRUEBAS DE AUTOPOIESIS Y BIO-LOCUS
=============================================================================
Archivo: test_autopoiesis_biolocus.py
Valida:
  1. Invariantes estocásticos de la Matriz de Transición T_k (sum_j T_ij = 1.0).
  2. Veto metabólico Fail-Closed (ATP < 20% -> Atractor S3 absorbente).
  3. Cierre operacional del Ciclo Trabajo-Constricción (T-C).
  4. Métrica de Información Semántica y cono de viabilidad.
  5. Cálculo de Entropía de Flujo (H_flux) e Irreducibilidad (I) de un Bio-Locus.
  6. Índice de Integración Agencial Phi^r (Cono de Luz Cognitivo).
  7. Simulación determinista de Knockout (KO) y delta H_flux.
  8. Sello criptográfico SHA-256 bajo Ley 527 de 1999.
=============================================================================
"""

import sys
import unittest
import numpy as np

import os

# Soporte dual: paquete global guanes_kernel o modulo local 03_Motor_Oncologico
try:
    sys.path.insert(0, r"C:\GuanesHealth\guanes_kernel_pkg")
    from guanes_kernel import (
        EstadoCelular,
        CicloTrabajoConstriccion,
        MedidorInformacionSemantica,
        MatrizTransicionTk,
        BioLocus
    )
except ImportError:
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    directorio_motor = os.path.join(os.path.dirname(directorio_actual), "03_Motor_Oncologico")
    sys.path.insert(0, directorio_motor)
    from autopoiesis_biolocus import (
        EstadoCelular,
        CicloTrabajoConstriccion,
        MedidorInformacionSemantica,
        MatrizTransicionTk,
        BioLocus
    )


class TestAutopoiesisBioLocus(unittest.TestCase):

    def test_01_matriz_transicion_invariantes_estocasticos(self):
        """Verifica que las filas de T_k sumen exactamente 1.0 y las probabilidades pertenezcan a [0, 1]."""
        tk = MatrizTransicionTk(
            v_mem=-70.0,
            ph_i=7.35,
            atp=85.0,
            g_gj=0.92,
            phi_gut=0.95,
            dosis_fda_repol=0.85
        )
        T = tk.matriz
        self.assertEqual(T.shape, (4, 4))
        for i in range(4):
            self.assertAlmostEqual(np.sum(T[i]), 1.0, places=5)
            self.assertTrue(np.all(T[i] >= 0.0))
            self.assertTrue(np.all(T[i] <= 1.0))

    def test_02_veto_metabolico_fail_closed_atp_bajo(self):
        """Verifica que si ATP < 20%, el sistema colapsa irreversiblemente al Estado 3 (Muerte/Lisis)."""
        tk_fallo = MatrizTransicionTk(
            v_mem=-30.0,
            ph_i=6.20,
            atp=12.5,  # ATP crítico < 20%
            g_gj=0.10,
            phi_gut=0.20
        )
        T = tk_fallo.matriz
        # Todas las transiciones deben drenar al estado 3 con probabilidad 1.0
        for i in range(4):
            self.assertEqual(T[i, 3], 1.0)
            self.assertEqual(np.sum(T[i, :3]), 0.0)

    def test_03_ciclo_trabajo_constriccion_cierre_operacional(self):
        """Verifica el automantenimiento termodinámico en doble escala temporal (T-C)."""
        ciclo = CicloTrabajoConstriccion()
        celda_sana = EstadoCelular(id_nodo=1, v_mem=-75.0, ph_i=7.40, atp=90.0, c_membrana=1.0)
        
        # Evaluar cierre en condiciones fisiológicas (pHe = 7.40)
        dictamen = ciclo.verificar_cierre_operacional(celda_sana, ph_e=7.40)
        self.assertTrue(dictamen["cierre_operacional"])
        self.assertTrue(dictamen["trabajo_interactivo_w_int"] > 0.0)
        self.assertTrue(dictamen["viable"])

        # Evaluar ruptura del cierre ante falta de ATP
        celda_agotada = EstadoCelular(id_nodo=2, v_mem=-25.0, ph_i=6.30, atp=10.0, c_membrana=0.5)
        dictamen_fallo = ciclo.verificar_cierre_operacional(celda_agotada, ph_e=6.20)
        self.assertFalse(dictamen_fallo["cierre_operacional"])
        self.assertFalse(dictamen_fallo["viable"])

    def test_04_informacion_semantica_y_viabilidad(self):
        """Verifica que la Información Semántica cuantifique positivamente el alejamiento del borde letal."""
        medidor = MedidorInformacionSemantica()
        celda_intacta = EstadoCelular(id_nodo=1, v_mem=-70.0, ph_i=7.30, atp=80.0)
        celda_danada = EstadoCelular(id_nodo=1, v_mem=-25.0, ph_i=6.60, atp=25.0)

        si_res = medidor.evaluar_informacion_semantica(celda_intacta, celda_danada)
        self.assertGreater(si_res["informacion_semantica_bits"], 0.0)
        self.assertTrue(si_res["umbral_viabilidad_satisfecho"])

    def test_05_bio_locus_entropia_flujo_e_irreducibilidad(self):
        """Verifica el cálculo de flujos, H_flux, e Irreducibilidad en un sincitio de 5 celdas."""
        nodos = [
            EstadoCelular(id_nodo=1, v_mem=-70.0, ph_i=7.30, atp=85.0),
            EstadoCelular(id_nodo=2, v_mem=-72.0, ph_i=7.35, atp=90.0),
            EstadoCelular(id_nodo=3, v_mem=-68.0, ph_i=7.25, atp=80.0),
            EstadoCelular(id_nodo=4, v_mem=-45.0, ph_i=6.90, atp=70.0),  # Nodo marginal en estrés
            EstadoCelular(id_nodo=5, v_mem=-71.0, ph_i=7.32, atp=88.0),
        ]
        locus = BioLocus("BIO_LOCUS_EPITELIAL_01", nodos)
        
        h_flux, h_norm = locus.calcular_entropia_flujo()
        self.assertGreater(h_flux, 0.0)
        self.assertTrue(0.0 <= h_norm <= 1.0)
        
        irred = locus.calcular_irreducibilidad()
        self.assertTrue(0.0 <= irred <= 1.0)

        phi_r = locus.calcular_indice_integracion_agencial()
        self.assertGreater(phi_r, 0.0)
        self.assertTrue(phi_r <= 1.0)

    def test_06_simulacion_knockout_in_silico(self):
        """Verifica el impacto del KO de un nodo en la entropía del flujo de información."""
        nodos = [
            EstadoCelular(id_nodo=1, v_mem=-70.0, ph_i=7.30, atp=85.0),
            EstadoCelular(id_nodo=2, v_mem=-72.0, ph_i=7.35, atp=90.0),
            EstadoCelular(id_nodo=3, v_mem=-68.0, ph_i=7.25, atp=80.0),
            EstadoCelular(id_nodo=4, v_mem=-45.0, ph_i=6.90, atp=70.0),
        ]
        locus = BioLocus("LOCUS_KO_TEST", nodos)
        resultado_ko = locus.simular_knockout(id_nodo_ko=4)
        
        self.assertEqual(resultado_ko["nodo_eliminado"], 4)
        self.assertIn("delta_h_flux", resultado_ko)
        self.assertIn("centralidad_autopoietica", resultado_ko)
        self.assertGreaterEqual(resultado_ko["delta_h_flux"], 0.0)

    def test_07_certificado_criptografico_sha256(self):
        """Verifica que el dictamen emita un sello SHA-256 inmutable de 64 caracteres hexadecimales."""
        nodos = [
            EstadoCelular(id_nodo=1, v_mem=-75.0, ph_i=7.40, atp=95.0),
            EstadoCelular(id_nodo=2, v_mem=-74.0, ph_i=7.38, atp=92.0),
        ]
        locus = BioLocus("LOCUS_CERT", nodos)
        cert = locus.generar_certificado_forense()
        
        self.assertIn("sello_sha256", cert)
        self.assertEqual(len(cert["sello_sha256"]), 64)
        self.assertEqual(cert["politica_imputacion"], "FAIL_CLOSED_ZERO_HEURISTIC")


if __name__ == "__main__":
    unittest.main()
