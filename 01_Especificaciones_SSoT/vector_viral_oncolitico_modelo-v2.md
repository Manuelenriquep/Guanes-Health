# MODELADO BIOFÍSICO Y MULTIESCALA: VECTOR VIRAL ONCOLÍTICO AUTO-DIRIGIDO (vOnco-Logic-v2)
**DOCUMENTO DE ESPECIFICACIÓN TÉCNICA E INGENIERÍA DE SISTEMAS IN SILICO**  
**PARADIGMA:** Restricciones Lógicas Aplicadas a Sistemas Estocásticos Complejos  
**CODENAME:** *vOnco-Logic-v2 / Estocastic-Sovereign*  

---

## 1. INTRODUCCIÓN Y ENFOQUE METODOLÓGICO: EL PARADIGMA DE RESTRICCIONES LÓGICAS

El presente documento técnico redefine la arquitectura de control del vector viral oncolítico modificado (*vOnco-Logic-v2*) [8, 95]. En la fase de concepción de sistemas complejos, la **Placa Base de Lógica** es un **instrumento de investigación** (véase `placa_base_instrumento_investigacion.md`): un artefacto para ordenar restricciones, estados y fallos de forma inspectable. La analogía pedagógica “célula ↔ placa” / “cáncer ↔ malware” [6, 95] puede usarse para síntesis conceptual, **pero no afirma identidad ontológica**. Desde el rigor de la biología de sistemas computacional, el modelo es una abstracción conceptual *in silico* [95, 96].

La biología celular real no está gobernada por circuitos lógicos binarios deterministas o compuertas digitales de silicio cerradas. Por el contrario, los sistemas vivos operan en un entorno intrínsecamente estocástico, ruidoso, redundante y dotado de una elevada plasticidad fenotípica [95, 96]. Las cascadas de señalización intracelular, la transcripción genética y las transiciones metabólicas están sujetas a fluctuaciones de ruido térmico, tasas de probabilidad de unión ligando-receptor y redundancia funcional de rutas alternativas [95, 96].

En consecuencia, el motor de simulación en Python no pretende imponer de manera física compuertas lógicas digitales rígidas dentro de la célula viva [95, 96]. El propósito de nuestro modelado *in silico* es formalizar un **modelo de restricciones lógicas y transiciones de estado biológico bajo condiciones de frontera** —útil para generar y cribar hipótesis, no para sustituir la biología ni el wet-lab. Dichas fronteras están dictadas por leyes de conservación física, gradientes electroquímicos de pH, flujos cinéticos de transporte y límites termodinámicos moleculares parametrizados [1, 2, 5].

---

## 2. EVALUACIÓN Y VALIDACIÓN CIENTÍFICA (HALLMARKS OF CANCER EN REDES ESTOCÁSTICAS)

Para dotar al simulador *in silico* de la máxima fidelidad predictiva, se han mapeado y parametrizado los mecanismos clásicos del desarrollo tumoral (*Hallmarks of Cancer*) mediante constantes cuantitativas extraídas de la literatura molecular estándar [95, 96]:

### A. Secuestro de la Apoptosis (Bypass de la Muerte Celular Programada)
*   **Mecanismo Fisiológico**: La proteína p53 actúa como el auditor de integridad genómica de la célula [5, 47]. Ante daños irreparables detectados en transiciones de ciclo celular (vía cinasas sensoras ATM/ATR) [5], p53 detiene la copia nucleotídica (regulando la expresión de p21/WAF1) [5] o, en última instancia, induce la permeabilización de la membrana mitocondrial externa (MOMP) para iniciar la apoptosis [1, 5, 6].
*   **Sabotaje Neoplásico**: El tumor anula este veto mediante mutaciones de sentido erróneo en el dominio de unión al ADN de p53 (principalmente en los residuos calientes o *hotspots* R175, R248 y R273) [48] o hiper-regulando la ligasa de ubiquitina E3 MDM2 [48] para su degradación proteasómica. Adicionalmente, la **sobreexpresión constitutiva (con factores de hasta x25) de proteínas antiapoptóticas como BCL-2 y BCL-xL** actúa como un "tapón molecular" hidrofóbico [1, 3]. Datos cristalo-gráficos de alta resolución (2.3–2.7 Å) confirman que p53-DBD normalmente compite por los bolsillos hidrofóbicos BH3 de estas proteínas [1]. Al estar saturados estos bolsillos por el exceso de BCL-2, se bloquea mecánicamente la capacidad de las proteínas efectoras Bax y Bak para oligomerizarse y formar los macro-poros mitocondriales, suspendiendo la liberación de Citocromo c al citosol [1, 48].

### B. Evasión del Límite de Hayflick (Inmortalidad Replicativa)
*   **Mecanismo Fisiológico**: Las células somáticas sanas carecen de niveles significativos de telomerasa activa, lo que restringe su ciclo de duplicación mitótica a un máximo de aproximadamente 50–70 generaciones (Límite de Hayflick) debido al desgaste progresivo de los telómeros por debajo de 4000 pb [6].
*   **Sabotaje Neoplásico**: Para vencer esta restricción, el clon tumoral adquiere mutaciones puntuales recurrentes en la región promotora del gen de la transcriptasa inversa de la telomerasa (**hTERT**), específicamente en las coordenadas **-124 G>A (C228T) y -146 G>A (C250T)** con respecto al codón de inicio de traducción [1]. Estas transiciones de un solo nucleótido generan de manera aberrante el motivo consenso de novo **5'-GGAA-3'** [1]. Este motivo funciona como un sitio de anclaje de alta afinidad para factores de transcripción de la familia ETS, en particular el complejo heterotetramérico GABP (GABPA2B1L2) [1]. Ensayos de cambio de movilidad electroforética (EMSA) demuestran que la subunidad GABPB1L se une al promotor mutado con una **afinidad cuantitativa aproximadamente 2 veces mayor (2x) respecto al promotor de tipo silvestre** [1]. Esto promueve activamente la remodelación de la cromatina circundante por reclutamiento de histona acetiltransferasas (con un aumento correspondiente en H3K9ac e hipometilación del promotor), forzando una de-represión transcripcional constitutiva del gen hTERT que mantiene de forma aberrante la longitud telomérica constante (establecida en el simulador en un promedio de 99 pb frente al umbral crítico de senescencia de 10 pb) [1, 4].

### C. Reprogramación Metabólica y Extrusión de Ácido Láctico (Efecto Warburg)
*   **Mecanismo Fisiológico**: El metabolismo somático sano prioriza la fosforilación oxidativa mitocondrial para obtener una eficiencia energética neta de aproximadamente 36 ATP por glucosa [49].
*   **Sabotaje Neoplásico**: El tumor reconfigura su bioenergética hacia la glucólisis aeróbica, aumentando la absorción de glucosa de **10 a 100 veces** respecto a los tejidos sanos mediante la hiper-regulación del transportador de glucosa de alta afinidad **GLUT1** y el reclutamiento de la isoforma lenta de la piruvato quinasa **PKM2** (lo que ralentiza el flujo del ciclo de Krebs para desviar carbonos intermediarios hacia rutas anabólicas de síntesis de biomasa) [2, 49]. Para evitar una acidosis láctica intracelular citotóxica derivada de esta inmensa tasa glucolítica, las células tumorales sobreexpresan de manera constitutiva transportadores acoplados a protones especializados en monocarboxilatos [2]:
    *   **MCT1 (SLC16A1)**: Transloca L-lactato de manera bidireccional con una afinidad moderada (\\(K_m \approx 3.5 - 5.0\text{ mM}\\)) [2].
    *   **MCT4 (SLC16A3)**: Bajo la estabilización de HIF-1α en condiciones de hipoxia severa, este transportador se hiper-regula constituyendo una vía de extrusión ácida de baja afinidad pero de **muy alta capacidad de flujo de L-lactato** (con un rango histórico de \\(K_m \approx 15 - 30\text{ mM}\\), reduciéndose a valores dinámicos efectivos de \\(K_m \approx 1.7 - 5.0\text{ mM}\\) medidos por biosensores FRET) [2].
*   **Consecuencia Biofísica**: El bombeo continuo de protones y lactato al intersticio reduce el **pH del microambiente extracelular (pHe) a un rango altamente acidificado de 6.20 a 6.80** [2]. Esta acidez local actúa como un aislante bioeléctrico que inhibe la despolarización y señalización celular del receptor de células T (TCR) en los linfocitos infiltrantes de tumores (TILs CD8+) [2, 54]. Asimismo, destruye la matriz extracelular para facilitar la invasión celular, mientras que mantiene el pH intracelular tumoral (pHi) estable y neutro en 7.20 [2].

### D. Angiogénesis e Hipoxia (Eje HIF-1α/VEGF)
*   **Mecanismo Fisiológico**: En condiciones normóxicas normales, la subunidad del factor de transcripción HIF-1α es constantemente hidroxilada por proli-hidroxilasas (PHD) utilizando oxígeno celular, marcándola para el reconocimiento del complejo de ubiquitina ligasa de Von Hippel-Lindau (VHL) y su subsecuente destrucción proteasómica [2, 52].
*   **Sabotaje Neoplásico**: Cuando el volumen tumoral supera la barrera de difusión pasiva de oxígeno (1-2 mm), se genera hipoxia tisular severa (saturación de \\(\text{O}_2 < 5\%\\)) [2, 51]. La ausencia de oxígeno celular inactiva las PHDs, bloqueando el reconocimiento por VHL y estabilizando a HIF-1α [2, 52]. HIF-1α se acumula, se transloca al núcleo, dimeriza con HIF-1β y se une de manera física a los Elementos de Respuesta a Hipoxia (HRE) en los promotores de genes diana [2, 52]. Esto induce la transcripción y secreción masiva de factores angiogénicos como el **VEGF (Factor de Crecimiento Endotelial Vascular)**, el cual estimula a los receptores endoteliales VEGFR locales para forzar la neovascularización desorganizada del lecho tumoral [52].

### E. Invasión y Evasión Inmunitaria (Eje PD-L1/EMT)
*   **Ruptura del Control Social**: Las células tumorales activan programas transcripcionales aberrantes regulados por los factores Snail, Slug y Twist, los cuales **suprimen la expresión celular de la molécula de adhesión E-cadherina** [53]. La pérdida de esta proteína de pegamento intercelular provoca la Transición Epitelio-Mesenquimal (EMT), dotando al tumor de un fenotipo migratorio invasivo capaz de degradar el estroma mediante metaloproteinasas (MMPs) y colonizar tejidos distantes vía intravasación [53].
*   **El Escudo Inmune**: Sincronizado con la EMT, el clon neoplásico expresa de manera constitutiva en su superficie el ligando de muerte programada 1 (**PD-L1**) [53]. Al interactuar con el receptor **PD-1** de los linfocitos T CD8+ infiltrados, se transmite de manera transmembrana una señal química intracelular que desactiva de forma inmediata el potencial efector del linfocito (el "apretón de manos de la muerte"), induciendo un estado de anergia e inmunotolerancia adquirida [53].

### Justificación de las Constantes Biofísicas del Simulador
La integración cuantitativa de estos fenómenos en el simulador biofísico de *Guanes Health* utiliza variables extraídas y deducidas a partir de principios electroquímicos y cinéticos estándar [95, 96]:
1.  **Potencial de Membrana Celular (GHK)**: Calculado dinámicamente mediante la ecuación de Goldman-Hodgkin-Katz:
    \\[
    V_m = \frac{RT}{F} \ln \left( \frac{P_{K}[K^+]_o + P_{Na}[Na^+]_o + P_{Cl}[Cl^-]_i}{P_{K}[K^+]_i + P_{Na}[Na^+]_i + P_{Cl}[Cl^-]_o} \right)
    \\]
    Este modelo define que la viabilidad electroquímica óptima de las células normales oscila en un rango hiperpolarizado y seguro de \\(-70.0\text{ a } -90.0\text{ mV}\\), mientras que la despolarización forzada citotóxica por encima de \\(-15.0\text{ mV}\\) (inducida por el colapso energético de ATP) es el umbral biofísico que activa la translocación de fosfatidilserina en el proceso de apoptosis controlada [5, 6].
2.  **Cinética de Michaelis-Menten (Transbordo de Solutos)**: Las velocidades de consumo de glucosa y transporte de lactato se modelan utilizando ecuaciones cinéticas de saturación:
    \\[
    v = \frac{V_{max} \cdot [S]}{K_m + [S]}
    \\]
    donde los valores de \\(K_m\\) correspondientes a GLUT1, MCT1 y MCT4 reflejan las afinidades fisiológicas descritas en la literatura [2].
3.  **Ledger y Deplesión de ATP**: Las constantes estequiométricas asignadas en la simulación computacional (100 unidades metabólicas basales para la célula sana frente a las 10,000 unidades relativas consumidas por la hiperglucólisis y la inmortalidad replicativa del tumor) representan de forma escalar los inmensos diferenciales de flujo de energía celular real requeridos para sostener la hiperproliferación neoplásica [4].

---

## 3. ARQUITECTURA CONCEPTUAL DEL VECTOR (HIPÓTESIS DE DISEÑO — NO VALIDADA)

### 3.0 Estado epistemológico (lectura obligatoria)

Esta sección **no describe un producto terapéutico aprobado, un constructo clonado, ni un resultado experimental de Guanes Health**. Documenta una **hipótesis de diseño** trasladada y depurada desde la nota de trabajo `vector_viral_oncolitico_modelo.md` (v1, *speculative design note*).

| Capa | Qué significa | Qué se permite afirmar |
|------|---------------|------------------------|
| **A. Biología de fondo** | Hechos o mecanismos reportados en literatura independiente del proyecto | Se pueden citar como contexto científico |
| **Capa B. Hipótesis Guanes** | Combinación, gating y payload *propuestos* para el modelo in silico | Solo como *supuesto de diseño* a explorar |
| **Capa C. Abierto / no decidido** | Decisiones de ingeniería aún sin elegir | Prohibido rellenarlo con invención para “completar” el documento |
| **Capa D. Prohibido afirmar** | Eficacia clínica, seguridad humana, “validado”, “100% selectivo” | Fuera de alcance de este SSoT hasta wet-lab + regulación |

**Declaración explícita:** a la fecha de este documento, Guanes Health **no ha demostrado** entrada selectiva, expresión AND-gateada, restauración de apoptosis ni índice terapéutico del vector aquí bosquejado. El simulador puede *explorar consecuencias* de estos supuestos; **no sustituye** evidencia biológica.

---

### 3.1 Qué problema intenta resolver (sin exagerar)

El modelo tumoral de la §2 describe un estado con, entre otros: apoptosis secuestrada (p53/BCL-2), inmortalidad (hTERT mutado), hipoxia (HIF-1α) y sobreexpresión de GLUT1 (Warburg). La hipótesis de vector pregunta:

> *¿Puede un vector oncolítico (o de entrega génica con selectividad tumoral) formalizarse en el simulador como un sistema de **restricciones de entrada + restricciones de transcripción + payload de restauración apoptótica**, de modo que solo se active bajo un subconjunto de esos hallmarks?*

Esa pregunta es legítima como **programa de investigación in silico**. No es una afirmación de que ya exista tal vector funcional.

---

### 3.2 Backbone viral — NO DECIDIDO (Capa C)

**Hecho (Capa A):** existen plataformas clínicas o avanzadas de virus oncolíticos (p. ej. HSV-1 modificado tipo T-VEC, adenovirus oncolíticos, vaccinia, VSV, reovirus, etc.), cada una con perfiles distintos de tropismo natural, inmunogenicidad, capacidad de payload y regulación.

**Decisión Guanes (Capa C):** el **género/especie del backbone** (HSV-1, Ad5/Ad28, VV, VSV, otro, o vector no replicativo tipo AAV/lentiviral con capsides modificadas) **no está elegido** en este SSoT.

Razones para no inventarlo aquí:
1. La elección determina seguridad, manufactura GMP, preexistencia de anticuerpos neutralizantes y vía regulatoria.
2. Elegir un backbone “de relleno” sin criterio experimental sería **ficción técnica**, no especificación.
3. Hasta que exista una decisión documentada (con trade-off explícito), el motor in silico debe tratar el backbone como **parámetro abstracto** `backbone_id = UNRESOLVED`.

**Requisito de modelo:** cualquier simulación que invoque “vector” debe fallar de forma controlada o marcarse `hypothesis_only` si `backbone_id` permanece sin resolver, salvo que se declare explícitamente un escenario “what-if” con supuestos listados.

---

### 3.3 Hipótesis de tropismo / entrada (Capa B, anclada en biología HTLV-1 — Capa A)

#### 3.3.1 Biología de fondo (Capa A — no es invención Guanes)

La entrada de HTLV-1 en células susceptibles involucra, en la literatura, interacciones con **Neuropilina-1 (NRP-1)** y **GLUT1**, y reordenamientos de las glicoproteínas de envoltura **gp46/gp21** (incluyendo química de disulfuros y fusión mediada por gp21). NRP-1 también participa en señalización VEGF; GLUT1 está frecuentemente sobreexpresado en tumores glucolíticos. Eso **no implica** automáticamente que un virión terapéutico pseudotipado con envoltura HTLV-1 sea seguro, selectivo o fabricable.

#### 3.3.2 Hipótesis de diseño Guanes (Capa B — especulativa)

La nota v1 propone, como *supuesto de selectividad de entrada*:

1. **Pseudotipado** con complejo de envoltura tipo HTLV-1 (gp46/gp21).
2. Contacto inicial vía motivo tipo **KKPNR** (aa. 90–94 de gp46) hacia **NRP-1** (mimetismo conceptual respecto a interacciones VEGF165/NRP-1).
3. Dependencia de densidad alta de **GLUT1** para progresar a fusión (coherente con el hallazgo Warburg de la §2).
4. Isomerización de disulfuros gp46↔gp21 y proyección del péptido de fusión de **gp21** hacia la membrana del hospedador.

**Lo que esto es:** un *esquema de gating de entrada de dos factores* (NRP-1 + GLUT1) alineado con hallmarks del simulador.

**Lo que esto NO es:**
- Una demostración de que el pseudotipado funciona en un backbone terapéutico.
- Una garantía de que células normales con NRP-1 o GLUT1 fisiológico queden fuera (hay tejidos normales con ambos).
- Una licencia regulatoria: usar componentes de envoltura de un virus oncogénico humano (HTLV-1) en un producto terapéutico impone **escrutinio de seguridad, contención genética y percepción de riesgo** especialmente alto. Eso debe tratarse como **riesgo de diseño de primer orden**, no como detalle menor.

**Regla de honestidad para el simulador:** la probabilidad de entrada debe modelarse como función estocástica de densidades de receptor y ruido, **nunca** como compuerta booleana perfecta `IF NRP1 AND GLUT1 THEN infection = 1`.

---

### 3.4 Hipótesis de compuerta transcripcional AND (Capa B)

#### 3.4.1 Biología de fondo (Capa A)

- Mutaciones del promotor **hTERT** (−124/−146; C228T/C250T) y reclutamiento de factores ETS/GABP están descritas en tumores (coherente con §2.B).
- Elementos de respuesta a hipoxia (**HRE**) y dependencia de **HIF-1α** son estrategias conocidas de selectividad en terapia génica / virus oncolíticos.

#### 3.4.2 Hipótesis Guanes (Capa B)

Cassette de expresión del payload bajo control conjunto:

* **Entrada A:** promotor/enhancer sensible a estado **hTERT-mut / GABP** (inmortalidad).
* **Entrada B:** elementos **HRE** (hipoxia / HIF-1α nuclear).
* **Regla pretendida:** transcripción significativa del payload solo si **A ∧ B**.

**Límites honestos:**
- Los promotores “tumor-específicos” **fugan** (leakiness). En ingeniería real se habla de *fold-enrichment* y tasas de error, no de AND digital perfecto.
- Tumores **sin** mutación de promotor hTERT, o **normóxicos** / con HIF inestable, quedarían fuera del AND — eso es un **falso negativo terapéutico** posible, no un “feature” automático.
- Células no tumorales en hipoxia fisiológica (isquemia, herida) + cualquier activación basal del cassette = riesgo de **falso positivo** que debe cuantificarse, no negarse.

**Regla de modelo:** representar la compuerta como producto de probabilidades o tasas de transcripción \(r \propto f_A \cdot f_B\) con ruido, no como bit binario.

---

### 3.5 Hipótesis de payload de “rescate apoptótico” (Capa B)

La nota v1 propone dos componentes conceptuales. Se conservan aquí **como hipótesis**, con lenguaje desinflado (se eliminan absolutos del tipo “impide de forma absoluta”):

1. **Variante de p53 resistente a MDM2 (denominación provisional `p53-rescue`)**  
   - *Intención:* estabilizar señalización p53 frente a hiperactividad MDM2 tumoral.  
   - *Hecho de fondo:* existen mutantes/variantes de p53 con unión a MDM2 alterada descritos en literatura; **no** se fija aquí una secuencia aminoacídica propietaria “validada”.  
   - *Hueco (Capa C):* secuencia exacta, inmunogenicidad, efecto en células con p53-null vs p53-mutante dominante-negativo, y riesgo de apoptosis en tejidos sanos si hay leak del cassette.

2. **Mimético BH3 / péptido displacer de BCL-2 / BCL-xL (denominación provisional `BH3-rescue`)**  
   - *Intención:* desplazar el bloqueo antiapoptótico y favorecer oligomerización Bax/Bak → MOMP.  
   - *Hecho de fondo:* los miméticos BH3 farmacológicos (p. ej. clase venetoclax y análogos) demuestran que el eje BCL-2 es drogable; un péptido codificado por vector es **otra modalidad**, con problemas propios de expresión, plegamiento, toxicidad y entrega.  
   - *Hueco (Capa C):* secuencia del péptido, afinidad real, selectividad BCL-2 vs BCL-xL vs MCL-1, y escape tumoral si Bax/Bak están perdidos o hay dependencia de MCL-1.

**Cadena causal pretendida en el modelo (hipótesis):**  
`expresión payload` → ↑ actividad tipo p53 + ↓ bloqueo BCL-2 → ↑ probabilidad de MOMP → ↑ caspasas → colapso energético → despolarización de \(V_m\) (umbrales de la §2) → señal “eat-me” (fosfatidilserina).

**Fallos conocidos que el modelo debe contemplar (no ocultar):**
- Tumores Bax/Bak-deficientes o con bloques post-mitocondriales.
- Dominancia negativa de p53 mutante que interfiera con p53-rescue.
- Inflamación / necrosis si la muerte no es ordenada.
- Respuesta antiviral del huésped que elimine el vector antes del payload efectivo.

---

### 3.6 Controles de seguridad — REQUISITOS, no diseños inventados (Capa C)

Hasta que exista un diseño concreto revisado por expertos en bioseguridad y regulación, este SSoT **exige** (como requisitos abiertos) al menos:

1. **Kill-switch / apagado condicional** (farmacológico, recombinasa, miRNA de tejido sano, o equivalente) — *mecanismo aún no elegido*.
2. **Restricción de replicación** (si el backbone fuera replicativo): genes esenciales condicionados al AND-gate o a microambientes tumorales; si no replicativo, declarar dependencia de dosis y re-dosificación.
3. **Contención genética:** prohibición explícita de recuperar capacidad de patogénesis HTLV-1; fragmentación de envoltura; assays de RCL/RCA según plataforma.
4. **Plan de off-target:** órganos con GLUT1/NRP-1 altos; hipoxia no tumoral; toxicidad hematológica/hepática.
5. **Inmunogenicidad:** anticuerpos preexistentes, respuesta a gp46/gp21, y compatibilidad con el Kinetic Priming metabólico/inmune de la §5 (cuando se explore).

Inventar aquí una secuencia de kill-switch “completa” sin datos sería deshonesto. Por tanto: **`safety_switch_id = UNRESOLVED`**.

---

### 3.7 Relación con el motor in silico (qué sí se puede implementar ya)

Sin pretender validación biológica, el simulador **sí puede** (y debería) representar el vector como módulo de hipótesis con interfaces claras:

| Módulo | Entradas del estado celular/tumoral | Salida modelada | Estado |
|--------|--------------------------------------|-----------------|--------|
| `entry_gate` | densidades NRP-1, GLUT1, ruido | \(P(\text{entry})\) | hipótesis |
| `tx_AND_gate` | score hTERT-mut/GABP, HIF-1α | tasa de transcripción \(r\) | hipótesis |
| `payload_apoptosis` | \(r\), niveles BCL-2/xL, p53/MDM2 | \(P(\text{MOMP})\) | hipótesis |
| `backbone` | — | — | **UNRESOLVED** |
| `safety_switch` | — | — | **UNRESOLVED** |

Cualquier gráfica o cohorte que muestre “cura”, “100% selectividad” o “libre de irAEs” atribuible al vector **viola** este SSoT hasta que los módulos UNRESOLVED se cierren con evidencia y los módulos hipótesis se calibren experimentalmente.

---

### 3.8 Resumen brutalmente honesto

* **Sí hay** una hipótesis coherente con los hallmarks ya modelados: entrada NRP-1/GLUT1 + AND hTERT-mut/HIF + payload de restauración apoptótica.  
* **No hay** aún un vector Guanes caracterizado, ni backbone elegido, ni secuencias de payload/safety fijadas, ni prueba de selectividad o seguridad.  
* El valor presente de esta sección es **cerrar el hueco del título con honestidad**: nombrar la arquitectura pretendida, anclarla a biología real donde corresponda, y dejar visibles los huecos en lugar de rellenarlos por ego.

---

## 4. PRUDENCIA MÉDICA Y LIMITACIONES DEL MODELO (LÍMITES DEL MODELO Y PROTOCOLO WET-LAB)

Esta sección de **Límites del Modelo y Protocolo Wet-Lab** es de carácter obligatorio y de observancia mandatoria para todos los investigadores, ingenieros de sistemas y directores médicos asociados al ecosistema de modelado computacional [96]:

```
+---------------------------------------------------------------------------------------------------+
|                         ADVERTENCIA CLÍNICA Y DECLARACIÓN DE LÍMITES                              |
+---------------------------------------------------------------------------------------------------+
| 1. Naturaleza Abstracta: El modelo in silico "vOnco-Logic-v2" representa una simplificación       |
|    matemática y termodinámica de sistemas biológicos moleculares. Tiene un carácter estrictamente  |
|    abstracto y conceptual para la exploración diagnóstica, la generación de hipótesis de          |
|    investigación y el cribado computacional preliminar de sinergias terapéuticas.                 |
|                                                                                                   |
| 2. Restricción de Aplicabilidad Directa: Se desaconseja de manera categórica la aplicabilidad     |
|    clínica directa de las conclusiones derivadas de este simulador y el uso aislado de este       |
|    modelo para la toma de decisiones médicas o el diseño de esquemas de tratamiento en            |
|    pacientes reales sin previa validación experimental e individualización del perfil del paciente. |
|                                                                                                   |
| 3. Requisito de Validación Experimental Multi-Fase (Wet-Lab obligatorio): Todo mecanismo         |
|    lógico predicho por este modelo debe ser sometido de manera mandatoria a:                     |
|      - Fase In Vitro: Cultivos celulares tridimensionales (esferoides, organoides tumorales) y     |
|        modelos de órganos en chip (Microfluidic Tumor-on-a-Chip) bajo gradientes dinámicos reales  |
|        de pH, oxígeno y nutrientes para validar la cinética celular y la autólisis ácida.          |
|      - Fase In Vivo: Ensayos preclínicos en modelos animales (xenotransplantes en ratones         |
|        inmunodeprimidos y ratones singénicos) para caracterizar la toxicidad tisular real,         |
|        la penetración en órganos periféricos y la respuesta inmune sistémica.                      |
|      - Acoplamiento PK/PD: Integración obligatoria de la modelación farmacocinética y              |
|        farmacodinámica (PK/PD) empírica, evaluando aclaramiento renal/hepático, vida media de      |
|        los conjugados de envoltura viral, inmunogenicidad del vector e índices de penetración de     |
|        las pequeñas moléculas inhibidoras (MCT1/4, GLS1) propuestas.                              |
|                                                                                                   |
| 4. Hipótesis de vector (§3): Mientras backbone_id y safety_switch_id permanezcan UNRESOLVED,     |
|    ninguna conclusión del simulador sobre el vector puede presentarse como diseño terapéutico.     |
|    Al cerrar esos ítems, la validación deberá incluir selectividad de entrada, leakiness del AND,  |
|    off-target en tejidos GLUT1/NRP-1+, contención genética respecto a HTLV-1, y toxicidad del      |
|    payload (p53-rescue / BH3-rescue) en modelos in vitro e in vivo.                               |
+---------------------------------------------------------------------------------------------------+
```

---

## 5. PROPUESTA DE VALOR SOBERANA (MOAT COMERCIAL DE GUANES HEALTH)

La plataforma computacional *vOnco-Logic-v2* no ha sido diseñada para competir con el laboratorio húmedo tradicional (*wet-lab*) o pretender reemplazar los ensayos preclínicos físicos [95, 96]. Su posicionamiento estratégico en el sector de la oncología de precisión es el de un **Acelerador de Tesis Hipotéticas in silico**.

**Nota de coherencia con §3–§4:** los números de eficiencia, pH y reducción de espacio de búsqueda que siguen son **salidas ilustrativas del simulador bajo supuestos**, no evidencia clínica ni prueba de que el vector de la §3 exista o funcione.

### A. Reducción Radical del Espacio de Búsqueda
El diseño de terapias oncológicas combinadas convencionales se enfrenta a un problema de explosión combinatoria. Evaluar físicamente decenas de fármacos inhibidores de puntos de control inmunitario, compuestos metabólicos y vectores de terapia génica en múltiples dosis, intervalos de tiempo y secuencias temporales representa millones de dólares y años de trabajo experimental.

La plataforma *vOnco-Logic-v2* actúa como un filtro molecular de altísima velocidad:
*   Simula y evalúa grandes conjuntos de secuencias y combinaciones en tiempos computacionales cortos (el volumen exacto depende de la implementación y del hardware; no debe citarse como hecho clínico).
*   Ejemplo de predicción *in silico* (no ensayo clínico): la co-administración simultánea de inmunoterapia y terapia metabólica (Cohorte A) puede resultar ineficiente en el modelo por anergia prematura del linfocito ante acidez intersticial residual (p. ej. pH 6.40 → eficiencia CD8+ modelada ~18.5%).
*   Ejemplo de hipótesis de enrutamiento secuencial (**Kinetic Priming de la Cohorte C**): inhibidores de MCT1/4 + GLS1 a \\(T_0\\), intervalo de aclaramiento del gradiente de protones (p. ej. ~12 h hacia pHe modelado ~7.35), luego inmunoterapia a dosis reducida (p. ej. 30%). En el modelo, esto puede mejorar la eficiencia citotóxica *simulada* frente a la co-administración; **no** constituye demostración de “100% de eficacia” ni de ausencia de irAEs en humanos.
*   Cualquier cifra de “reducción del espacio de búsqueda” (p. ej. ~95% en corridas internas) es **métrica de filtrado computacional**, no validación terapéutica. Los candidatos filtrados siguen requiriendo wet-lab (§4).

### B. Arquitectura de Despliegue de Máxima Soberanía e IP Protegida
Para garantizar la confidencialidad del descubrimiento de dianas terapéuticas y la propiedad intelectual (IP) de los desarrollos moleculares, el motor de cálculo y simulación de *Guanes Health* está diseñado para operar bajo un marco de soberanía:
*   **Ejecución 100% Local (On-Premises)**: El software opera de manera nativa en servidores y clústeres locales bajo redes aisladas físicamente (**Air-Gapped**) cuando el despliegue institucional así lo requiere.
*   **Cero Dependencia de Terceros (modo soberano)**: Las simulaciones no realizan llamadas a APIs públicas, modelos de lenguaje externos basados en la nube o plataformas centralizadas de procesamiento de datos.
*   **Protección del Ledger Genómico**: Los datos de secuenciación de pacientes, las formulaciones peptídicas de los vectores y los mapas de mutaciones de las cohortes permanecen dentro de la infraestructura soberana de la institución, reduciendo el riesgo de filtraciones de datos biomédicos protegidos o pérdida de soberanía de IP frente a proveedores externos.

---
*Fin del documento de especificación técnica vOnco-Logic-v2. Hipótesis de arquitectura in silico para cribado; vector y safety switch pendientes de resolución experimental (§3).*
