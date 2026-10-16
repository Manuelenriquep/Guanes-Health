# Placa Base de Subversión y Normalización Bioeléctrica (5 Niveles Cartesanos)

**Versión:** `v1.0.0-SSoT` (Inmutable — Acoplamiento Electroquímico Guanes Health + Michael Levin)  
**Estado:** **NORMATIVO (Capa B Validada In-Silico)**  
**Ecosistema:** Guanes Health (`01_Especificaciones_SSoT`) ↔ Obra Matriz *La Física de la Libertad* (Capítulo 2, Sección 2.5)

---

## NIVEL I — Axiomas de Dominio e Invariantes *Fail-Closed*

Todo modelo o simulación de reversión fenotípica tumoral mediante modulación bioeléctrica y control de pH estromal debe satisfacer de forma estricta los siguientes invariantes termodinámicos y electroquímicos:

* **`FC-BIO-01` (Frontera de Viabilidad de Membrana):** El potencial transmembrana $V_m(t)$ debe permanecer acotado en el intervalo fisiológico $[-95.0\text{ mV}, -5.0\text{ mV}]$. Cualquier excursión fuera de este rango invalida la simulación por lisis osmótica o electroporación irreversible.
* **`FC-BIO-02` (Conservación de Conductancia Sincitial):** La conductancia normalizada de las uniones comunicantes (*gap junctions*, $GJC(t)$, mediada por Conexina 43) pertenece estrictamente a $[0.0, 1.0]$.
* **`FC-BIO-03` (Termodinámica de la Fuerza Protón-Motriz $\Delta \mu_{H^+}$):** Ninguna bomba optogenética extractora de protones (*Arch* / *Archaerhodopsin*) puede modelarse con cinética constante independiente del pH extracelular ($pH_e$). En un microambiente tumoral ácido ($pH_e = 6.20$, frente a $pH_i \approx 7.35$), el gradiente químico de protones ($\Delta pH = pH_i - pH_e = +1.15$) genera una **retropresión electroquímica** opuesta a la extrusión de $H^+$:
  $$\Delta \mu_{H^+} = F \cdot V_m - 2.303 \cdot R \cdot T \cdot (pH_i - pH_e)$$
* **`FC-BIO-06` (Degradación de la Constante de Tiempo Optogenética $\tau_{\text{opto}}$):** La constante de relajación hacia el potencial de hiperpolarización objetivo ($V_{m,\text{target}} = -75.0\text{ mV}$) se alarga proporcionalmente a la acidez extracelular:
  $$\tau_{\text{opto}}(pH_e) = \tau_0 \cdot \left( 1.0 + \kappa_{pH} \cdot \max(0, 7.35 - pH_e) \right)$$
* **`FC-BIO-07` (Compuerta Epigenética de Butirato / HDAC1):** La represión de la histona desacetilasa 1 (HDAC1) y la consiguiente caída de la expresión oncogénica ($E_{\text{onco}}$) requieren superar el umbral bioeléctrico de hiperpolarización ($V_m < -55.0\text{ mV}$) acoplado al transporte cooperativo de segundos mensajeros vía $GJC$.
* **`FC-BIO-08` (Honestidad Epistemológica — Primer Principio de Feynman):** Queda prohibido presentar los resultados del modelo de ecuaciones diferenciales ordinarias (ODE) como datos de ensayo clínico humano. Su estatus ontológico exacto es **prueba de concepto computacional (*in-silico*)** fundamentada en parámetros biofísicos publicados (Chernet & Levin, 2013/2014; Webb et al., 2011; Ecuación de Goldman-Hodgkin-Katz).

---

## NIVEL II — Arquitectura del Sistema Acoplado (4 Estados Continuos)

El acoplamiento entre el microambiente metabólico de **Guanes Health** y el software morfogénico de **Michael Levin** se define sobre el vector de estado $\mathbf{x}(t) = [pH_e(t),\, V_m(t),\, GJC(t),\, E_{\text{onco}}(t)]^T$ para $t \in [0, 48\text{ h}]$:

1. **Neutralización del Estroma Ácido (Intervención *NHE1-Shield*):**
   $$\frac{dpH_e}{dt} = u_{\text{NHE1}} \cdot k_{pH} \cdot \left( pH_{e,\text{target}} - pH_e(t) \right)$$
2. **Dinámica del Potencial de Membrana ($V_m$) bajo Retropresión Protónica:**
   $$\frac{dV_m}{dt} = u_{\text{opto}} \cdot \frac{V_{m,\text{eff}}(pH_e) - V_m(t)}{\tau_0 \cdot \left[ 1 + \kappa_{pH} \cdot \max(0, 7.35 - pH_e(t)) \right]}$$
3. **Restauración de la Red de Conexinas ($GJC$):**
   $$\frac{d(GJC)}{dt} = u_{\text{gap}} \cdot k_{\text{gap}} \cdot \left( GJC_{\text{eff}}(pH_e) - GJC(t) \right)$$
4. **Transducción Epigenética a Expresión Oncogénica ($E_{\text{onco}}$ vía HDAC1):**
   $$\frac{dE_{\text{onco}}}{dt} = -\left( \lambda_V \cdot f_{\text{hiper}}(V_m) + \lambda_{\text{gap}} \cdot GJC(t) \cdot f_{\text{hiper}}(V_m) \right) E_{\text{onco}}(t) + \gamma_{\text{basal}} \cdot \left( 1 - E_{\text{onco}}(t) \right)$$

---

## NIVEL III — Parámetros Canónicos Calibrados (Ledger de Trazabilidad)

| Parámetro | Símbolo | Valor Canónico | Unidad | Fundamento Biofísico / Referencia |
| :--- | :---: | :---: | :---: | :--- |
| Potencial tumoral basal ($KRAS^{G12D}$) | $V_{m,0}$ | $-15.16$ | $\text{mV}$ | Chernet & Levin (2013), despolarización mitótica |
| Potencial somático diferenciado | $V_{m,\text{target}}$ | $-75.00$ | $\text{mV}$ | Levin (2014, 2021), atractor morfogenético sano |
| pH extracelular tumoral basal | $pH_{e,0}$ | $6.20$ | u. pH | Webb et al. (2011), *Nat. Rev. Cancer* (efecto Warburg / NHE1) |
| pH extracelular homeostático | $pH_{e,\text{target}}$ | $7.38$ | u. pH | Fisiología intersticial normalizada |
| Conductancia $GJC$ tumoral aislada | $GJC_0$ | $0.10$ | adim. | Cierre de Conexina 43 por fosforilación oncogénica |
| Conductancia $GJC$ sincitial sana | $GJC_{\text{target}}$ | $0.85$ | adim. | Acoplamiento electroquímico tisular restaurado |
| Constante de tiempo optogenética base | $\tau_0$ | $3.20$ | $\text{h}$ | Cinética de hiperpolarización sostenida sin freno ácido |
| Coeficiente de retropresión protónica | $\kappa_{pH}$ | $3.60$ | $\text{u. pH}^{-1}$ | Penalización termodinámica por $\Delta \mu_{H^+}$ adverso |
| Tasa de represión epigenética por $V_m$ | $\lambda_V$ | $0.04855$ | $\text{h}^{-1}$ | Bloqueo de transporte Na+/Butirato $\to$ inhibición HDAC1 |
| Tasa de supresión cooperativa por $GJC$ | $\lambda_{\text{gap}}$ | $0.05640$ | $\text{h}^{-1}$ | Difusión intercelular de señales morfogenéticas (cAMP/IP3) |

---

## NIVEL IV — Matriz de Resultados de la Cohorte Virtual ($t = 48\text{ h}$)

| Brazo Experimental (*In-Silico*, 48 h) | $pH_e(48\text{h})$ | $V_m(48\text{h})$ | $GJC(48\text{h})$ | Expresión Oncogénica $E_{\text{onco}}$ | Integración Tisular $I_{\text{tisular}}$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Control Negativo ($KRAS^{G12D}$)** | $6.20$ | $-15.16\text{ mV}$ | $0.10$ | **$100.0\%$** | **$0.0\%$** |
| **2. Optogenética Aislada en Ácido** | $6.20$ | $-62.79\text{ mV}$ | $0.10$ | **$36.2\%$** | **$5.8\%$** |
| **3. Levin Canónico (Sin Blindaje pH)** | $6.20$ | $-62.79\text{ mV}$ | $0.73$ | **$19.1\%$** | **$53.6\%$** |
| **4. Sinergia Guanes Health + Levin** | **$7.38$** | **$-75.00\text{ mV}$** | **$0.85$** | **$5.1\%$** | **$84.8\%$** |

---

## NIVEL V — Trazabilidad de Artefactos Reproducibles

* **Motor de Simulación Python:** [`../03_Motor_Oncologico/simulador_normalizacion_bioelectrica.py`](../03_Motor_Oncologico/simulador_normalizacion_bioelectrica.py)
* **Gráfico Multipanel 300 DPI:** [`../02_Simulaciones_Visuales/grafico_normalizacion_bioelectrica.png`](../02_Simulaciones_Visuales/grafico_normalizacion_bioelectrica.png)
* **Reporte Cuantitativo SSoT:** [`./reporte_normalizacion_bioelectrica.md`](./reporte_normalizacion_bioelectrica.md)
