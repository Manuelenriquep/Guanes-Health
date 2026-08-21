# ESTUDIO DE INTEGRACIÓN FISIOLÓGICA: ACOPLAMIENTO INMUNE-METABÓLICO EN EL MICROAMBIENTE HEPÁTICO Y ONCO-VIROLÓGICO (v3.0)
**DOCUMENTO DE ESPECIFICACIÓN CIENTÍFICA Y MODELADO MULTIESCALA DE SISTEMAS BIOLÓGICOS**  
*Guanes Health - División de Biología de Sistemas e Investigación In Silico*

---

## I. INTRODUCCIÓN Y ENFOQUE METODOLÓGICO: LA RED MULTIESCALA DE RESTRICCIONES

El modelado predictivo de la patología humana requiere trascender las descripciones fenomenológicas tradicionales para adoptar una metodología basada en **restricciones biofísicas, leyes de conservación y transiciones de estado delimitadas por el microambiente** [71, 92]. La célula humana no opera de forma aislada ni binaria; constituye un nodo metabólico y electroquímico integrado dentro de un ecosistema celular tridimensional indisoluble, donde la matriz extracelular y los fluidos intersticiales actúan como transductores mecánicos y químicos que dictan el destino fenotípico [86].

El presente estudio formaliza la **Placa de Integración Fisiológica v3.0**, unificando el modelo metabólico del parénquima hepático (Hepatocito Sano v1.0) [92], la cinética del receptor de entrada viral NTCP (SLC10A1) [124, 255] y la suite de control estocástico del microambiente inmunitario (Inmunología Celular v2.0) [71]. Este marco nos permite explorar, con rigor molecular e *in silico*, las sinergias y conflictos de viabilidad que emergen durante la infección por el virus de la Hepatitis B (HBV) y la progresión hacia el carcinoma hepatocelular (HCC) bajo presión selectiva y citoquinas inflamatorias [124].

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
*   **Mecanismo de Exclusión (Veto de NAPQI Libre - FC-BIO-HEP01)**: El pool nominal de GSH oscila entre **5.0 a 10.0 mM** [99]. Si debido a una sobredosis de xenobióticos o ayuno extremo, el pool de GSH desciende por debajo de un umbral crítico del **30% de su valor nominal**, se veta de forma absoluta la Fase I para detener la producción de NAPQI libre [97]. De forma simultánea y determinista, el sistema celular ejecuta la **permeabilización de la membrana mitocondrial externa (MOMP)**, induciendo la liberación de Citocromo c al citosol para activar la apoptosis por caspasas [97]. Este apagado *fail-closed* previene el daño oxidativo generalizado de membranas que culminaría en lisis lítica desordenada, necrosis celular y liberación descontrolada de DAMPs inflamatorios al parénquima [97].

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

## V. CASOS DE SIMULACIÓN Y SUGERENCIAS DE EXPANSIÓN DEL MODELO IN SILICO

Para trasladar de forma rigurosa la Placa Base de Lógica de la Inmunología Celular v2.0 y el módulo del Hepatocito Sano v1.0 a nuestro entorno de ejecución de Python, se propone expandir el motor canónico (`simulador_onco_homeostasis_v4.py`) para unificar la virología molecular, el aclaramiento metabólico y la inmunovigilancia.

### Propuesta de Código Unificado de Simulación Hepática e Inmune:
El siguiente módulo de expansión puede ser integrado o ejecutado de forma aislada para simular el aclaramiento viral frente a la inflamación por IL-6 y el bloqueo competitivo con Myrcludex B:

```python
import math
import numpy as np

class HepatocitoInmuneIntegrado:
    """
    Simulador multiescala del hepatocito incorporando gradiente de oxigenación,
    regulación del receptor de entrada NTCP por la vía inflamatoria de IL-6,
    bloqueo competitivo con Myrcludex B, e infección por viriones de Hepatitis B (HBV).
    """
    def __init__(self, gsh_nominal=8.0, o2_pp=60.0):
        # Constantes Biofísicas del Hepatocito (v1.0)
        self.ph_intracelular = 7.20
        self.potencial_membrana = -35.0      # mV (necesario para cotransporte Na+/taurocolato)
        self.gsh_pool = gsh_nominal          # mM
        self.gsh_nominal = gsh_nominal
        self.o2_presion_parcial = o2_pp      # mmHg (Zonación Hepática)
        
        # Parámetros del Receptor de Entrada NTCP (SLC10A1)
        self.ntcp_densidad_basal = 1.0       # Fracción nominal (1.0 = 100%)
        self.ntcp_densidad_membrana = 1.0
        self.es_variante_S267F = False       # Si True, refractario a HBV y transporte de sales
        
        # Estado de Infección Viral por HBV y Carga Antigénica
        self.carga_viral_de_novo = 0.0       # Escala lineal de viriones intracelulares
        self.mhc_i_presentacion = 1.0        # Densidad superficial para CD8+ (antígeno viral)
        self.viabilidad = 1.0                # 1.0 = sano/funcional, 0.0 = apoptosis
        
        # Variables del Microambiente e Inmunología (v2.0)
        self.il6_concentracion = 0.0         # pg/mL (Citoquina inflamatoria)
        self.lactato_extracelular = 1.5      # mM
        self.pHe = 7.40                      # pH estromal/sinusoidal
        
        # Farmacodinámica del Inhibidor de Entrada
        self.myrcludex_b_nM = 0.0            # Concentración del lipopéptido competidor
        
        # Aplicar norma de zonación inicial
        self._aplicar_norma_zonacion()

    def _aplicar_norma_zonacion(self):
        """Aplica la jerarquía normativa basada en la presión parcial de oxígeno (Nivel 4)."""
        if self.o2_presion_parcial < 20.0:
            # Estado de Excepción: Isquemia. El hepatocito deprime transportadores metabólicos
            self.ntcp_densidad_basal = 0.2
        elif self.o2_presion_parcial <= 35.0:
            # Zona 3 (Pericentral): Menor oxigenación, expresión basal estándar
            self.ntcp_densidad_basal = 0.8
        else:
            # Zona 1 (Periportal): Alta oxigenación, expresión y aclaramiento de sales biliar máximo
            self.ntcp_densidad_basal = 1.2
        self.ntcp_densidad_membrana = self.ntcp_densidad_basal

    def evaluar_regulacion_y_entrada_viral(self, inóculo_HBV, delta_t=1.0):
        """
        Ejecuta la cinética de regulación transcripcional de NTCP y simula la tasa de entrada de HBV.
        """
        if self.viabilidad <= 0.0:
            return "NODE_INACTIVE: Apoptosis o Necrosis disparada"

        # 1. Represión de NTCP mediada por IL-6 (Vía JNK dependiente) - Nivel 4.2 de Inmuno
        # IL-6 induce una caída de hasta el 98% de NTCP de forma dosis-dependiente (función de saturación de Hill)
        represion_il6 = 1.0
        if self.il6_concentracion > 0:
            represion_il6 = 1.0 - 0.98 * (self.il6_concentracion / (self.il6_concentracion + 50.0))
            
        # 2. Densidad final de NTCP en membrana sinusoidal
        self.ntcp_densidad_membrana = self.ntcp_densidad_basal * represion_il6
        
        # Si presenta el polimorfismo refractario S267F, el receptor NTCP es nulo para HBV y sales biliares
        if self.es_variante_S267F:
            self.ntcp_densidad_membrana = 0.0
            
        # 3. Competencia estequiométrica basolateral de Myrcludex B frente a HBV
        # Myrcludex B bloquea con una potencia 100 veces mayor la entrada viral que la biliar.
        # Ki viral nominal = 1.0 nM; Ki biliar nominal = 100.0 nM
        fraccion_bloqueo_viral = 1.0 / (1.0 + (self.myrcludex_b_nM / 1.0))
        fraccion_bloqueo_biliar = 1.0 / (1.0 + (self.myrcludex_b_nM / 100.0))
        
        # 4. Cinética de Infección de novo por HBV (Capa B)
        # La tasa de penetración viral depende de la densidad de NTCP disponible y de la presencia del inhibidor
        tasa_entrada = inóculo_HBV * self.ntcp_densidad_membrana * fraccion_bloqueo_viral
        self.carga_viral_de_novo += tasa_entrada * delta_t
        
        # El hepatocito procesa y presenta antígenos del HBV en el complejo MHC-I de forma directamente proporcional
        self.mhc_i_presentacion = min(10.0, 1.0 + (self.carga_viral_de_novo * 1.5))
        
        # 5. Efecto biliar y colestasis tóxica por deplesión prolongada de NTCP (Riesgo del modelo)
        # Si ntcp_densidad_membrana se bloquea fuertemente por Myrcludex B biliar (>90% de inhibición), 
        # o por colestasis, la acumulación de sales biliares daña la membrana mitocondrial
        aclaramiento_sales_biliares = self.ntcp_densidad_membrana * fraccion_bloqueo_biliar
        if aclaramiento_sales_biliares < 0.1 and not self.es_variante_S267F:
            # Pérdida crítica del aclaramiento: deplesión estequiométrica de GSH y colapso de la membrana
            self.gsh_pool = max(0.0, self.gsh_pool - 0.5 * delta_t)
            
        # Evaluar Veto Redox del Hepatocito (Nivel 2.2 - Apoptosis Fail-Closed)
        if (self.gsh_pool / self.gsh_nominal) < 0.30:
            self.viabilidad = 0.0  # Apoptosis iniciada por MOMP por exceso de estrés redox biliar
            
        return {
            "NTCP_Membrana": self.ntcp_densidad_membrana,
            "Carga_Viral": self.carga_viral_de_novo,
            "MHC_I": self.mhc_i_presentacion,
            "GSH_Pool": self.gsh_pool,
            "Viabilidad_Hepatocito": self.viabilidad
        }

    def evaluar_lisis_por_cd8(self, cd8_presente=False, anti_pd_1=False):
        """
        Calcula la probabilidad lítica de los TILs CD8+ sobre el hepatocito infectado,
        incorporando el veto por acidosis estromal profunda (Nivel 2.1 de Inmuno)
        y la anergia/agotamiento del TCR mediado por PD-1/PD-L1.
        """
        if self.viabilidad <= 0.0 or not cd8_presente:
            return 0.0
            
        # VETO EXCLUSIÓN: Parálisis de lisis en acidosis estromal local extrema (pHe <= 6.50)
        if self.pHe <= 6.50:
            return 0.0  # Veto del Escudo Ácido (FC-BIO-2.1)
            
        # Cálculo de afinidad e interacción TCR/MHC-I
        prob_reconocimiento = self.mhc_i_presentacion / 10.0
        
        # Checkpoint de veto por PD-1/PD-L1 (Evasión tumoral o viral crónica)
        # En inflamación prolongada, el ligando PD-L1 de la célula diana silencia la señal
        pd_l1_expresion = min(1.0, self.carga_viral_de_novo * 0.2)
        pd1_interferencia = 0.0 if anti_pd_1 else pd_l1_expresion
        
        fuerza_lítica = prob_reconocimiento * (1.0 - pd1_interferencia)
        fuerza_lítica = max(0.0, min(1.0, fuerza_lítica))
        
        # Aplicar daño por lisis inmunitaria CD8+ al hepatocito diana
        self.viabilidad = max(0.0, self.viabilidad - fuerza_lítica)
        
        return fuerza_lítica
```

---

## VI. DECLARACIÓN FINAL

“Esto es cribado de hipótesis in silico sobre instrumentos de placa; no es consejo médico ni evidencia clínica.”

---
*Fin del Estudio de Integración Fisiológica v3.0. Documento técnico de referencia para el pipeline experimental de Guanes Health.*
