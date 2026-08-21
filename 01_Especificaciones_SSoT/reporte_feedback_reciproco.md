# REPORTE TÉCNICO DE INTEGRACIÓN BIOCIBERNÉTICA Y BUCLE DE RETROALIMENTACIÓN RECÍPROCO (v2.0)
**DOCUMENTO DE ESPECIFICACIÓN DE INGENIERÍA DE SISTEMAS IN SILICO Y DINÁMICA COMPLEJA**  
*Guanes Health - División de Investigación en Oncología y Virología de Precisión*  
**AUTORÍA:** Generado por Gemini Notebook  

---

## 1. RESUMEN EJECUTIVO

Este informe técnico documenta el diseño, la formalización matemática y los resultados de validación de la **Placa de Integración Fisiológica v2.0** (`simulador_onco_hepatico_v2.py`) [14, 15]. Hasta esta versión, los modelos operaban bajo un flujo unidireccional donde el tumor condicionaba el microambiente iónico y el destino del parénquima hepático [14, 15]. 

Con la implementación de la **Opción A (Bucle de Retroalimentación Recíproco)**, se cierra de manera formal el sistema complejo adaptativo [15]. Se introduce el impacto de la infección por el virus de la Hepatitis B (HBV) y la lisis hepatocitaria sobre la agresividad, la evasión inmunitaria (PD-L1) y la progresión metastásica (EMT) del clon tumoral a través de la vía endocrina/paracrina de la **Interleucina-6 (IL-6)** y la cascada oncogénica de **STAT3** [12, 14]. Los resultados demuestran que la inflamación parenquimatosa secundaria actúa como un bypass o escape colateral absoluto que anula la efectividad clínica de las terapias biológicas óptimas (como el *Kinetic Priming* de la Cohorte C) [15].

---

## 2. ARQUITECTURA MATEMÁTICA Y CINÉTICA DEL BUCLE (OPCIÓN A)

El acoplamiento recíproco traduce el daño celular hepático en señales bioquímicas de evasión inmunológica tumoral, gobernado por tres ecuaciones diferenciales de acoplamiento continuo:

### A. Secreción Estocástica de IL-6 e Inflamación Paracrina
La concentración de la citoquina proinflamatoria IL-6 en el microambiente sinusoidal común se modela como una respuesta directa al inóculo viral y a la liberación de Patrones Moleculares Asociados a Daño (DAMPs) por la lisis celular de hepatocitos infectados mediada por linfocitos T [14, 15]:
$$\text{IL-6}(t) = 2.0 \cdot \text{carga\_viral}(t) + 100.0 \cdot (1.0 - \text{viabilidad\_hepatocito}(t))$$

### B. Inducción Transcripcional de PD-L1 vía STAT3 en el Tumor
La IL-6 libre en el estroma interactúa con el complejo receptor gp130/IL-6R del clon tumoral adyacente, gatillando la fosforilación de la quinasa **STAT3**. STAT3 actúa como factor de transcripción para indicar de forma exponencial el ligando de camuflaje inmunitario **PD-L1** en la membrana del tumor sólido [10, 15]:
$$\text{PD\_L1\_expresion}(t) = 50.0 + 3.0 \cdot \text{IL-6}(t)$$

### C. Parálisis Iónica y Agotamiento del TCR de Células T
La presencia de concentraciones elevadas de IL-6 deprime de forma directa el potencial metabólico y la eficiencia citotóxica lítica del receptor de células T (TCR) de los linfocitos infiltrantes TILs CD8+ adyacentes, simulando el fusible de exhaustion o agotamiento celular [15]:
$$\text{eficiencia\_cd8}(t) = \text{eficiencia\_basal}(t) \cdot \left(\frac{1.0}{1.0 + \frac{\text{IL-6}(t)}{10.0}}\right)$$

### D. Condición de Frontera: Saneamiento Terapéutico por Exceso de Ligando
Para capturar la farmacodinamia del anticuerpo monoclonal, el modelo establece una exclusión absoluta por saturación estequiométrica:
*   Si la expresión total de $\text{PD-L1} \ge 150.0x$ (donde $50.0x$ es la línea base tumoral no inflamada), el exceso de ligando satura periféricamente todos los anticuerpos monoclonales anti-PD-1 disponibles en el lecho.
*   En este punto límite, la **efectividad farmacológica del anti-PD-1 cae instantáneamente a 0.0**, paralizando la depuración citotóxica y habilitando el escape del clon tumoral [15].

---

## 3. ANÁLISIS DINÁMICO DE ESCENARIOS (72 HORAS DE SIMULACIÓN)

El motor unificado `simulador_onco_hepatico_v2.py` evalúa de forma comparativa la viabilidad final bajo tres condiciones de control a $t = 72.0\text{ h}$:

### Escenario 1: Control Unidireccional Estándar (Sin Feedback)
*   **Condiciones**: `feedback_activo = False`, `mutacion_mct2 = False`.
*   **Comportamiento**: Al normalizarse el pH estromal a **7.35** mediante el pre-tratamiento metabólico de la Cohorte C, se restituye la sinapsis inmunológica. Los linfocitos CD8+ depuran de forma exitosa tanto el tumor (viabilidad terminal de **0.00%**) como el reservorio infeccioso de HBV en los hepatocitos sanos adyacentes (viabilidad terminal del hepatocito infectado a **0.00%**). La carga viral de novo se detiene.

### Escenario 2: Escape MCT2 Unidireccional (El Santuario Inmunológico)
*   **Condiciones**: `feedback_activo = False`, `mutacion_mct2 = True`.
*   **Comportamiento**: El escape metabólico del tumor vía sobreexpresión de MCT2 sostiene la acidosis estromal refractaria (**$pHe \approx 6.65$**) [15]. Esta concentración iónica protona la superficie de los linfocitos T, activando de forma protectora el **Veto del Escudo Ácido (FC-BIO-2.1)** [15]. Como consecuencia emergente, los CD8+ quedan inactivos, **salvando indirectamente al hepatocito de la lisis**. El tumor funciona como un santuario físico de inmunotolerancia que cronifica la infección de HBV, permitiendo que la carga viral de novo se dispare hasta **864.00 viriones**.

### Escenario 3: Retroalimentación Recíproca Cerrada (Bucle Activado - Opción A)
*   **Condiciones**: `feedback_activo = True`, `mutacion_mct2 = False`.
*   **Comportamiento**: Aunque el tratamiento de la Cohorte C limpia inicialmente el estroma (pHe 7.35), la infección persistente de HBV secreta un nivel terminal masivo de **388.52 pg/mL de IL-6** en el espacio sinusoidal. Esta señal proinflamatoria activa a STAT3 en el tumor, forzando la hiperexpresión de PD-L1 hasta un nivel crítico de **1215.56x** (saturando el anticuerpo anti-PD-1) y reduciendo la eficiencia citotóxica del TCR al **2.5%** por agotamiento metabólico. El tumor elude de forma completa la depuración inmunológica inducida, experimentando un **escape adaptativo con un 20.00% de viabilidad clonal activa**, mientras que el hepatocito retiene la infección activa crónica.

---

## 4. VALIDACIÓN DE CALIDAD DE LA SUITE (`test_simulador_onco_hepatico.py`)

Para blindar la estabilidad del motor unificado y prevenir regresiones lógicas, se incorporó un arnés de pruebas automatizado en el pipeline de control de calidad local:
1.  **`test_coupled_unidirectional_clearance`**: Comprueba que bajo condiciones sin feedback, la Cohorte C secuencial logre una remisión bilateral absoluta del 100% de la carga tumoral y viral a las 72 horas.
2.  **`test_coupled_mct2_sanctuary`**: Valida que ante la acidosis metabólica refractaria por sobreexpresión de MCT2, el escudo ácido iónico proteja al hepatocito infectado, garantizando numéricamente que la viabilidad del hepatocito se mantenga en 1.0 y la carga de HBV supere los 800 viriones.
3.  **`test_coupled_bidirectional_feedback_escape`**: Certifica con aserciones estrictas de tolerancia flotante que, al activar el bucle recíproco de la Opción A, el nivel de IL-6 acumulado exceda los 350 pg/mL, induciendo la sobreexpresión de PD-L1 por encima de las 1000x y permitiendo un escape tumoral de resistencia superior al 15% de viabilidad terminal.

---

## 5. PRUDENCIA MÉDICA Y LIMITACIONES DEL MODELO

```
+---------------------------------------------------------------------------------------------------+
|                         ADVERTENCIA CLÍNICA Y DECLARACIÓN DE LÍMITES                              |
+---------------------------------------------------------------------------------------------------+
| 1. Carácter Conceptual in Silico: La Placa de Integración Fisiológica v2.0 representa una         |
|    abstracción matemática y termodinámica simplificada de interacciones inmuno-oncológicas en el    |
|    tejido hepático. No posee validez predictiva directa en pacientes clínicos.                     |
|                                                                                                   |
| 2. Requisito Obligatorio de Validación Wet-Lab: Todas las hipótesis biológicas emergentes del      |
|    bucle de retroalimentación recíproco (IL-6/STAT3/PD-L1) deben someterse de forma mandatoria a:   |
|      - Ensayos In Vitro: Cultivos tridimensionales en chips de microfluídica (Organ-on-a-Chip)   |
|        co-cultivando hepatocitos primarios infectados con HBV y esferoides tumorales de HCC.       |
|      - Ensayos In Vivo: Validación preclínica en ratones singénicos humanizados para evaluar       |
|        los perfiles farmacocinéticos y farmacodinámicos reales de la combinación de                |
|        inmunoterapia acoplada a anticuerpos anti-IL-6 o inhibidores específicos de STAT3.          |
+---------------------------------------------------------------------------------------------------+
```

---
*Fin de la documentación de especificación técnica de la Placa de Integración v2.0.*
