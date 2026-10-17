# 📑 Documentación Técnica: Motor Bioeléctrico, Cinética Estromal y Kernel Nivel 0
**Single Source of Truth (SSoT) — Guanes Health**  
*Fecha de consolidación:* Octubre 2026  
*Repositorio de código:* `c:\GuanesHealth\Guanes Health\03_Motor_Oncologico`  
*Batería de pruebas:* `c:\GuanesHealth\Guanes Health\04_Bateria_Inviolable` (18 suites PASS)

---

### 1. Propósito de esta Documentación
Este documento compila de forma modular y autosuficiente los modelos matemáticos, las ecuaciones cinéticas, las constantes físicas y las reglas de bioseguridad en silicio desarrolladas para el ecosistema de **Guanes Health**. Sirve como referencia técnica directa para la posterior redacción de capítulos teóricos y publicaciones científicas.

---

### 2. Frente Bioeléctrico: Potencial de Membrana y Redes Conexinas
*Implementación:* [`guanes_bioelectrico.py`](file:///C:/GuanesHealth/Guanes%20Health/03_Motor_Oncologico/guanes_bioelectrico.py)  
*Pruebas:* [`test_guanes_bioelectrico.py`](file:///C:/GuanesHealth/Guanes%20Health/04_Bateria_Inviolable/test_guanes_bioelectrico.py)

#### 2.1 Ecuación de Goldman-Hodgkin-Katz (GHK)
Modela el potencial transmembrana en reposo ($V_{mem}$) en función de la permeabilidad y concentración de los iones principales ($K^+$, $Na^+$, $Cl^-$) a $T = 310.15\text{ K}$ ($37^\circ\text{C}$):

$$V_{mem} = \frac{RT}{F} \ln \left( \frac{P_{K}[K^+]_e + P_{Na}[Na^+]_e + P_{Cl}[Cl^-]_i}{P_{K}[K^+]_i + P_{Na}[Na^+]_i + P_{Cl}[Cl^-]_e} \right)$$

* Constante térmica: $\frac{RT}{F} \approx 26.725\text{ mV}$.
* Estado diferenciado sano: $P_{Na}/P_K = 0.04 \implies V_{mem} \approx -72.0\text{ mV}$.
* Estado despolarizado oncogénico: $P_{Na}/P_K \ge 0.70 \implies V_{mem} \ge -25.0\text{ mV}$ (típicamente $-15\text{ mV}$).

#### 2.2 Conductancia de Conexinas Homotípicas (Cx43)
La comunicación intercelular por uniones gap decae ante diferencias pronunciadas de potencial entre células vecinas ($\Delta V_{mem} = |V_A - V_B|$):

$$G_{GJ}(\Delta V) = G_{min} + \frac{G_{max} - G_{min}}{1 + \exp\left(a \cdot (|\Delta V| - V_0)\right)}$$

* Parámetros: $G_{min} = 0.05$, $G_{max} = 1.00$, $V_0 = 25.0\text{ mV}$, $a = 0.15\text{ mV}^{-1}$.

#### 2.3 Dinámica en Retícula y Cono Cognitivo de Luz ($\Phi_{cone}$)
* La retícula espacial resuelve la difusión electrotónica:
  $$\frac{dV_i}{dt} = \frac{1}{C_m} \sum_{j \in N(i)} g_{gap, ij} (V_j - V_i)$$
* **Teorema de la Patología Única (Smaller Selves):** Células con $V_{mem} \ge -25\text{ mV}$ y $G_{GJ} < 0.20$ quedan aisladas computacionalmente del órgano y revierten a un fenotipo amebiano mitótico.
* **Normalización Bioeléctrica (Levin):** La hiperpolarización forzada ($V_{mem} \to -75\text{ mV}$) y reapertura de conexinas ($G_{GJ} \to 0.85$) disuelve los *smaller selves* y restaura el cono cognitivo:
  $$\Phi_{cone} = \left(\frac{N_{acoplados}}{N_{total}}\right) \cdot \exp\left(-\frac{\sigma_{V}}{15.0}\right)$$

---

### 3. Frente Biofísico: Cinética Estromal y Eje Gut-Liver-Immune
*Implementación:* [`guanes_biofisica.py`](file:///C:/GuanesHealth/Guanes%20Health/03_Motor_Oncologico/guanes_biofisica.py)  
*Pruebas:* [`test_guanes_biofisica.py`](file:///C:/GuanesHealth/Guanes%20Health/04_Bateria_Inviolable/test_guanes_biofisica.py)

#### 3.1 Cinética de Extrusión de Protones por NHE1
$$J_{NHE1} = V_{max} \cdot f_{alostérico}(pH_i) \cdot f_{contrapresión}(pH_e) \cdot f_{voltaje}(V_{mem})$$

* Sensor alostérico intracelular:
  $$f_{alostérico} = \frac{1}{1 + 10^{n_H \cdot (pH_i - pK_a)}} \quad (pK_a = 6.45, \ n_H = 2.8)$$
* Contrapresión ácida estromal ($pH_e = 6.20$ a $6.50$):
  $$f_{contrapresión} = \frac{1}{1 + 10^{5.991 - pH_e}}$$

#### 3.2 Inhibición Alostérica Cuaternaria de PFK-1
La enzima marcapasos de la glucólisis se apaga al acidificarse el citosol:

$$\frac{v_{PFK}}{V_{max}} = \frac{1}{1 + 10^{n_H \cdot (pK_a - pH_i)}} \times 100\% \quad (pK_a = 6.80, \ n_H = 4.0)$$

#### 3.3 Trampa Bioeléctrica del Ácido
Condición: $V_{mem} \le -60\text{ mV}$ en $pH_e \le 6.50$ con $pH_i \le 6.80$.  
Efecto: El influjo forzado de $H^+$ apaga la PFK-1 y colapsa el ATP citosólico a $< 15\%$, induciendo muerte metabólica selectiva.

#### 3.4 Eje Entero-Hepático-Inmune
* Integridad de mucosa:
  $$\phi_{gut} = 0.3 \cdot \min\left(1, \frac{TEER}{1000}\right) + 0.7 \cdot \frac{1}{1 + \exp(-2(Akk - 1.5))}$$
* Translocación de endotoxina portal ($LPS$):
  $$LPS_{portal} = 0.05 + 15.0 \cdot (1 - \phi_{gut})^2 \quad [\text{ng/mL}]$$
* Activación de $IL\text{-}6$ y cascada $p\text{-STAT3} \to PD\text{-}L1$:
  $$PDL1_{factor} = 1.0 + 15.0 \cdot \left(\frac{IL6}{IL6 + 300}\right)$$

---

### 4. Orquestador Kernel Nivel 0: Inferencia Activa y Bioseguridad
*Implementación:* [`guanes_kernel_level0.py`](file:///C:/GuanesHealth/Guanes%20Health/03_Motor_Oncologico/guanes_kernel_level0.py)  
*Pruebas:* [`test_guanes_kernel_level0.py`](file:///C:/GuanesHealth/Guanes%20Health/04_Bateria_Inviolable/test_guanes_kernel_level0.py)

#### 4.1 Descenso de Energía Libre Variacional ($F \to 0$)
Cuantifica la discrepancia informacional entre el estado actual y el atractor homeostático:

$$F(\mathbf{x}) = w_v (V_{mem} - V^*)^2 + w_\phi (\phi_{gut}^* - \phi_{gut})^2 + w_{atp} (ATP^* - ATP)^2 + w_{pdl1} (PDL1 - 1.0)^2$$

* La trayectoria óptima minimiza la acción de Hamilton: $\delta S = \delta \int F \, dt = 0$.

#### 4.2 Matriz de Exclusiones Fail-Closed de Bioseguridad
* **`FC-BIO-01`:** Veto si $\phi_{gut} < 0.899$ (disbiosis / endotoxemia portal).
* **`FC-BIO-02`:** Veto si $ATP < 15.0\%$ en tejido sano (toxicidad metabólica letal).
* **`FC-BIO-03`:** Veto si $V_{mem} \ge -25\text{ mV}$ (persistencia de Smaller Self oncogénico).
* **`FC-BIO-04`:** Veto si $PD\text{-}L1 > 5.0\times$ o índice $TOX > 0.80$ (inmunosupresión o agotamiento tumoral irreversible).

#### 4.3 Trazabilidad Criptográfica SHA-256
Cada dictamen emite un hash SHA-256 inmutable que garantiza la reproducibilidad determinista $O(1)$ en tiempo inferior a $0.01\text{ ms}$.

---

### 5. Frente Farmacocinético / Farmacodinámico (PK/PD Cuantitativo)
*Implementación:* [`guanes_pkpd.py`](file:///C:/GuanesHealth/Guanes%20Health/03_Motor_Oncologico/guanes_pkpd.py)  
*Pruebas:* [`test_guanes_pkpd.py`](file:///C:/GuanesHealth/Guanes%20Health/04_Bateria_Inviolable/test_guanes_pkpd.py)

#### 5.1 Fármacos y Biológicos Modelados
1. **Cariporida (HOE-642) — Inhibidor de NHE1:**
   * Masa Molar: $371.84\text{ g/mol}$, $V_d = 1.4\text{ L/kg}$, $t_{1/2} = 4.5\text{ h}$ ($k_e \approx 0.154\text{ h}^{-1}$).
   * Afinidad $IC_{50} = 0.05\ \mu\text{M}$ ($50\text{ nM}$).
   * Límite de seguridad MTD: $5.0\ \mu\text{M}$.
2. **PQ1 — Modulador alostérico de Conexina 43 (Cx43):**
   * $EC_{50} = 0.12\ \mu\text{M}$ ($120\text{ nM}$), $t_{1/2} = 6.0\text{ h}$, $E_{max} = 0.90$.
   * Límite de seguridad MTD: $10.0\ \mu\text{M}$.
3. **Akkermansia muciniphila (Biológico Luminal) + Inulina:**
   * Cinética logística luminal: $\frac{dN}{dt} = r N (1 - \frac{N}{K}) - k_{wash} N$.
   * $r_{max} = 0.28\text{ h}^{-1}$, $k_{wash} = 0.05\text{ h}^{-1}$, $K = 1.0$ (saturación eubiótica).
4. **Buffer Tris / Bicarbonato:**
   * Amortiguación de $pH_e$ con neutralización de protones y decaimiento sistémico ($t_{1/2} = 2.0\text{ h}$).

#### 5.2 Invariantes Fail-Closed Farmacológicas
* **`FC-PKPD-01`:** Dosis negativas, NaN o infinitas disparan `ValueError` y veto inmediato.
* **`FC-PKPD-02`:** Concentración pico que supere la dosis máxima tolerable ($C_{max} > \text{MTD}$) dispara veto Fail-Closed sin ejecución.
* **Trazabilidad:** Cada punto en la trayectoria temporal $(t, C, E)$ está encadenado criptográficamente con SHA-256.

---

### 6. Extensión Tridimensional Esferoidal: `BioelectricLattice3D`
*Implementación:* [`guanes_bioelectrico_3d.py`](file:///C:/GuanesHealth/Guanes%20Health/03_Motor_Oncologico/guanes_bioelectrico_3d.py)  
*Pruebas:* [`test_guanes_bioelectrico_3d.py`](file:///C:/GuanesHealth/Guanes%20Health/04_Bateria_Inviolable/test_guanes_bioelectrico_3d.py)

#### 6.1 Tres Capas Histológicas Concéntricas
1. **Núcleo Necrótico Central ($r \le R_{necrotic}$):**
   * Anoxia severa ($pO_2 < 2\text{ mmHg}$), colapso de glucosa, acidosis extrema ($pH_e \le 6.40$), despolarización oncogénica persistente ($V_{mem} \ge -15\text{ mV}$) y conexinas selladas ($G_{GJ} \le 0.05$).
2. **Zona Intermedia Hipóxica / Quiescente ($R_{necrotic} < r \le R_{quiescent}$):**
   * Hipoxia moderada ($pO_2 \approx 10\text{ mmHg}$), glucólisis acelerada, $V_{mem} \approx -22\text{ mV}$ ("Smaller Self"), conexinas desacopladas ($G_{GJ} \approx 0.12$). Es la zona diana de normalización bioeléctrica.
3. **Borde Proliferativo / Invasivo Exterior ($R_{quiescent} < r \le R_{max}$):**
   * Normoxia por perfusión capilar exterior ($pO_2 \approx 38\text{ mmHg}$), glucosa $4.5\text{ mM}$, mayor estabilidad estromal.

#### 6.2 PDE de Reacción-Difusión 3D
* **Oxígeno:**
  $$\frac{\partial pO_2}{\partial t} = D_{O_2} \nabla^2 (pO_2) - V_{max, O_2} \frac{pO_2}{K_m + pO_2}$$
  con $D_{O_2} = 1.8 \times 10^{-3}\text{ mm}^2/\text{s}$, $K_m = 2.5\text{ mmHg}$.
* **Difusión Electrotónica por Uniones Gap 3D:**
  $$\frac{dV_i}{dt} = \frac{1}{C_m} \sum_{j \in \text{vecinos 3D}} G_{GJ, ij} (V_j - V_i)$$
* **Cono Cognitivo Tridimensional ($\Phi_{3D}$):**
  $$\Phi_{3D} = \left(\frac{V_{\text{acoplado}}}{V_{\text{total}}}\right) \exp\left(-\frac{\sigma(V_{mem})}{15.0}\right), \quad R_{\text{efectivo}} = \left(\frac{3 V_{\text{acoplado}}}{4 \pi}\right)^{1/3}$$
* **Sello SHA-256 Volumétrico:** Huella criptográfica inmutable del tensor tridimensional completo.

---

### 7. Motor de Renderizado Cinematográfico y Dashboard de Alta Fidelidad
*Implementación:* [`guanes_visualizer.py`](file:///C:/GuanesHealth/Guanes%20Health/02_Simulaciones_Visuales/guanes_visualizer.py)  
*Pruebas:* [`test_guanes_visualizer.py`](file:///C:/GuanesHealth/Guanes%20Health/04_Bateria_Inviolable/test_guanes_visualizer.py)  
*Artefacto Gráfico:* [`guanes_health_comprehensive_dashboard.png`](file:///C:/GuanesHealth/Guanes%20Health/02_Simulaciones_Visuales/guanes_health_comprehensive_dashboard.png)

#### 7.1 Estructura del Instrumento Visual (9 Cuadrantes en Grid 3x3)
1. **Fila 1 (Microambiente 3D y Levin Normalization):**
   * *Cuadrante 1.1:* Mapa de calor de $V_{mem}$ sagital pre-tratamiento (fragmentación oncogénica / *Smaller Self*).
   * *Cuadrante 1.2:* Mapa de calor de $V_{mem}$ post-rescate bioeléctrico de Levin (repolarización e integración de sincitio).
   * *Cuadrante 1.3:* Gradiente radial de difusión de $pO_2$ tras reacción-difusión en 3D.
2. **Fila 2 (Monitor Farmacocinético y Farmacodinámico PK/PD):**
   * *Cuadrante 2.1:* Curva temporal $C(t)$ de Cariporida contrastada contra $IC_{50}$ y el límite máximo seguro MTD.
   * *Cuadrante 2.2:* Curva temporal $C(t)$ del modulador de conexinas PQ1 contrastada contra $EC_{50}$.
   * *Cuadrante 2.3:* Curva logística de colonización de *Akkermansia muciniphila* y $\Delta pH_e$ estromal por amortiguador.
3. **Fila 3 (Consola de Invariantes y Bioseguridad Level 0):**
   * *Cuadrante 3.1:* Histograma del Cono Cognitivo 3D (vóxeles acoplados vs. células aisladas).
   * *Cuadrante 3.2:* Comparativa multivariable de convergencia homeostática ($ATP$, $\phi_{gut}$, $PD\text{-}L1$).
   * *Cuadrante 3.3:* Certificado determinista *Correct by Construction* con latencia de silicio ($< 1\text{ ms}$), estado de cortafuegos `FC-BIO-01` a `04`, `FC-PKPD-01` a `02` y firma criptográfica SHA-256 inmutable.

---

### 8. Batería de Pruebas de Estrés y Sensibilidad Multimórbida
*Implementación y Pruebas:* [`guanes_stress_tests.py`](file:///C:/GuanesHealth/Guanes%20Health/04_Bateria_Inviolable/guanes_stress_tests.py)

#### 8.1 Ensayos Límite y Mutaciones Farmacológicas Evaluadas
1. **Mutación de Resistencia en Conexinas Cx43:**
   * *Mecanismo:* Pérdida de afinidad a moduladores alostéricos (PQ1), impidiendo la apertura de uniones gap.
   * *Respuesta Inviolable:* **Veto `FC-BIO-03`** (Detección mecánica de persistencia de *Smaller Self* despolarizado en $V_{mem} \ge -25\text{ mV}$).
2. **Acidosis Estromal Refractaria Crítica ($pH_e < 5.80$):**
   * *Mecanismo:* Saturación extrema de protones extracelulares con repolarización forzada, activando la trampa de ácido protón-motriz.
   * *Respuesta Inviolable:* **Veto `FC-BIO-02`** (Interrupción por colapso metabólico de $ATP < 15.0\%$).
3. **Sobredosis Masiva de Cariporida ($250\text{ mg}$):**
   * *Mecanismo:* $C_{max} \approx 5.83\ \mu\text{M}$ superando el umbral de máxima tolerancia ($\text{MTD} = 5.0\ \mu\text{M}$).
   * *Respuesta Inviolable:* **Veto `FC-PKPD-02`** (Bloqueo preventivo por toxicidad off-target sistémica).
4. **Colapso Mucosal y Ruptura de Barrera Intestinal ($TEER < 200\ \Omega$):**
   * *Mecanismo:* Agotamiento de *Akkermansia muciniphila* y lisis de uniones estrechas.
   * *Respuesta Inviolable:* **Veto `FC-BIO-01`** (Veto instantáneo por caída de $\phi_{gut} < 0.899$ y translocación endotóxica de $LPS$).

#### 8.2 Métricas de Bioseguridad en Silicio
* **Tasa de Detección y Veto:** $100.0\%$ (4/4 escenarios mórbi-tóxicos neutralizados).
* **Falsos Negativos:** $0.0\%$.
* **Latencia de Decisión:** $\le 0.001\text{ s}$ por dictamen.




