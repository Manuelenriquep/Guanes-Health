# Mapa SSoT — arquitectura y límites (v2.0)

Guanes Health. Instrumento de cribado *in silico* (placas = herramientas de modelado, no ontología celular).

Complementa: [`placa_base_instrumento_investigacion.md`](./placa_base_instrumento_investigacion.md), [`ledger_parametros_cart_hcc.md`](./ledger_parametros_cart_hcc.md).

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
5. **CD8+ / estroma** — veto por pHe ≤ 6.50 (Capa B).
6. **CAR-T** — Kd–pH (histidinas), NHE1, proxy TOX si se añade; nombre comercial STROMA-SHIELD es etiqueta de diseño, no producto validado.
7. **iCasp9** — apoptosis inducida por rimiducid (cinética Capa B).
8. **Extravasación** — IFP / colágeno; esbozo η_mig (sin PDE).
9. **Antígeno HCC** — GPC3 de membrana + señuelo sGPC3 (fase líquida).

---

## 3. Integración

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

### Pendiente

| ID | Qué falta |
|----|-----------|
| **UNRESOLVED-02b** | Transporte espacial (malla / PDE / quimiotaxis) |
| **UNRESOLVED-03** | Acoplamiento metabolito–TOX (“succinate trap”) |
| **UNRESOLVED-04** | Anclaje literario amplio + sensibilidad global (Sobol) |

El barrido local existente (`analisis_sensibilidad_local_cart.py`) usa rangos **asumidos** del ledger; no sustituye UNRESOLVED-04.

---

## 4. Cómo hablar de esto (anti-ridículo)

| Evitar | Preferir |
|--------|----------|
| “Validado”, “cura”, “protección absoluta” | “Cierra frontera del toy model” / “hipótesis Capa B” |
| “Firmware del linfocito” | “Parámetros del instrumento CAR-T” |
| “Plenamente verificado por el arnés” | “Cubierto por test de regresión X” |
| “Norma Suprema” / metáfora digital literal | Gradiente de O₂ / regla del modelo |

---

*Guanes Health, 2026 — SSoT operativo v2.*
