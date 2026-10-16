# PLACA BASE DE LÓGICA: MOTOR ONCOLÓGICO & HOMEOSTASIS CELULAR IN-SILICO
**ESPECIFICACIÓN TÉCNICA UNIFICADA DE RESTRICCIÓN BIOFÍSICA, ACOPLAMIENTO ENTERO-HEPÁTICO Y TERAPIA CELULAR**  
**Versión 6.0 (Formato Canónico 5 Niveles - GUANES-HEALTH-2026-STABLE)**  
**División de Inmunología de Sistemas, Biofísica Celular y Modelado In-Silico — Guanes Health**  
**Entorno de Integración:** `placa_sana.py`, `placa_cancer.py`, `inmuno_utils.py`, `parche_restauracion.py` & `simulador_onco_homeostasis_v5.py`  
**Ámbito:** Simulación In-Silico · Microambiente Tumoral Ácido · Eje Entero-Hepático ($\phi_{gut}$) · CAR-T / NHE1-Shield · Restauración Homeostática

---

## INTRODUCCIÓN Y DEMARCACIÓN EPISTEMOLÓGICA

Esta especificación técnica constituye el chasis biofísico y matemático inmutable que gobierna las simulaciones de viabilidad celular, evasión inmune y respuesta terapéutica en el microambiente tumoral del hepatocarcinoma (HCC).

> [!IMPORTANT]
> **Postulado Epistemológico Fundamental:** La placa base es un **instrumento de cribado y demarcación de restricciones**, no una ontología biológica viva. Su función exclusiva es actuar como un filtro determinista implacable de viabilidad física y termodinámica, verificando gradientes electroquímicos, balances de protones, puntos de control inmunitario y tono inflamatorio sistémico, impidiendo alucinaciones computacionales en el diseño de vectores y terapias celulares adoptivas.

---

## NIVEL I: ÁRBOL DE REGLAS CONDICIONALES (Axiomas Biofísicos, Inmunes y Sistémicos)

El estado biofísico y funcional de una célula tumoral o inmune se modela como un vector de estado determinista en el espacio de Hilbert continuo-discreto:

$$\mathcal{S}_{cell} = \langle pHe, pHi, [ATP], [Lactato], \text{MCT4}, \text{NHE1}, \text{BCL2}, \text{PD-L1}, [IL-6], \phi_{gut}, [TOX], \text{Apoptosis} \rangle$$

```
                         [ INGESTIÓN DEL VECTOR DE ESTADO ]
                                          │
                                          ▼
                         [ EVALUACIÓN DE GRADIENTES Y ENTORNO ]
                                          │
         ┌───────────────────┬────────────┴───────────┬───────────────────┐
         ▼                   ▼                        ▼                   ▼
  [ Eje pH / MCT4 ]    [ Política CD8+ ]         [ Eje Gut-Liver ]    [ Eje BCL-2 ]
 (Warburg / Protones) (Gated-6.50 / Anergia)    (Akkermansia / LPS)  (MOMP / Caspasas)
         │                   │                        │                   │
  ¿Extrusión Activa   ¿pHe > 6.50 Y            ¿phi_gut >= 0.899?    ¿BCL-2 Sobreevade
   en pHe Ácido?       Fracción >= 0.20?       (Baja IL-6 Portal)     Muerte Mitocondrial?
    NO ──┐              NO ──┐                   NO ──┐                  SÍ ──┐
         ▼                   ▼                        ▼                       ▼
🛑 COLAPSO ÁCIDO     🛑 ANERGIA TOTAL         ⚠️ FATIGA EPIGENÉTICA   🛡️ EVASIÓN TUMORAL
(pHi < 6.80 Muerte) (Citotoxicidad = 0.0)    (Inducción TOX/PD-L1)   (Apoptosis Inactiva)
```

### Axioma 1.1: Eflujo de Protones y Metabolismo de Warburg (Transporte MCT4 / NHE1)
- **SI:** El pH extracelular se encuentra en rango ácido ($pHe \le 6.50$) Y los transportadores transmembrana de eflujo de protones/lactato (MCT4 y NHE1) están plenamente activos:
- **➔ ENTONCES:** La célula sostiene la glicólisis anaerobia acelerada ($[ATP] \ge 10000\text{ u. rel.}$), mantiene un $pHi$ fisiológico viable ($pHi \approx 7.20$) y extruye activamente ácido láctico al estroma.
- **PORQUE:** Conforme a la bioenergética tumoral (Efecto Warburg), la sobreexpresión de transportadores monocarboxilato compensa el gradiente químico adverso, evitando la acidificación letal del citoplasma.

### Axioma 1.2: Política Inmune Canónica Gated-6.50 (Anergia Ácida de Linfocitos T CD8+ y CAR-T)
- **SI:** Un linfocito T citotóxico CD8+ o célula CAR-T convencional sin blindaje de protones infiltra un estroma con $pHe \le 6.50$:
- **➔ ENTONCES:** El motor anula determinísticamente su eficiencia lítica ($\eta_{cd8} = 0.0$), forzando anergia funcional inmediata; si $6.50 < pHe < 7.35$, la eficiencia sigue la rampa lineal:
  $$\eta_{cd8}(pHe) = \max\left(0.0, \, \frac{pHe - 6.50}{7.35 - 6.50}\right) \quad \text{con filtro de corte: } \eta_{cd8} < 0.20 \implies 0.0$$
- **PORQUE:** La acidosis extracelular severa inhibe la fosforilación de p38 MAPK y colapsa la síntesis de perforinas y granzima B en linfocitos T no modificados.

### Axioma 1.3: Eje Entero-Hepático-Tumoral ($\phi_{gut}$ / LPS $\rightarrow$ IL-6 $\rightarrow$ STAT3 $\rightarrow$ PD-L1 / TOX)
- **SI:** La integridad de la barrera intestinal cae ($\phi_{gut} < 0.899$) por disbiosis o ausencia de *Akkermansia muciniphila*:
- **➔ ENTONCES:** La traslocación portal de lipopolisacáridos (LPS) eleva la concentración estromal de IL-6 ($IL6_{basal} = IL6_{physio} + K_{LPS\_IL6} \cdot (1 - \phi_{gut})$), induciendo la sobreexpresión tumoral de PD-L1 ($\times 12$) y disparando la fatiga epigenética irreversible mediada por el factor de transcripción **TOX** ($H3K27me3$).
- **PORQUE:** La inflamación sistémica portal acopla el intestino con el hígado, creando un bucle estromal de inmunosupresión que inutiliza vacunas y terapias celulares desprovistas de soporte de barrera.

### Axioma 1.4: Rescate Homeostático Multimodal (Parche Oncolítico y Blindaje NHE1-Shield)
- **SI:** Se administra la co-intervención multimodal: Parche de neutralización estromal ($pHe \rightarrow 7.35$), silenciamiento de BCL-2 ($BCL2 \rightarrow 1.0$), e inhibición de MCT4 en tumor acoplado al blindaje NHE1-Shield en linfocito:
- **➔ ENTONCES:** La célula tumoral activa la cascada de Caspasa-3/9 con liberación de Citocromo C (MOMP), colapsando el ATP tumoral a niveles basales y restituyendo la citotoxicidad inmune a $\ge 94.7\%$.
- **PORQUE:** La remoción combinada del camuflaje ácido y del bloqueo anti-apoptótico reactiva los programas intrínsecos de muerte programada inmutables de la fisiología sana.

---

## NIVEL II: MATRIZ DE EXCLUSIONES SEMÁNTICAS & VETOS FAIL-CLOSED (`FC-BIO-*`)

Para salvaguardar la coherencia biofísica y evitar que el simulador produzca artefactos matemáticos inviables, el motor opera bajo la doctrina **Fail-Closed**.

```
                                [ MATRIZ DE VETOS BIOFÍSICOS ]
                                                │
             ┌───────────────────┬──────────────┴──────┬───────────────────┐
             ▼                   ▼                     ▼                   ▼
      [ FC-BIO-01 ]       [ FC-BIO-03 ]         [ FC-BIO-2.1 ]      [ FC-BIO-GUT ]
 (1ª Ley Termodinámica) (pH Fuera de Rango)    (Anergia Ácida pHe) (Permeabilidad Gut)
             │                   │                     │                   │
             ▼                   ▼                     ▼                   ▼
     🛑 ABORTAR RUN      🛑 ABORTAR RUN        🛑 ANERGIA TOTAL    ⚠️ CORTE SISTÉMICO
    (Violación Masa)    (Física Imposible)    (Eficiencia = 0.0)   (Agotamiento TOX)
```

| Código | Condición Evaluada / Ecuación | Acción de Bloqueo | Sustento Físico / Mecanístico |
| :--- | :--- | :--- | :--- |
| `FC-BIO-01` | Balance de masa/energía violado | Abortar simulación | Primera Ley de la Termodinámica y estequiometría de metabolitos. |
| `FC-BIO-02` | $pH = \emptyset \lor pH \notin \mathbb{R}$ | Abortar simulación | Integridad estricta de entrada de datos (Fail-Closed). |
| `FC-BIO-03` | $pH \le 0.0 \lor pH \ge 14.0$ | Abortar simulación | Límites físicos de disolución acuosa y concentración de $[H^+]$. |
| `FC-BIO-04` | $[ATP] < 0 \lor [Lactato] < 0$ | Abortar simulación | No negatividad de concentraciones químicas absolutas. |
| `FC-BIO-05` | Alucinación ontológica ("célula = silicio") | Bloqueo Epistemológico | La placa es un instrumento de cribado numérico, no materia viva. |
| `FC-BIO-2.1`| $pHe \le 6.50$ en linfocito no blindado | Forzar $\eta_{cd8} = 0.0$ | Parálisis por acidosis estromal e inhibición de vía de perforinas. |
| `FC-BIO-GUT`| $\phi_{gut} < 0.0 \lor \phi_{gut} > 1.0$ | Abortar simulación | La fracción de sellado de mucosa intestinal es una cota acotada en $[0, 1]$. |
| `FC-BIO-TOX`| $[IL6] > 500\text{ pg/mL} \land \phi_{gut} < 0.5$ | Activar Fatiga Epigenética | Acumulación sostenida de $H3K27me3$ y silenciamiento de locus $IL2/IFNG$. |

---

## NIVEL III: CONSTANTES E INMUTABLES BIOFÍSICAS Y FARMACOLÓGICAS (Ledger 2026)

Valores inmutables calibrados para la simulación biofísica estándar Guanes Health 2026:

```python
# ==============================================================================
# LEDGER DE PARÁMETROS BIOFÍSICOS Y CELULARES (SSoT CAPA B - 2026)
# ==============================================================================
# 1. Parámetros de pH y Microambiente Ácido
PH_ACIDO_TUMORAL: float = 6.20        # pHe extremo inferior del microambiente tumoral
PH_FISIOLOGICO_SANO: float = 7.35     # pHe fisiológico estándar de tejido sano
PH_INTRACELULAR_BASAL: float = 7.20   # pHi citosólico de la célula tumoral aclimatada
PH_APOPTOSIS_CRITICO: float = 6.80    # Umbral de acidificación intracelular pro-apoptótica
PH_INTRACELULAR_LETAL: float = 5.20   # Autólisis ácida irreversible
PH_VETO_CD8: float = 6.50             # Piso de anergia lítica de linfocitos T (FC-BIO-2.1)
ANERGY_GATE_THRESHOLD: float = 0.20   # Umbral de corte mínimo de citotoxicidad funcional
PH_FISICO_MIN: float = 0.0            # Cota física inferior de pH acuoso
PH_FISICO_MAX: float = 14.0           # Cota física superior de pH acuoso

# 2. Bioenergética y Marcadores Anti-Apoptóticos
ATP_WARBURG: int = 10000              # Nivel relativo de ATP en glicólisis acelerada tumoral
ATP_BASAL_SANO: int = 5000            # Nivel de ATP en fosforilación oxidativa fisiológica
ATP_MINIMO_SOBREVIVENCIA: float = 20.0# Umbral mínimo de viabilidad metabólica
ATP_COLAPSADO_PARCHE: int = 30        # Nivel de ATP tras bloqueo selectivo de MCT4
BCL2_FACTOR_TUMORAL: float = 25.0     # Nivel de sobreexpresión anti-apoptótica tumoral
BCL2_FACTOR_SANO: float = 1.0         # Nivel basal de BCL-2

# 3. Parámetros Eje Entero-Hepático-Tumoral (Gut-Liver-Tumor)
PHI_GUT_OPTIMO: float = 1.0           # Barrera epitelial perfecta (Akkermansia muciniphila)
PHI_GUT_CRITICO_RESCATE: float = 0.899# Umbral crítico de barrera para rescate inmunológico
IL6_FISIOLOGICO: float = 5.0          # Concentración basal fisiológica de IL-6 (pg/mL)
IL6_TORMENTA_MAX: float = 800.0       # Concentración máxima portal en Leaky Gut severo (pg/mL)
K_LPS_IL6: float = 795.0              # Constante de transducción LPS -> IL-6 portal
ALPHA_IL6_PDL1: float = 11.0          # Factor de amplificación de PD-L1 mediado por STAT3
K_IL6_TUMOR: float = 50.0             # Constante de semi-saturación tumoral para IL-6

# 4. Parámetros de Linaje y Réplica
LIMITE_HAYFLICK_MAX: int = 50         # Generaciones máximas de replicación en célula sana
TELOMERO_MINIMO_BP: float = 10.0      # Umbral crítico de longitud telomérica relativa
```

---

## NIVEL IV: RED DE DEPENDENCIA MECANÍSTICA (Mapa Kelseniano Biofísico)

Las leyes naturales y los modelos matemáticos se organizan en una jerarquía estricta de precedencia determinista:

```
                              [ GRADO 1: SUPREMO ]
             Primera y Segunda Ley de la Termodinámica (Energía y Entropía)
             Ecuación de Nernst y Gradientes Electroquímicos de Membrana
             No Negatividad de Concentraciones y Ley de Conservación de Masa
                                        │
                                        ▼
                               [ GRADO 2: BIOLÓGICO ]
                   Eje de Transporte de Protones (MCT1 / MCT4 / NHE1)
                   Vía Intrínseca Mitocondrial de Apoptosis (BCL-2 / MOMP / Caspasas)
                   Eje Entero-Hepático (Barrera Gut phi_gut -> LPS -> IL-6 -> STAT3)
                   Punto de Control Inmunitario (PD-1 / PD-L1 / Anergia Ácida)
                                        │
                                        ▼
                        [ GRADO 3: INTERVENCIÓN CAPA B ]
                       Política Canónica 'Gated-6.50' (inmuno_utils.py)
                       Blindaje de Linfocitos 'NHE1-Shield' (S267F)
                       Parche de Restauración Oncológica Guanes
```

1. **Grado 1 (Supremo - Leyes Físicas y Termodinámicas):**
   - Conservación de la materia y energía; balance estequiométrico redox ($NADH/NAD^+$).
   - Ecuación de Nernst y potencial electroquímico transmembrana ($V_m$).
   - Imposibilidad de concentraciones químicas negativas o pH fuera del rango físico $(0, 14)$.
2. **Grado 2 (Biológico - Fisiología y Hallmarks of Cancer):**
   - Cinética enzimática de extrusión ácida tumoral mediada por transportadores monocarboxilato.
   - Vía intrínseca mitocondrial: BCL-2 impide la oligomerización de BAX/BAK y la liberación de Citocromo C.
   - Cascada inflamatoria portal: Endotoxemia por LPS activa receptor TLR4 hepático gatillando secreción masiva de IL-6.
3. **Grado 3 (Intervención - Modelos In-Silico Capa B):**
   - Algoritmo de filtrado de citotoxicidad `inmuno_utils.py` (Gated-6.50).
   - Simulación de reprogramación genética de linfocitos (NHE1-Shield).
   - Parche de restauración homeostática y normalización microambiental.

*Regla de Jerarquía Biofísica:* Ninguna hipótesis, vector viral o intervención de Grado 3 puede violar las vías biológicas de Grado 2 ni las leyes termodinámicas de Grado 1.

---

## NIVEL V: CASOS DE PRUEBA LÓGICA (Unittest de Robustez Inviolable)

```python
import unittest
from enum import Enum
from typing import Any, Dict

# ==============================================================================
# MOTOR DETERMINISTA DE SIMULACIÓN ONCOLÓGICA Y HOMEOSTASIS (CAPA B)
# ==============================================================================

class EstadoCelular(str, Enum):
    HOMEOSTASIS = "HOMEOSTASIS"
    TUMORAL_WARBURG = "TUMORAL_WARBURG"
    APOPTOSIS_EN_CURSO = "APOPTOSIS_EN_CURSO"
    COLAPSO_ACIDO = "COLAPSO_ACIDO"
    ANERGIA_INMUNE = "ANERGIA_INMUNE"


class MotorOncologico5Capas:
    def __init__(self):
        # Constantes Ledger 2026
        self.PH_ACIDO_TUMORAL = 6.20
        self.PH_FISIOLOGICO_SANO = 7.35
        self.PH_VETO_CD8 = 6.50
        self.ANERGY_GATE_THRESHOLD = 0.20
        self.BCL2_FACTOR_TUMORAL = 25.0
        self.BCL2_FACTOR_SANO = 1.0
        self.ATP_WARBURG = 10000
        self.ATP_BASAL_SANO = 5000

    @staticmethod
    def validar_ph(ph: Any) -> float:
        if ph is None:
            raise ValueError("FC-BIO-02: pH nulo. Abortado (Fail-Closed).")
        try:
            val = float(ph)
        except (TypeError, ValueError) as exc:
            raise ValueError("FC-BIO-02: pH no numérico o corrupto.") from exc
        if val <= 0.0 or val >= 14.0:
            raise ValueError(f"FC-BIO-03: pH {val} fuera de rango físico real (0 < pH < 14).")
        return val

    @staticmethod
    def calcular_eficiencia_cd8(pHe: float, nhe1_shield: bool = False) -> float:
        """Implementación canónica de la Política Inmune Gated-6.50."""
        pHe_val = MotorOncologico5Capas.validar_ph(pHe)
        if nhe1_shield:
            return 0.947  # Linfocito acorazado con NHE1-Shield mantiene alta lisis en ácido
        if pHe_val <= 6.50:
            return 0.0   # FC-BIO-2.1: Anergia total en medio ácido
        
        # Rampa lineal de 6.50 a 7.35
        fraccion_cruda = (pHe_val - 6.50) / (7.35 - 6.50)
        fraccion_cruda = min(1.0, max(0.0, fraccion_cruda))
        
        # Anergy Gate: Fracción menor a 0.20 se degrada a 0.0
        if fraccion_cruda < 0.20:
            return 0.0
        return round(fraccion_cruda, 4)

    @staticmethod
    def simular_eje_gut_liver(phi_gut: float) -> Dict[str, float]:
        """Calcula inducción de IL-6 portal, PD-L1 y silenciamiento TOX."""
        if not (0.0 <= phi_gut <= 1.0):
            raise ValueError(f"FC-BIO-GUT: phi_gut {phi_gut} fuera de intervalo físico [0, 1].")
        
        il6_portal = 5.0 + 795.0 * (1.0 - phi_gut)
        pdl1_relativo = 1.0 + 11.0 * (il6_portal / (il6_portal + 50.0))
        agotamiento_tox = round((1.0 - phi_gut) * 82.3 + 1.2, 2)
        
        return {
            "phi_gut": phi_gut,
            "il6_pg_ml": round(il6_portal, 2),
            "pdl1_densidad": round(pdl1_relativo, 2),
            "agotamiento_epigenetico_pct": min(100.0, agotamiento_tox)
        }


class CelulaTumoralModelo:
    def __init__(self):
        self.pHe = 6.20
        self.pHi = 7.20
        self.atp = 10000
        self.bcl2 = 25.0
        self.mct4_bloqueado = False
        self.pd_l1_activo = True
        self.apoptosis_activa = False
        self.estado = EstadoCelular.TUMORAL_WARBURG

    def bloquear_mct4(self):
        self.mct4_bloqueado = True
        if self.pHe <= 6.50:
            self.pHi = 6.60  # Acidificación citosólica crítica
        self._actualizar_estado()

    def aplicar_parche_restauracion(self):
        self.pHe = 7.35
        self.pHi = 7.20
        self.bcl2 = 1.0
        self.pd_l1_activo = False
        self.atp = 5000
        self.apoptosis_activa = True
        self.estado = EstadoCelular.APOPTOSIS_EN_CURSO

    def _actualizar_estado(self):
        if self.pHi < 6.80 and self.bcl2 > 1.0:
            self.estado = EstadoCelular.COLAPSO_ACIDO
        elif self.bcl2 <= 1.0:
            self.apoptosis_activa = True
            self.estado = EstadoCelular.APOPTOSIS_EN_CURSO
        else:
            self.estado = EstadoCelular.TUMORAL_WARBURG


# ==============================================================================
# SUITE DE PRUEBAS UNITARIAS INVIOLABLES
# ==============================================================================

class TestPlacaBaseOncologica5Capas(unittest.TestCase):

    def setUp(self):
        self.motor = MotorOncologico5Capas()

    def test_politica_gated_650_anergia_inmune(self):
        """Valida que un CD8+ en pH ácido tumoral (6.20) tenga eficiencia 0.0 (FC-BIO-2.1)."""
        eficiencia_acida = self.motor.calcular_eficiencia_cd8(pHe=6.20, nhe1_shield=False)
        self.assertEqual(eficiencia_acida, 0.0)

        # En pH fisiológico (7.35) debe alcanzar 1.0
        eficiencia_fisiologica = self.motor.calcular_eficiencia_cd8(pHe=7.35, nhe1_shield=False)
        self.assertEqual(eficiencia_fisiologica, 1.0)

        # En pH intermedio 6.60 (fracción cruda < 0.20) debe caer por Anergy Gate a 0.0
        eficiencia_subumbral = self.motor.calcular_eficiencia_cd8(pHe=6.60, nhe1_shield=False)
        self.assertEqual(eficiencia_subumbral, 0.0)

    def test_blindaje_nhe1_shield_en_microambiente_acido(self):
        """Valida que el CAR-T acorazado con NHE1-Shield sostenga lisis activa a pH 6.20."""
        eficiencia_shield = self.motor.calcular_eficiencia_cd8(pHe=6.20, nhe1_shield=True)
        self.assertGreater(eficiencia_shield, 0.90)

    def test_veto_fail_closed_ph_corrupto_o_imposible(self):
        """FC-BIO-02 y FC-BIO-03: Abortar si el pH es None o fuera de rango físico."""
        with self.assertRaises(ValueError):
            self.motor.validar_ph(None)
        with self.assertRaises(ValueError):
            self.motor.validar_ph(-2.0)
        with self.assertRaises(ValueError):
            self.motor.validar_ph(15.5)

    def test_acoplamiento_eje_gut_liver_akkermansia(self):
        """Valida el acoplamiento sistémico: Leaky Gut severo (phi=0.0) dispara IL-6 a 800 pg/mL."""
        leaky_gut = self.motor.simular_eje_gut_liver(phi_gut=0.0)
        self.assertEqual(leaky_gut["il6_pg_ml"], 800.0)
        self.assertGreater(leaky_gut["agotamiento_epigenetico_pct"], 80.0)

        # Con barrera perfecta (phi=1.0) la IL-6 permanece en nivel fisiológico (5 pg/mL)
        gut_optimo = self.motor.simular_eje_gut_liver(phi_gut=1.0)
        self.assertEqual(gut_optimo["il6_pg_ml"], 5.0)
        self.assertLess(gut_optimo["agotamiento_epigenetico_pct"], 2.0)

    def test_bloqueo_mct4_y_restauracion_homeostatica(self):
        """Valida la auto-acidificación citosólica tras bloqueo de MCT4 y apoptosis por parche."""
        celula = CelulaTumoralModelo()
        self.assertEqual(celula.estado, EstadoCelular.TUMORAL_WARBURG)

        # Bloqueo de MCT4 en medio ácido provoca colapso ácido citosólico
        celula.bloquear_mct4()
        self.assertEqual(celula.estado, EstadoCelular.COLAPSO_ACIDO)
        self.assertEqual(celula.pHi, 6.60)

        # Aplicación de Parche Oncolítico activa apoptosis y neutraliza el estroma
        celula.aplicar_parche_restauracion()
        self.assertEqual(celula.estado, EstadoCelular.APOPTOSIS_EN_CURSO)
        self.assertTrue(celula.apoptosis_activa)
        self.assertEqual(celula.pHe, 7.35)
        self.assertEqual(celula.bcl2, 1.0)


if __name__ == '__main__':
    unittest.main()
```

---

## 6. Referencia Canónica al Software Bioeléctrico
Para la derivación electroquímica del potencial de membrana ($V_{mem}$), acoplamiento por conexinas (*gap junctions*) e isomorfismo de red bioeléctrica según Michael Levin, consultar la especificación SSoT:  
[`investigacion_michael_levin_software_bioelectrico.md`](./investigacion_michael_levin_software_bioelectrico.md).
