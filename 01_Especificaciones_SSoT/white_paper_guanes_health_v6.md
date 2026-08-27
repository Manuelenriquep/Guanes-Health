# Guanes Health v6.0: A Deterministic In-Silico Prototype of Coupled Biophysical and Systemic Constraints on T-Cell Function

**Technical Report & Model Specification (v6.0)**

* **Author:** Manuel Enrique Prada Forero (`gerente@guanes.biz`)
* **Affiliation:** Independent Researcher, Bucaramanga, Colombia
* **Permanent DOI:** [10.5281/zenodo.22101265](https://doi.org/10.5281/zenodo.22101265)
* **Code Repository:** [https://github.com/Manuelenriquep/Guanes-Health](https://github.com/Manuelenriquep/Guanes-Health)
* **Interactive Console:** [https://health.guanes.biz](https://health.guanes.biz)
* **Release Date:** August 2026
* **License:** Source-Available v1.1 (Academic & Research Evaluation)

---

## 1. Abstract

This technical report presents **Guanes Health v6.0**, an open-source, deterministic *in silico* research prototype (Layer B) modeling the multi-scale coupling between local tumor microenvironment (TME) biophysics and the systemic entero-hepatic immune axis. Rather than serving as a clinical diagnostic or predictive tool, the model evaluates the logical consistency and physical boundaries of mechanistic assumptions governing T-cell dysfunction in solid tumors.

Under baseline parameters cataloged in our physical constants ledger, the simulation demonstrates that exposing conventional CD8+ T lymphocytes to an acidic stroma ($\text{pH}_e = 6.20$) produces rapid cytosolic acidification ($\text{pH}_i \rightarrow 5.78$), allosterically inhibiting phosphofructokinase-1 (PFK-1 activity $< 3.0\%$) and depleting cellular ATP ($< 0.10\%$ at 180 min), resulting in model-derived lytic paralysis despite maintaining $100\%$ simulated TCR antigen affinity. Conversely, modeling an active proton exchange mechanism (**NHE1-Shield 1K3R4E**) maintains simulated $\text{pH}_i$ at $6.85$, sustaining $91.28\%$ of ATP and yielding a simulated lytic efficacy of $50.37\%$. At the systemic scale, modeling mucosal barrier impairment ($\phi_{\text{gut}} < 89.9\%$) produces elevated portal IL-6 inputs, driving modeled tumor PD-L1 expression to $11.2\times$ and inducing simulated epigenetic silencing ($\text{TOX}^+/\text{H3K27me3}$). Simulated co-intervention restoring mucosal integrity ($\phi_{\text{gut}} \ge 90\%$) resolves cytokine leakage and extends simulated Active Cytolytic Time (ACT) to $9.04\text{ hours}$ (overall simulated clearance: $56.32\%$). All equations, parameter provenance categories, reproducible execution protocols, and explicit limitations are detailed herein to invite peer falsification and critical evaluation.

---

## 2. Introduction & Motivation

Current paradigms in cancer immunotherapy—including mRNA-based personalized neoantigen vaccines, immune checkpoint inhibitors, and adoptive cell therapies (CAR-T, TCR-T)—have achieved remarkable precision in genomic antigen identification and synthetic receptor engineering. However, clinical response rates in non-inflamed solid tumors remain highly variable.

Standard computational oncology workflows frequently treat antigen recognition in isolation from physical and systemic hardware constraints:
1. **The Local Biophysical Barrier:** The dense, poorly perfused solid tumor stroma is characterized by severe extracellular acidosis ($\text{pH}_e 6.0 - 6.5$) driven by dysregulated glycolysis and carbonic anhydrase activity. Protons passively permeate infiltrating lymphocytes, allosterically shutting down rate-limiting glycolytic enzymes and paralyzing ATP-dependent kinesin/myosin motors required for lytic granule exocytosis.
2. **The Systemic Entero-Hepatic Axis:** Gut mucosal barrier permeability (*Leaky Gut*) permits the translocation of bacterial lipopolysaccharides (LPS) into the portal circulation, stimulating hepatic Kupffer cells and sinusoidal endothelial cells to secrete IL-6. This portal cytokine surge induces tumor STAT3 phosphorylation and surface PD-L1 upregulation, driving continuous synapse exhaustion and repressive chromatin remodeling (H3K27me3 deposition).

**Guanes Health v6.0** was developed as a deterministic, multi-scale *in silico* research prototype designed to formalize these coupled constraints into an inspectable set of ordinary differential equations (ODEs), establishing a clear mathematical framework for evaluating co-intervention hypotheses prior to experimental wet-lab calibration.

---

## 3. Model Scope & Epistemological Boundaries

To maintain rigorous scientific demarcation, Guanes Health strictly enforces formal architectural boundaries:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        GUANES HEALTH v6.0 LAYER B ARCHITECTURE                         │
└────────────────────────────────────────────────────────────────────────────────────────┘
  │
  ├── 1. FAIL-CLOSED INVARIANT POLICY (POLITICA_RELLENO = NUNCA)
  │    └── Zero heuristic imputation for unobserved physiological variables.
  │        Any state violating physical bounds triggers VETO_FAIL_CLOSED or PARAMETER_OUT_OF_BOUNDS.
  │
  ├── 2. PARAMETER TRACEABILITY
  │    └── Constants are categorized in physical_constants_ledger_v2.json as:
  │        [literature], [assumed], or [in-silico-only].
  │
  └── 3. THE DUAL-PINCER BIO-CONTROL HYPOTHESIS
       ├── Local Front: Tumor Acidosis (pHe 6.20) → PFK-1 Inhibition → ATP Depletion.
       └── Systemic Front: Gut Mucosal Barrier (phi_gut) → LPS / IL-6 Axis → PD-L1 / TOX Lock.
```

### 3.1 What This Model IS:
* A deterministic computational prototype of coupled biophysical and systemic constraints.
* A transparent, reproducible mathematical system modeling enzyme kinetics, ion exchange fluxes, and receptor saturation dynamics.
* A research instrument (Layer B) designed to test the logical consistency of co-intervention hypotheses.

### 3.2 What This Model is NOT:
* ❌ **NOT a clinical tool or medical device:** Outputs cannot and must not be used for patient diagnosis, prognosis, or treatment planning.
* ❌ **NOT an experimentally validated simulator:** The equations represent theoretical biophysical formulations and have not undergone wet-lab biological or clinical trial validation.
* ❌ **NOT a claim of therapeutic cure:** Simulated lytic outcomes are mathematical deductions from fixed toy model assumptions, not clinical predictions.

---

## 4. Mathematical Formulation

The core solver couples four differential and algebraic subsystems:

### 4.1 Local Stroma Acidification & NHE1 Proton Extrusion
Net cytosolic proton accumulation in infiltrating lymphocytes is modeled as passive influx balanced against active extrusion and cytosolic buffering capacity ($\beta_i \approx 30\text{ mM/pH unit}$):

$$\frac{d[H^+]_i}{dt} = \frac{P_H \cdot A_{\text{cell}}}{V_{\text{cell}} \cdot \beta_i} \left( [H^+]_e - [H^+]_i \right) - J_{\text{NHE1}}$$

Where the active proton flux through the engineered NHE1-Shield (constitutively active mutant 1K3R4E) follows Michaelis-Menten kinetics:

$$J_{\text{NHE1}} = V_{\max,\text{NHE1}} \cdot \frac{[H^+]_i}{[H^+]_i + K_{m,\text{NHE1}}}$$

### 4.2 Allosteric Inhibition of Glycolysis (PFK-1 Hill Equation)
Phosphofructokinase-1 (PFK-1) acts as the primary glycolytic pacemaker. Its relative enzymatic activity as a function of cytosolic $\text{pH}_i$ is modeled via a 4-state cooperative Hill formulation:

$$\text{Activity}_{\text{PFK}}(\text{pH}_i) = \frac{1}{1 + 10^{n_{\text{PFK}} \cdot (\text{pKa}_{\text{PFK}} - \text{pH}_i)}}$$

With baseline parameters $n_{\text{PFK}} = 4.0$ and $\text{pKa}_{\text{PFK}} = 6.80$. Cellular ATP production is directly coupled to $\text{Activity}_{\text{PFK}}$:

$$\frac{d[\text{ATP}]}{dt} = k_{\text{glyco}} \cdot \text{Activity}_{\text{PFK}}(\text{pH}_i) - k_{\text{basal\_drain}} \cdot [\text{ATP}]$$

### 4.3 Entero-Hepatic Axis: Mucosal Permeability & PD-L1 Induction
Portal vein IL-6 concentration is coupled to the mucosal barrier integrity parameter $\phi_{\text{gut}} \in [0.0, 1.0]$ (inspired by *Akkermansia muciniphila* abundance):

$$\text{IL-6}_{\text{portal}}(t) = \text{IL-6}_{\text{physio}} + K_{\text{LPS}} \cdot (1.0 - \phi_{\text{gut}})$$

Tumor surface PD-L1 fold-induction is modeled via saturable STAT3 transcriptional activation:

$$\text{PD-L1}_{\text{tumor}}(t) = \text{PD-L1}_{\text{basal}} \cdot \left( 1.0 + \alpha_{\text{IL6}} \cdot \frac{\text{IL-6}_{\text{portal}}}{\text{IL-6}_{\text{portal}} + K_{\text{IL6}}} \right)$$

### 4.4 Epigenetic Exhaustion & Active Cytolytic Time (ACT)
Chronic PD-1/PD-L1 synapse engagement drives the expression of TOX and subsequent repressive histone trimethylation ($\text{H3K27me3}$):

$$\frac{d[\text{H3K27me3}]}{dt} = k_{\text{epi}} \cdot \left( \frac{\text{PD-L1}}{\text{PD-L1} + K_{\text{synapse}}} \right) \cdot (1.0 - [\text{H3K27me3}]) - k_{\text{demeth}} \cdot [\text{H3K27me3}]$$

The instantaneous cytolytic clearance capacity of the lymphocyte pool is defined by:

$$\text{Capacity}_{\text{lytic}}(t) = 100 \cdot \left( \frac{[\text{ATP}]^2}{[\text{ATP}]^2 + K_{\text{half}}^2} \right) \cdot (1.0 - [\text{H3K27me3}])$$

**Active Cytolytic Time (ACT)** is defined as the total cumulative duration (in hours) during which $\text{Capacity}_{\text{lytic}}(t) \ge 30.0\%$.

---

### 4.5 Parameter Provenance Ledger

| Parameter Symbol | Description | Baseline Value | Unit | Provenance Category | Literature Reference / Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- |
| $\text{pH}_e$ | Extracellular Stroma pH | 6.20 | pH units | Literature | Swietach et al. (2014), solid tumor acidic microenvironment |
| $\text{pKa}_{\text{PFK}}$ | PFK-1 Allosteric pKa | 6.80 | pH units | Literature | Ui (1966), Kemp & Foe (1983), proton cooperativity |
| $n_{\text{PFK}}$ | PFK-1 Hill Coefficient | 4.0 | dimensionless | Assumed | 4-subunit cooperative homotetramer model |
| $V_{\max,\text{NHE1}}$ | NHE1 Max Proton Flux | $1.2 \times 10^{-14}$ | $\text{mol}/(\text{s}\cdot\text{cell})$ | In-Silico Only | Calibrated for 1K3R4E active extrusion capacity |
| $\text{IL-6}_{\text{physio}}$ | Baseline Portal IL-6 | 2.50 | $\text{pg/mL}$ | Literature | Wieckowska et al. (2008), portal vein baseline |
| $K_{\text{LPS}}$ | Maximal LPS-driven IL-6 | 650.0 | $\text{pg/mL}$ | Assumed | Calibrated for severe endotoxemic cytokine surge |
| $\phi_{\text{gut}}$ | Mucosal Seal Ratio | 0.20 – 1.00 | normalized | In-Silico Scenario | Proxy for *Akkermansia muciniphila* barrier function |

---

## 5. Simulation Protocol & Reproducibility

The entire simulation suite is deterministic, requires zero external proprietary solvers, and executes in clean Python 3.12 environments.

```bash
# 1. Clone repository and install pinned dependencies
git clone https://github.com/Manuelenriquep/Guanes-Health.git
cd Guanes-Health
pip install -r requirements.txt

# 2. Run 100-Patient Virtual Cohort Simulation
python "03_Motor_Oncologico/simulador_poblacional_vacunas_arn.py"

# 3. Run Coupled 72-Hour Multi-Scale Dynamic Model
python "03_Motor_Oncologico/simulador_onco_homeostasis_v6.py"

# 4. Run Active Cytolytic Time (ACT) 48-Hour Co-Intervention Sweep
python "03_Motor_Oncologico/simulador_combinado_akkermansia_nhe1.py"

# 5. Execute Full Inviolable Regression Battery (14/14 Suites)
python "04_Bateria_Inviolable/run_tests_pipeline.py"
```

All generated tabular outputs (`.csv`) and graphical figures (`.png`) are automatically saved to `02_Simulaciones_Visuales/`.

---

## 6. Illustrative Results (100-Patient Virtual Cohort)

A synthetic cohort of $N=100$ virtual patients was simulated across four distinct intervention arms ($n=25$ per arm) under stochastic microbiome and antigen densities:

| Intervention Arm | Mean Lysis Output (%) | Standard Deviation (%) | Minimum Lysis (%) | Maximum Lysis (%) | Model Interpretation (In Silico) |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Arm A: Standard mRNA Vaccine** | **0.0013%** | 0.0003% | 0.0008% | 0.0018% | Severe energetic arrest due to stroma acidosis ($pHe = 6.20$) and PFK-1 inhibition. |
| **Arm B: Vaccine + Akkermansia** | **0.0015%** | 0.0000% | 0.0015% | 0.0015% | PD-L1 upregulation is mitigated, but unshielded T-cells remain paralyzed by acidity. |
| **Arm C: Vaccine + NHE1-Shield** | **50.37%** | 13.95% | 33.33% | 71.44% | Ion shielding sustains ATP, but efficacy varies depending on basal gut permeability. |
| **Arm D: Total Synergy** | **56.32%** | 0.0000% | 56.32% | 56.32% | Sparing of ATP via NHE1 combined with gut barrier resolution maximizes ACT to 9.04h. |

*Note: Zero standard deviation in Arms B and D indicates deterministic convergence at fixed boundary saturation parameters.*

---

## 7. Known Limitations

1. **Spatial Homogeneity:** The tumor stroma is modeled as a well-mixed single compartment without 3D spatial diffusion gradients, vascular heterogeneity, or hypoxia zones.
2. **Lumped Microbiome Proxy:** The systemic gut barrier is represented by a single continuous scalar ($\phi_{\text{gut}}$) inspired by *Akkermansia muciniphila*, omitting complex polymicrobial community dynamics and short-chain fatty acid (SCFA) signaling.
3. **Acute Temporal Horizon:** Solvers model acute kinetics (48 to 72 hours) and do not account for long-term immune memory formation, antigen escape variants, or systemic tolerance.
4. **No Direct Biological Wet-Lab Calibration:** The equations reflect theoretical biophysical formulations and have not been calibrated against live cell microcalorimetry or microfluidic assays.
5. **Synthetic In-Silico Cohorts:** The 100-patient simulation draws from synthetic parameter distributions to test model sensitivity, not from real patient clinical trial datasets.
6. **Binary Functional States:** The NHE1-Shield is modeled as a binary functional state rather than continuous surface expression and turnover kinetics.

---

## 8. Discussion & Future Directions

### 8.1 Current Value of the Prototype
Guanes Health v6.0 demonstrates that high-affinity antigen recognition is a necessary but insufficient condition for solid tumor clearance if biophysical and systemic constraints are left unaddressed. By modeling the quantitative coupling between enzyme kinetics (PFK-1), membrane transport (NHE1), and mucosal endotoxemia, the suite provides a transparent hypothesis-generating instrument for systems biologists.

### 8.2 Roadmap Toward Experimental Calibration & Falsification Criteria

Validation in this context does not mean "proving clinical efficacy"; it means **empirically bounding, calibrating, or falsifying the deterministic ODE predictions** against wet-lab measurements.

We establish a formalized 5-layer de-risking hierarchy and an immediate **"Experiment Zero"** protocol:
* **Layer 0 (Software Stability & Invariants):** Fail-closed parameter boundaries and deterministic solver convergence ($0 cost).
* **Layer 1 (Cellular In-Vitro Minimum Viable Assay):** Primary CD8+ T-cells or GPC3-CAR-Ts cultured at $\text{pH}_e 7.40 \text{ vs } 6.20 \pm \text{Cariporide/EIPA}$ ($10\,\mu\text{M}$ NHE1 blocker). Primary readouts: ratiometric $\text{pH}_i$ (BCECF-AM), cellular ATP (CellTiter-Glo/Seahorse), and cytolysis at $3\text{--}6\text{ h}$. **Kill Switch:** If unshielded T-cells retain $>25\%$ ATP at 3h under $\text{pH}_e 6.20$, or if NHE1 inhibition causes no bioenergetic penalty in acidic stroma, the PFK-1/NHE1 local hypothesis is formally falsified.
* **Layer 2 (Reduced Systemic Axis):** Caco-2 transwell monocultures ($\text{TEER}$) coupled with LPS/IL-6 challenged hepatocytes and 3D tumor spheroids to test the STAT3 $\rightarrow$ PD-L1 $\rightarrow$ TOX axis.
* **Layer 3 (Preclinical In-Vivo Models):** Murine HCC orthotopic models measuring stroma pH microelectrodes, portal endotoxin, and mucosal integrity proxies.
* **Layer 4 (Clinical Correlation):** Retrospective and prospective multi-omic cohort validation.

*For complete protocols, pre-registration parameters, and latent variable operationalization, see:*  
[`experimental_validation_falsification_roadmap.md`](experimental_validation_falsification_roadmap.md) (English) / [`roadmap_falsacion_experimental_wetlab.md`](roadmap_falsacion_experimental_wetlab.md) (Spanish).

---

## 9. Data & Code Availability

* **GitHub Repository:** [https://github.com/Manuelenriquep/Guanes-Health](https://github.com/Manuelenriquep/Guanes-Health)
* **Permanent Archive DOI:** [10.5281/zenodo.22101265](https://doi.org/10.5281/zenodo.22101265)
* **Interactive Exploration Console:** [https://health.guanes.biz](https://health.guanes.biz)
* **License:** Source-Available v1.1 (Academic evaluation, verification, and non-commercial research).

---

## 10. References

1. **Swietach, P., et al.** (2014). Tumor acidosis and its role in immune evasion and metabolic remodeling. *Philosophical Transactions of the Royal Society B*, 369(1638), 20130098.
2. **Kemp, R. G., & Foe, L. G.** (1983). Allosteric properties of phosphofructokinase. *Molecular and Cellular Biochemistry*, 57(2), 147-154.
3. **Routy, B., et al.** (2018). Gut microbiome influences efficacy of PD-1-based immunotherapy against epithelial tumors. *Science*, 359(6371), 91-97.
4. **Gopalakrishnan, V., et al.** (2018). Gut microbiome modulates response to anti-PD-1 immunotherapy in melanoma patients. *Science*, 359(6371), 97-103.
5. **Wieckowska, A., et al.** (2008). In vivo assessment of portal and systemic IL-6 levels in liver disease. *Hepatology*, 48(6), 1888-1896.
6. **Cardone, R. A., et al.** (2005). The role of NHE1 in tumor cell biology: more than an ion transporter. *Nature Reviews Cancer*, 5(10), 786-795.
7. **Prada Forero, M. E.** (2026). Guanes Health Simulation Suite v6.0. *Zenodo Archive*. DOI: 10.5281/zenodo.22101265.
