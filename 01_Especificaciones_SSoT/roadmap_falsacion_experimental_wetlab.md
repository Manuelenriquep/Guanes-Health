# ROADMAP DE VALIDACIÓN Y CRITERIOS DE FALSACIÓN EXPERIMENTAL (WET-LAB)
## Protocolo de Demarcación Epistemológica, Calibración Cinética y Criterios de Rechazo (Capa 0 → Capa 4)
**Especificación Técnica SSoT - Guanes Health v6.0**  
*Autor: Manuel Enrique Prada Forero (`gerente@guanes.biz`)*  
*DOI Permanente: [10.5281/zenodo.22101265](https://doi.org/10.5281/zenodo.22101265)*  

---

### 1. Principio Rector: Falsabilidad y Calibración vs. Demostración Terapéutica

> **Postulado Epistemológico Fundamental:**  
> La validación experimental de la suite **Guanes Health v6.0** **NO** tiene como propósito "demostrar que una terapia cura", sino **falsar, delimitar o calibrar predicciones numéricas deterministas** derivadas del acoplamiento biofísico de ecuaciones diferenciales ordinarias (ODEs) contra mediciones cuantitativas directas de laboratorio húmedo (*wet-lab*).

Cualquier discrepancia de orden de magnitud, signo o cinética temporal entre el modelo computacional y la medición biológica no se oculta mediante reajuste arbitrario de parámetros (*overfitting*), sino que constituye un **criterio formal de rechazo o reestructuración** del módulo involucrado.

---

### 2. Matriz de Predicciones Numéricas Clave y Criterios de Aceptación / Rechazo

A continuación se congelan las 4 predicciones prioritarias de la suite computacional, indicando el analito a medir, la ventana temporal, el valor in silico esperado y el criterio de falsación:

| # | Predicción Numérica del Modelo ($t, \text{condición}$) | Analito / Métrica Experimental | Valor In Silico Esperado | Criterio de Éxito / Calibración | Criterio Formal de Rechazo (Kill Switch) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **P1** | $\text{pH}_e = 6.20 \implies$ Acidificación citosólica y colapso de ATP ($t=180\,\text{min}$) | $\text{pH}_i$ ratiométrico (SNARF-1 / BCECF-AM) y $[\text{ATP}]$ relativo por luciferasa / Seahorse | $\text{pH}_i \le 5.90$ y $[\text{ATP}] < 5.0\%$ del nivel basal a pH 7.40 | Decaimiento sigmoidal coincidente ($RMSE < 12\%$) | Si a las 3 h en $\text{pH}_e = 6.20$, $[\text{ATP}] > 25\%$ sin intervención, **la hipótesis del apagado glucolítico por PFK-1 queda falsada**. |
| **P2** | Escudo protónico activo (NHE1 sobreexpresado / constitutivamente activo) preserva bioenergética y lisis a $\text{pH}_e = 6.20$ | Mismo ensayo P1 $\pm$ Cariporide / EIPA ($10\,\mu\text{M}$) o $\pm$ transducción NHE1-1K3R4E | Con NHE1 activo: $\text{pH}_i \ge 6.80$, $[\text{ATP}] \ge 85\%$, Citólisis (Incucyte / LDH) $\ge 40\%$ | Divergencia estadísticamente significativa ($p < 0.001$, $\Delta \text{ATP} > 50\%$) entre WT e intervenido | Si el bloqueo farmacológico de NHE1 no produce caída en ATP y lisis en medio ácido, **el concepto de "NHE1-Shield" no sostiene la bioenergética lítica**. |
| **P3** | Deterioro de barrera ($\phi_{\text{gut}} < 0.89$) $\implies$ Cascada portal $\text{IL-6} \uparrow \implies \text{PD-L1} \uparrow \implies \text{Silenciamiento Epigenético}$ | Cocultivo monocapa/esferoide bajo LPS ($0.1\text{--}10\,\text{ng/mL}$) o $\text{IL-6}$; cuantificación de STAT3-P, superficie PD-L1 (citometría) y expresión de TOX | $\text{PD-L1} > 4.0\times$ basal; activación de TOX y detención lítica a 48–72 h | Respuesta dosis-dependiente saturable acoplada a la vía JAK/STAT3 | Si la inducción de PD-L1 o el fenotipo exhausto se desacoplan de la concentración de endotoxina/IL-6, **el enlace multiescala local-sistémico es inválido**. |
| **P4** | Existencia de un umbral crítico de integridad de barrera ($\phi_{\text{gut}} \approx 0.90$) para desbloqueo de citólisis activa | Barrido estequiométrico de integridad epitelial / permeabilidad vs. Tiempo de Citólisis Activa (ACT) | Transición de fase no lineal (bifurcación) en la ventana $\phi_{\text{gut}} \in [0.85, 0.92]$ | Curva sigmoidal abrupta con punto de inflexión en el rango predicho | Si la respuesta lítica es lineal y plana sin zona de conmutación umbral, **el umbral de bifurcación es un artefacto matemático**. |

---

### 3. Jerarquía de Ejecución Experimental: Orden de Costo y De-risking (Capa 0 → Capa 4)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        JERARQUÍA EXPERIMENTAL DE-RISKING                               │
└────────────────────────────────────────────────────────────────────────────────────────┘
  │
  ├── CAPA 0: Consistencia Interna & Invariantes In-Silico (Costo: $0)
  │    └── ODEs deterministas, fail-closed policy, análisis de sensibilidad global.
  │
  ├── CAPA 1: El "Experimento Cero" Celular In Vitro (Costo: Mínimo / Placas Estándar)
  │    └── Célula T/CAR-T en gradiente de pH (7.4 vs 6.2) ± Cariporide/EIPA.
  │        Medición: pHi, ATP (Luciferasa/Seahorse) y Killing (Incucyte/LDH) a 3-6h.
  │
  ├── CAPA 2: Eje Sistémico Reducido & Cocultivo 3D (Costo: Medio)
  │    └── Monocapa Caco-2 (TEER) + Hepatocitos/Kupffer + Esferoide tumoral 3D (LPS/IL-6/PD-L1).
  │
  ├── CAPA 3: Validación In Vivo Preclínica (Costo: Alto / Solo si Capas 1 y 2 sobreviven)
  │    └── Modelo murino HCC ortotópico / xenoinjerto: microelectrodos pH, LPS portal, Akkermansia.
  │
  └── CAPA 4: Correlación Clínica Retrospectiva / Ensayos Prospectivos
       └── Biomarcadores en biopsias líquidas/tejido (pH tumoral, LPS sérico, microbiota, IL-6, TOX).
```

---

### 4. Protocolo Detallado del "Experimento Cero" (Capa 1: Wet-Lab Mínimo In Vitro)

Este ensayo constituye el **filtro obligatorio y decisivo**. Si este experimento falla, la hipótesis bioenergética central queda refutada sin necesidad de incurrir en costos de experimentación animal.

#### 4.1 Diseño del Ensayo
* **Población Efectora:** Linfocitos T humanos primarios CD8+ (o CAR-T dirigidos contra GPC3 / antígeno modelo).
* **Condiciones de Medio (Buffer Fosfato-Citrato / MES tamponado a $37^\circ\text{C}$):**
  1. Control Fisiológico: $\text{pH}_e = 7.40 \pm 0.02$.
  2. Acidosis Tumoral Moderada: $\text{pH}_e = 6.60 \pm 0.02$.
  3. Acidosis Tumoral Severa: $\text{pH}_e = 6.20 \pm 0.02$.
* **Brazos de Perturbación Farmacológica / Genética:**
  * Brazo A: T-cells salvajes (WT) control vehículo (DMSO $0.1\%$).
  * Brazo B: T-cells WT + Inhibidor selectivo de NHE1 (Cariporide $10\,\mu\text{M}$ o EIPA $20\,\mu\text{M}$).
  * Brazo C: T-cells transducidas con NHE1 constitutivamente activo (o sobreexpresión funcional).
* **Puntos de Muestreo Temporal ($t$):** $0\,\text{min}$, $30\,\text{min}$, $60\,\text{min}$, $120\,\text{min}$, $180\,\text{min}$, $360\,\text{min}$.

#### 4.2 Métricas Cuantitativas
1. **$\text{pH}_i$ Dinámico:** Sonda ratiométrica BCECF-AM calibrada con nigericina ($10\,\mu\text{M}$) a 5 puntos de pH.
2. **Bioenergética celular:**
   * Cuantificación absoluta de ATP intracelular ($\text{pmol}/10^6\text{ células}$) por bioluminiscencia (CellTiter-Glo).
   * Tasa de acidificación extracelular (ECAR) y consumo de oxígeno (OCR) mediante analizador Seahorse XFe96.
3. **Potencia Lítica / Citotoxicidad:**
   * Co-cultivo con línea celular diana marcada con fluorescencia (ej. Huh-7 GPC3+ vs GPC3-).
   * Cuantificación de lisis tumoral en tiempo real por videomicroscopía Incucyte (área de fluorescencia integrada) o liberación de LDH.

---

### 5. Operacionalización de Parámetros Latentes ($\phi_{\text{gut}}$)

El parámetro adimensional $\phi_{\text{gut}} \in [0.0, 1.0]$ no debe tratarse en el laboratorio como un escalar abstracto, sino que debe mapearse a variables físicas y bioquímicas cuantificables:

| Parámetro Modelo | Variable Biológica Operacionalizada | Técnica de Medición Estándar | Rango Típico Fisiológico ($\phi_{\text{gut}} \approx 1.0$) | Rango Típico Patológico ($\phi_{\text{gut}} \le 0.3$) |
| :--- | :--- | :--- | :--- | :--- |
| $\phi_{\text{gut}}$ (Integridad de barrera) | Resistencia Eléctrica Transepitelial (TEER) en monocapa Caco-2/HT29 | Volt-Ohmímetro Epithelial (EVOM) | $> 400\,\Omega \cdot \text{cm}^2$ | $< 80\,\Omega \cdot \text{cm}^2$ |
| $\phi_{\text{gut}}$ (Permeabilidad macromolecular) | Flujo transepitelial de FITC-Dextrano (4 kDa) | Espectrofluorometría | Permeabilidad aparente $P_{app} < 1 \times 10^{-6}\,\text{cm/s}$ | $P_{app} > 8 \times 10^{-6}\,\text{cm/s}$ |
| $K_{\text{LPS}}$ (Translocación endotoxémica) | Concentración de endotoxina (LPS libre) | Ensayo LAL cromogénico cinético o Recombinant Factor C (rFC) | $< 0.1\,\text{EU/mL}$ ($< 10\,\text{pg/mL}$) | $1.5\text{--}10.0\,\text{EU/mL}$ ($150\text{--}1000\,\text{pg/mL}$) |
| Proxy *Akkermansia* | Abundancia relativa de *Akkermansia muciniphila* | qPCR / Secuenciación 16S rRNA / Metagenómica Shotgun | $3.0\%\text{--}5.0\%$ de la microbiota fecal total | $< 0.01\%$ (indetectable) |
| Inflamación Portal | Concentración de $\text{IL-6}$ en suero o plasma portal | ELISA de alta sensibilidad / Multiplex Luminex | $< 3.0\,\text{pg/mL}$ | $20.0\text{--}150.0\,\text{pg/mL}$ |

---

### 6. Criterios de Rigor Estadístico y Metodología de Validación

Para garantizar validez científica estricta:

1. **Pre-registro Experimental:** Fijar previamente las hipótesis cinéticas y ventanas temporales antes de la recolección de datos ($t = 180\,\text{min}$, $\text{pH}_e = 6.20$).
2. **Réplicas Biológicas vs. Técnicas:** Exigir un mínimo de $N = 3$ donantes biológicos independientes con $n \ge 3$ réplicas técnicas por condición.
3. **Separación Estricta de Datasets (Train vs. Test):**
   * **Dataset de Calibración:** Utilizado exclusivamente para refinar constantes cinéticas ($V_{\max}, K_m, \text{pKa}$).
   * **Dataset de Validación Independiente:** Con las constantes congeladas, se evalúa el poder predictivo del solver bajo condiciones no vistas (ej. gradientes continuos de pH o pulsos cinéticos). **Prohibido el reajuste (*no-refit*) en el set de prueba**.
4. **Métricas de Error Cuantitativo:**
   * Error Cuadrático Medio Normalizado ($NRMSE \le 15\%$).
   * Coeficiente de Determinación ($R^2 \ge 0.85$).
   * Cobertura de Intervalos de Confianza del $95\%$.

---

### 7. Taxonomía de Resultados Posibles

Cualquiera de los siguientes tres escenarios constituye un avance científico legítimo:

* **Escenario A — Calibrado:** La topología de las ODEs es correcta; los datos experimentales permiten sustituir los parámetros de la categoría `[in-silico-only]` o `[assumed]` por valores empíricos definitivos de la categoría `[wet-lab calibrated]`.
* **Escenario B — Parcialmente Válido:** Uno de los frentes (ej. local NHE1/ATP) sostiene la predicción con alta fidelidad, mientras que el frente sistémico (eje LPS/IL-6/PD-L1) requiere acoplamiento con vías no consideradas (ej. TGF-$\beta$ o IFN-$\gamma$).
* **Escenario C — Falsado:** El comportamiento dinámico biológico contradice de raíz las ecuaciones de conservación o los mecanismos de transporte asumidos. Se declara formalmente la refutación de la hipótesis y se rediseña la arquitectura del modelo.
