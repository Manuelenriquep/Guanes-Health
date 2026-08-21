# Ledger de parámetros — núcleo (placas + parche)

Inventario A→B de `placa_sana.py`, `placa_cancer.py` y `parche_restauracion.py`.  
Instrumento de cribado; **no** calibración wet-lab ni predicción clínica.

Complementa: [`madurez_artefactos_motor.md`](./madurez_artefactos_motor.md), [`ssot_framework_map-v3.md`](./ssot_framework_map-v3.md), [`placa_base_instrumento_investigacion.md`](./placa_base_instrumento_investigacion.md), [`vector_viral_oncolitico_modelo-v2.md`](./vector_viral_oncolitico_modelo-v2.md) §2.

---

## Tabla operativa (Capa B)

| Parámetro (código) | Valor | Unidad | Capa | Fuente / justificación | Estado trazabilidad |
|--------------------|-------|--------|------|------------------------|---------------------|
| `CelulaSana.POTENCIAL_MIN` / `MAX` | −70 / −90 | mV | B | Orden de magnitud de \(V_m\) en reposo | Ancla A débil |
| `CelulaSana.FIDELIDAD_ADN_POL` | 1e−7 | tasa error | B | Orden de magnitud (modelo) | `UNRESOLVED` (cita curada) |
| `CelulaSana.ATP_NOMINAL` | 100 | u. rel. | B | Escala relativa del instrumento | Sin ancla A |
| `CelulaSana.ATP_MINIMO_SOBREVIVENCIA` | 20.0 | u. rel. | B | Umbral binario de viabilidad | `UNRESOLVED` |
| `CelulaSana.PH_EXTRACELULAR_NOMINAL` | 7.35 | — | B | pHe fisiológico nominal | Ancla A (fisiología general) |
| `CelulaSana.LIMITE_HAYFLICK_MAX` | 50 | generaciones | B | Rango ~50–70 (SSoT vector v2 §2.B) | Proxy A→B |
| `CelulaSana.TELOMERO_MINIMO_BP` | 10.0 | u. rel. | B | Umbral simplificado (no pb reales) | `UNRESOLVED` (v5 usa 4000 pb) |
| `CelulaTumoral.ATP_WARBURG` | 10000 | u. rel. | B | Escala relativa “exceso Warburg” | Solo Capa B |
| `CelulaTumoral.PH_ACIDO_TUMORAL` | 6.20 | — | B | Extremo inferior pHe ácido 6.20–6.80 | Ancla A (orden) |
| `CelulaTumoral.PH_INTRACELULAR_BASAL` | 7.20 | — | B | pHi tumoral citado en SSoT vector v2 §2.C | Ancla A (orden) |
| `CelulaTumoral.BCL2_FACTOR` | 25.0 | × basal | B | “Hasta ×25” en narrativa SSoT | Ancla A (orden) |
| `CelulaTumoral.PH_FISICO_MIN` / `MAX` | 0 / 14 | — | B | Fail-closed | Ingeniería |
| `ParcheRestauracion.PH_VETO_CD8` | 6.50 | — | B | FC-BIO-2.1; alineado a v5 (**RESOLVED-B-03**) | Ancla A (veto ≤6.50) |
| `ParcheRestauracion.PH_FISIOLOGICO` | 7.35 | — | B | Techo de la rampa CD8 | = pHe nominal |
| `ParcheRestauracion.ANERGY_GATE` | 0.20 | fracción | B | Truncado de fatiga modelada | Hipótesis Capa B |
| `ParcheRestauracion.PH_RESTAURADO` | 7.35 | — | B | Restauración a pHe sano | Alineado |
| `ParcheRestauracion.ATP_COLAPSADO` | 30 | u. rel. | B | Colapso post-bloqueo MCT4 modelado | `UNRESOLVED` |
| `ParcheRestauracion.PH_INTRACELULAR_LETAL` | 5.2 | — | B | Autólisis ácida modelada | `UNRESOLVED` |
| `ParcheRestauracion.BCL2_FISIOLOGICO` | 1.0 | × basal | B | Reset BCL-2 en toy model | Ingeniería |

`PH_PARALISIS_CD8` es alias deprecado de `PH_VETO_CD8` (compat).

---

## Anclas Capa A (resumen)

| Hecho de fondo (A) | Uso en el núcleo (B) |
|--------------------|----------------------|
| pHe tumoral ~6.2–6.8; pHi ~7.2 | `PH_ACIDO_TUMORAL`, `PH_INTRACELULAR_BASAL` |
| Veto CD8 a pHe ≤ 6.50 (FC-BIO-2.1) | `PH_VETO_CD8` + anergy gate |
| Sobreexpresión BCL-2 (orden ×25) | `BCL2_FACTOR = 25` |
| Hayflick ~50–70 | `LIMITE_HAYFLICK_MAX = 50` |
| Eje PD-1/PD-L1 | flags del toy model |
| MCT4 / eflujo lactato-H⁺ | `mct4_bloqueado` + colapso modelado |

---

## Huecos explícitos (Capa C)

| Ítem | Nota |
|------|------|
| Calibración empírica de ATP relativo | Escalas distintas núcleo vs dinámica v5 |
| Umbral telómero en pb en el núcleo | Núcleo relativo; v5 usa 4000 pb |
| Cinética temporal del parche | Paso determinista, no ODE |
| Portar acoplamiento `hepatico_v2` a v5 | Pendiente; no confundir con `hepatico_v3` ausente |

---

## Reglas

1. Nada en esta tabla es evidencia clínica ni wet-lab de Guanes Health.
2. `UNRESOLVED` no se rellena con cifras de chat; solo con cita curada en SSoT.
3. Si se cambia un valor del núcleo, actualizar esta tabla en el mismo cambio.
4. CAR-T/HCC: [`ledger_parametros_cart_hcc.md`](./ledger_parametros_cart_hcc.md).

**Estado del documento:** activo (Gated-6.50 unificado en núcleo).
