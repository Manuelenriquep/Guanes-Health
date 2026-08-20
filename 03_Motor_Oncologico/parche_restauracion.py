"""
Deterministic restoration routines for the current oncology prototype.

Model-layer comparison: isolated immunotherapy path vs combined intervention
that restores a subset of *modeled* tumor states. Not a clinical protocol.
See SSoT: placa_base_instrumento_investigacion.md
"""

from placa_cancer import CelulaTumoral
from placa_sana import CelulaSana


class ParcheRestauracion:
    PH_PARALISIS_CD8 = 7.0
    EFICIENCIA_CD8_ACIDO = 10.0
    EFICIENCIA_CD8_MAX = 100.0
    PH_RESTAURADO = 7.35
    ATP_COLAPSADO = 30
    PH_INTRACELULAR_LETAL = 5.2
    BCL2_FISIOLOGICO = 1.0

    def simular_inmunoterapia_aislada(self, celula_tumoral):
        """
        Camino modelado: monoterapia anti-PD-1.
        Neutraliza camuflaje PD-L1 en el estado; el pH ácido modelado
        reduce la eficiencia CD8+ simulada.
        """
        self._assert_celula_valida(celula_tumoral)
        celula_tumoral.camuflaje_pd_l1 = False
        if celula_tumoral.pH_extracelular < self.PH_PARALISIS_CD8:
            return self.EFICIENCIA_CD8_ACIDO
        return self.EFICIENCIA_CD8_MAX

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
            "eficiencia_CD8": self.EFICIENCIA_CD8_MAX,
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
    print("==================================================")
    print("SIMULACIÓN IN SILICO — RESTAURACIÓN DE ESTADO (MODELO)")
    print("Placa = instrumento; no ontología celular.")
    print("==================================================")

    sana = CelulaSana()
    print("\n--- HOMEOSTASIS (placa sana) ---")
    print(f"  Estado modelado -> {sana.obtener_estado()}")

    tumor = CelulaTumoral()
    parche = ParcheRestauracion()

    print("\n--- MONOTERAPIA ANTI-PD-1 (modelo) ---")
    eficiencia = parche.simular_inmunoterapia_aislada(tumor)
    print(f"  pH extracelular: {tumor.pH_extracelular:.2f}")
    print(f"  Eficiencia CD8+ simulada: {eficiencia}%")

    tumor = CelulaTumoral()
    resultado = parche.aplicar_protocolo_combinado(tumor)
    print("\n--- PROTOCOLO COMBINADO (modelo) ---")
    print(f"  Resultado del modelo -> {resultado}")
    print("==================================================")


if __name__ == "__main__":
    simular_sistema_completo()
