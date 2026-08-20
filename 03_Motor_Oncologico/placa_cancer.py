"""
Placa-instrumento: modelo determinista de estado tumoral (toy model).

Artefacto de investigación Guanes Health (no ontología: el tumor no "es"
malware de silicio). Variables simplificadas (pH, ATP relativo, BCL-2,
PD-L1) para exploración in silico. Ver SSoT:
`placa_base_instrumento_investigacion.md`.
"""


class CelulaTumoral:
    ATP_WARBURG = 10000
    PH_ACIDO_TUMORAL = 6.20
    PH_INTRACELULAR_BASAL = 7.20
    BCL2_FACTOR = 25.0
    PH_FISICO_MIN = 0.0
    PH_FISICO_MAX = 14.0

    def __init__(self):
        self.pH_extracelular = self.PH_ACIDO_TUMORAL
        self.pH_intracelular = self.PH_INTRACELULAR_BASAL
        self.atp = self.ATP_WARBURG
        self.mct4_bloqueado = False
        self.camuflaje_pd_l1 = True
        self.bcl2_expression = self.BCL2_FACTOR
        self.apoptosis_habilitada = False
        self.apoptosis_activa = False

    def establecer_pH(self, ph):
        """Fija el pH del microambiente. Fail-closed si el valor es nulo o no físico."""
        if ph is None:
            raise ValueError("FC02: pH nulo. Protocolo abortado (fail-closed).")
        try:
            ph_valor = float(ph)
        except (TypeError, ValueError) as exc:
            raise ValueError("FC02: pH corrupto. Protocolo abortado (fail-closed).") from exc
        if not (self.PH_FISICO_MIN < ph_valor < self.PH_FISICO_MAX):
            raise ValueError("FC03: pH físicamente imposible. Protocolo abortado (fail-closed).")
        self.pH_extracelular = ph_valor
