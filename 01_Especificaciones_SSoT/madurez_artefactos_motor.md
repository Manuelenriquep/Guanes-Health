# Madurez de artefactos del motor

**Ámbito:** `03_Motor_Oncologico/` (+ tests asociados).  
**Propósito:** declarar qué es **línea canónica**, qué es **experimental**, qué es **WIP/ausente** y qué queda **histórico**.  
**No afirma** fidelidad biológica ni validez clínica.

Complementa: [`placa_base_instrumento_investigacion.md`](./placa_base_instrumento_investigacion.md), [`ssot_framework_map-v3.md`](./ssot_framework_map-v3.md), [`ledger_parametros_nucleo.md`](./ledger_parametros_nucleo.md), [`ledger_trazabilidad_dinamica.md`](./ledger_trazabilidad_dinamica.md), [`ledger_parametros_cart_hcc.md`](./ledger_parametros_cart_hcc.md).

---

## Etiquetas

| Etiqueta | Significado operativo |
|----------|------------------------|
| **Canónico** | Entrada preferida para lectura, demos y crítica externa; tests de regresión asociados. |
| **Experimental** | Extensión activa; útil para exploración; no sustituye al canónico de su línea. |
| **Histórico / deprecado** | Conservado por trazabilidad; no ampliar salvo migración o borrado consciente. |
| **Compat** | Alias de importación; no duplicar lógica aquí. |

---

## 1. Núcleo canónico (demo + placas)

Línea mínima: homeostasis modelada → tumor toy → restauración determinista.  
Política CD8: **Gated-6.50** vía [`inmuno_utils.py`](../03_Motor_Oncologico/inmuno_utils.py).

| Artefacto | Etiqueta | Notas |
|-----------|----------|-------|
| `inmuno_utils.py` | **Canónico** (política compartida) | Fuente única CD8 Gated-6.50 |
| `placa_sana.py` | **Canónico** | Placa-instrumento sana |
| `placa_cancer.py` | **Canónico** | Placa-instrumento tumoral |
| `parche_restauracion.py` | **Canónico** | Demo README; delega CD8 a `inmuno_utils` |
| `placa_base_sana.py` | Compat | Reexporta `placa_sana` |
| `placa_base_cancer.py` | Compat | Reexporta `placa_cancer` |

Tests: `test_parche_restauracion.py`, `test_inmuno_utils.py`.  
Ledger A→B: [`ledger_parametros_nucleo.md`](./ledger_parametros_nucleo.md).

---

## 2. Línea dinámica canónica (metabólico-inmunológica)

| Artefacto | Etiqueta | Notas |
|-----------|----------|-------|
| `simulador_onco_homeostasis_v5.py` | **Canónico** | Dinámica MCT/inmuno; importa `inmuno_utils` |
| `analisis_parametrico_mct2.py` | Experimental | Barrido MCT2 |
| `barrido_estocastico_oxigeno.py` | Experimental | Barrido O₂ → HIF → VEGF (Capa B) |

Tests: `04_Bateria_Inviolable/test_simulador_homeostasis_v5.py`.  
Ledger A→B: [`ledger_trazabilidad_dinamica.md`](./ledger_trazabilidad_dinamica.md).

---

## 3. Acoplamiento onco-hepático

| Artefacto | Etiqueta | Notas |
|-----------|----------|-------|
| `simulador_hepatocito_infeccion.py` | **Canónico** (hepático) | NTCP / HBV / Myrcludex (Capa B) |
| `simulador_onco_hepatico_v3.py` | **Canónico** (acoplamiento) | Feedback IL-6 → PD-L1; importa **v5** + `inmuno_utils` |
| `simulador_onco_hepatico_v2.py` | Histórico | Dependía de `…_v4`; no ampliar |
| `grafico_dinamica_temporal.py` | Experimental (visual) | IL-6/PD-L1 sobre acoplamiento **v3** |
| `simulador_cointervencion_escenarios.py` | Experimental | Comparativa de 4 escenarios sobre **v3** |
| `simulador_s267f_toxicidad.py` | Experimental | Barrido WT vs S267F |
| `simulador_cart_hcc_interaccion.py` | Experimental | Esqueleto CAR-T/HCC |
| `analisis_sensibilidad_local_cart.py` | Experimental | Rangos asumidos del ledger CAR-T |

Tests de acoplamiento vigente: `test_simulador_onco_hepatico_v3.py` (v2 permanece como regresión histórica).  
Ledger A→B: [`ledger_trazabilidad_dinamica.md`](./ledger_trazabilidad_dinamica.md).  
Manual: [`../README-HEPATIC.md`](../README-HEPATIC.md).

---

## 4. Histórico / deprecado (no ampliar)

| Artefacto | Etiqueta | Sustituto |
|-----------|----------|-----------|
| `simulador_onco_homeostasis.py` | Histórico | → `…_v5.py` |
| `simulador_onco_homeostasis_v2.py` | Histórico | → `…_v5.py` |
| `simulador_onco_homeostasis_v3.py` | Histórico | → `…_v5.py` |
| `simulador_onco_homeostasis_v4.py` | Histórico | → `…_v5.py` (aún dependencia de scripts experimentales / `hepatico_v2`) |
| `simulador_onco_hepatico_v1.py` | Histórico | → `…_v3.py` |
| `simulador_onco_hepatico_v2.py` | Histórico | → `…_v3.py` |

Los tests `test_simulador_homeostasis.py` / `_v2` / `_v3` y `test_simulador_onco_hepatico_v2.py` son **regresión histórica**.

---

## 5. Cómo elegir qué correr

| Objetivo | Comando / entrada |
|----------|-------------------|
| Demo mínima (README) | `py "03_Motor_Oncologico/parche_restauracion.py"` |
| Dinámica canónica | `py "03_Motor_Oncologico/simulador_onco_homeostasis_v5.py"` |
| Acoplamiento hepático vigente | `py "03_Motor_Oncologico/simulador_onco_hepatico_v3.py"` |
| Suite de tests | `py -m unittest discover -s "04_Bateria_Inviolable" -v` |

---

## Reglas

1. Un PR que “mejore el motor” debe declarar si toca **núcleo**, **dinámica v5**, **acoplamiento v3** o solo **experimental**.
2. Cambios a la política CD8 van **solo** en `inmuno_utils.py` (+ test); no reimplementar en cada simulador.
3. No promover un experimental a canónico sin actualizar esta tabla, el README correspondiente y el mapa SSoT v3.
4. No borrar históricos en silencio: primero marcar aquí, luego migrar tests.

**Estado del documento:** activo (inmuno_utils + hepático v3 canónicos).
