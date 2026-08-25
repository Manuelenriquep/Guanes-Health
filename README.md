# Guanes Health: Deterministic In Silico Biophysical Modeling Suite (v6.0)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22101265.svg)](https://doi.org/10.5281/zenodo.22101265)
[![White Paper](https://img.shields.io/badge/White%20Paper-v6.0%20Technical%20Report-blueviolet.svg)](01_Especificaciones_SSoT/white_paper_guanes_health_v6.md)
[![License: Source-Available v1.1](https://img.shields.io/badge/License-Source--Available%20v1.1-blue.svg)](LICENSE)
[![Online Console](https://img.shields.io/badge/Live%20Console-health.guanes.biz-0ea5e9.svg)](https://health.guanes.biz)
[![Tests: 100% PASS](https://img.shields.io/badge/Tests-14%2F14%20PASS-emerald.svg)](04_Bateria_Inviolable)

**Guanes Health** is an open research instrument and deterministic *in silico* simulation suite modeling the multi-scale coupling between **local tumor microenvironmental biophysics** (acidosis, proton transport kinetics, and bioenergetic collapse) and the **systemic entero-hepatic immune axis** (mucosal barrier integrity, endotoxemia, and epigenetic exhaustion).

---

## 1. Epistemological Demarcation & Scope Discipline

* **Layer B Research Instrument:** This software is a deterministic computational model designed to test the logical consistency and physical limits of mechanistic hypotheses. It is **not** a clinical diagnostic tool, a therapeutic recommendation engine, or an ontology of living tissue.
* **Fail-Closed Rigor (`POLITICA_RELLENO = NUNCA`):** Zero heuristic imputation for unobserved physiological variables. Any state transition violating thermodynamic or physical boundaries immediately triggers a `VETO_FAIL_CLOSED` or `ALARMA_DERIVA_FISICA`.
* **Traceable Ledgers:** All numeric constants are cataloged with provenance labels (`literature`, `measured`, or `synthetic illustration`) in [`physical_constants_ledger_v2.json`](../guanes-health-core/physical_constants_ledger_v2.json).

---

## 2. The Dual-Pincer Mechanistic Paradigm

Current cancer immunotherapy focuses predominantly on genomic antigen identification (the "brute force" software approach). Guanes Health models why perfect antigen recognition inevitably fails *in vivo* if the physical and systemic hardware constraints are ignored.

```
                                  [ DUAL-PINCER BIO-CONTROL ]
                                               │
               ┌───────────────────────────────┴───────────────────────────────┐
               ▼                                                               ▼
  ┌───────────────────────────────┐                               ┌───────────────────────────────┐
  │     1. LOCAL HARDWARE SHIELD  │                               │    2. SYSTEMIC BARRIER AXIS   │
  ├───────────────────────────────┤                               ├───────────────────────────────┤
  │ • Stroma Acidosis (pHe 6.20)  │                               │ • Akkermansia muciniphila     │
  │ • PFK-1 Allosteric Inhibition │                               │ • Mucosal Integrity (φ_gut)   │
  │ • ATP Starvation (< 0.1%)     │                               │ • Portal LPS → IL-6 Surge     │
  │ • Active Extrusion:           │                               │ • Tumor STAT3 / PD-L1 Axis    │
  │   NHE1-Shield (1K3R4E)        │                               │ • TOX Epigenetic Silencing    │
  └───────────────────────────────┘                               └───────────────────────────────┘
```

### A. The Local Front: The mRNA Vaccine Biophysical Paradox
While mRNA personalized vaccines achieve 100% TCR antigen affinity in the lymph node ($\text{pH} = 7.40$), infiltrating a solid tumor stroma ($\text{pH}_e = 6.20$) causes rapid cytosolic acidification ($\text{pH}_i \rightarrow 5.78$). 
* This cooperatively inhibits **Phosphofructokinase-1 (PFK-1)**, collapsing cellular ATP to **0.10%** at 180 min.
* Starved of chemical energy, the lymphocyte suffers complete motor paralysis of lytic vesicle exocytosis (**0.00% real cytolysis**).
* **NHE1-Shield (mutant 1K3R4E)** actively pumps protons, maintaining $\text{pH}_i = 6.85$, retaining **91.28% ATP**, and sustaining **95.42% cytolytic efficacy**.

### B. The Systemic Front: The Gut-Liver Mucosal Gatekeeper
Translocation of portal endotoxins (LPS) under *Leaky Gut* conditions ($\phi_{\text{gut}} < 1.0$) drives hepatic **IL-6 secretion up to 800 pg/mL**, triggering **GP130/STAT3** signaling in hepatocellular carcinoma (HCC).
* Tumor surface **PD-L1 density increases up to 12.1-fold**.
* Chronic synapse saturation activates **TOX**, depositing repressive **H3K27me3** chromatin marks that irreversibly silence *IL2* and *IFNG* promoters.
* **Bifurcation Threshold:** Active cytolysis ($\text{ACT} \ge 50\%$) strictly requires a mucosal seal of **$\phi_{\text{gut}} \ge 89.9\%$** (*Akkermansia muciniphila*).

---

## 3. Simulation Engines & Reproducibility

Every scenario is fully reproducible locally via Python 3:

```bash
# 1. mRNA Vaccine Biophysical Limit vs. NHE1-Shield (6-Hour Kinetic Solver)
py "03_Motor_Oncologico/simulador_limites_vacunas_arn_v1.py"

# 2. Coupled Multi-Scale Ecosystem v6.0 (72-Hour Co-Intervention & Gut Doctrine)
py "03_Motor_Oncologico/simulador_onco_homeostasis_v6.py"

# 3. Active Cytolytic Time (ACT 48-Hour Multi-Scale Co-Intervention)
py "03_Motor_Oncologico/simulador_combinado_akkermansia_nhe1.py"

# 4. Akkermansia Parametric Dose Sweep (φ_gut = 0.0 to 1.0)
py "03_Motor_Oncologico/simulador_barrido_akkermansia_v1.py"

# 5. Gated-6.50 Metabolic Divergence Demo
py "03_Motor_Oncologico/demo_divergencia_estatico_vs_placa.py"
```

High-resolution charts are automatically rendered to [`02_Simulaciones_Visuales/`](02_Simulaciones_Visuales/).

---

## 4. Test Battery & Verification

The repository enforces an inviolable regression suite covering numerical boundaries, halfspace projection, and gating rules:

```bash
py "04_Bateria_Inviolable/run_tests_pipeline.py"
```
*Result: 14/14 suites PASS (100% deterministic alignment).*

---

## 5. Live Interactive Console

Inspect the multi-scale engine in real time through the web HUD interface:
👉 **[https://health.guanes.biz](https://health.guanes.biz)**

---

## 6. Citation & Academic Attribution

If you reference or utilize this simulation framework, mathematical equations, or biophysical ledgers in academic or industrial research, please cite:

```bibtex
@software{prada_forero_2026_guanes_health,
  author       = {Prada Forero, Manuel Enrique},
  title        = {{Guanes Health Simulation Suite: Biophysical and Systemic In Silico Modeling for Cancer Immunotherapy}},
  year         = 2026,
  version      = {6.0.0},
  publisher    = {Zenodo / GitHub},
  doi          = {10.5281/zenodo.22101265},
  url          = {https://health.guanes.biz}
}
```

Or see the native [`CITATION.cff`](./CITATION.cff) file.

---

## 7. License & Authorship

* **Author:** Manuel Enrique Prada Forero
* **License:** `Guanes Health Source-Available License v1.1` (Academic study, peer inspection, and non-commercial audit are permitted. Commercial use or redistribution requires prior written consent).
* **Licensing Contact:** `gerente@guanes.biz`
