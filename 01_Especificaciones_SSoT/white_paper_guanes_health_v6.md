# Guanes Health: A Deterministic In Silico Research Instrument for Modeling Biophysical and Systemic Constraints on Cellular Immunotherapy

**Technical Report v6.0**

**Author:** Manuel Enrique Prada Forero  
**Affiliation:** Guanes Health Collective  
**Contact:** `gerente@guanes.biz`  
**Permanent Digital Object Identifier (DOI):** [10.5281/zenodo.22101265](https://doi.org/10.5281/zenodo.22101265)  
**Interactive Research Instrument:** [https://health.guanes.biz](https://health.guanes.biz)  
**Open Science Repository:** [https://github.com/Manuelenriquep/Guanes-Health](https://github.com/Manuelenriquep/Guanes-Health)  
**Publication Date:** August 25, 2026  
**License:** Guanes Health Source-Available License v1.1  

---

## Abstract

This technical report presents *Guanes Health v6.0*, an open-source, deterministic *in silico* research instrument (Layer B) designed to evaluate the logical consistency and physical boundaries of cellular immunotherapy in solid tumors. Rather than acting as a predictive clinical engine, the model investigates the mechanistic interplay between **local tumor microenvironment (TME) bioenergetics** and the **systemic entero-hepatic immune axis** under explicit, parameter-traceable assumptions.

Under the baseline parameters calibrated in our physical constants ledger, the simulation indicates that exposing conventional CD8+ T lymphocytes to an acidic stroma ($pHe = 6.20$) results in rapid uncompensated cytosolic acidification ($pHi$ decaying to $5.78$ at $180\text{ min}$). Within the model's allosteric framework, this drops Phosphofructokinase-1 (PFK-1) activity to $2.31\%$, reducing simulated cellular ATP to $0.10\%$ and halting model-derived granule exocytosis ($0.00\%$ simulated cytolysis) despite maintaining $100\%$ simulated TCR antigen affinity. In contrast, modeling a constitutively active proton exchanger (**NHE1-Shield 1K3R4E**, based on engineered calmodulin-binding domain deletions) sustains simulated $pHi$ at $6.85$, preserving $91.28\%$ of baseline ATP and maintaining $95.42\%$ cytolytic efficacy within the computational environment.

At the systemic scale, modeling portal endotoxin translocation under compromised mucosal barrier conditions ($\\phi_{\\text{gut}} < 89.9\\%$) produces elevated hepatic IL-6 inputs, driving modeled tumor PD-L1 expression to $11.2\\times$ and triggering simulated epigenetic exhaustion ($\\text{TOX}^+/\\text{H3K27me3}$). Simulated co-intervention restoring mucosal integrity ($\\phi_{\\text{gut}} \\ge 90\\%$) extends simulated Active Cytolytic Time (ACT) to $9.04\text{ hours}$. These computational outputs illustrate the utility of fail-closed deterministic modeling for prioritizing biophysical hypotheses prior to empirical wet-lab validation.

---

## 1. Epistemological Framework & Scope Discipline

*Guanes Health* is structured as a **Layer B research instrument**—a formal mathematical abstraction intended to make kinetic and state hypotheses inspectable, falsifiable, and auditable.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        GUANES HEALTH v6.0 LAYER B ARCHITECTURE                         │
└────────────────────────────────────────────────────────────────────────────────────────┘
  │
  ├── 1. FAIL-CLOSED INVARIANT POLICY (POLITICA_RELLENO = NUNCA)
  │    └── Zero heuristic imputation for unobserved physiological variables.
  │        Any state violating physical bounds triggers VETO_FAIL_CLOSED or ALARMA_DERIVA_FISICA.
  │
  ├── 2. PARAMETER TRACEABILITY
  │    └── Constants are categorized in physical_constants_ledger_v2.json as:
  │        [measured], [literature], or [synthetic illustration].
  │
  └── 3. THE DUAL-PINCER BIO-CONTROL HYPOTHESIS
       ├── Local Front: Tumor Acidosis (pHe 6.20) → PFK-1 / GAPDH Inhibition → ATP Depletion.
       └── Systemic Front: Gut Mucosal Barrier (phi_gut) → LPS / IL-6 Axis → PD-L1 / TOX Lock.
```

### Scope Limitations:
1. **In Silico Abstraction:** This system is a deterministic toy model of control logic and membrane transport kinetics. It is **not** a validated clinical diagnostic system or a pharmacokinetic simulator.
2. **Biological Reality:** Living tissues exhibit spatial heterogeneity, stochastic variations, and redundant signaling networks not captured in simplified ordinary differential equations (ODEs).
3. **Wet-Lab Prerequisite:** All numerical outputs represent computational deductions that require empirical verification through *in vitro* (e.g., Seahorse XF96, microfluidic pH gradients) and *in vivo* studies.

---

## 2. Mathematical Formulation: Local Stroma Bioenergetics

### 2.1 Cytosolic Acidification Dynamics
In the unarmored lymphocyte model, net proton accumulation is governed by passive influx through membrane channels and active extrusion, balanced against intracellular buffering capacity ($\\beta_i \\approx 30\text{ mM/pH unit}$):

$$\\frac{d[H^+]_i}{dt} = \\frac{P_{H} \\cdot A_{\\text{cell}}}{V_{\\text{cell}} \\cdot \\beta_i} \\left( [H^+]_e - [H^+]_i \\right) - J_{\\text{active}}$$

For an unarmored lymphocyte ($J_{\\text{active}} \\approx 0$ under extreme acid stress), exposure to $pHe = 6.20$ results in simulated $pHi$ decay toward $5.78$ with an apparent time constant $\\tau = 45\text{ min}$.

### 2.2 Cooperative Allosteric Inhibition of PFK-1
PFK-1 catalytic efficiency is modeled via a Hill equation with parameters reflecting proton-dependent allosteric inactivation ($pK_a = 6.60, n_{\\text{PFK}} = 4.0$):

$$\\alpha_{\\text{PFK}}(pHi) = \\frac{1}{1 + 10^{n_{\\text{PFK}} \\cdot (pK_a - pHi)}}$$

At model state $pHi = 5.78$, relative PFK-1 activity drops to $\\alpha_{\\text{PFK}} = 2.31\\%$.

### 2.3 ATP Homeostasis & Exocytosis Coupling
Cellular ATP kinetics balance glycolytic generation against baseline maintenance consumption ($k_{\\text{cons}} = 0.05\text{ min}^{-1}$):

$$\\frac{d[\\text{ATP}]}{dt} = k_{\\text{prod}} \\cdot \\alpha_{\\text{PFK}}(pHi) - k_{\\text{cons}} \\cdot [\\text{ATP}]$$

Simulated exocytosis of perforin/granzyme granules is coupled to available chemical energy via a non-linear Hill saturation function ($K_{1/2} = 20\\%$ ATP):

$$\\text{Cytolysis}(\\%) = 100 \\cdot \\frac{[\\text{ATP}]^2}{[\\text{ATP}]^2 + K_{1/2}^2}$$

Under prolonged stroma acidosis ($t = 180\text{ min}$), model ATP declines to $0.10\\%$, resulting in simulated cytolytic arrest ($0.00\\%$ efficiency) despite constant $100\\%$ modeled TCR antigen recognition.

---

## 3. Ion Transport Engineering: NHE1-Shield (1K3R4E)

The **NHE1-Shield construct** models the biophysical consequences of expressing an engineered $\\text{Na}^+/\\text{H}^+$ exchanger (mutant 1K3R4E; K641E/R643E/R645E/R647E) uncoupled from autoinhibitory calmodulin regulatory domains ($V_{\\text{max}} = 22.0\text{ mM/min}, pK_a = 6.75$):

$$J_{\\text{active}} = \\frac{V_{\\text{max}}}{1 + 10^{n \\cdot (pHi - pK_a)}}$$

Within the simulation:
* Simulated $pHi$ stabilizes at dynamic equilibrium: **$6.85$**.
* Modeled PFK-1 activity is retained at **$71.53\\%$**.
* Simulated cellular ATP pool is maintained at **$91.28\\%$**.
* Modeled cytolytic capacity persists at **$95.42\\%$**.

---

## 4. Multi-Scale Entero-Hepatic Coupling: The Akkermansia Axis

The systemic module models portal endotoxin translocation as a function of normalized mucosal barrier integrity ($\\phi_{\\text{gut}} \\in [0.0, 1.0]$):

1. **Portal IL-6 Input:**
   $$\\text{IL-6}_{\\text{portal}} = \\text{IL-6}_{\\text{physio}} + K_{\\text{LPS-IL6}} \\cdot (1.0 - \\phi_{\\text{gut}}) \\cdot 0.8$$
2. **Modeled Tumor PD-L1 Induction:**
   $$\\text{PD-L1}_{\\text{fold}} = 1.0 + \\alpha_{\\text{PDL1}} \\cdot \\left( \\frac{\\text{IL-6}}{\\text{IL-6} + K_{\\text{IL6}}} \\right)$$
3. **Epigenetic Exhaustion Score (TOX / H3K27me3):**
   $$\\text{H3K27me3}(\\%) = \\min\\left(100.0, \\, \\left(\\frac{\\text{PD-L1}}{16.0}\\right) \\cdot \\left(\\frac{\\text{IL-6}}{\\text{IL-6} + K_{\\text{IL6}}}\\right) \\cdot 125\\right)$$

**Model Threshold:** Within the simulation parameters, sustaining effective cytolysis ($ACT \\ge 9.0\text{ h}$) strictly requires dual intervention: mucosal barrier sealing ($\\phi_{\\text{gut}} \\ge 89.9\\%$, calibrated to *Akkermansia muciniphila* postbiotic/probiotic administration) and local ion transport shielding (NHE1-Shield).

---

## 5. Model Output Summary (t = 180 min Simulation Run)

*Note: All values below represent deterministic computational outputs under ledger parameterization, not in vivo clinical measurements.*

| Parameter | Basal ($t=0$) | Conventional Model ($t=180\text{m}$) | NHE1-Shield Model ($t=180\text{m}$) | Full Synergy Model (*Akkermansia* + NHE1) |
| :--- | :---: | :---: | :---: | :---: |
| **Extracellular pH ($pHe$)** | $7.40$ | $6.20$ | $6.20$ | $6.20$ |
| **Simulated Cytosolic pH ($pHi$)** | $7.20$ | $5.78$ | $6.85$ | $6.85$ |
| **Modeled PFK-1 Glycolytic Activity** | $80.2\\%$ | $2.31\\%$ | $71.5\\%$ | $71.5\\%$ |
| **Simulated Cellular ATP Pool** | $100.0\\%$ | $0.10\\%$ | $91.3\\%$ | $91.3\\%$ |
| **Modeled TCR Antigen Recognition** | $100.0\\%$ | $100.0\\%$ | $100.0\\%$ | $100.0\\%$ |
| **Modeled Tumor PD-L1 Induction** | $1.0\\times$ | $11.2\\times$ | $11.2\\times$ | $2.6\\times$ |
| **Modeled Epigenetic Exhaustion** | $0.0\\%$ | $85.0\\%$ | $85.0\\%$ | $18.2\\%$ |
| **Modeled Active Cytolytic Time (ACT)** | N/A | $1.06\text{ h}$ | $2.50\text{ h}$ | **$9.04\text{ h}$** |
| **Modeled Final Lysis Efficacy** | $96.1\\%$ | **$0.00\\%$** | $16.5\\%$ | **$100.0\\%$ (Clearance)** |

---

## 6. Reproducibility & Code Availability

The complete source code, test batteries, and visual generation engines are openly accessible:

```bash
# 1. Run 6-Hour Biophysical Limits Simulation
py "03_Motor_Oncologico/simulador_limites_vacunas_arn_v1.py"

# 2. Run 72-Hour Multi-Scale Coupled Ecosystem
py "03_Motor_Oncologico/simulador_onco_homeostasis_v6.py"

# 3. Execute Full Regression Suite (14/14 Suites PASS)
py "04_Bateria_Inviolable/run_tests_pipeline.py"
```

Live web implementation: [https://health.guanes.biz](https://health.guanes.biz)

---

## 7. Citation & Attribution

```bibtex
@techreport{prada_forero_2026_guanes_health,
  author       = {Prada Forero, Manuel Enrique},
  title        = {{Guanes Health: A Deterministic In Silico Research Instrument for Modeling Biophysical and Systemic Constraints on Cellular Immunotherapy}},
  institution  = {Guanes Health Collective},
  year         = 2026,
  month        = aug,
  type         = {Technical Report},
  number       = {GH-TR-2026-v6.0},
  doi          = {10.5281/zenodo.22101265},
  url          = {https://health.guanes.biz}
}
```
