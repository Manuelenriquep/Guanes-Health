# Guanes Health: In-Silico Biophysical Simulation Prototype (v6.0)

> **Deterministic in-silico prototype of coupled biophysical and systemic constraints on T-cell function. Not clinically validated.**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22101265.svg)](https://doi.org/10.5281/zenodo.22101265)
[![Technical Report](https://img.shields.io/badge/Technical%20Report-White%20Paper%20v6.0-blueviolet.svg)](01_Especificaciones_SSoT/white_paper_guanes_health_v6.md)
[![License: Source-Available v1.1](https://img.shields.io/badge/License-Source--Available%20v1.1-blue.svg)](LICENSE)
[![Online Console](https://img.shields.io/badge/Interactive%20Console-health.guanes.biz-0ea5e9.svg)](https://health.guanes.biz)
[![Tests: PASS](https://img.shields.io/badge/Tests-14%2F14%20PASS-emerald.svg)](04_Bateria_Inviolable)

**Guanes Health** is an independent computational biology prototype and deterministic *in silico* research instrument modeling the multi-scale coupling between **local tumor microenvironmental biophysics** (acidosis, proton transport kinetics, and PFK-1 metabolic inhibition) and the **systemic entero-hepatic immune axis** (mucosal barrier integrity, endotoxemia, and epigenetic histone silencing).

---

## 1. What This Is and What It Is NOT

### What this IS:
* A **deterministic theoretical research prototype** designed to explore mathematical hypotheses and physical constraints in computational oncology.
* A **coupled ODE simulation suite** investigating how local proton extrusion (NHE1 kinetics) and mucosal barrier parameters (phi_gut) jointly influence T-cell bioenergetics in silico.
* An **open-source / source-available computational codebase** with full parameter traceability and deterministic test invariants.

### What this is NOT:
* NOT a clinical tool or medical device: Outputs must not be used for clinical decision-making, diagnosis, or prognosis.
* NOT an experimentally validated model: The simulations have not been calibrated or validated against wet-lab biological assays or patient clinical trial cohorts.
* NOT a therapeutic recommendation or cure: No claim of medical efficacy, therapeutic outcome, or disease cure is made or implied.

---

## 2. Reproduce Simulation Outputs

All simulation figures and statistical tables can be reproduced deterministically from the command line:

### Prerequisites:
* Python 3.12+
* Dependencies: `numpy`, `scipy`, `pandas`, `matplotlib`, `seaborn`

```bash
# Clone the repository
git clone https://github.com/Manuelenriquep/Guanes-Health.git
cd Guanes-Health

# Install dependencies
pip install -r requirements.txt
```

### Reproducibility Commands:

```bash
# 1. 100-Patient Virtual Cohort (4 Arms: Standard, Akkermansia, NHE1, Synergy)
python "03_Motor_Oncologico/simulador_poblacional_vacunas_arn.py"

# 2. Coupled Multi-Scale Dynamic Model (72-Hour ODE Solver)
python "03_Motor_Oncologico/simulador_onco_homeostasis_v6.py"

# 3. Active Cytolytic Time Sweep (ACT 48-Hour Co-Intervention)
python "03_Motor_Oncologico/simulador_combinado_akkermansia_nhe1.py"

# 4. Inviolable Regression Test Suite (14/14 Suites)
python "04_Bateria_Inviolable/run_tests_pipeline.py"
```

### Generated Artifacts:
| Output File | Location | Description |
| :--- | :--- | :--- |
| `grafico_poblacional_vacunas_arn.png` | `02_Simulaciones_Visuales/` | 4-panel distribution of cytolytic efficacy across 100 simulated patients |
| `resultados_simulacion_pacientes_arn.csv` | `02_Simulaciones_Visuales/` | Raw numerical telemetry for all 100 virtual patient parameter sets |
| `analisis_estocastico_oxigeno.png` | `02_Simulaciones_Visuales/` | In silico sensitivity analysis under stochastic oxygen/pH regimes |

---

## 3. Parameter Ledger & Provenance

Every physical, enzymatic, and kinetic constant used by the solvers is cataloged with its explicit source in the parameter ledgers:

| Parameter Symbol | Description | Baseline Value | Unit | Provenance Source | Notes |
| :--- | :--- | :---: | :---: | :---: | :--- |
| pHe | Extracellular Stroma pH | 6.20 | pH units | Literature | Typical solid tumor acidic core (Warburg effect) |
| pKa_PFK | PFK-1 Allosteric pKa | 6.80 | pH units | Literature | Cooperativity threshold for glycolytic pacemaker |
| n_PFK | Hill Coefficient (PFK-1) | 4.0 | dimensionless | Assumed | Cooperative proton binding model |
| Vmax_NHE1 | NHE1 Max Proton Flux | 1.2e-14 | mol/(s*cell) | In-Silico Only | Calibrated for 1K3R4E mutant extrusion rate |
| IL6_physio | Baseline Portal IL-6 | 2.50 | pg/mL | Literature | Healthy portal venous concentration |
| K_LPS | LPS-induced IL-6 Scaling | 650.0 | pg/mL | Assumed | Maximal portal cytokine surge under severe barrier leak |
| phi_gut | Mucosal Barrier Integrity | 0.20 - 1.00 | normalized ratio | In-Silico Scenario | Proxy for Akkermansia muciniphila abundance |

*Full Ledgers:*
* [`physical_constants_ledger_v2.json`](01_Especificaciones_SSoT/ledger_parametros_nucleo.md)
* [`mct1_pharmacology_ledger.json`](01_Especificaciones_SSoT/ledger_parametros_cart_hcc.md)

---

## 4. Known Model Limitations

1. **Spatial Homogeneity:** The tumor stroma is modeled as a well-mixed single compartment without 3D spatial diffusion gradients or vascular heterogeneity.
2. **Simplified Microbiome Proxy:** The systemic gut barrier is represented by a single lumped parameter (phi_gut) inspired by *Akkermansia muciniphila*, omitting complex polymicrobial interactions.
3. **Short Temporal Horizon:** Solvers model acute dynamics (48 to 72 hours) and do not account for long-term immune selection, tumor clonal evolution, or systemic tolerance.
4. **No Direct Wet-Lab Calibration:** Equations represent theoretical biophysical formulations and have not undergone experimental wet-lab biological calibration.
5. **Deterministic In-Silico Cohorts:** The 100-patient simulation draws from synthetic parameter distributions to test model sensitivity, not from clinical patient datasets.
6. **Binary Resistance States:** The NHE1-Shield is modeled as a binary functional state rather than continuous surface expression kinetics.

---

---

## 5. Technical Report & Formal Specification

For a comprehensive derivation of the coupled differential equations, parameter provenance, and 100-patient virtual cohort analysis, please read the complete Technical Report:

👉 **[Technical Report v6.0 (White Paper)](01_Especificaciones_SSoT/white_paper_guanes_health_v6.md)**

---

## 6. Interactive Research HUD

An interactive parameter exploration HUD is available at:  
👉 **[https://health.guanes.biz](https://health.guanes.biz)**

---

## 7. Citation & Academic Attribution

If referencing this computational prototype or its biophysical equations in academic research:

```bibtex
@software{prada_forero_2026_guanes_health,
  author       = {Prada Forero, Manuel Enrique},
  title        = {{Guanes Health Simulation Suite: Biophysical and Systemic In Silico Modeling for Cancer Immunotherapy}},
  year         = 2026,
  version      = {6.0.0},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.22101265},
  url          = {https://health.guanes.biz}
}
```

---


---

## 8. How to Critique This Model

We invite peer researchers in mathematical oncology and biophysics to test, critique, and attempt to falsify this prototype against the following open questions:

1. **Enzyme Kinetics Sensitivity:** Is the Hill cooperative model of PFK-1 inhibition ({\\text{PFK}}=4.0$, $\\text{pKa}=6.80$) adequately calibrated against intact T-cell glycolytic flux data, or does intracellular buffering mitigate the ATP collapse?
2. **Microbiome Proxy Granularity:** Does the lumped parameter $\\phi_{\\text{gut}}$ represent portal LPS translocation with sufficient fidelity, or are specific bacterial taxa dynamics required?
3. **NHE1 Flux Feasibility:** Are the continuous proton extrusion rates assumed for the NHE1-Shield (.2 \\times 10^{-14} \\text{mol}/(\\text{s}\\cdot\\text{cell})$) thermodynamically feasible under sustained energetic demands?
4. **Spatial Gradients:** How would 3D reaction-diffusion equations across a vascularized tumor geometry alter the predicted Active Cytolytic Time (ACT) thresholds?

To propose parameter corrections or report mathematical edge cases, please see [CONTRIBUTING.md](CONTRIBUTING.md) or open an Issue.

## 9. License & Ethics Statement

* **Author:** Manuel Enrique Prada Forero (`gerente@guanes.biz`)
* **License:** [Source-Available v1.1](LICENSE) (Free for academic research, evaluation, and peer review. Commercial application requires authorization).
* **Statement:** This software was created for computational science research. All users agree that model outputs are theoretical approximations and will not be applied to medical treatment or clinical decision-making.
