# Placa Base de Lógica de Guanes Health (v6.0)
**Arquitectura Multiescala de Control Biofísico, Bioeléctrico y Sistémico**
**División de Biofísica de Sistemas, Inmunología Computacional y Modelado In Silico — Guanes Health**

---

### Demarcación Epistemológica y Principio de Rigor

Este sistema no constituye un modelo clínico determinista ni pretende suplantar la validación experimental en laboratorio húmedo (*wet-lab*). Se trata de una **arquitectura de ingeniería de sistemas aplicada a la biología matemática (Capa B)** que formaliza reglas de control, barreras físicas e invariantes electroquímicas bajo supuestos explícitos.

Unifica cuantitativamente:
1. La **biología celular de sistemas** y la auditoría genómica.
2. La **termodinámica de membranas** y el metabolismo de protones (Warburg, NHE1, MCT1/4).
3. Los hallazgos de **bioelectricidad y reprogramación morfogenética de Michael Levin** ($V_{mem}$, uniones gap Cx43, Cono de Luz Cognitivo).
4. El **eje homeostático sistémico (Intestino-Hígado-Tumor)** mediado por la integridad mucosa ($\phi_{gut}$), *Akkermansia muciniphila*, LPS portal y el eje IL-6 / STAT3 / PD-L1.

---

### 📑 DIAGRAMA ARQUITECTÓNICO DE LA PLACA BASE v6.0

```
+---------------------------------------------------------------------------------------------------------+
|                                    PLACA BASE DE LÓGICA UNIFICADA v6.0                                  |
+---------------------------------------------------------------------------------------------------------+
|                                                                                                         |
|  [NIVEL I: ÁRBOL DE REGLAS CONDICIONALES DE HOMEOSTASIS Y CÓDIGO BIOELÉCTRICO]                          |
|     - REG-I-01 (Auditoría Genómica p53/p21): Suspensión de CDK ante roturas de ADN.                     |
|     - REG-I-02 (Sensor Metabólico AMPK): Freno anabólico si desciende el ATP mitocondrial.               |
|     - REG-I-03 (Carga Bioeléctrica Vm / Gap Junctions):                                                 |
|          SI Vm despolariza a -15 mV Y las conexinas (GJC) se desenganchan,                              |
|          ENTONCES la célula aborta la memoria morfogenética del órgano, aísla su "yo" computacional     |
|          y regresa a un fenotipo amebiano atávico mitótico (Oncogénesis).                               |
|     - REG-I-04 (Normalización Bioeléctrica Levin):                                                      |
|          SI se fuerza la hiperpolarización (Vm -> -75 mV) Y se reabren las Gap Junctions,               |
|          ENTONCES se reestablece la señalización no-local y se reprime la transcripción oncogénica,      |
|          reintegrando la célula a la arquitectura del tejido a pesar de mutaciones en el ADN.           |
|                                                                                                         |
|  [NIVEL II: MATRIZ DE EXCLUSIONES SEMÁNTICAS - CORTAFUEGOS FAIL-CLOSED]                                 |
|     - VETO FC-BIO-01 (Apoptosis Intrínseca): Desatascado de BAX/BAK -> MOMP -> Efferocitosis.           |
|     - VETO FC-BIO-02 (Límite de Hayflick): Senescencia determinista si telómeros <= 4000 pb.             |
|     - VETO FC-BAR-01 (Firewall de Mucosa / Leaky Gut):                                                  |
|          SI TEER < 1000 u. o la integridad de Akkermansia cae por debajo del 89.9%,                     |
|          ENTONCES translocación de LPS portal -> Alarma de IL-6 -> Escudo tumoral PD-L1.                |
|                                                                                                         |
|  [NIVEL III: CONSTANTES BIOFÍSICAS, INMUTABLES DE MEMBRANA Y LÍMITES DEL MICROAMBIENTE]                  |
|     - Potencial de Membrana Sano (Vm): -70 mV a -90 mV.                                                 |
|     - Potencial Tumoral Despolarizado (Vm): -15 mV.                                                     |
|     - Inactivación Alostérica de PFK-1 por Protones: pKa = 6.60, n_Hill = 4.0.                          |
|     - Umbral de Eubiosis de Akkermansia: 1.0% a 5.0% (Umbral de rescate de barrera >= 89.9%).           |
|     - Acidosis Estromal Extracelular (pHe): 6.20 a 6.50.                                                |
|     - Gasto Energético en Gradientes: ~1/3 del presupuesto total de ATP de la célula.                   |
|                                                                                                         |
|  [NIVEL IV: RED DE DEPENDENCIAS NORMATIVAS Y CONEXIÓN DE ESCALAS (BUCLE SISTÉMICO)]                     |
|     Intestino (Akkermansia -> phi_gut) -> Vena Porta (LPS -> IL-6) -> Hígado/Tumor (STAT3 -> PD-L1)    |
|     -> Linfocito T (Acidosis -> PFK-1 OFF -> Colapso de ATP -> TOX / H3K27me3)                         |
|     -> Trampa Bioeléctrica del Ácido: Vm=-75 mV en pHe=6.20 succiona H+ (ATP colapsa a 1.07%).          |
|                                                                                                         |
|  [NIVEL V: ARNÉS DE VERIFICACIÓN E SUITE DE SIMULACIÓN IN SILICO (PYTHON)]                              |
|     - Motores deterministas con pruebas unitarias automatizadas (unittest).                             |
|                                                                                                         |
+---------------------------------------------------------------------------------------------------------+
```

---

### Detalle de los 5 Niveles de la Placa Lógica

#### NIVEL I: Árbol de Reglas Condicionales (Lógica Homeostática y Código Bioeléctrico)
* **Auditoría Genómica (`REG-I-01`, p53 / p21):** Ante roturas de doble cadena de ADN, la activación de ATM/ATR y p53 estabiliza p21/WAF1, deteniendo las quinasas Cdk2/Ciclina E para priorizar la reparación de la hebra por el sistema Mismatch Repair (MMR) antes de autorizar la replicación.
* **Gobernanza Bioenergética (`REG-I-02`, AMPK / PFK-1):** Cuando la demanda energética compromete el ATP celular, AMPK inhibe mTORC1 y activa la autofagia. Bajo acidosis tumoral ($pH_e \approx 6.20$), los protones citosólicos inhiben de forma alostérica a la enzima glucolítica PFK-1 ($pK_a = 6.60$, $n_{Hill} = 4.0$), apagando la síntesis de energía.
* **El Pegamento Cognitivo Bioeléctrico (`REG-I-03`, $V_m$ y Conexinas):** Siguiendo los descubrimientos de Michael Levin, el potencial de membrana ($V_m$) y las uniones comunicantes (*gap junctions*) actúan como un pegamento cognitivo que coordina el patrón del órgano. Si una célula se despolariza ($V_m \approx -15\text{ mV}$) y cierra sus conexinas, pierde el contacto eléctrico con el colectivo, reduce el límite de su "yo" computacional y regresa a un estado unicelular amebiano atávico que prolifera y migra (metástasis).
* **Normalización Reprogramada sin Reparación Genómica (`REG-I-04`):** Forzar la hiperpolarización celular ($V_m \approx -75\text{ a }-85\text{ mV}$) mediante canales iónicos o la reexpresión de conexinas permite reabrir el canal comunicante con las células vecinas. Esta sincronización iónica impone un control *top-down* que suprime la expresión oncogénica ($KRAS$), detiene el crecimiento tumoral y fuerza la reintegración al tejido sin necesidad de modificar el ADN.

---

#### NIVEL II: Matriz de Exclusiones Semánticas (Cortafuegos *Fail-Closed*)
* **Veto FC-BIO-01 (Apoptosis e MOMP):** Si el daño genómico es irreparable o se desatascan los bolsillos BH3 de Bcl-2/Bcl-xL, BAX/BAK forman poros mitocondriales (MOMP), liberando Citocromo c para ejecutar la apoptosis con señalización externa de fosfatidilserina (efferocitosis limpia e ininflamatoria).
* **Veto FC-BIO-02 (Límite de Hayflick):** La senescencia somática se gatilla de forma determinista cuando la longitud telomérica alcanza los $\le 4000\text{ pb}$ (exactamente a las 50 divisiones partiendo de 8000 pb). Las mutaciones en el promotor $hTERT$ (-124 G>A / -146 G>A) reclutan al factor GABP para evadir este veto.
* **Veto FC-BAR-01 (Integridad de la Barrera Intestinal):** Si la abundancia de *Akkermansia muciniphila* cae por debajo del umbral crítico del **89.9% de integridad de barrera** (TEER $< 1000\ \Omega\cdot\text{cm}^2$), la translocación de lipopolisacáridos (LPS) por la vena porta dispara la IL-6 sinusoidal en el hígado. La IL-6 induce la vía GP130/STAT3 en el tumor, hiperexpresando el escudo PD-L1 y promoviendo el silenciamiento epigenético (marca H3K27me3 por el factor TOX) en los linfocitos infiltrantes.

---

#### NIVEL III: Constantes Biofísicas e Inmutables del Hardware Celular
* **Potencial de Membrana Somático Sano ($V_m$):** $-70.0\text{ a }-90.0\text{ mV}$ (hiperpolarizado, quiescente).
* **Potencial de Membrana Tumoral ($V_m$):** $\sim -15.0\text{ mV}$ (despolarizado, mitótico).
* **Consumo Energético del Gradiente Iónico:** Las células dedican aproximadamente **$1/3$ de su presupuesto total de ATP** a mantener los gradientes iónicos de membrana, lo que refleja su jerarquía como reservorio de información.
* **Fidelidad Replicativa de la ADN Polimerasa:** Tasa de error basal de $10^{-7}$ por base.
* **Umbral de Barrera Intestinal:** Resistencia TEER nominal de $1000.0\ \Omega\cdot\text{cm}^2$ y nivel de LPS en plasma $\le 50.0\text{ pg/mL}$.
* **Resistencia Ácida Estromal:** $pH_e \approx 6.20 - 6.50$.
* **Cinética Alostérica de PFK-1:** $pK_a = 6.60$, coeficiente de Hill $n = 4.0$.

---

#### NIVEL IV: Red de Dependencias Normativas y Conexión Multiescala
El sistema conecta los eventos locales y sistémicos en un bucle cerrado no lineal:
1. **Paso Sistémico:** La pérdida de *Akkermansia* en el colon causa *Leaky Gut* $\rightarrow$ Aumento de LPS en la vena porta $\rightarrow$ Secreción de IL-6 por hepatocitos y células de Kupffer.
2. **Paso Tumoral:** IL-6 une el receptor GP130 $\rightarrow$ Activación de STAT3 $\rightarrow$ Hiperexpresión de PD-L1 ($>1200\times$) $\rightarrow$ Invasión por Transición Epitelio-Mesenquimal (EMT).
3. **Paso Inmune Biofísico:** La célula T entra al estroma tumoral ácido ($pH_e = 6.20$) $\rightarrow$ Entran protones al citosol $\rightarrow$ Apagón de la PFK-1 $\rightarrow$ Depletación del ATP celular ($<0.10\%$) $\rightarrow$ Parálisis de los motores de exocitosis (kinesinas/miosinas) $\rightarrow$ Extinción de la degranulación lítica.
4. **La Trampa Bioeléctrica del Ácido:** Intentar hiperpolarizar la célula T ($V_m = -75\text{ mV}$) mediante optogenética en medio de un microambiente ácido ($pH_e = 6.20$) genera una fuerza electromotriz que succiona protones al citosol, agotando el ATP al **1.07%** por el esfuerzo de extrusión. **Por ello, la amortiguación del pH estromal (o el escudo iónico NHE1-Shield) es un requisito físico obligatorio antes de la estimulación bioeléctrica.**

---

#### NIVEL V: Arnés de Verificación e Suite de Simulación *In Silico*
Todos los componentes de esta Placa Base se encuentran codificados y verificados dinámicamente en el entorno de ejecución mediante scripts en Python y consolas web:
* `simulador_onco_homeostasis_v6.py`: Motor multiescala unificado del microambiente y eje hepático.
* `simulador_limites_vacunas_arn_v1.py`: Resolución de la cinética de PFK-1 y colapsos energéticos.
* `simulador_poblacional_vacunas_arn.py`: Cohorte estocástica ($N=100$) que demuestra el umbral de eubiosis del 89.9%.
* `simulador_normalizacion_bioelectrica.py`: Modelo biofísico de reprogramación de $V_m$ y conexinas.
* `simulador_normalizacion_acidez_acoplado.py`: Acoplamiento entre hiperpolarización optogenética y resistencia por acidez estromal.
* `bio_game_ipd_ms_simulator.py`: Motor espacial $20 \times 20$ de jugadores de autoescala (Shreesha, Pigozzi, Goldstein, & Levin, IEEE Trans. 2025) acoplado a la biofísica de conexinas.
* `web-mvp/`: Consola interactiva en tiempo real con telemetría multiescala, simulador espacial y conector bioeléctrico.
* `guanes-health-in-silico-manuscript.pdf`: Manuscrito científico formal compilado con las ecuaciones y figuras del sistema.

---

### Declaración Metodológica de Cierre

Esta **Placa Base de Lógica v6.0** constituye exclusivamente una plataforma de simulación matemática y abstracción de ingeniería de sistemas *in silico*. Sirve como herramienta de cribado de hipótesis y análisis de consistencia lógica bajo supuestos explícitos, distinguiéndose de manera absoluta de cualquier protocolo clínico o recomendación médica directa.
