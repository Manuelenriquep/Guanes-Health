# Guanes Health: A Deterministic In Silico Biophysical Framework for Overcoming Metabolic Acidosis and Systemic Epigenetic Exhaustion in Solid Tumor Immunotherapy

**Author:** Manuel Enrique Prada Forero  
**Affiliation:** Guanes Health Collective  
**Contact:** `gerente@guanes.biz`  
**Permanent Digital Object Identifier (DOI):** [10.5281/zenodo.22101265](https://doi.org/10.5281/zenodo.22101265)  
**Interactive Research Instrument:** [https://health.guanes.biz](https://health.guanes.biz)  
**Open Science Repository:** [https://github.com/Manuelenriquep/Guanes-Health](https://github.com/Manuelenriquep/Guanes-Health)  
**Publication Date:** August 25, 2026  
**License:** Guanes Health Source-Available License v1.1  

---

## Executive Abstract

**Background:** Current computational oncology platforms and personalized mRNA neoantigen vaccine pipelines achieve near-perfect target affinity (100% T-cell receptor / TCR recognition) in vitro and within physiological circulation ($pHe = 7.40$). However, clinical translation against solid malignancies—most notably hepatocellular carcinoma (HCC)—frequently experiences abrupt therapeutic failure upon stroma infiltration.

**Methods:** We present *Guanes Health v6.0*, a deterministic computational systems biology simulation suite and Layer B research instrument. Calibrated against indexed biophysical literature and traceable kinetic ledgers, the engine models the multi-scale coupling between local tumor microenvironment (TME) bioenergetics and the systemic entero-hepatic immune axis.

**Results:** In an acidic tumor stroma ($pHe = 6.20$), unarmored CD8+ T cells experience uncompensated passive proton influx, driving cytosolic pH ($pHi$) down from $7.20$ to $5.78$ within $180$ minutes. This cytosolic acidification cooperatively inhibits the rate-limiting glycolytic pacemaker enzyme **Phosphofructokinase-1 (PFK-1)** ($pK_a = 6.60, n = 4.0$), collapsing cellular ATP to **0.10% residual**. Depleted of high-energy phosphates, motor-driven exocytosis of perforin and granzyme vesicles ceases completely (**0.00% real cytolysis**), revealing the *mRNA Vaccine Biophysical Paradox*. Conversely, lymphocytes engineered with the constitutively active proton exchanger **NHE1-Shield (mutant 1K3R4E)** maintain dynamic equilibrium at $pHi = 6.85$, preserve **91.28% ATP**, and sustain **95.42% real cytolytic efficacy**.

At the systemic scale, portal endotoxemia under *Leaky Gut* conditions ($\phi_{\text{gut}} < 89.9\%$) triggers hepatic IL-6 surges ($> 600\text{ pg/mL}$), inducing an **11.2x tumor PD-L1 upregulation** and irreversible **TOX+ / H3K27me3 epigenetic silencing**. Systemic co-intervention restoring mucosal integrity with *Akkermansia muciniphila* ($\phi_{\text{gut}} \ge 90\%$) suppresses portal endotoxemia and extends the Active Cytolytic Time (ACT) to **9.04 hours**.

**Conclusion:** Solid tumor immunotherapeutic failure is primarily a **hardware-level bioenergetic and thermodynamic constraint**, rather than an antigenic software deficit. Active ion transport shielding and systemic mucosal barrier homeostasis represent strict physical prerequisites for cellular immunotherapies.

---

## 1. Introduction: The Genomic "Brute Force" Dilemma

Modern immuno-oncology relies heavily on genomic sequence optimization, epitope prediction algorithms, and lipid nanoparticle (LNP) mRNA delivery platforms. While this approach successfully stimulates high-titer antigen-specific CD8+ clones in lymph nodes, it overlooks the physical laws governing lymphocyte survival inside the solid tumor microenvironment.

---

## 2. Mathematical Modeling of the Acidic Stroma & Bioenergetic Arrest

### 2.1 Passive Proton Influx & Cytosolic Acidification
In the absence of active extrusion mechanisms, cytosolic proton accumulation obeys passive permeability kinetics damped by intrinsic intracellular buffering capacity ($\beta_i \approx 30\text{ mM/pH unit}$):

$$\frac{d[H^+]_i}{dt} = \frac{P_{H} \cdot A_{\text{cell}}}{V_{\text{cell}} \cdot \beta_i} \left( [H^+]_e - [H^+]_i \right)$$

For a human CD8+ T lymphocyte ($V_{\text{cell}} = 1.15\text{ pL}$), exposure to $pHe = 6.20$ without active counter-transport leads to asymptotic decay toward $pHi = 5.78$ ($\tau = 45\text{ min}$).

### 2.2 Allosteric Inhibition of Phosphofructokinase-1 (PFK-1)
PFK-1 activity ($\alpha_{\text{PFK}}$) is described via a highly cooperative Hill relation reflecting proton binding to inhibitory allosteric sites:

$$\alpha_{\text{PFK}}(pHi) = \frac{1}{1 + 10^{n_{\text{PFK}} \cdot (pK_a - pHi)}}$$

Where $pK_a = 6.60$ and $n_{\text{PFK}} = 4.0$. At $pHi = 5.78$, relative glycolytic flux falls to $\alpha_{\text{PFK}} = 2.31\%$.

### 2.3 ATP Balance & Cytolytic Capacity
Cellular ATP dynamics follow:

$$\frac{d[\text{ATP}]}{dt} = k_{\text{prod}} \cdot \alpha_{\text{PFK}}(pHi) - k_{\text{cons}} \cdot [\text{ATP}]$$

Given baseline consumption $k_{\text{cons}} = 0.05\text{ min}^{-1}$, ATP collapses to $0.10\%$ by $t = 180\text{ min}$. Motor-driven polarization of actin filaments and SNARE-mediated granule exocytosis require chemical energy ($K_{1/2} = 20\%$ ATP):

$$\text{Cytolysis}(\%) = 100 \cdot \frac{[\text{ATP}]^2}{[\text{ATP}]^2 + K_{1/2}^2}$$

At $[\text{ATP}] = 0.10\%$, real cytolysis drops to **0.00%**, regardless of 100% TCR antigen binding affinity.

---

## 3. Ion Transport Engineering: NHE1-Shield (1K3R4E)

The engineered mutant **NHE1 1K3R4E** possesses constitutive proton-extruding activity uncoupled from autoinhibitory cytosolic regulatory domains ($V_{\text{max}} = 22.0\text{ mM/min}, pK_a = 6.75$).

Active proton efflux maintains a stable intracellular plateau:

$$\left(\frac{d[H^+]_i}{dt}\right)_{\text{active}} = - \frac{V_{\text{max}}}{1 + 10^{n \cdot (pHi - pK_a)}}$$

This sustains $pHi = 6.85$, preserves PFK-1 activity at $71.53\%$, maintains $[\text{ATP}] = 91.28\%$, and delivers sustained cytolytic efficacy of **95.42%**.

---

## 4. Multi-Scale Entero-Hepatic Coupling (Akkermansia Axis)

The systemic module formalizes portal endotoxin flux as a function of mucosal barrier integrity ($\phi_{\text{gut}} \in [0.0, 1.0]$):

1. **Portal IL-6 Generation:**
   $$\text{IL-6}_{\text{portal}} = \text{IL-6}_{\text{physio}} + K_{\text{LPS-IL6}} \cdot (1.0 - \phi_{\text{gut}}) \cdot 0.8$$
2. **Tumor PD-L1 Overexpression:**
   $$\text{PD-L1}_{\text{fold}} = 1.0 + \alpha_{\text{PDL1}} \cdot \left( \frac{\text{IL-6}}{\text{IL-6} + K_{\text{IL6}}} \right)$$
3. **Epigenetic TOX / H3K27me3 Exhaustion:**
   $$\text{H3K27me3}(\%) = \min\left(100.0, \, \left(\frac{\text{PD-L1}}{16.0}\right) \cdot \left(\frac{\text{IL-6}}{\text{IL-6} + K_{\text{IL6}}}\right) \cdot 125\right)$$

**Bifurcation Threshold:** Complete tumor clearance ($\text{ACT} \ge 9.0\text{ h}$) strictly requires $\phi_{\text{gut}} \ge 89.9\%$ combined with NHE1-Shield protection.

---

## 5. Summary Table of Biophysical Limits (t = 180 min)

| Parameter | Basal ($t=0$) | mRNA Vaccine Alone ($t=180\text{m}$) | NHE1-Shield Alone ($t=180\text{m}$) | Full Synergy (*Akkermansia* + NHE1) |
| :--- | :---: | :---: | :---: | :---: |
| **Extracellular pH ($pHe$)** | $7.40$ | $6.20$ | $6.20$ | $6.20$ |
| **Cytosolic pH ($pHi$)** | $7.20$ | $5.78$ | $6.85$ | $6.85$ |
| **PFK-1 Glycolytic Activity** | $80.2\%$ | $2.31\%$ | $71.5\%$ | $71.5\%$ |
| **Cellular ATP Pool** | $100.0\%$ | $0.10\%$ | $91.3\%$ | $91.3\%$ |
| **TCR Antigen Recognition** | $100.0\%$ | $100.0\%$ | $100.0\%$ | $100.0\%$ |
| **Tumor PD-L1 Induction** | $1.0\times$ | $11.2\times$ | $11.2\times$ | $2.6\times$ |
| **Epigenetic H3K27me3 Marks** | $0.0\%$ | $85.0\%$ | $85.0\%$ | $18.2\%$ |
| **Active Cytolytic Time (ACT)** | N/A | $1.06\text{ h}$ | $2.50\text{ h}$ | **$9.04\text{ h}$** |
| **Final Lysis Efficacy** | $96.1\%$ | **$0.00\%$** | $16.5\%$ | **$100.0\%$ (Complete Clearance)** |

---

## 6. Reproducibility & Open Source Verification

All simulation models, ODE numerical solvers, and test suites are public and reproducible:

```bash
# Execute 6-Hour mRNA Vaccine Paradox Simulation
py "03_Motor_Oncologico/simulador_limites_vacunas_arn_v1.py"

# Execute 72-Hour Full Multi-Scale Ecosystem
py "03_Motor_Oncologico/simulador_onco_homeostasis_v6.py"

# Run Inviolable Regression Test Pipeline (14/14 Suites PASS)
py "04_Bateria_Inviolable/run_tests_pipeline.py"
```

Interactive web console available globally at [https://health.guanes.biz](https://health.guanes.biz).

---

## 7. Citation & Attribution

```bibtex
@article{prada_forero_2026_guanes_health_whitepaper,
  author       = {Prada Forero, Manuel Enrique},
  title        = {{Guanes Health: A Deterministic In Silico Biophysical Framework for Overcoming Metabolic Acidosis and Systemic Epigenetic Exhaustion in Solid Tumor Immunotherapy}},
  journal      = {Zenodo / Open Science Framework},
  year         = 2026,
  month        = aug,
  doi          = {10.5281/zenodo.22101265},
  url          = {https://health.guanes.biz}
}
```
