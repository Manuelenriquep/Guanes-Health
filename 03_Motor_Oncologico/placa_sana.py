"""
Placa-instrumento: modelo determinista de línea base "célula sana".

Artefacto de investigación Guanes Health (no ontología: la célula no "es"
una placa de silicio). Codifica un subconjunto pequeño de homeostasis para
comparar contra el estado tumoral modelado. Ver SSoT:
`placa_base_instrumento_investigacion.md`.
"""


class CelulaSana:
    # NIVEL III: CONSTANTES E INMUTABLES FÍSICOS
    POTENCIAL_MIN = -70.0
    POTENCIAL_MAX = -90.0
    FIDELIDAD_ADN_POL = 1e-7
    ATP_NOMINAL = 100
    ATP_MINIMO_SOBREVIVENCIA = 20.0
    PH_EXTRACELULAR_NOMINAL = 7.35
    LIMITE_HAYFLICK_MAX = 50
    TELOMERO_MINIMO_BP = 10.0

    def __init__(self):
        self.potencial_membrana = -80.0
        self.atp = self.ATP_NOMINAL
        self.pH_extracelular = self.PH_EXTRACELULAR_NOMINAL
        self.dano_genomico = 0.0
        self.generaciones = 0
        self.longitud_telomeros = 100.0

        # Fusible nativo conectado (habilitado) pero no disparado
        self.apoptosis_habilitada = True
        self.apoptosis_activa = False
        self.senescencia_activa = False
        self.mutaciones_acumuladas = 0

    def obtener_estado(self):
        """Snapshot determinista del estado operativo nominal."""
        return {
            "pH_extracelular": self.pH_extracelular,
            "ATP": self.atp,
            "apoptosis_habilitada": self.apoptosis_habilitada,
        }

    def is_viable(self):
        return (
            self.POTENCIAL_MAX <= self.potencial_membrana <= self.POTENCIAL_MIN
            and self.atp >= self.ATP_MINIMO_SOBREVIVENCIA
            and not self.apoptosis_activa
            and not self.senescencia_activa
        )

    def reparar_adn(self):
        if self.dano_genomico > 0.0:
            if self.dano_genomico <= 5.0:
                self.dano_genomico = 0.0
            else:
                self.ciclo_celular_checkpoint()

    def ciclo_celular_checkpoint(self):
        if self.dano_genomico > 5.0 and self.apoptosis_habilitada:
            self.apoptosis()

    def apoptosis(self):
        if not self.apoptosis_habilitada:
            return
        self.apoptosis_activa = True

    def dividir(self):
        if not self.is_viable():
            return False

        self.atp -= 2
        self.generaciones += 1
        self.longitud_telomeros -= 1.8
        self.dano_genomico += 0.1

        if (
            self.longitud_telomeros <= self.TELOMERO_MINIMO_BP
            or self.generaciones >= self.LIMITE_HAYFLICK_MAX
        ):
            self.senescencia_activa = True
            self.longitud_telomeros = max(self.longitud_telomeros, self.TELOMERO_MINIMO_BP)
            return False

        self.reparar_adn()
        return True
