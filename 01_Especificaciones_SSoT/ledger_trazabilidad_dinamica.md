# Ledger de parámetros — dinámica v5 / acoplamiento v3

Inventario A→B de `simulador_onco_homeostasis_v5.py`, `simulador_onco_hepatico_v3.py` e `inmuno_utils.py`.  
Instrumento de cribado; **no** calibración wet-lab ni predicción clínica.

Complementa: [`madurez_artefactos_motor.md`](./madurez_artefactos_motor.md), [`ssot_framework_map-v3.md`](./ssot_framework_map-v3.md), [`ledger_parametros_nucleo.md`](./ledger_parametros_nucleo.md), [`vector_viral_oncolitico_modelo-v2.md`](./vector_viral_oncolitico_modelo-v2.md) §2, [`estudio_integracion_inmunologica_v3.md`](./estudio_integracion_inmunologica_v3.md).

---

## 1. Condiciones iniciales y política CD8

| Parámetro (código) | Valor | Unidad | Capa | Fuente / justificación | Estado trazabilidad |
|--------------------|-------|--------|------|------------------------|---------------------|
| `tumor.pHe` (basal cohorte) | 6.20 | — | B | Extremo inferior pHe ácido ~6.2–6.8 (SSoT vector v2 §2.C) | Ancla A (orden) |
| `tumor.pHi` (basal) | 7.20 | — | B | pHi tumoral neutro citado en vector v2 §2.C | Ancla A (orden) |
| `tumor.atp_nivel` (basal) | 10000.0 | u. rel. | B | Escala relativa “exceso Warburg” del toy model | Solo Capa B |
| `tumor.Bcl2_expresion` | 25.0 | × basal | B | Factor “hasta ×25” (vector v2 §2.A) | Ancla A (orden) |
| `tumor.PD_L1_expresion` (basal) | 50.0 | u. rel. | B | Camuflaje basal del toy model | `UNRESOLVED` |
| `tumor.telomeros` (tumor) | 3920 | pb (modelo) | B | Por debajo del umbral senescencia 4000 | Ingeniería |
| `inmuno_utils.PH_VETO_CD8` | 6.50 | — | B | FC-BIO-2.1 / **RESOLVED-B-03** | Ancla A (veto ≤6.50) |
| `inmuno_utils.PH_FISIOLOGICO` | 7.35 | — | B | Techo de la rampa CD8 | Ancla A (fisiología) |
| `inmuno_utils.ANERGY_GATE` | 0.20 | fracción | B | Truncado de fatiga modelada | Hipótesis Capa B |

---

## 2. Cinética MCT2 / pH / ATP (forma cerrada, no ODE)

Las trayectorias usan \(1 - e^{-k\Delta t}\) hacia un asintótico; **no** hay integrador de ecuaciones diferenciales.

| Parámetro (código) | Valor | Unidad | Capa | Rol en el modelo | Estado trazabilidad |
|--------------------|-------|--------|------|------------------|---------------------|
| `mct2_expresion` (máx. escape) | 15.0 | × basal | B | Tope de sobreexpresión adaptativa | `UNRESOLVED` |
| `mct2_expresion` (inhibido) | 0.5 | × basal | B | Bypass atenuado bajo `inhibicion_mct2` | `UNRESOLVED` |
| \(k\) MCT2 (`exp(-0.1·Δt)`) | 0.1 | h⁻¹ | B | Velocidad de subida MCT2 | `UNRESOLVED` |
| \(k\) pHi (`exp(-0.4·Δt)`) | 0.4 | h⁻¹ | B | Velocidad de acidificación citoplasmática | `UNRESOLVED` |
| \(k\) pHe (`exp(-0.25·Δt)`) | 0.25 | h⁻¹ | B | Velocidad de lavado/acidosis estromal | `UNRESOLVED` |
| \(k\) ATP (`exp(-0.35·Δt)`) | 0.35 | h⁻¹ | B | Velocidad de colapso ATP | `UNRESOLVED` |
| Asintótico pHi | `max(5.50, 5.75 + 0.85·(1−1/MCT2))` | — | B | Rescate vs colapso según MCT2 | Ingeniería Capa B |
| Asintótico pHe | `min(7.35, 7.35 − 0.75·(1−1/MCT2))` | — | B | Acidosis residual vs lavado | Ingeniería Capa B |
| Asintótico ATP | `max(10, 30 + 770·(1−1/MCT2))` | u. rel. | B | Piso energético según MCT2 | Solo Capa B |
| \(k\) depuración tumoral | 0.5 | h⁻¹ | B | `1−exp(−0.5·fuerza·Δt)` | `UNRESOLVED` |

---

## 3. Cronograma y anti-PD-1 (v5 / v3)

| Parámetro (código) | Valor | Unidad | Capa | Fuente / justificación | Estado trazabilidad |
|--------------------|-------|--------|------|------------------------|---------------------|
| `tiempo_total` | 72.0 | h | B | Horizonte de la cohorte | Ingeniería |
| `paso_tiempo` (nominal) | 0.1 | h | B | Discretización (`linspace`) | Ingeniería |
| `t_metabolico` | 12.0 | h | B | Inicio bloqueo MCT1/4 modelado | `UNRESOLVED` |
| Retraso anti-PD-1 Cohorte C | +12.0 | h | B | `t_inmunoterapia = 24` | Hipótesis de cronograma |
| Rampa `efectividad_PD1` | `(pHe−6.0)/(7.35−6.0)` si pHe &lt; 7.30 | — | B | Distinta del veto CD8 6.50 | `UNRESOLVED` |
| Factor historial CD8 (solo v5) | ×0.1 si aún no hay anti-PD-1 o pHe &lt; 7.30 | — | B | Mezcla acidosis + timing en la serie reportada | Ingeniería (documentar; no confundir con `inmuno_utils`) |

---

## 4. Acoplamiento hepático v3 (IL-6 / PD-L1)

| Parámetro (código) | Valor | Unidad | Capa | Fuente / justificación | Estado trazabilidad |
|--------------------|-------|--------|------|------------------------|---------------------|
| `beta_pd_l1` (default) | 3.0 | u. rel. / (pg/mL) | B | `PD_L1 = 50 + β·[IL-6]` | Hipótesis; ver estudio v3 / reporte feedback |
| `beta_pd_l1` (co-intervención tip.) | 0.1 | idem | B | Escenario atenuado en tests | Exploratorio Capa B |
| Literal umbral anti-PD-1 | `150.0` | u. rel. | B | `if PD_L1 >= 150 → efectividad_PD1 = 0` (**no** es constante nombrada en código) | `UNRESOLVED` |
| Liberación IL-6 | `2.0·carga_viral + 100.0·(1−viab_hep)` | pg/mL (modelo) | B | Paracrino hepatocito → estroma | `UNRESOLVED` |
| Atenuación CD8 por IL-6 | `/(1 + [IL-6]/10)` | — | B | Solo si `feedback_activo` | `UNRESOLVED` |
| `inóculo_tasa` (default) | 10.0 | u. modelo / paso | B | Entrada viral de novo | `UNRESOLVED` |
| `myrcludex_nM` (esc. co-int.) | 10.0 | nM | B | Competencia NTCP (hepatocito) | Orden de magnitud; ver estudio v3 |

---

## 5. Fronteras numéricas verificadas (regresión)

Forma cerrada en el asintótico \(t \to 72\,\mathrm{h}\) (MCT2 saturado). Tests canónicos:

| Escenario | Predicción Capa B | Test |
|-----------|-------------------|------|
| Escape MCT2 | pHe ≈ 6.65; cruda CD8 ≈ 0.176 → **0** (anergy gate); viab. tumor ≈ 1 | `test_simulador_homeostasis_v5.test_cohorte_c_escape_mct2_anula_cd8`, `test_simulador_onco_hepatico_v3.test_coupled_mct2_sanctuary` |
| Triple inhibición | pHe ≈ 7.35; pHi piso 5.50; CD8 100%; viab. ≈ 0 | `test_simulador_homeostasis_v5.test_cohorte_c_triple_inhibicion` |
| Sin escape (Cohorte C) | pHe 7.35; viab. tumor 0 | `test_simulador_homeostasis_v5.test_cohorte_c_sin_escape` |
| Gated-6.50 unitario | 6.50 / 6.65 → 0; 7.35 → 1 | `test_inmuno_utils`, `test_parche_restauracion` |

Los tests `test_simulador_homeostasis_v3` (importan v4) son **regresión histórica**, no la fuente de verdad de este ledger.

---

## 6. Huecos Capa C (backlog)

| Ítem | Nota |
|------|------|
| ATP en unidades físicas | 10000 / 10–30 son interruptores relativos |
| Densidad PD-L1 / GPC3 absolutas | Hoy u. rel.; sin moléc./µm² |
| Transporte espacial | Compartimento único; PDE = UNRESOLVED-02 (mapa v3) |
| Constantes \(k\) y tope MCT2×15 | Sin ancla experimental curada en repo |
| Nombrar `UMBRAL_PD_L1_SAT = 150` en código | Hoy literal; conviene constante explícita |

---

## Reglas

1. Nada en esta tabla es evidencia clínica ni wet-lab de Guanes Health.
2. `UNRESOLVED` no se rellena con cifras de chat; solo con cita curada en SSoT.
3. Cambios a CD8 van en `inmuno_utils.py` + este ledger + `ledger_parametros_nucleo.md`.
4. Si se cambia un asintótico o \(k\) en v5/v3, actualizar esta tabla y los tests de frontera en el mismo cambio.

**Estado del documento:** activo (trazabilidad dinámica canónica v5/v3).
