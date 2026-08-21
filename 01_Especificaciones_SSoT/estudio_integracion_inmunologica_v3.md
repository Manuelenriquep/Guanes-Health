# ESTUDIO DE INTEGRACIÓN FISIOLÓGICA: ACOPLAMIENTO INMUNE-METABÓLICO EN EL MICROAMBIENTE HEPÁTICO Y ONCO-VIROLÓGICO (v3.0)
**DOCUMENTO DE ESPECIFICACIÓN Y MODELADO MULTIESCALA (SSoT operativo)**  
*Guanes Health — investigación in silico*  
**Estado:** Activo (hipótesis + Capa B)  
**Complementa:** `placa_base_instrumento_investigacion.md`, `literatura_referencia.md`  
**Código canónico:** `03_Motor_Oncologico/simulador_hepatocito_infeccion.py`  
**Acoplamiento onco:** `03_Motor_Oncologico/simulador_onco_hepatico_v1.py`  
**Batería:** `04_Bateria_Inviolable/test_simulador_hepatocito.py`, `test_simulador_onco_hepatico.py`

| Capa | Contenido aquí |
|------|----------------|
| **A** | Biología de fondo (NTCP/HBV, IL-6, zonación, pHe, GSH) citada de literatura |
| **B** | Umbrales y cinéticas del toy model (O2→NTCP, Hill IL-6, Ki Myrcludex, veto GSH) |
| **C** | Abierto: calibración empírica; feedback hepatocito→tumor |

La “placa” en este documento es **instrumento de investigación**, no ontología celular.  
Declaración: cribado de hipótesis in silico — no consejo médico ni evidencia clínica.

---

## I. INTRODUCCIÓN Y ENFOQUE METODOLÓGICO: LA RED MULTIESCALA DE RESTRICCIONES

El modelado *in silico* de patología requiere ordenar **restricciones biofísicas, leyes de conservación y transiciones de estado** delimitadas por el microambiente [71, 92]. La célula no se trata aquí como compuerta binaria, sino como nodo metabólico/electroquímico embebido en un ecosistema tridimensional [86].

Este estudio formaliza la **integración fisiológica v3.0** (instrumento de placa): unifica el modelo metabólico del hepatocito (v1.0) [92], la cinética de NTCP (SLC10A1) [124, 255] y el control estocástico del microambiente inmunitario (v2.0) [71]. Sirve para explorar hipótesis sobre infección por HBV y progresión hacia HCC bajo inflamación [124] — siempre como **modelo**, no como validación wet-lab.

---

## II. LA PLACA DE REGULACIÓN DE LA CÉLULA PARENQUIMATOSA (HEPATOCITO SANO v1.0)

El hepatocito se comporta como un sistema multitarea de control de flujos gobernado por restricciones termodinámicas e invariantes de óxido-reducción [92]. Su funcionamiento se estructura en reglas condicionales acopladas a la localización anatómica sinusoidal [100].

### A. Metabolismo y Zonación Kelseniana (La Norma Suprema del Oxígeno)
La "Norma Suprema" (Grundnorm) que determina la heterogeneidad fenotípica del hepatocito es el **gradiente tridimensional de presión parcial de oxígeno ($pO_2$) a lo largo del sinusoide hepático** [100]:
*   **Zona 1 (Periportal, Oxigenada - $pO_2 \approx 60\text{ a }65\text{ mmHg}$)**: La abundancia de oxígeno controla la tasa de fosforilación oxidativa mitocondrial para sostener procesos biosintéticos de alta demanda energética [101]. Aquí se prioriza y cataliza la **gluconeogénesis**, la **beta-oxidación de ácidos grasos** para la síntesis masiva de ATP, y el **ciclo de la urea** de alta capacidad [101]. Molecularmente, esta zona mantiene apagada la señalización Wnt, permitiendo la activación de la vía YAP y el supresor tumoral APC [101].
*   **Zona 3 (Pericentral, Hipóxica - $pO_2 \approx 30\text{ a }35\text{ mmHg}$)**: La norma metabólica cambia hacia rutas de menor demanda de ATP o de carácter anabólico reductor [102]. Se prioriza la **glucólisis**, la **lipogénesis de novo** y la desintoxicación masiva a través de isoformas del Citocromo P450, principalmente **CYP2E1** [102]. Este perfil es regulado por la activación constitutiva de la vía Wnt/$\beta$-catenina [102].
*   **Estado de Excepción (Isquemia - $pO_2 < 20\text{ mmHg}$)**: Ante shocks hipovolémicos o interrupciones del flujo sinusoidal, se suspende la zonación normal [102]. El hepatocito deprime las rutas biosintéticas de alto costo (síntesis de albúmina, urea y gluconeogénesis) para estabilizar de forma generalizada a **HIF-1α**, forzando la transición a una glucólisis anaerobia de supervivencia [103]. Si la presión parcial desciende por debajo de las 10 mmHg de forma prolongada, el nodo celular pericentral entra en **necrosis isquémica centrolobulillar** por deplesión catastrófica de ATP [103, 104].

### B. Homeostasis de Sales Biliares y el Receptor NTCP (SLC10A1)
La homeostasis del aclaramiento biliar es una prioridad fisiológica del hepatocito para evitar la toxicidad por detergentes lipídicos [225]. 
*   **Captación Basolateral**: El transportador transmembrana **NTCP (SLC10A1)**, localizado exclusivamente en la membrana basolateral (sinusoidal) del hepatocito, utiliza el potencial electroquímico generado por la bomba Na+/K+ ATPasa para cotransportar de forma activa sales biliares conjugadas con una estequiometría de **2 $Na^+$ por cada molécula de taurocolato** [258]. Este sistema es responsable de más del 80% de la captación de ácidos biliares en primer paso circulatorio [258].
*   **Excreción Apical (Canalicular)**: Los ácidos biliares conjugados intracitoplasmáticos son activamente exportados al canalículo biliar contra gradientes de concentración masivos mediante la bomba **BSEP (ABCB11)** y el transportador **MRP2**, un proceso termodinámicamente desfavorable acoplado directamente al consumo de ATP [258].
*   **La Restricción de Polaridad Celular**: La correcta translocación de transportadores sinusoidal (NTCP) a la cara basolateral y de exportadores (BSEP) a la apical es un inmutable estructural dependiente de la actina y de un anillo ininterrumpido de uniones herméticas (**ZO-1, ocludina y claudina-1**) [98]. La deslocalización de estos componentes anula de inmediato la viabilidad polar de la placa biliar [98].

### C. Desintoxicación Acoplada y Apoptosis Fail-Closed (Veto Redox de NAPQI)
El procesamiento de xenobióticos lipofílicos nocivos (como el paracetamol) en el retículo endoplásmico liso exige la sincronía obligatoria entre las reacciones de Fase I y Fase II [95]:
*   **Fase I ( CYP2E1 / CYP3A4)**: Oxida el compuesto original generando un intermediario electrofílico altamente reactivo y de elevada energía libre de Gibbs, la *N-acetil-p-benzoquinona imina* (**NAPQI**) [95].
*   **Fase II (Glutatión S-Transferasa - GST / UGT)**: Conjuga de manera inmediata al NAPQI con el antioxidante citoplasmático **glutatión reducido (GSH)** para neutralizar su electrofilia y facilitar su excreción hidrofílica [95].
*   **Mecanismo de Exclusión (Veto de NAPQI Libre - FC-BIO-HEP-01)**: El pool nominal de GSH oscila entre **5.0 a 10.0 mM** [99]. Si debido a una sobredosis de xenobióticos o ayuno extremo, el pool de GSH desciende por debajo de un umbral crítico del **30% de su valor nominal**, se veta de forma absoluta la Fase I para detener la producción de NAPQI libre [97]. De forma simultánea y determinista, el sistema celular ejecuta la **permeabilización de la membrana mitocondrial externa (MOMP)**, induciendo la liberación de Citocromo c al citosol para activar la apoptosis por caspasas [97]. Este apagado *fail-closed* previene el daño oxidativo generalizado de membranas que culminaría en lisis lítica desordenada, necrosis celular y liberación descontrolada de DAMPs inflamatorios al parénquima [97].

---

## III. LA PLACA DE CONTROL ESTOCÁSTICO DEL MICROAMBIENTE (INMUNOLOGÍA CELULAR v2.0)

El sistema inmunitario no opera de forma homogénea ni como un interruptor binario; constituye un sistema adaptativo complejo regulado por constantes fisicoquímicas, balances metabólicos y afinidades competitivas [71].

### A. La Sinapsis Inmunológica y la Exclusión por Escudo Ácido (Veto de pH)
*   **Compuerta de Activación CD8+ (Nivel 1.1)**: La activación y el desencadenamiento de la lisis celular por parte de un linfocito T CD8+ efector requiere la coincidencia estricta de una señal antigénica específica (unión TCR al complejo MHC-I/Antígeno en la diana) [72], una coestimulación positiva (CD28 acoplado a CD80/CD86 de la APC) [73] y la **ausencia** de señales de veto mediadas por checkpoints co-inhibitorios como el eje **PD-1/PD-L1 o CTLA-4** [73].
*   **El Veto Lógico por Acidosis Extrema (Nivel 2.1)**: Aunque se cumpla la firma multifactorial de activación, la desgranulación citotóxica y la liberación exocítica de perforinas y granzimas por los TILs CD8+ queda **absolutamente excluida si el pH del estroma extracelular local ($pHe$) desciende a niveles $\le 6.50$** [77].
*   **Mecanismo Biofísico del Veto**: La alta concentración de protones libres ($H^+$) en el microambiente acidificado por el eflujo del tumor (vía glucólisis/MCT4) altera la carga de superficie del linfocito, paraliza los filamentos de actina requeridos para la degranulación y desestabiliza electroquímicamente los gradientes iónicos transmembrana necesarios para la entrada de calcio adaptativa [78]. El sistema transiciona a un estado de parálisis funcional de seguridad (*fail-closed*) para evitar la toxicidad descontrolada sobre el estroma normal [78].

### B. Plasticidad y Polarización de Macrófagos (Competencia iNOS / Arginasa-1 por Arginina)
*   **Polarización M1 (Activación Clásica)**: En presencia de un microambiente con concentraciones de lactato extracelular normales ($< 2.0\text{ mM}$) e interferón gamma (IFN-γ), los macrófagos adoptan el fenotipo proinflamatorio y antitumoral M1, potenciando la lisis celular y la presentación antigénica [74].
*   **Polarización M2 (Activación Alternativa)**: Si la concentración de lactato extracelular supera el umbral crítico de **$10.0\text{ mM}$** (acumulación inducida por el Efecto Warburg tumoral) acoplada a IL-4/IL-13, el macrófago transiciona de forma determinista al fenotipo inmunosupresor M2 [74]. Los macrófagos M2 remodelan la matriz extracelular, promueven la neoangiogénesis y silencian la inmunidad adaptativa lítica [74].
*   **Exclusión de Coexistencia Fenotípica (M1/M2 - Nivel 2.2)**: La expresión simultánea de perfiles M1 y M2 funcionales en el mismo macrófago está excluida debido a que las enzimas marcadoras de cada estado—la sintasa de óxido nítrico inducible (**iNOS**, perfil M1) y la **Arginasa-1** (perfil M2)— **compiten de forma excluyente por el mismo sustrato limitante: el aminoácido L-arginina** [79]. El consumo por una vía priva estequiométricamente de sustrato a la otra, forzando la diferenciación hacia estados fenotípicos discretos para evitar cortocircuitos metabólicos [79].

### C. El Bucle de Agotamiento de Células T CD8+ (TOX y Anestesia Metabólica)
*   **Activación del Fusible de Exhaustion (Nivel 1.3)**: Sometidos a una exposición crónica, tónica y persistente a antígenos específicos combinada con la unión alostérica persistente del eje PD-1/PD-L1 [75], los linfocitos T CD8+ activan de forma irreversible la transcripción del factor regulador **TOX** [75].
*   **Consecuencia Celular**: TOX induce una remodelación epigenética profunda que degrada progresivamente la capacidad bioenergética y la masa mitocondrial del linfocito [75]. Se atenúa de manera irreversible la secreción de interleucina-2 (IL-2) y de IFN-γ, disminuyendo de forma tónica la fuerza citotóxica lítica [75]. Este es un fusible bioquímico evolutivo diseñado para limitar la autoinmunidad masiva, pero secuestrado por el nicho tumoral para consolidar su camuflaje local [75].

### D. El Reclutamiento Competitivo de Tregs y Secuestro de IL-2 (CD25)
*   **Compuerta de Tolerancia Treg (Nivel 1.4)**: Cuando la concentración local de citoquinas inmunosupresoras como el **TGF-β** y la **IL-10** en la matriz supera el umbral del estroma, se activa la transcripción nuclear de **FoxP3** en células T CD4+ vírgenes, reprogramándolas hacia el linaje de células T reguladoras (Tregs) activas [76].
*   **Exclusión de Autonomía Inmune (Nivel 2.3)**: El linfocito T CD8+ efector tiene prohibida la proliferación clonal exponencial o el mantenimiento de su capacidad lítica en ausencia de **interleucina-2 (IL-2)** [80].
*   **El Mecanismo de Secuestro**: Las Tregs sobreexpresan de manera constitutiva la subunidad alfa del receptor de IL-2 de alta afinidad (**CD25**), actuando como un sumidero competitivo que **secuestra y absorbe físicamente la IL-2 disponible en el microambiente** [76, 80]. Al depletarse la IL-2, las células T CD8+ efectoras interrumpen su progresión en la fase G1 del ciclo celular, induciendo tolerancia clonal periférica [80].

---

## IV. INTERFAZ DE ACOPLAMIENTO Y VIROLOGÍA HEPÁTICA (HBV / IL-6 / MYRCLUDEX B)

La interacción entre el parénquima hepático y la matriz inmunitaria en el contexto de la infección viral por HBV describe dinámicas de competencia estequiométrica y regulación hormonal cruzada:

### A. Cinética de Entrada de HBV y Determinantes de NTCP (KGIVISLVL-158)
El virus de la Hepatitis B (HBV) y su satélite de ARN, el virus de la Hepatitis Delta (HDV), secuestran la función de aclaramiento fisiológico de sales biliares para ingresar al hepatocito [127, 255]:
*   **Adhesión Reversible**: En la fase inicial, los viriones se adhieren de forma reversible a los Proteoglicanos de Heparán Sulfato (HSPGs) de la membrana sinusoidal mediante el dominio determinante antigénico de la glicoproteína HBsAg de la envoltura viral [128].
*   **Unión de Alta Afinidad**: El dominio **preS1** de la proteína de superficie grande de HBV (LHB) interacciona de forma directa y con afinidad nanomolar con los residuos **157 a 165 (KGIVISLVL)** localizados en el bucle extracelular de NTCP [127, 261, 264]. Ensayos de mutación dirigida demuestran que el residuo específico en la **posición 158 de NTCP es el determinante crítico de especie** que rige la susceptibilidad de entrada del patógeno [127, 261].
*   **Superposición de Funciones**: Las coordenadas de anclaje de preS1 solapan físicamente con los bolsillos de unión de los ácidos biliares (determinados por los residuos N262 y Q293/L294) [127, 261]. En consecuencia, variantes naturales no funcionales en el transporte de sales biliares, como el polimorfismo **S267F**, resultan completamente refractarias y resistentes a la entrada viral [127, 261].

### B. Supresión Inflamatoria de NTCP Mediada por IL-6 e IL-1β (Vía JNK / HNF-1α / HNF-4α)
La activación de los receptores de reconocimiento de patrones innatos (PRRs, como TLRs o NLRs citoplasmáticos) en macrófagos y células de Kupffer locales induce el ensamblaje del inflamasoma y la secreción paracrina de citoquinas proinflamatorias [87, 271]:
*   **La Vía JNK de Represión Transcripcional**: La unión de la interleucina-6 (**IL-6**) a su receptor en el hepatocito activa la cascada de la citoquina-quinasa e induce la fosforilación de la quinasa transductora **c-Jun N-terminal (JNK)** [271].
*   **Supresión de Factores Hepatocitarios**: JNK activo suprime directamente la transcripción y capacidad de unión nuclear de los factores enriquecidos en hígado **HNF-1α y HNF-4α**, los cuales son transactivadores esenciales del promotor del gen *SLC10A1* de NTCP [266, 271]. Esta cascada induce una **reducción de hasta el 98% en los niveles de ARNm de NTCP** en PHH y células HepaRG expuestas a IL-6 [271].
*   **Acoplamiento de IL-1β**: Simultáneamente, la interleucina-1β (**IL-1β**) actúa de manera sinérgica, deprimiendo el promotor de NTCP mediante la inactivación JNK-dependiente del complejo receptor heterodimérico **RAR/RXR** [271].
*   **Hipótesis de Defensa Innata**: Esta represión masiva funciona en la homeostasis hepática como un mecanismo de contención o *firewall* fisiológico innato: ante la inflamación aguda de un foco de infección, el sistema inmunológico local silencia la expresión basolateral de NTCP para proteger a los hepatocitos sanos adyacentes de la entrada y propagación de nuevos viriones *de novo* [255, 271, 279].

### C. Bloqueo Competitivo Farmacológico: Myrcludex B y Riesgos de Colestasis Mitocondrial
*   **Mecanismo de Myrcludex B (Hepcludex)**: Es un lipopéptido sintético N-acetilado de 47 aminoácidos que mimetiza la región preS1 de LHB de HBV [130, 277]. Compite de manera directa y estéreo-específica con los viriones por los residuos 157-165 de NTCP basolateral, impidiendo de forma total la adhesión del virus [277].
*   **Diferencial de Selectividad**: Myrcludex B exhibe una afinidad ultra-alta por el receptor, de modo que la concentración requerida para inhibir de forma absoluta la entrada viral es **100 veces menor** que la dosis necesaria para bloquear el transporte fisiológico de sales biliares conjugadas [130, 277].
*   **El Límite Termodinámico y Riesgo de Colestasis**: Si la dosificación farmacológica supera este umbral terapéutico y bloquea de manera prolongada el transporte de Na+/taurocolato basolateral [277], el flujo portal de ácidos biliares se detiene, interrumpiendo la circulación enterohepática [258, 259]. 
*   **Daño Mitocondrial por Detergente**: La colestasis intrahepática resultante provoca la retención citoplasmática de sales biliares, cuyas propiedades tensioactivas anfipáticas desestructuran la membrana mitocondrial, desacoplan la cadena de transporte de electrones, liberan proteasas (cathepsina B) e inducen la apoptosis del hepatocito sano, comprometiendo la viabilidad funcional de la placa tisular [225, 259, 280].

### D. Integración Divergente de la Glutamina (JHU083) y Reprogramación Epigenética (TET2)
*   **Efecto Divergente JHU083 (Nivel 4.1)**: La administración del antagonista metabólico JHU083 actúa como un interruptor selectivo en el estroma [82]. Al bloquear competitivamente el consumo de glutamina, el tumor (con alta demanda para su biomasa) colapsa energéticamente, reduciendo drásticamente su producción de lactato (MCT4) y aliviando la acidosis y la hipoxia estromal [83]. Simultáneamente, las células T CD8+ efectoras muestran resiliencia metabólica, redirigiendo su perfil metabólico hacia la fosforilación oxidativa mitocondrial para adquirir un fenotipo de memoria inmunológica de larga vida y resistente al agotamiento por TOX [83].
*   **Reprogramación por TET2 (Nivel 4.2)**: En condiciones de hipoxia severa ($pO_2 < 5\text{ mmHg}$), la interacción del factor de transcripción NF-κB acoplada a la enzima desmetilasa **TET2** anula la impronta inmunosupresora local, permitiendo reprogramar epigenéticamente a macrófagos específicos (TAMs) hacia un perfil antitumoral e inflamatorio M1 activo dentro de nichos tradicionalmente tolerogénicos [84].

---

## V. CASOS DE SIMULACIÓN Y EXPANSIÓN DEL MODELO IN SILICO

El módulo canónico ya vive en el motor (no duplicar lógica en este markdown):

- Código hepatocito: `03_Motor_Oncologico/simulador_hepatocito_infeccion.py`
- Acoplamiento Cohorte C ↔ hepatocito: `03_Motor_Oncologico/simulador_onco_hepatico_v1.py`
- Tests: `04_Bateria_Inviolable/test_simulador_hepatocito.py`, `test_simulador_onco_hepatico.py`
- Pipeline: incluido en `04_Bateria_Inviolable/run_tests_pipeline.py`

### Parámetros Capa B congelados en batería

| Símbolo / regla | Valor en modelo | Notas |
|-----------------|-----------------|-------|
| Zonación NTCP basal | isquemia 0.2 / Z3 0.8 / Z1 1.2 | umbrales pO2 20 y 35 mmHg |
| Hill IL-6 | techo 0.98, K=50 pg/mL | `NTCP = basal * (1 - 0.98 * IL6/(IL6+50))` |
| Ki Myrcludex viral / biliar | 1 nM / 100 nM | fracción `1/(1+C/Ki)` |
| Umbral aclaramiento biliar | **0.15** | por debajo → depleción GSH 0.5 mM por unidad de tiempo |
| VETO FC-BIO-HEP-01 | GSH < 30% nominal | viabilidad → 0 |
| VETO FC-BIO-2.1 | pHe ≤ 6.50 | lisis CD8 = 0 |
| Escenarios 72 h | Control / IL-6 100 / Myrcludex 10 nM / 1000 nM | paso 0.5 h |

### Expansión abierta (Capa C)

| Ítem | Estado |
|------|--------|
| Acoplamiento unidireccional Cohorte C → hepatocito HBV | **Cerrado (Capa B)** — `03_Motor_Oncologico/simulador_onco_hepatico_v1.py` |
| Feedback hepatocito→tumor (IL-6/DAMPs alteran estroma) | **UNRESOLVED** |
| Calibración empírica de constantes | **UNRESOLVED** |

---

## VI. DECLARACIÓN FINAL

“Esto es cribado de hipótesis in silico sobre instrumentos de placa; no es consejo médico ni evidencia clínica.”

---
*Fin del Estudio de Integración Fisiológica v3.0. Referencia operativa para el pipeline de Guanes Health.*
