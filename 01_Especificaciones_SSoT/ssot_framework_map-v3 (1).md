# ÚNICA FUENTE DE VERDAD (SSOT): MAPA DE ARQUITECTURA Y LIMITACIONES BIOLÓGICAS (v3.0)
**Proyecto Guanes-Health - División de Oncología Computacional e Ingeniería In Silico**

Este documento constituye el **plano lógico unificado (SSoT)** que rige el diseño de simulaciones del microambiente hepático y tumoral. Define la organización en capas del software, el rol conceptual estricto de cada placa lógica integrada y el estado de integración (RESOLVED vs UNRESOLVED) que delimita el alcance científico de este instrumento de cribado.

---

## 1. CAPAS DE ABSTRACCIÓN METODOLÓGICA (A / B / C)

Para evitar la ontologización de metáforas biológicas y mantener la transparencia epistemológica del modelo, el software se divide estrictamente en tres niveles de maduración:

*   **Capa A (Especificación Conceptual e Inmunológica)**: 
    Modelos teóricos, diagramas de transición de estados y conjuntos de reglas cualitativas escritas en prosa formal y pseudocódigo (p. ej., el "Veto del Escudo Ácido" o la lógica de "Placa Base"). No posee capacidad de ejecución directa; actúa únicamente como el catálogo de hipótesis biológicas [5, 21].
*   **Capa B (Modelo Determinista de Juguete - *Toy Model* / Ejecutable)**: 
    Implementación matemática y computacional simplificada que traduce las hipótesis cualitativas en curvas dinámicas cuantificables (usando cinéticas de Hill de primer orden, ecuaciones de Michaelis-Menten y modelos de compartimentos discretos) [10, 18]. Cada comportamiento se valida mediante aserciones rígidas de límites en una suite de pruebas de regresión (`test_*.py`) [10, 17]. **Este es el estado operativo real de las simulaciones en el repositorio.**
*   **Capa C (Modelo Predictivo Calibrado - *Aspiracional / Wet-Lab*)**: 
    La transición final del modelo hacia datos experimentales reales. Requiere el anclaje de todas las constantes físicas abstractas a mediciones experimentales cuantitativas (Resonancia de Plasmón Superficial (SPR), ELISA, cultivos 3D de organoides hepáticos, tasas de difusión reales de protones). **Actualmente vacío y definido como Backlog de Ingeniería.**

---

## 2. INVENTARIO DE PLACAS LÓGICAS Y SU ROL OPERATIVO

### A. Placas Parenquimatosas y del Huésped
1.  **Placa Base de Línea Base Operativa (Célula Sana)**: Define los umbrales de viabilidad metabólica basal, los límites de replicación mitótica y el declive cronológico de envejecimiento lineal mediante el acortamiento programado de telómeros (Límite de Hayflick) [1, 5].
2.  **Placa Hepatocito**: Modela la zonación metabólica a lo largo del sinusoide hepático bajo la influencia directa del gradiente de oxígeno. Gobierna la tasa basal del co-transportador basolateral de sales biliares **NTCP (SLC10A1)** [13, 16].

### B. Placas Patológicas y de Subversión
3.  **Placa de Infección Sinusoidal (HBV)**: Simula la cinética de penetración viral y colonización del parénquima a través del secuestro de NTCP. Modela la respuesta antiviral innata mediante el control paracrino de **IL-6** [8, 13].
4.  **Placa de Subversión Oncológica (Carcinoma Hepatocelular)**: Representa el desvío metabólico del tumor (Warburg), el eflujo masivo de lactato e hidronios por el transportador **MCT2/MCT4**, y la evasión de apoptosis por sobreexpresión de proteínas antiapoptóticas [7, 11, 12].

### C. Placas de Intervención Sintética
5.  **Placa Lógica Inmunológica (CD8+ TILs)**: Modela el microambiente inmunitario del estroma. Define la sensibilidad de los linfocitos infiltrantes y su desactivación por desgranulación fallida ante un pH extracelular local inferior o igual a 6.50 (Veto del Escudo Ácido) [21]. En el código de Capa B (`simulador_onco_homeostasis_v5.py` y `simulador_onco_hepatico_v3.py`), esta desactivación se modela con un piso biológico de `6.50` y una compuerta de anergia (Anergy Gate) de `20.0%` (las eficiencias por debajo del `0.20` se truncan a `0.0` para simular la fatiga de degranulación y anergia metabólica), unificando la especificación teórica de Capa A con la estabilidad numérica del modelo.
6.  **Placa de Lógica CAR-T (STROMA-SHIELD v1.1)**: Establece el comportamiento lógico del linfocito reprogramado sintéticamente. Codifica la optimización de la homeostasis iónica citoplásmica, la transición alostérica por protonación de histidinas en el scFv y la dinámica de agotamiento por el factor transcripcional **TOX** [17, 18].
7.  **Placa Completa iCasp9**: Actúa como el mecanismo de seguridad analógico del CAR-T. Define la tasa de apoptosis celular dirigida por la homodimerización de la caspasa 9 quimérica controlada por el inductor sintético **rimiducid (AP1903)** [15].
8.  **Placa de Extravasación y Tráfico**: Modela las barreras físicas y mecánicas que retrasan la infiltración inmunológica en el núcleo tumoral densificado, tales como la Presión de Fluido Intersticial (IFP) y el andamiaje del colágeno estromal [19].
9.  **Placa HCC (Mimetismo e Identificación Antigénica)**: Define la estequiometría de enlace frente al antígeno diana de membrana **GPC3** y los sumideros de interferencia competitiva en fase líquida [20].

---

## 3. ESTADO DE INTEGRACIÓN DE BRECHAS DE CRIBADO

Para asegurar la honestidad científica y el control de regresión frente a terceros investigadores, se documenta el estado actual de resolución de las brechas de simulación:

### A. Módulos Integrados (RESOLVED-B)
*   **[RESOLVED-B-01] Paratopos de Interferencia Soluble (sGPC3)**: 
    *   *Mecanismo*: Implementación de la competencia estérica hiperbólica por antígenos señuelo solubles:
        $$\phi_{\text{libre}} = \frac{1}{1 + \frac{[\text{sGPC3}]}{K_{i,\text{sGPC3}}}}$$
    *   *Parámetro*: Constante de afinidad del señuelo $K_{i,\text{sGPC3}} = 2.5\text{ ng/mL}$.
    *   *Código*: Integrado de forma operativa en `simulador_cart_hcc_interaccion.py`.
    *   *Verificación*: Cubierto y validado por la prueba unitaria de regresión `test_senuelo_sgpc3_resolved_b` en `test_cart_hcc_interaccion.py`. El escape tumoral parcial por saturación en fase líquida está verificado bajo el control de calidad de la suite de pruebas unitarias [20].
    *   *Nota de Capa C*: La calibración empírica con Alfafetoproteína (AFP) soluble y la determinación wet-lab de las constantes dinámicas de clivaje siguen abiertas.

### B. Módulos Pendientes (UNRESOLVED)
*   **[UNRESOLVED-02] Tránsito Físico y Barreras de Confección Mecánica**:
    Las restricciones físicas de la placa de extravasación (rigidez del colágeno, Presión del Fluido Intersticial y el uso del compuesto **OTR4120** para estabilizar gradientes quimiotácticos) están documentadas cualitativamente en el backlog, pero no se ha codificado un motor geométrico de transporte por difusión que limite la tasa de encuentro espacial de los efectores [19].
*   **[UNRESOLVED-03] El Mecanismo Epigenético "Succinate Trap"**:
    La inducción del estado de agotamiento terminal mediada por el factor de transcripción **TOX** en el CAR-T se simula actualmente mediante una tasa puramente temporal. Falta codificar el acoplamiento directo al desvío metabólico intracelular (secuestro de $\alpha$-cetoglutarato por la colágena hidroxilasa **P4HA1** bajo hipoxia local), lo que limita la utilidad del modelo para evaluar knockout genéticos de fitness metabólico.
*   **[UNRESOLVED-04] Curaduría y Muestreo de Incertidumbre de Constantes**:
    Todas las constantes del simulador hepático-tumoral acoplado y del CAR-T están calibradas heurísticamente para forzar el comportamiento cualitativo coherente del modelo de juguete (*toy model*). Ningún parámetro clave ($K_d$, $pK_a$, tasas catalíticas, concentraciones de citoquinas) ha sido sometido a un análisis de sensibilidad global (método de Sobol) o muestreo de Monte Carlo para acotar su intervalo de confianza frente a la literatura experimental.

---
*Fin de la Especificación Técnica SSoT v3.0 (Resolución del Veto CD8). Guanes Health, 2026. Todos los artefactos descritos y sus grados de madurez se declaran alineados de forma verificable con el ledger operativo del proyecto.*
