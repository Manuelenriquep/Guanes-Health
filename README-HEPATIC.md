# Simulador onco-hepático acoplado (v2.0)

Manual operativo del acoplamiento hepatocito–tumor–inmune en este repositorio.  
Guanes Health — prototipo *in silico* (instrumento de placa).

**Alcance:** cribado de hipótesis sobre un modelo determinista. No es consejo médico ni evidencia clínica.

---

## 1. Qué modela

El stack acopla, en Capa B (toy model parametrizado):

- hepatocito sinusoidal (`simulador_hepatocito_infeccion.py`): O₂ → NTCP, HBV, Myrcludex B, veto GSH (`VETO FC-HEP-01`);
- tumor / estroma (`simulador_onco_homeostasis_v4.py` vía acoplamiento v2; dinámica standalone canónica: `…_v5.py`): metabolismo, pHe, checkpoints;
- bucle paracrino (`simulador_onco_hepatico_v2.py`): IL-6 → STAT3 → PD-L1 tumoral.

`simulador_onco_hepatico_v3.py` está **ausente (WIP)**; no forma parte del stack ejecutable.

Madurez global del motor: [`01_Especificaciones_SSoT/madurez_artefactos_motor.md`](01_Especificaciones_SSoT/madurez_artefactos_motor.md).  
Mapa SSoT: [`01_Especificaciones_SSoT/ssot_framework_map-v3.md`](01_Especificaciones_SSoT/ssot_framework_map-v3.md).  
El **núcleo canónico** (demo README) es `placa_*` + `parche_restauracion.py` (Gated-6.50); esta línea es el **acoplamiento canónico vigente** (v2).

---

## 2. Mapa de archivos

### Motores (`03_Motor_Oncologico/`)

| Archivo | Madurez | Rol |
|---------|---------|-----|
| `simulador_onco_homeostasis_v5.py` | Canónico (dinámica standalone) | MCT/inmuno + Gated-6.50 |
| `simulador_onco_homeostasis_v4.py` | Histórico (dinámica); aún dependencia de acoplamiento v2 | Célula sana/tumoral usada por `hepatico_v2` |
| `simulador_hepatocito_infeccion.py` | Canónico (hepático) | Hepatocito + HBV / NTCP / Myrcludex |
| `simulador_onco_hepatico_v2.py` | Canónico (acoplamiento) | Acoplamiento bidireccional IL-6 / PD-L1 |
| `simulador_onco_hepatico_v3.py` | **WIP / ausente** | No existe en el repo |
| `grafico_dinamica_temporal.py` | Experimental (visual) | Trayectoria IL-6 / PD-L1 y \(t_{\mathrm{escape}}\) modelado |
| `simulador_cointervencion_escenarios.py` | Experimental | Comparativa de 4 escenarios |
| `simulador_s267f_toxicidad.py` | Experimental | Barrido Myrcludex WT vs S267F |
| `simulador_cart_hcc_interaccion.py` | Experimental | Toy model CAR-T/HCC |
| `analisis_sensibilidad_local_cart.py` | Experimental | Barrido local 1D/2D |
| `simulador_onco_homeostasis.py` … `_v3.py` | Histórico | No ampliar → usar `_v5` para dinámica nueva |
| `simulador_onco_hepatico_v1.py` | Histórico | No ampliar → usar `_v2` |

### Tests (`04_Bateria_Inviolable/`)

| Archivo | Rol |
|---------|-----|
| `test_simulador_onco_hepatico_v2.py` | Regresión numérica de los 4 escenarios acoplados |
| `test_cart_hcc_interaccion.py` | Fronteras numéricas CAR-T (incl. RESOLVED-B-01/02) |
| `test_analisis_sensibilidad_local_cart.py` | Fronteras del barrido local CAR-T |
| `run_tests_pipeline.py` | Suite completa del repo |

Ledger / mapa: `01_Especificaciones_SSoT/madurez_artefactos_motor.md`, `ledger_parametros_nucleo.md`, `ledger_parametros_cart_hcc.md`, `ssot_framework_map-v3.md`.

### Figuras (`02_Simulaciones_Visuales/`)

- `dinamica_temporal_il6_pdl1.png`
- `cointervencion_escenarios.png`
- `analisis_toxicidad_s267f.png`
- `sensibilidad_local_cart_hcc.png`

---

## 3. Ecuaciones del modelo (Capa B)

Constantes del simulador; anclaje bibliográfico en `01_Especificaciones_SSoT/`. No están calibradas empíricamente contra wet-lab en este repo.

### NTCP bajo IL-6

$$\mathrm{Densidad}_{NTCP}(t) = \mathrm{Densidad}_{basal} \cdot \left( 1.0 - 0.98 \cdot \frac{[IL\text{-}6](t)}{[IL\text{-}6](t) + 50.0} \right)$$

Variante **S267F**: densidad de membrana forzada a `0.0` (sin entrada viral modelada; sin aclaramiento biliar por NTCP).

### Myrcludex B (competencia)

$$\mathrm{FraccionBloqueo}_{viral} = \frac{1.0}{1.0 + [\mathrm{Myrcludex}]/(1.0\,\mathrm{nM})}$$

$$\mathrm{FraccionBloqueo}_{biliar} = \frac{1.0}{1.0 + [\mathrm{Myrcludex}]/(100.0\,\mathrm{nM})}$$

### Veto colestasis (`VETO FC-HEP-01`)

$$\mathrm{Aclaramiento} = \mathrm{Densidad}_{NTCP}(t) \cdot \mathrm{FraccionBloqueo}_{biliar}$$

Si aclaramiento &lt; `0.15`, GSH cae a `0.5 mM/h`. Si GSH &lt; 30% nominal (&lt; `2.4 mM`), se dispara apoptosis modelada (MOMP).

### Feedback IL-6 → PD-L1

$$[IL\text{-}6](t) = 2.0 \cdot \mathrm{CargaViral}(t) + 100.0 \cdot (1.0 - \mathrm{ViabilidadHepatocito}(t))$$

$$\mathrm{PD\text{-}L1}_{tumor}(t) = 50.0 + \beta \cdot [IL\text{-}6](t)$$

Con \(\beta = 3.0\) (feedback pleno) o \(\beta = 0.1\) (proxy de atenuación IL-6/STAT3 en el Escenario 4). Si PD-L1 ≥ `150.0`, la eficacia anti-PD-1 modelada cae a `0`.

---

## 4. Ejecución

Python 3.12+, `numpy`, `matplotlib`. Desde la raíz del repo:

```bash
py -3 03_Motor_Oncologico/simulador_cointervencion_escenarios.py
py -3 03_Motor_Oncologico/grafico_dinamica_temporal.py
py -3 03_Motor_Oncologico/simulador_s267f_toxicidad.py
```

Salidas gráficas → `02_Simulaciones_Visuales/`.

---

## 5. Tests

```bash
py -3 04_Bateria_Inviolable/test_simulador_onco_hepatico_v2.py
py -3 04_Bateria_Inviolable/test_cart_hcc_interaccion.py
py -3 04_Bateria_Inviolable/run_tests_pipeline.py
```

El arnés **aserte** salidas del modelo (no “certifica” biología). Umbrales esperados bajo los parámetros actuales:

| Test | Condición modelada |
|------|--------------------|
| `test_coupled_unidirectional_clearance` | Cohorte C, sin feedback → viabilidad tumor/hepatocito → 0 |
| `test_coupled_mct2_sanctuary` | MCT2 on → pHe ≈ 6.65, viabilidades 1.0, carga viral alta |
| `test_coupled_bidirectional_feedback_escape` | Feedback \(\beta=3\) → IL-6 y PD-L1 altos, escape tumoral |
| `test_coupled_cointervention_clearance` | Myrcludex 10 nM + \(\beta=0.1\) → viabilidad tumoral 0, GSH &gt; 5 |

---

## 6. Límites

- Simplificación determinista de un sistema biológico estocástico.
- No usar para decisiones clínicas ni diseño de tratamiento real.
- Hipótesis emergentes requieren validación experimental independiente.

Ver también: `01_Especificaciones_SSoT/placa_base_instrumento_investigacion.md`.
