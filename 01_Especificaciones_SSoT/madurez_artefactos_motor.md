# Madurez de artefactos del motor

**Ámbito:** `03_Motor_Oncologico/` (+ tests asociados).  
**Propósito:** declarar qué es **línea canónica**, qué es **experimental** y qué queda **histórico / deprecado**.  
**No afirma** fidelidad biológica ni validez clínica.

Complementa: [`placa_base_instrumento_investigacion.md`](./placa_base_instrumento_investigacion.md), [`ledger_parametros_nucleo.md`](./ledger_parametros_nucleo.md), [`ledger_parametros_cart_hcc.md`](./ledger_parametros_cart_hcc.md).

---

## Etiquetas

| Etiqueta | Significado operativo |
|----------|------------------------|
| **Canónico** | Entrada preferida para lectura, demos y crítica externa; tests de regresión asociados. |
| **Experimental** | Extensión activa; útil para exploración; no sustituye al núcleo canónico. |
| **Histórico / deprecado** | Conservado por trazabilidad; no ampliar salvo migración o borrado consciente. |
| **Compat** | Alias de importación; no duplicar lógica aquí. |

---

## 1. Núcleo canónico (demo + placas)

Línea mínima del instrumento: homeostasis modelada → tumor toy → restauración determinista.

| Artefacto | Etiqueta | Notas |
|-----------|----------|-------|
| `placa_sana.py` | **Canónico** | Placa-instrumento sana |
| `placa_cancer.py` | **Canónico** | Placa-instrumento tumoral |
| `parche_restauracion.py` | **Canónico** | Demo README; anti-PD-1 vs protocolo combinado (Capa B) |
| `placa_base_sana.py` | Compat | Reexporta `placa_sana` |
| `placa_base_cancer.py` | Compat | Reexporta `placa_cancer` |

Ledger A→B: [`ledger_parametros_nucleo.md`](./ledger_parametros_nucleo.md).

---

## 2. Línea dinámica canónica (acoplamiento onco-hepático)

Extensión canónica **aparte del núcleo**: dinámica temporal + hepatocito + feedback IL-6/PD-L1. Manual: [`../README-HEPATIC.md`](../README-HEPATIC.md).

| Artefacto | Etiqueta | Notas |
|-----------|----------|-------|
| `simulador_onco_homeostasis_v4.py` | **Canónico** (línea dinámica) | Generación actual de dinámica MCT/inmuno |
| `simulador_hepatocito_infeccion.py` | **Canónico** (hepático) | NTCP / HBV / Myrcludex (Capa B) |
| `simulador_onco_hepatico_v2.py` | **Canónico** (acoplamiento) | Feedback IL-6 → PD-L1 |
| `grafico_dinamica_temporal.py` | Experimental (visual) | Figuras ilustrativas, no evidencia |
| `simulador_cointervencion_escenarios.py` | Experimental | Comparativa de escenarios |
| `simulador_s267f_toxicidad.py` | Experimental | Barrido WT vs S267F |
| `simulador_cart_hcc_interaccion.py` | Experimental | Esqueleto CAR-T/HCC; ledger propio |
| `analisis_sensibilidad_local_cart.py` | Experimental | Rangos asumidos del ledger CAR-T |
| `analisis_parametrico_mct2.py` | Experimental | Barrido MCT2 |
| `barrido_estocastico_oxigeno.py` | Experimental | Barrido O₂ → HIF → VEGF (Capa B) |

---

## 3. Histórico / deprecado (no ampliar)

| Artefacto | Etiqueta | Sustituto |
|-----------|----------|-----------|
| `simulador_onco_homeostasis.py` | Histórico | → `…_v4.py` |
| `simulador_onco_homeostasis_v2.py` | Histórico | → `…_v4.py` |
| `simulador_onco_homeostasis_v3.py` | Histórico | → `…_v4.py` |
| `simulador_onco_hepatico_v1.py` | Histórico | → `…_v2.py` |

Los tests `test_simulador_homeostasis*.py` / `test_simulador_onco_hepatico.py` que apuntan a versiones antiguas son **regresión histórica**; la suite de acoplamiento vigente es `test_simulador_onco_hepatico_v2.py`.

---

## 4. Cómo elegir qué correr

| Objetivo | Comando / entrada |
|----------|-------------------|
| Demo mínima (README) | `py "03_Motor_Oncologico/parche_restauracion.py"` |
| Acoplamiento hepático | Ver `README-HEPATIC.md` |
| Suite de tests | `py -m unittest discover -s "04_Bateria_Inviolable" -v` |

---

## Reglas

1. Un PR que “mejore el motor” debe declarar si toca **núcleo**, **línea dinámica** o solo **experimental**.
2. No promover un experimental a canónico sin actualizar esta tabla, el README correspondiente y, si aplica, un ledger A→B.
3. No borrar históricos en silencio: primero marcar aquí, luego migrar tests.

**Estado del documento:** activo (congelación inicial de madurez).
