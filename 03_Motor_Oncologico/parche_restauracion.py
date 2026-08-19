"""
Deterministic restoration routines for the current oncology prototype.

This module compares a simplified isolated immunotherapy path against a
combined intervention that restores a subset of modeled tumor states.
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
        Monoterapia anti-PD-1.
        Neutraliza el camuflaje, pero el microambiente ácido paraliza CD8+.
        """
        self._assert_celula_valida(celula_tumoral)
        celula_tumoral.camuflaje_pd_l1 = False
        if celula_tumoral.pH_extracelular < self.PH_PARALISIS_CD8:
            return self.EFICIENCIA_CD8_ACIDO
        return self.EFICIENCIA_CD8_MAX

    def aplicar_protocolo_combinado(self, celula_tumoral):
        """
        Terapia combinada Guanes: MCT4 + BH3 + anti-PD-1.
        Restaura pH perimetral, colapsa ATP tumoral y fuerza autólisis.
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
    print("SIMULACIÓN DE TRATAMIENTO POR RESTAURACIÓN LÓGICA")
    print("==================================================")

    sana = CelulaSana()
    print("\n--- HOMEOSTASIS ---")
    print(f"  Célula sana -> {sana.obtener_estado()}")

    tumor = CelulaTumoral()
    parche = ParcheRestauracion()

    print("\n--- MONOTERAPIA ANTI-PD-1 ---")
    eficiencia = parche.simular_inmunoterapia_aislada(tumor)
    print(f"  pH extracelular: {tumor.pH_extracelular:.2f}")
    print(f"  Eficiencia CD8+: {eficiencia}%")

    tumor = CelulaTumoral()
    resultado = parche.aplicar_protocolo_combinado(tumor)
    print("\n--- PROTOCOLO COMBINADO ---")
    print(f"  Resultado clínico -> {resultado}")
    print("==================================================")


if __name__ == "__main__":
    simular_sistema_completo()
