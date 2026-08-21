# Mapa SSoT — arquitectura y límites (v3.0)

Guanes Health. Instrumento de cribado *in silico* (placas = herramientas de modelado, no ontología celular).

**Estado:** activo. Sustituye operativamente a [`ssot_framework_map-v2.md`](./ssot_framework_map-v2.md).

Complementa: [`placa_base_instrumento_investigacion.md`](./placa_base_instrumento_investigacion.md), [`madurez_artefactos_motor.md`](./madurez_artefactos_motor.md), [`ledger_parametros_nucleo.md`](./ledger_parametros_nucleo.md), [`ledger_parametros_cart_hcc.md`](./ledger_parametros_cart_hcc.md).

---

## 1. Capas A / B / C

| Capa | Qué es | Estado aquí |
|------|--------|-------------|
| **A** | Hipótesis / biología de fondo (prosa, reglas cualitativas) | Catálogo; no ejecuta |
| **B** | Toy model determinista + tests de frontera | **Operativo** en el repo |
| **C** | Calibración wet-lab / predictivo | Vacío (backlog) |

Los tests comprueban **coherencia numérica del código**, no biología experimental.

---

## 2. Inventario de placas (roles)

Cada “placa” es un **instrumento** para ordenar variables y vetos.

### Huésped
1. **Célula sana** — homeostasis, telómeros / Hayflick (modelo).
2. **Hepatocito** — zonación O₂ → NTCP (modelo).

### Patología
3. **Infección HBV** — entrada vía NTCP; IL-6 paracrina (modelo).
4. **HCC** — Warburg, MCT, checkpoints (modelo).

### Intervención (modelo)
5. **CD8+ / estroma** — política **Gated-6.50** (Capa B):
   - piso: pHe ≤ 6.50 → eficiencia = 0 (FC-BIO-2.1);
   - rampa lineal 6.50 → 7.35;
   - *anergy gate* 0.20: fracción cruda &lt; 0.20 → 0.0.
   - **Fuente única:** `03_Motor_Oncologico/inmuno_utils.py`.
   - Consumidores: `parche_restauracion.py`, `simulador_onco_homeostasis_v5.py`, `simulador_onco_hepatico_v3.py`.
   - Tests: `test_inmuno_utils.py`, `test_parche_restauracion.py`, `test_simulador_homeostasis_v5.py`.
6. **CAR-T** — Kd–pH (histidinas), NHE1, proxy TOX si se añade; etiqueta de diseño STROMA-SHIELD, no producto validado.
7. **iCasp9** — apoptosis inducida por rimiducid (cinética Capa B).
8. **Extravasación** — IFP / colágeno; esbozo η_mig (sin PDE).
9. **Antígeno HCC** — GPC3 de membrana + señuelo sGPC3 (fase líquida).

---

## 3. Madurez de líneas de código (resumen)

| Línea | Artefacto | Estado |
|-------|-----------|--------|
| Política CD8 | `inmuno_utils.py` | **Canónico** |
| Núcleo | `placa_*` + `parche_restauracion.py` | **Canónico** |
| Dinámica | `simulador_onco_homeostasis_v5.py` | **Canónico** |
| Acoplamiento onco-hepático | `simulador_onco_hepatico_v3.py` | **Canónico** (usa v5) |
| Acoplamiento v2 | `simulador_onco_hepatico_v2.py` | Histórico (usaba v4) |

Detalle: [`madurez_artefactos_motor.md`](./madurez_artefactos_motor.md).

---

## 4. Integración RESOLVED-B / UNRESOLVED

### Cerrado en Capa B (toy model + test)

**[RESOLVED-B-01] Señuelo sGPC3**

- Ecuación: \(\phi = 1/(1 + [sGPC3]/K_i)\), \(K_i = 2.5\) ng/mL (**hipótesis**, no SPR).
- Código: `factor_senuelo_sgpc3` en `simulador_cart_hcc_interaccion.py`.
- Test: `test_senuelo_sgpc3_resolved_b` (frontera numérica).
- Abierto: AFP, Ki experimental, shedding dinámico.

**[RESOLVED-B-02] Esbozo η_mig (IFP / colágeno)**

- Coeficiente escalar de encuentro; **no** es transporte por difusión.
- Umbrales Capa B: IFP 15 mmHg, colágeno 50 µg/mg.
- Código: `factor_infiltracion_mig`. Test: `test_eta_mig_resolved_b02`.
- Abierto: PDE, heparanasa, dosis real OTR4120.

**[RESOLVED-B-03] Política CD8 Gated-6.50**

- Implementación única en `inmuno_utils.calcular_eficiencia_cd8`.
- Consumida por núcleo, dinámica v5 y acoplamiento v3.
- Frontera útil: pHe ≈ 6.65 (escape MCT2) → cruda ≈ 0.176 → truncado a 0 por anergy gate.

### Pendiente

| ID | Qué falta |
|----|-----------|
| **UNRESOLVED-02** | Transporte espacial (malla / PDE / quimiotaxis). η_mig sigue siendo escalar (RESOLVED-B-02), no motor geométrico. |
| **UNRESOLVED-03** | Acoplamiento metabolito–TOX (“succinate trap”). |
| **UNRESOLVED-04** | Anclaje literario amplio + sensibilidad global (Sobol). |

El barrido local CAR-T (`analisis_sensibilidad_local_cart.py`) usa rangos **asumidos** del ledger; no sustituye UNRESOLVED-04.

---

## 5. Cómo hablar de esto (anti-ridículo)

| Evitar | Preferir |
|--------|----------|
| “Validado”, “cura”, “protección absoluta” | “Cierra frontera del toy model” / “hipótesis Capa B” |
| “Firmware del linfocito” | “Parámetros del instrumento CAR-T” |
| “Plenamente verificado por el arnés” | “Cubierto por test de regresión X” |
| “Norma Suprema” / metáfora digital literal | Gradiente de O₂ / regla del modelo |

---

*Guanes Health, 2026 — SSoT operativo v3 (Gated-6.50 en `inmuno_utils`; acoplamiento canónico v3).*
