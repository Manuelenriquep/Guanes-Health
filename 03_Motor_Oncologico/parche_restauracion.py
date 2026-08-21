"""
Deterministic restoration routines for the current oncology prototype.

Model-layer comparison: isolated immunotherapy path vs combined intervention
that restores a subset of *modeled* tumor states. Not a clinical protocol.
See SSoT: placa_base_instrumento_investigacion.md

CD8 efficiency uses policy Gated-6.50 (Capa B), aligned with
simulador_onco_homeostasis_v5.py and FC-BIO-2.1.
"""

from placa_cancer import CelulaTumoral
from placa_sana import CelulaSana


class ParcheRestauracion:
    # Veto ácido (Capa A / FC-BIO-2.1) + política numérica Capa B
    PH_VETO_CD8 = 6.50
    PH_FISIOLOGICO = 7.35
    ANERGY_GATE = 0.20  # Fracción: por debajo → eficiencia modelada = 0
    PH_RESTAURADO = 7.35
    ATP_COLAPSADO = 30
    PH_INTRACELULAR_LETAL = 5.2
    BCL2_FISIOLOGICO = 1.0
    EFICIENCIA_CD8_MAX = 100.0

    # Alias histórico (deprecado): el umbral operativo es PH_VETO_CD8
    PH_PARALISIS_CD8 = PH_VETO_CD8

    @classmethod
    def calcular_eficiencia_cd8(cls, pHe):
        """
        Eficiencia citotóxica CD8+ modelada (fracción 0–1).

        Caída lineal entre pHe fisiológico (7.35) y piso 6.50;
        si la fracción cruda es < ANERGY_GATE (0.20), se trunca a 0.0.
        """
        pHe = float(pHe)
        if pHe <= cls.PH_VETO_CD8:
            return 0.0
        cruda = (pHe - cls.PH_VETO_CD8) / (cls.PH_FISIOLOGICO - cls.PH_VETO_CD8)
        cruda = min(1.0, max(0.0, cruda))
        if cruda < cls.ANERGY_GATE:
            return 0.0
        return cruda

    def simular_inmunoterapia_aislada(self, celula_tumoral):
        """
        Camino modelado: monoterapia anti-PD-1.
        Neutraliza camuflaje PD-L1 en el estado; el pH ácido modelado
        reduce la eficiencia CD8+ simulada (Gated-6.50).
        Returns efficiency as percent (0–100) for the demo API.
        """
        self._assert_celula_valida(celula_tumoral)
        celula_tumoral.camuflaje_pd_l1 = False
        return self.calcular_eficiencia_cd8(celula_tumoral.pH_extracelular) * 100.0

    def aplicar_protocolo_combinado(self, celula_tumoral):
        """
        Camino modelado combinado: bloqueo MCT4 + ajuste BCL-2 + anti-PD-1.
        Actualiza variables del toy model (pH, ATP relativo, apoptosis).
        No constituye indicación clínica.
        """
        self._assert_celula_valida(celula_tumoral)

        celula_tumoral.mct4_bloqueado = True
        celula_tumoral.pH_intracelular = self.PH_INTRACELULAR_LETAL
        celula_tumoral.pH_extracelular = self.PH_RESTAURADO
        celula_tumoral.atp = self.ATP_COLAPSADO

        celula_tumoral.bcl2_expression = self.BCL2_FISIOLOGICO
        celula_tumoral.apoptosis_habilitada = True
        celula_tumoral.apoptosis_activa = True
        celula_tumoral.camuflaje_pd_l1 = False

        autolisis = (
            celula_tumoral.apoptosis_activa is True
            and celula_tumoral.pH_intracelular < 5.5
        )

        return {
            "pH_final": celula_tumoral.pH_extracelular,
            "eficiencia_CD8": self.calcular_eficiencia_cd8(
                celula_tumoral.pH_extracelular
            )
            * 100.0,
            "ATP_tumoral_restante": celula_tumoral.atp,
            "autolisis_acida_activada": autolisis,
        }

    def _assert_celula_valida(self, celula_tumoral):
        if celula_tumoral is None:
            raise ValueError("FC01: célula nula. Protocolo abortado (fail-closed).")
        if not isinstance(celula_tumoral, CelulaTumoral):
            raise ValueError("FC01: tipo celular inválido. Protocolo abortado (fail-closed).")

        ph = getattr(celula_tumoral, "pH_extracelular", None)
        if ph is None:
            raise ValueError("FC02: pH extracelular ausente. Protocolo abortado (fail-closed).")
        try:
            ph_valor = float(ph)
        except (TypeError, ValueError) as exc:
            raise ValueError("FC02: pH extracelular corrupto. Protocolo abortado (fail-closed).") from exc
        if not (CelulaTumoral.PH_FISICO_MIN < ph_valor < CelulaTumoral.PH_FISICO_MAX):
            raise ValueError("FC03: pH físicamente imposible. Protocolo abortado (fail-closed).")


def simular_sistema_completo():
    print("=== Restauracion de estado (modelo) ===")
    print("Placa = instrumento; no ontologia celular.")
    print("Politica CD8: Gated-6.50 (Capa B).\n")

    sana = CelulaSana()
    print(f"[homeostasis] {sana.obtener_estado()}")

    tumor = CelulaTumoral()
    parche = ParcheRestauracion()

    eficiencia = parche.simular_inmunoterapia_aislada(tumor)
    print(f"[anti-PD-1 sola] pHe={tumor.pH_extracelular:.2f}  CD8={eficiencia}%")

    tumor = CelulaTumoral()
    resultado = parche.aplicar_protocolo_combinado(tumor)
    print(f"[protocolo combinado] {resultado}")


if __name__ == "__main__":
    simular_sistema_completo()
