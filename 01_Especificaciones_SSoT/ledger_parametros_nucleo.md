# Ledger de parámetros — núcleo (placas + parche)

Inventario A→B de `placa_sana.py`, `placa_cancer.py` y `parche_restauracion.py`.  
Instrumento de cribado; **no** calibración wet-lab ni predicción clínica.

Complementa: [`madurez_artefactos_motor.md`](./madurez_artefactos_motor.md), [`placa_base_instrumento_investigacion.md`](./placa_base_instrumento_investigacion.md), [`vector_viral_oncolitico_modelo-v2.md`](./vector_viral_oncolitico_modelo-v2.md) §2.

---

## Tabla operativa (Capa B)

| Parámetro (código) | Valor | Unidad | Capa | Fuente / justificación | Estado trazabilidad |
|--------------------|-------|--------|------|------------------------|---------------------|
| `CelulaSana.POTENCIAL_MIN` / `MAX` | −70 / −90 | mV | B | Orden de magnitud de \(V_m\) en reposo (literatura fisiológica general) | Ancla A débil; umbrales del toy model |
| `CelulaSana.FIDELIDAD_ADN_POL` | 1e−7 | tasa error | B | Orden de magnitud de error de polimerasa (modelo) | `UNRESOLVED` (cita curada en repo) |
| `CelulaSana.ATP_NOMINAL` | 100 | u. rel. | B | Escala relativa del instrumento | Sin ancla A (unidades relativas) |
| `CelulaSana.ATP_MINIMO_SOBREVIVENCIA` | 20.0 | u. rel. | B | Umbral binario de viabilidad | `UNRESOLVED` |
| `CelulaSana.PH_EXTRACELULAR_NOMINAL` | 7.35 | — | B | pHe fisiológico nominal | Ancla A (fisiología general) |
| `CelulaSana.LIMITE_HAYFLICK_MAX` | 50 | generaciones | B | Dentro del rango ~50–70 citado en SSoT v2 §2.B | Proxy A→B (elegido extremo inferior) |
| `CelulaSana.TELOMERO_MINIMO_BP` | 10.0 | u. rel. | B | Umbral simplificado (no pb reales) | `UNRESOLVED` (v4 usa 4000 pb) |
| `CelulaTumoral.ATP_WARBURG` | 10000 | u. rel. | B | Escala relativa “exceso Warburg” del toy model | Sin calibración A; solo Capa B |
| `CelulaTumoral.PH_ACIDO_TUMORAL` | 6.20 | — | B | Extremo inferior del rango pHe ácido 6.20–6.80 (SSoT v2 §2.C) | Ancla A (orden de magnitud) |
| `CelulaTumoral.PH_INTRACELULAR_BASAL` | 7.20 | — | B | pHi tumoral neutro/estable citado en SSoT v2 §2.C | Ancla A (orden de magnitud) |
| `CelulaTumoral.BCL2_FACTOR` | 25.0 | × basal | B | Factor de sobreexpresión “hasta ×25” (SSoT v2 §2.A) | Ancla A (orden de magnitud; no cuantificación de línea celular) |
| `CelulaTumoral.PH_FISICO_MIN` / `MAX` | 0 / 14 | — | B | Fail-closed de rango físico | Ingeniería del instrumento |
| `ParcheRestauracion.PH_PARALISIS_CD8` | 7.0 | — | B | Umbral de eficiencia CD8 modelada (más laxo que veto ≤6.50 del stack hepático) | `UNRESOLVED` vs FC-BIO-2.1 (incoherencia intencional de líneas; no unificar sin decisión) |
| `ParcheRestauracion.EFICIENCIA_CD8_ACIDO` | 10.0 | % rel. | B | Penalización determinista bajo pHe ácido | `UNRESOLVED` |
| `ParcheRestauracion.EFICIENCIA_CD8_MAX` | 100.0 | % rel. | B | Techo del toy model | Ingeniería |
| `ParcheRestauracion.PH_RESTAURADO` | 7.35 | — | B | Restauración a pHe nominal sano | Alineado a `PH_EXTRACELULAR_NOMINAL` |
| `ParcheRestauracion.ATP_COLAPSADO` | 30 | u. rel. | B | Colapso energético post-bloqueo MCT4 modelado | `UNRESOLVED` |
| `ParcheRestauracion.PH_INTRACELULAR_LETAL` | 5.2 | — | B | Autólisis ácida modelada tras bloqueo MCT4 | `UNRESOLVED` (cinética real de acidificación) |
| `ParcheRestauracion.BCL2_FISIOLOGICO` | 1.0 | × basal | B | “Reset” del factor BCL-2 en el toy model | Ingeniería (no dosis farmacológica) |

Flags de estado (`camuflaje_pd_l1`, `mct4_bloqueado`, `apoptosis_*`) son **booleanos de Capa B**; el ancla A es cualitativa (eje PD-1/PD-L1; MCT4; apoptosis), no numérica.

---

## Anclas Capa A (resumen)

Documentadas con más detalle en `vector_viral_oncolitico_modelo-v2.md` §2 y bibliografía asociada del SSoT. Aquí solo el puente al código:

| Hecho de fondo (A) | Uso en el núcleo (B) |
|--------------------|----------------------|
| pHe tumoral ~6.2–6.8; pHi ~7.2 | `PH_ACIDO_TUMORAL`, `PH_INTRACELULAR_BASAL` |
| Sobreexpresión BCL-2/BCL-xL (orden ×25 en la narrativa SSoT) | `BCL2_FACTOR = 25` |
| Hayflick ~50–70 divisiones | `LIMITE_HAYFLICK_MAX = 50` |
| Eje PD-1/PD-L1 y acidosis que deprime CD8+ | flags + eficiencia CD8 del parche |
| MCT4 / eflujo de lactato-H⁺ | `mct4_bloqueado` + colapso pHi/ATP modelado |

**Qué no implica:** que 6.20, 25× o 10000 u. ATP sean mediciones de un experimento Guanes Health. Son **proxies del instrumento**.

---

## Huecos explícitos (Capa C)

| Ítem | Nota |
|------|------|
| Calibración empírica de ATP relativo | Escalas distintas entre núcleo (`100`/`10000`) y v4 (`~1.0` mM relativo) |
| Unificación `PH_PARALISIS_CD8` (7.0) vs veto CD8 ≤6.50 (línea hepática) | Decisión de ingeniería pendiente; no “arreglar” por chat |
| Umbral telómero en pb reales en el núcleo | El núcleo usa escala relativa; v4 usa 4000 pb |
| Cinética temporal del parche | El núcleo es un paso determinista, no ODE |

---

## Reglas

1. Nada en esta tabla es evidencia clínica ni wet-lab de Guanes Health.
2. `UNRESOLVED` no se rellena con cifras de chat; solo con cita curada en SSoT.
3. Si se cambia un valor del núcleo, actualizar esta tabla en el mismo cambio.
4. Para CAR-T/HCC usar [`ledger_parametros_cart_hcc.md`](./ledger_parametros_cart_hcc.md), no este archivo.

**Estado del documento:** activo (esqueleto de trazabilidad del núcleo).
