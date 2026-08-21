# Reporte: feedback recíproco hepatocito–tumor (v2.0)

Especificación operativa del bucle IL-6 → STAT3 → PD-L1 en `simulador_onco_hepatico_v2.py`.  
Guanes Health — modelo *in silico* (Capa B).

Declaración: cribado de hipótesis sobre instrumento de placa — no consejo médico ni evidencia clínica.

---

## 1. Resumen

Hasta v1, el acoplamiento era mayormente unidireccional (estroma tumoral → hepatocito).  
En v2 se añade el bucle recíproco: infección/lisis hepática → IL-6 → inducción de PD-L1 tumoral, que puede saturar anti-PD-1 *en el modelo* y permitir escape tumoral simulado pese a Cohorte C.

Esto documenta ecuaciones y escenarios numéricos del código. No demuestra eficacia clínica.

---

## 2. Ecuaciones de acoplamiento (Capa B)

### A. IL-6 paracrina

$$\mathrm{IL\text{-}6}(t) = 2.0 \cdot \mathrm{carga\_viral}(t) + 100.0 \cdot (1.0 - \mathrm{viabilidad\_hepatocito}(t))$$

### B. PD-L1 tumoral (proxy STAT3)

$$\mathrm{PD\_L1}(t) = 50.0 + \beta \cdot \mathrm{IL\text{-}6}(t)$$

### C. Eficiencia CD8+ bajo IL-6

$$\mathrm{eficiencia\_cd8}(t) = \mathrm{eficiencia\_basal}(t) \cdot \left(\frac{1.0}{1.0 + \mathrm{IL\text{-}6}(t)/10.0}\right)$$

### D. Saturación anti-PD-1

Si \(\mathrm{PD\text{-}L1} \ge 150.0\) (basal tumoral no inflamado = 50), la eficacia anti-PD-1 modelada cae a `0.0`.

---

## 3. Escenarios a \(t = 72\,\mathrm{h}\) (salidas típicas del motor)

### Escenario 1 — Unidireccional (sin feedback)

`feedback_activo=False`, `mutacion_mct2=False` → pHe ≈ 7.35; viabilidad tumor y hepatocito → 0 en el modelo.

### Escenario 2 — Escape MCT2

`mutacion_mct2=True` → pHe ≈ 6.65; CD8+ deprimidos; hepatocito y tumor viables; carga viral elevada (santuario *modelado*).

### Escenario 3 — Feedback activo

`feedback_activo=True`, \(\beta=3.0\) → IL-6 y PD-L1 altos; escape tumoral parcial (p. ej. ~20% viabilidad) en el modelo.

---

## 4. Regresión

Suite canónica: `04_Bateria_Inviolable/test_simulador_onco_hepatico_v2.py`.

Las aserciones fijan umbrales numéricos del simulador (IL-6, PD-L1, viabilidades). No validan biología wet-lab.

---

## 5. Límites

Abstracción determinista. Sin validez predictiva en pacientes. Hipótesis del bucle IL-6/STAT3/PD-L1 requieren contraste experimental independiente.
