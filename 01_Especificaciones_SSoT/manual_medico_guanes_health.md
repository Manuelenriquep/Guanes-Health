# GUANES HEALTH v6.0
## Manual de Exploración y Fundamentos Fisiopatológicos para el Médico Clínico e Investigador

> **Acceso a la consola interactiva:** [https://health.guanes.biz](https://health.guanes.biz)  
> **Repositorio de código y trazabilidad:** [github.com/Manuelenriquep/Guanes-Health](https://github.com/Manuelenriquep/Guanes-Health)  
> **DOI permanente (Zenodo):** [10.5281/zenodo.22101265](https://doi.org/10.5281/zenodo.22101265)  
> **Autor:** Manuel Enrique Prada Forero (`gerente@guanes.biz`) · Bucaramanga, Colombia

---

### 1. Prólogo Epistemológico: ¿Qué es Guanes Health?

Estimado colega médico:

Este instrumento digital no es un software de inteligencia artificial generativa, ni un asistente de diagnóstico, ni un dispositivo médico. 

**Guanes Health v6.0** es un **prototipo biofísico determinista de simulación *in silico*** (Capa B) basado en sistemas acoplados de ecuaciones diferenciales ordinarias (ODE). Su objetivo no es prescribir tratamientos, sino resolver un problema que la oncología moderna sufre en el quirófano y en la sala de infusión:

> **La Paradoja de la Inmunoterapia en Tumores Sólidos:**  
> Diseñamos células CAR-T y vacunas de ARNm con una afinidad antigénica del $100\%$ por el neoantígeno tumoral. Sin embargo, en tumores sólidos no inflamados ("fríos"), más del $80\%$ de los pacientes no responden o experimentan recaídas tempranas.  
> **¿Por qué?** Porque el linfocito citotóxico ($\text{CD8}^+$) no fracasa por falta de reconocimiento inmune, sino por **colapso biofísico y metabólico** al ingresar al microambiente tumoral.

Guanes Health formaliza matemáticamente la **Hipótesis de las Dos Pinzas**: para que una célula T logre erradicar un tumor sólido, se debe vencer simultáneamente la **parálisis energética local** (acidosis) y el **agotamiento fenotípico sistémico** (eje intestino-hígado).

---

### 2. El Marco Fisiopatológico de las "Dos Pinzas"

```
                              ┌───────────────────────────────┐
                              │     LINFOCITO CITOTÓXICO      │
                              │     (CAR-T / CD8+ Nativo)     │
                              └──────────────┬────────────────┘
                                             │
                      ┌──────────────────────┴──────────────────────┐
                      ▼                                             ▼
       [ PINZA LOCAL: MICROAMBIENTE ]                [ PINZA SISTÉMICA: EJE PORTAL ]
         Efecto Warburg del Tumor                       Permeabilidad Intestinal
                    │                                             │
      Acidosis Extracelular (pHe ~ 6.2)              Translocación de LPS bacteriano
                    │                                             │
       Caída de pHi Citosólico (< 6.4)               Vena Porta ➔ Células de Kupffer
                    │                                             │
       Inhibición Alostérica PFK-1                   Tormenta Portal de IL-6
                    │                                             │
            Depleción de ATP                         Sobreexpresión Tumoral de PD-L1
                    │                                             │
         PARÁLISIS CITOLÍTICA                       AGOTAMIENTO EPIGENÉTICO
        (Sin exocitosis de gránulos)               (Vía TOX+ / Silenciamiento H3K27me3)
                      ▲                                             ▲
                      └──────────────────────┬──────────────────────┘
                                             │
                              ┌──────────────┴────────────────┐
                              │   COLAPSO DE LA INMUNOTERAPIA │
                              └───────────────────────────────┘
```

#### Pinza 1: El Frente Bioquímico Local (Microambiente y PFK-1)
* **El entorno:** Los tumores sólidos hiperglucolíticos (Efecto Warburg) expulsan ácido láctico y protones al estroma celular, reduciendo el pH extracelular a rangos extremos ($\text{pH}_e = 6.0 - 6.5$).
* **El colapso metabólico:** El linfocito T infiltrante sufre un influjo pasivo masivo de protones, acidificando su citosol ($\text{pH}_i \rightarrow 5.78$).
* **El punto crítico enzimático:** La **Fosfofructoquinasa-1 (PFK-1)**, enzima marcapasos de la vía glucolítica, posee sitios alostéricos de unión a protones que la inactivan cooperativamente (modelo Hill con exponente $n=4.0$ y $\text{pKa}=6.80$). Con la PFK-1 apagada ($<3\%$ de actividad), la célula T agota su ATP en menos de 180 minutos.
* **Consecuencia clínica:** Los motores moleculares de dineína, cinesina y actina-miosina quedan sin energía: la célula no puede movilizar ni exocitar sus gránulos de **perforinas y granzimas**. El linfocito queda paralizado frente al tumor.

#### Pinza 2: El Frente Inflamatorio Sistémico (Eje Intestino-Hígado)
* **La barrera mucosa ($\phi_{\text{gut}}$):** La pérdida de integridad en la mucosa del colon (inducida por disbiosis, desnutrición o quimioterapia previa) permite la fuga de lipopolisacárido (**LPS**) de bacterias Gram-negativas hacia la circulación portal.
* **La estación de filtrado hepático:** El LPS estimula los receptores TLR4 en las **células de Kupffer** y el endotelio sinusoidal del hígado, liberando una oleada de **IL-6**.
* **El escape tumoral:** La IL-6 portal induce fosforilación de STAT3 en el lecho tumoral, sobreexpresando **PD-L1** (hasta 11 veces sobre la línea base) y forzando al linfocito T a entrar en un estado de **agotamiento epigenético irreversible**, orquestado por el factor de transcripción **TOX** y marcas represivas de cromatina (**H3K27me3**).

---

### 3. Diccionario de Parámetros de la Consola

Al ingresar a [health.guanes.biz](https://health.guanes.biz), encontrarás los siguientes controles deterministas:

| Parámetro en Pantalla | Variable Biofísica | Rango Nominal | Significado Clínico / Fisiológico |
| :--- | :---: | :---: | :--- |
| **pH Extracelular (pHe)** | $\text{pH}_e$ | $6.00 - 7.40$ | Grado de acidosis del estroma tumoral. Valores $\le 6.50$ representan el núcleo hipóxico/ácido de un tumor sólido agresivo. |
| **Densidad GPC3** | $\rho_{\text{antígeno}}$ | $\text{moléc./célula}$ | Densidad del neoantígeno diana en la superficie tumoral (ej. Glipicano-3 en Carcinoma Hepatocelular). |
| **Reserva Energética (ATP)** | $[\text{ATP}]_i$ | $0 - 100\%$ | Estado bioenergético basal del linfocito T infiltrante. |
| **Blindaje de Membrana** | $\text{NHE1}$ | Activo / Apagado | Intercambiador $\text{Na}^+/\text{H}^+$ 1 ($\text{SLC9A1}$, constructo hiperactivo 1K3R4E). Bombea protones hacia el exterior utilizando el gradiente de sodio para mantener el $\text{pH}_i$ en $6.85$. |
| **Integridad Mucosa ($\phi_{\text{gut}}$)** | $\phi_{\text{gut}}$ | $0\% - 100\%$ | Estado de la barrera intestinal / Abundancia de *Akkermansia muciniphila*. $100\%$ = eubiosis y sellado de uniones estrechas; $\le 50\%$ = *Leaky Gut* y endotoxemia portal. |

#### Panel de Telemetría Dinámica Estimada:
* **IL-6 Portal:** Carga inflamatoria en la vena porta inducida por la fuga de endotoxina LPS.
* **PD-L1 Tumoral:** Factor multiplicador de evasión inmune en la superficie neoplásica.
* **Metilación H3K27me3:** Porcentaje de silenciamiento epigenético represivo en el locus de citocinas citolíticas del linfocito T.
* **Tiempo Citolítico Activo (ACT):** Ventana temporal (en horas) durante la cual el linfocito mantiene viabilidad energética y capacidad de lisis sostenida antes de agotarse.

---

### 4. Protocolo de Exploración Práctica (4 Experimentos Guiados)

Abre [health.guanes.biz](https://health.guanes.biz) y replica los siguientes 4 escenarios para comprobar la lógica del modelo:

---

#### Experimento 1: La Trampa Estándar (CAR-T o Vacuna ARNm Convencional)
* **Objetivo:** Observar por qué fracasa una terapia celular estándar en un microambiente ácido.
* **Configuración:**
  * **pH Extracelular (pHe):** `6.20` (tumor ácido).
  * **Blindaje de Membrana:** `Linfocito CD8 Nativo / Vacuna ARNm (Sin Blindaje)`.
  * **Integridad Mucosa ($\phi_{\text{gut}}$):** `92%` (intestino sano).
* **Haz clic en:** `EJECUTAR SIMULACIÓN MULTIESCALA`.
* **Resultado en el Gráfico:**
  * La curva de **Viabilidad (azul)** colapsa casi verticalmente.
  * La **Citólisis Tumoral (rojo)** se congela en menos del $3.0\%$.
  * **Conclusión Clínica:** Aunque el paciente tiene intestino sano y la célula T reconoce el antígeno, la acidosis inactivó la PFK-1 citosólica. La célula se quedó sin ATP y murió por agotamiento isquémico antes de lisar el tumor.

---

#### Experimento 2: El Escudo Solitario (Intervención Local sin Protección Sistémica)
* **Objetivo:** Probar qué ocurre si resolvemos la acidosis pero el paciente tiene inflamación intestinal.
* **Configuración:**
  * **pH Extracelular (pHe):** `6.20`.
  * **Blindaje de Membrana:** `CAR-T + NHE1-Shield (Mutante 1K3R4E)`.
  * **Integridad Mucosa ($\phi_{\text{gut}}$):** Ajusta el slider a `25%` (*Leaky Gut* severo / endotoxemia).
* **Haz clic en:** `EJECUTAR SIMULACIÓN MULTIESCALA`.
* **Resultado en el Gráfico:**
  * La célula T sobrevive a la acidez gracias al intercambiador NHE1.
  * Sin embargo, observa la curva de **Silenciamiento TOX (amarilla)**: se dispara por encima del $80\%$.
  * La telemetría marca **IL-6 Portal $> 500\text{ pg/mL}$** y **PD-L1 Tumoral $> 8.5\times$**.
  * El **Tiempo de Lisis (ACT)** se detiene abruptamente antes de erradicar el clon tumoral.
  * **Conclusión Clínica:** Blindar la membrana contra el ácido no cura al paciente si la translocación de LPS desde el intestino mantiene activo el eje IL-6/STAT3/PD-L1. La célula T es bloqueada por agotamiento de receptor.

---

#### Experimento 3: La Co-Intervención de Dos Pinzas (El Fenómeno de Sinergia)
* **Objetivo:** Comprobar la hipótesis central de rescate biológico de Guanes Health.
* **Configuración:**
  * **pH Extracelular (pHe):** `6.20` (entorno tumoral hostil).
  * **Blindaje de Membrana:** `CAR-T + NHE1-Shield (Mutante 1K3R4E)`.
  * **Integridad Mucosa ($\phi_{\text{gut}}$):** Desplaza el slider a `95%` (Restauración con *Akkermansia* / Barrera intacta).
* **Haz clic en:** `EJECUTAR SIMULACIÓN MULTIESCALA`.
* **Resultado en el Gráfico:**
  * La viabilidad celular se mantiene estable ($>90\%$).
  * El silenciamiento epigenético TOX cae por debajo del umbral inhibitorio.
  * El **ACT (Tiempo Citolítico Activo)** se expande a **$9.04\text{ horas}$**.
  * La **Citólisis Tumoral** asciende progresivamente hasta alcanzar el **$100.0\%$ (Lisis Completa)**.
  * **Conclusión Clínica:** La sinergia entre el escudo iónico local y la impermeabilidad mucosa sistémica protege al efector inmune en ambos frentes temporales y moleculares.

---

#### Experimento 4: El Umbral de Catástrofe (*Leaky Gut Threshold*)
* **Objetivo:** Identificar el punto de inflexión donde la disbiosis intestinal anula la terapia.
* **Procedimiento:** Con el blindaje NHE1 activado y $\text{pHe} = 6.20$, mueve gradualmente el slider de $\phi_{\text{gut}}$ desde $100\%$ hacia abajo:
  * Nota cómo entre **$100\%$ y $90\%$** la respuesta lítica se mantiene robusta.
  * Al descender de **$89.9\%$**, la IL-6 portal supera los $70\text{ pg/mL}$ e induce una transición de fase en la expresión de PD-L1, acortando exponencialmente el ACT.
  * **Conclusión Clínica:** El modelo matemático predice una **no-linealidad biológica**: existe un umbral mínimo de integridad mucosa por debajo del cual cualquier terapia celular sólida pierde efectividad.

---

### 5. Hoja de Ruta de Falsación en Laboratorio Húmedo (*Wet-Lab Roadmap*)

Todo modelo teórico debe ser susceptible de ser refutado o falsado experimentalmente. Guanes Health está diseñado para someterse a prueba en una jerarquía de 5 capas:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      NIVELES DE FALSACIÓN WET-LAB                      │
├─────────┬────────────────────────────┬─────────────────────────────────┤
│ Capa 0  │ Estabilidad Numérica       │ Solvers ODE fail-closed sin     │
│         │ de Invariantes             │ imputación heurística.          │
├─────────┼────────────────────────────┼─────────────────────────────────┤
│ Capa 1  │ "Experimento Cero"         │ Análisis de flujo metabólico en │
│         │ Bioenergético In Vitro     │ Agilent Seahorse XF: Medición   │
│         │                            │ de ECAR, OCR y ATP a pHe 6.2.   │
├─────────┼────────────────────────────┼─────────────────────────────────┤
│ Capa 2  │ Ensayo Transwell           │ Modelo Caco-2 (TEER) acoplado a │
│         │ Eje Entero-Hepático        │ esferoides 3D y macrófagos.     │
├─────────┼────────────────────────────┼─────────────────────────────────┤
│ Capa 3  │ Modelos Murinos            │ Medición in vivo con micro-     │
│         │ Ortotópicos (HCC)          │ electrodos de pH y LPS portal.  │
├─────────┼────────────────────────────┼─────────────────────────────────┤
│ Capa 4  │ Cohortes Clínicas          │ Correlación multi-ómica de      │
│         │ Humanas                    │ pacientes no respondedores.     │
└─────────┴────────────────────────────┴─────────────────────────────────┘
```

#### El "Experimento Cero" en Analizador Seahorse XF:
El modelo hace una predicción cuantitativa directa:
* En linfocitos T CD8 no modificados a $\text{pH}_e = 6.20$, la tasa de acidificación extracelular glucolítica (ECAR) y los niveles de ATP intracelular deben desplomarse en un $90\%$ antes de 180 minutos.
* Si en un ensayo Seahorse in vitro las células T expuestas a $\text{pH}_e = 6.20$ mantienen su glucólisis y ATP intactos sin intervención de transporte protónico, **la Ecuación 4.2 del modelo queda falsada**.

---

### 6. Literatura Científica y Fuentes de Parámetros

Todas las constantes utilizadas por el simulador provienen de la literatura biofísica revisada por pares:

1. **Acidosis Tumoral y Bioenergética:**  
   * Warburg, O. (1956). *On the origin of cancer cells.* Science, 123(3191), 309-314.  
   * Webb, B. A., et al. (2011). *Dysregulated pH: a hallmark of cancer.* Nature Reviews Cancer, 11(9), 671-677.
2. **Cinética Alostérica de PFK-1 por Protones:**  
   * Dobson, G. P., et al. (1986). *Phosphofructokinase and the control of glycolytic flux in ischemic tissue.* Biochemical Journal.
3. **Transportador de Protones NHE1 / SLC9A1:**  
   * Counillon, L., & Pouysségur, J. (2000). *The expanding family of eucaryotic Na+/H+ exchangers.* Journal of Biological Chemistry.
4. **Eje Entero-Hepático, Akkermansia y Respuesta a Inmunoterapia:**  
   * Routy, B., et al. (2018). *Gut microbiome influences efficacy of PD-1-based immunotherapy against epithelial tumors.* Science, 359(6371), 91-97.  
   * Derosa, L., et al. (2022). *Intestinal Akkermansia muciniphila predicts clinical response to immune checkpoint inhibitors.* Nature Medicine.
5. **Agotamiento Epigenético y Factor de Transcripción TOX:**  
   * Khan, O., et al. (2019). *TOX transcriptionally and epigenetically programs CD8+ T cell exhaustion.* Nature, 571(7764), 211-218.

---

### 7. Preguntas Abiertas para Debate con tu Sobrino

Cuando tu sobrino termine de explorar la consola, plantéale estas preguntas para profundizar en la discusión:

1. *¿Qué estrategias farmacológicas actuales conoces para alcalinizar transitoriamente el estroma tumoral o inhibir la anhidrasa carbónica IX (CA-IX)?*
2. *En tus rotaciones de gastroenterología/oncología, ¿has observado correlación entre el uso de antibióticos de amplio espectro (que barren Akkermansia) y la tasa de fracaso de pembrolizumab o nivolumab?*
3. *Si tuvieras acceso a un equipo Seahorse XF en la universidad o el hospital, ¿qué tipo celular te gustaría someter al estrés de pH 6.2 para medir su caída de ATP?*

---
*Manual generado para Guanes Health Simulation Suite v6.0 · Bucaramanga, Colombia.*
