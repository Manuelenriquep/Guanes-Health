# MANUAL TÉCNICO DE REFERENCIA: SIMULADOR MULTIESCALA DE ONCOLOGÍA Y VIROLOGÍA HEPÁTICA (v2.0)
**GUÍA DE IMPLEMENTACIÓN, EJECUCIÓN Y VALIDACIÓN PARA EL REPOSITORIO ONCO-VIROLÓGICO**  
*Guanes Health - División de Oncología Computacional e Biología de Sistemas*

---

## 1. INTRODUCCIÓN AL ECOSISTEMA INTEGRADO

Este repositorio contiene la arquitectura de software *in silico* de la **Placa de Integración Fisiológica v3.0**, un entorno multiescala diseñado para simular la interacción dinámica entre el parénquima hepático (Hepatocito Sano v1.1), el microambiente de un tumor sólido (Carcinoma Hepatocelular), el estroma celular y el sistema inmunitario adaptativo (Inmunología v2.0).

El objetivo de este sistema es servir como una herramienta analítica para el cribado preliminar de hipótesis terapéuticas secuenciales, permitiendo explorar cómo las perturbaciones metabólicas (gradientes de pH, lactato y oxígeno) y virales (infección por Hepatitis B) convergen para condicionar el éxito de tratamientos avanzados de inmunoterapia.

---

## 2. MAPA DE ARCHIVOS Y COMPONENTES

El repositorio se estructura de forma modular. Todos los módulos operan bajo constantes biofísicas inmutables basadas en literatura de referencia científica:

### A. Motores de Simulación y Modelos Celulares
*   **`simulador_onco_homeostasis_v4.py`**: Modelo fundacional de la célula humana (sana y tumoral). Implementa las leyes de desgaste telomérico, potencial transmembrana (Goldman-Hodgkin-Katz), regulación de ciclo celular por daño genómico (eje p53-p21) y el bypass metabólico adaptativo de MCT2 frente a terapias ácidas.
*   **`simulador_hepatocito_infeccion.py`**: Modelo biofísico del hepatocito sinusoidal (v1.1). Incorpora zonación hepática por gradiente de oxígeno, aclaramiento basolateral de sales biliares por NTCP (SLC10A1), infección cinética por HBV, apoptosis por colestasis tóxica (`VETO FC-HEP-01`) y presentación de antígenos en el complejo MHC-I.
*   **`simulador_onco_hepatico_v2.py`**: El integrador acoplado bidireccional (v2.0). Cierra el sistema dinámico complejo al vincular la secreción paracrina de IL-6 del hepatocito con la activación de STAT3 y la sobreexpresión de PD-L1 en el tumor, forzando un escape adaptativo inmunomediado.

### B. Scripts de Visualización Científica
*   **`grafico_dinamica_temporal.py`**: Simula el bucle temporal del microambiente y grafica en un eje dual el momento preciso del escape tumoral ($t_{\text{escape}}$), correlacionando la acumulación de $[IL\text{-}6]$ y la inducción de $[PD\text{-}L1]$.
*   **`simulador_cointervencion_curacion.py`**: Modela de forma simultánea los cuatro escenarios de tratamiento y genera una matriz comparativa tridimensional de curvas cinéticas.

### C. Suites de Control de Calidad y Pruebas Unitarias
*   **`test_simulador_onco_hepatico-v2.py`**: Arnés de pruebas de integración automatizadas (`unittest`). Verifica numéricamente con aserciones estrictas las transiciones lógicas del modelo, el santuario viral del tumor y el éxito de la co-intervención terapéutica.

### D. Gráficos Generados (`/workspace/artifacts/`)
*   **`dinamica_temporal_il6_pdl1.png`**: Trayectoria de acumulación de citoquinas inflamatorias y saturación de anticuerpos monoclonales.
*   **`cointervencion_curacion_grafico.png`**: Matriz comparativa de viabilidad y depuración de los cuatro escenarios terapéuticos basales.
*   **`analisis_toxicidad_s267f.png`**: Análisis de asimetría biológica entre el genotipo salvaje (WT) y la variante poblacional resistente S267F.

---

## 3. ESPECIFICACIÓN FÍSICA DE LAS ECUACIONES CINÉTICAS

### A. Represión de NTCP por la vía Inflamatoria (IL-6 / JNK)
La densidad funcional de los receptores NTCP en la membrana basolateral del hepatocito sinusoidal se deprime de forma dosis-dependiente ante la secreción paracrina de IL-6 (mecanismo inmunológico de contención contra el HBV):
$$\text{Densidad}_{\text{NTCP}}(t) = \text{Densidad}_{\text{basal}} \cdot \left( 1.0 - 0.98 \cdot \frac{[IL\text{-}6](t)}{[IL\text{-}6](t) + 50.0} \right)$$
*   *Nota*: Si se presenta la variante **S267F**, la densidad en membrana es forzada inmediatamente a **0.0**, confiriendo inmunidad total a costa de suspender el aclaramiento de sales biliares.

### B. Farmacodinámica Competitiva de Myrcludex B
El lipopéptido sintético bloquea el anclaje del virus preS1 compitiendo físicamente por NTCP basolateral, exhibiendo una potencia selectiva 100 veces superior para la infección frente a la captación de sales:
$$\text{Fracción Bloqueo}_{\text{viral}} = \frac{1.0}{1.0 + \frac{[\text{Myrcludex B}]}{1.0 \text{ nM}}}$$
$$\text{Fracción Bloqueo}_{\text{biliar}} = \frac{1.0}{1.0 + \frac{[\text{Myrcludex B}]}{100.0 \text{ nM}}}$$

### C. El Veto de Apoptosis por Colestasis (`VETO FC-HEP-01`)
El aclaramiento real de sales biliares se calcula dinámicamente como:
$$\text{Aclaramiento} = \text{Densidad}_{\text{NTCP}}(t) \cdot \text{Fracción Bloqueo}_{\text{biliar}}$$
Si el aclaramiento desciende por debajo del umbral de **0.15**, la retención de detergentes biliares en el citoplasma deplementa el pool mitocondrial de glutatión (GSH) a una tasa constante de **0.5 mM/h**. Si el pool de GSH desciende por debajo de la fracción crítica del **30% nominal** (< 2.4 mM), se gatilla la permeabilización de membrana mitocondrial (MOMP) detonando la apoptosis del hepatocito.

### D. El Bucle de Retroalimentación Hepatocito-Tumor (STAT3 / PD-L1)
La inflamación local sinusoidal (carga viral + DAMPs de lisis) se acumula en forma de IL-6 paracrina:
$$[IL\text{-}6](t) = 2.0 \cdot \text{Carga Viral}(t) + 100.0 \cdot (1.0 - \text{Viabilidad Hepatocito}(t))$$
Esta IL-6 actúa sobre los receptores GP130 del tumor, estimulando la transcripción mediada por STAT3 que hiper-regula el escudo PD-L1:
$$\text{PD\text{-}L1}_{\text{tumor}}(t) = 50.0 + 3.0 \cdot [IL\text{-}6](t)$$
Si la expresión de PD-L1 cruza el umbral terapéutico de **150.0x**, los anticuerpos monoclonales anti-PD-1 del tratamiento biológico se saturan, reduciendo la efectividad lítica inmunitaria de las células CD8+ a **0.00** de forma instantánea.

---

## 4. GUÍA DE EJECUCIÓN DEL SIMULADOR

Para ejecutar los escenarios interactivos de simulación o graficar los perfiles dinámicos en tu terminal local, asegúrate de tener configurado un entorno Python 3.12 con las librerías `numpy` y `matplotlib`.

### A. Ejecutar el Barrido Comparativo de los 4 Escenarios
Para simular de forma paralela los escenarios basales (Control, Santuario MCT2, Feedback Activo y la Co-Intervención del Escenario 4), ejecuta el siguiente comando:
```bash
python3 simulador_cointervencion_curacion.py
```
*   **Resultados Esperados**: El script correrá la integración temporal (0 a 72h con pasos de 0.1h), imprimirá las variables terminales en la consola y exportará la matriz gráfica comparativa de 2x2 subplots en `cointervencion_curacion_grafico.png`.

### B. Localizar el Punto Crítico de Escape Temporal ($t_{\text{escape}}$)
Para correr el análisis fino de acumulación de citoquinas y determinar la ventana terapéutica exacta de la co-intervención, ejecuta:
```bash
python3 grafico_dinamica_temporal.py
```
*   **Resultados Esperados**: Retornará el instante exacto en que la IL-6 supera el umbral que satura los checkpoints (encontrado a **$t = 1.80\text{ h}$** bajo las condiciones de control) y exportará las trayectorias dinámicas duales a `dinamica_temporal_il6_pdl1.png`.

### C. Ejecutar el Barrido del Genotipo S267F vs. Wild-Type
Para correr el ensayo que mapea la asimetría funcional y la resistencia biológica absoluta del mutante frente al genotipo salvaje bajo el efecto de Myrcludex B, ejecuta:
```bash
python3 simulador_s267f_toxicidad.py
```
*   **Resultados Esperados**: Modelará la respuesta a dosis variables del inhibidor (0 a 1000 nM) y exportará la gráfica de curvas de viabilidad, GSH y carga viral residual en `analisis_toxicidad_s267f.png`.

---

## 5. INSTRUCCIONES PARA EL ARNÉS DE PRUEBAS AUTOMATIZADAS

La validación y control de regresión matemática se realiza mediante el módulo de pruebas de integración de Python. Para correr la suite completa y verificar que los inmutables físicos del modelo sigan intactos, ejecuta:

```bash
python3 -m unittest test_simulador_onco_hepatico-v2.py
```

### Resultados de Aserción del Arnés (Veredicto Esperado):
*   `test_coupled_unidirectional_clearance`: **PASADO**. Certifica que bajo la Cohorte C sin feedback, el estroma limpio (pHe 7.35) depure al 100% el tumor y la infección viral.
*   `test_coupled_mct2_sanctuary`: **PASADO**. Certifica que el escape de MCT2 (pH 6.65) deprima a los CD8+ protegiendo al hepatocito como un santuario viral.
*   `test_coupled_bidirectional_feedback_escape`: **PASADO**. Certifica que el feedback recíproco de la Opción A acumule IL-6 > 300 pg/mL e induzca PD-L1 > 1000x, escapando de la terapia.
*   `test_coupled_cointervention_clearance`: **PASADO**. Certifica que la triple intervención (Myrcludex B 10 nM + anti-IL-6) logre una viabilidad tumoral del **0.00%** manteniendo al hepatocito viable sin depletar el GSH (> 5.0 mM).

---

## 6. DECLARACIÓN DE RIGOR CIENTÍFICO E INVESTIGACIÓN *IN SILICO*

El modelado predictivo multiescala de *Guanes Health* es una herramienta bioinformática abstracta orientada al cribado preliminar de hipótesis moleculares y el diseño acelerado de terapias secuenciales sinérgicas. Los resultados, constantes y dinámicas aquí expuestas operan bajo restricciones termodinámicas matemáticas estrictamente calibradas sobre la literatura biológica estándar.

```
+---------------------------------------------------------------------------------------------------+
|                         ADVERTENCIA CLÍNICA Y DECLARACIÓN DE LÍMITES                              |
+---------------------------------------------------------------------------------------------------+
| 1. Naturaleza Abstracta: El modelo in silico representativo de la placa de integración fisiológica|
|    y la co-intervención representa una simplificación matemática de sistemas biológicos reales.    |
|    Tiene un carácter conceptual para la exploración diagnóstica y cribado in silico.              |
|                                                                                                   |
| 2. Restricción de Aplicabilidad Directa: Se desconseja de manera categórica la aplicabilidad      |
|    clínica directa de las conclusiones derivadas de este simulador para la toma de decisiones      |
|    médicas o el diseño de tratamientos reales sin previa validación en laboratorio húmedo.         |
|                                                                                                   |
| 3. Requisito de Validación Experimental Multi-Fase (Wet-Lab): Todo mecanismo lóbulo predicho por  |
|    este modelo debe ser validado físicamente en cultivos tridimensionales de organoides tumorales  |
|    (Tumor-on-a-Chip) y ensayos in vivo en modelos animales competentes para determinar la          |
|    biodistribución real, índices de aclaramiento y toxicidades sistémicas inmunomediadas.          |
+---------------------------------------------------------------------------------------------------+
```

---
*Fin del Manual Técnico de Referencia para el Repositorio Hepático-Tumoral. Guanes Health, 2026.*
