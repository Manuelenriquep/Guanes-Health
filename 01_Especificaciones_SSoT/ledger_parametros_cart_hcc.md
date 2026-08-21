# Ledger de parámetros — CAR-T / HCC (Capa B)

Inventario operativo del esqueleto `simulador_cart_hcc_interaccion.py`.  
Instrumento de cribado; **no** tabla de calibración wet-lab.

| Parámetro | Valor en código | Unidad | Capa | Fuente / estado | Rango exploratorio declarado |
|-----------|-----------------|--------|------|-----------------|------------------------------|
| `kd_acido` | 1.0 | nM | B | Orden de magnitud compatible con ancla A (abajo); **no** es el scFv pH-sensible | 0.5–2 nM exploratorio (Capa B) |
| `kd_neutro` | 1200.0 | nM | B | Hipótesis de instrumento (estado desprotonado) | `UNRESOLVED` |
| `pka_histidinas` | 6.70 | — | B | Calibración para ventana pHe 6.2–6.5 | `UNRESOLVED` (pKa scFv) |
| `n_hill` | 10.0 | — | B | Cooperatividad idealizada | `UNRESOLVED` |
| `UMBRAL_GPC3` | 1000.0 | moléc./cél. | B | Veto fail-closed del toy model | `UNRESOLVED` (densidad HepG2/Huh7) |
| `densidad_gpc3` (basal) | 5000.0 | moléc./cél. | B | Escenario nominal del esqueleto | ±20 % **asumido** (Capa B) |
| `UMBRAL_ATP_NHE1` | 100.0 | u. rel. | B | Umbral binario del modelo | `UNRESOLVED` (ATP real) |
| `PH_IN_MIN` | 7.10 | — | B | Piso NHE1 modelado | `UNRESOLVED` |
| `k_casp` | 2.5 | h⁻¹ | B | Ajuste a >99 % kill / 4 h a 10–50 nM | `UNRESOLVED` (cinética rimiducid) |
| `km_rimiducid` | 10.0 | nM | B | Hipótesis de instrumento | `UNRESOLVED` |
| `k_lisis` | 0.005 | h⁻¹ | B | Tasa base de aclaramiento | ±20 % **asumido** (Capa B) |
| `sgpc3_ng_ml` | 0.0 (escenario) | ng/mL | B | **RESOLVED-B-01** — barrido tip. 1–10 | exploratorio |
| `ki_sgpc3` / `KI_SGPC3_NOM` | 2.5 | ng/mL | B | Hipótesis instrumento (no SPR) | `UNRESOLVED` (Capa A) |
| `IFP_UMBRAL_MMHG` | 15.0 | mmHg | B | **RESOLVED-B-02** esbozo | `UNRESOLVED` (literatura IFP HCC) |
| `COLAGENO_UMBRAL_UG_MG` | 50.0 | µg/mg | B | **RESOLVED-B-02** esbozo | `UNRESOLVED` |
| `otr4120` | 0.0 | u. rel. | B | Alivio de pena por colágeno | `UNRESOLVED` (dosis real) |
| pHe estromal (escenario) | 6.20 | — | B | Escenario ácido nominal | barrido 6.0–7.4 (exploratorio) |

---

## Ancla Capa A (referencia de orden de magnitud)

**Ligando de referencia:** mAb anti-GPC3 GC33 (codrituzumab). No es el scFv pH-sensible del toy model.

| Magnitud | Valor reportado | Nota |
|----------|-----------------|------|
| \(K_d\) (GPC3) | **0.67 nM** | Afinidad de unión del hGC33 (mutante aglicosilado reportado con la misma afinidad) |

**Citas**

1. Allegretta M, Filmus J. *Therapeutic Potential of Targeting Glypican-3 in Hepatocellular Carcinoma.* Anticancer Agents Med Chem. Reporta \(K_d = 0.67\,\mathrm{nmol/L}\) para hGC33. [PMC3843004](https://pmc.ncbi.nlm.nih.gov/articles/PMC3843004/)
2. Ishiguro T, et al. *Anti-glypican 3 antibody as a potential antitumor agent for human liver cancer.* Cancer Res. 2008;68(23):9832–9838. doi:[10.1158/0008-5472.CAN-08-1973](https://doi.org/10.1158/0008-5472.CAN-08-1973) — biología de GC33 / hGC33 (contexto del ancla).

**Qué implica para el código**

- `kd_acido = 1.0` nM queda como **proxy Capa B** del mismo orden (nanomolar).
- **No** se sustituye el parámetro del modelo por 0.67: el simulador modela un scFv pH-dependiente, no el mAb GC33 a pH neutro.
- `kd_neutro` y el interruptor por histidinas siguen `UNRESOLVED` respecto a dato experimental.

---

**Reglas**

1. Nada en esta tabla es evidencia clínica.
2. `UNRESOLVED` no se rellena con cifras de chat; solo con cita curada en SSoT.
3. Los rangos “±20 % asumido” sirven solo para envolventes locales en `analisis_sensibilidad_local_cart.py`.
4. Densidades GPC3 de líneas celulares (literatura) **no** están curadas ni mapeadas al veto del código (`UNRESOLVED`).

Ver también: [`placa_base_instrumento_investigacion.md`](./placa_base_instrumento_investigacion.md).
