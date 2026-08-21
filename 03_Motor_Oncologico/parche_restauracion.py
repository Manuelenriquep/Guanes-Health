"""
Deterministic restoration routines for the current oncology prototype.

Model-layer comparison: isolated immunotherapy path vs combined intervention
that restores a subset of *modeled* tumor states. Not a clinical protocol.
See SSoT: placa_base_instrumento_investigacion.md

CD8 efficiency uses shared Gated-6.50 policy (`inmuno_utils`).
"""

from inmuno_utils import (
    ANERGY_GATE,
    PH_FISIOLOGICO,
    PH_VETO_CD8,
    calcular_eficiencia_cd8 as eficiencia_cd8_gated,
)
from placa_cancer import CelulaTumoral
from placa_sana import CelulaSana


class ParcheRestauracion:
    PH_VETO_CD8 = PH_VETO_CD8
    PH_FISIOLOGICO = PH_FISIOLOGICO
    ANERGY_GATE = ANERGY_GATE
    PH_RESTAURADO = 7.35
    ATP_COLAPSADO = 30
    PH_INTRACELULAR_LETAL = 5.2
    BCL2_FISIOLOGICO = 1.0
    EFICIENCIA_CD8_MAX = 100.0
    PH_PARALISIS_CD8 = PH_VETO_CD8  # alias deprecado

    @staticmethod
    def calcular_eficiencia_cd8(pHe):
        """Delegado a inmuno_utils (fuente única Gated-6.50)."""
        return eficiencia_cd8_gated(pHe)

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
