# EXPERIMENTAL VALIDATION & FALSIFICATION ROADMAP (WET-LAB)
## Epistemological Demarcation, Kinetic Calibration, and Rejection Criteria (Layer 0 → Layer 4)
**SSoT Technical Specification - Guanes Health v6.0**  
*Author: Manuel Enrique Prada Forero (`gerente@guanes.biz`)*  
*Permanent DOI: [10.5281/zenodo.22101265](https://doi.org/10.5281/zenodo.22101265)*  

---

### 1. Guiding Principle: Falsifiability & Calibration vs. Claims of Cure

> **Core Epistemological Postulate:**  
> The experimental validation of the **Guanes Health v6.0** simulation suite is **NOT** intended to "prove that a therapy cures", but to **falsify, bound, or calibrate deterministic numerical predictions** derived from ordinary differential equations (ODEs) against direct, quantitative wet-lab biological measurements.

Any discrepancy in order of magnitude, mathematical sign, or temporal kinetics between in silico outputs and biological reality is not concealed through parameter tweaking (*overfitting*), but acts as a **formal rejection criterion** for the underlying module.

---

### 2. Frozen Core Predictions & Falsification Matrix

| # | In-Silico Prediction ($t, \text{condition}$) | Measurable Biological Analyte | In-Silico Target Value | Calibration / Success Metric | Formal Rejection Criterion (Kill Switch) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **P1** | $\text{pH}_e = 6.20 \implies$ Cytosolic acidification & ATP collapse ($t=180\,\text{min}$) | Ratiometric $\text{pH}_i$ (SNARF-1 / BCECF-AM) & relative $[\text{ATP}]$ (luciferase / Seahorse) | $\text{pH}_i \le 5.90$ and $[\text{ATP}] < 5.0\%$ of baseline at pH 7.40 | Sigmoidal collapse profile ($RMSE < 12\%$) | If after 3 h at $\text{pH}_e = 6.20$, $[\text{ATP}] > 25\%$ without intervention, **the PFK-1 glycolytic arrest hypothesis is falsified**. |
| **P2** | Active proton extrusion (NHE1-Shield 1K3R4E) preserves bioenergetics & cytolysis at $\text{pH}_e = 6.20$ | Same P1 assay $\pm$ Cariporide / EIPA ($10\,\mu\text{M}$) or $\pm$ NHE1 overexpression | With active NHE1: $\text{pH}_i \ge 6.80$, $[\text{ATP}] \ge 85\%$, Cytolysis (Incucyte / LDH) $\ge 40\%$ | Statistically significant divergence ($p < 0.001$, $\Delta \text{ATP} > 50\%$) vs WT | If pharmacological NHE1 blockade does not cause an ATP collapse in acidic media, **the "NHE1-Shield" does not sustain lytic bioenergetics**. |
| **P3** | Mucosal barrier decay ($\phi_{\text{gut}} < 0.89$) $\implies$ Portal $\text{IL-6} \uparrow \implies \text{PD-L1} \uparrow \implies \text{Epigenetic Lock}$ | Co-culture under LPS ($0.1\text{--}10\,\text{ng/mL}$) or $\text{IL-6}$; measure STAT3-P, surface PD-L1 (flow cytometry), and TOX | $\text{PD-L1} > 4.0\times$ baseline; TOX induction and lytic arrest at 48–72 h | Saturable dose-response curve coupled to the JAK/STAT3 pathway | If PD-L1 induction or exhaustion uncouples from endotoxin/IL-6 concentrations, **the multi-scale portal-stromal coupling is invalid**. |
| **P4** | Critical threshold of barrier integrity ($\phi_{\text{gut}} \approx 0.90$) required for active cytolysis | Parameter sweep of epithelial integrity / permeability vs Active Cytolytic Time (ACT) | Nonlinear phase transition (bifurcation) in the window $\phi_{\text{gut}} \in [0.85, 0.92]$ | Sharp sigmoidal curve with inflection point in predicted range | If the cytolytic response is linear/flat without a sharp threshold, **the bifurcation threshold is a mathematical artifact**. |

---

### 3. De-Risking Hierarchy (Layer 0 → Layer 4)

1. **Layer 0 — Internal Consistency ($0 Cost):** Deterministic ODE checks, fail-closed invariant validation, global sensitivity analysis.
2. **Layer 1 — The "Experiment Zero" (Cellular / Minimal In-Vitro Assay):** Primary CD8+ T-cells or CAR-Ts at $\text{pH}_e 7.4 \text{ vs } 6.2 \pm \text{Cariporide/EIPA}$. Measures $\text{pH}_i$, $[\text{ATP}]$ (CellTiter-Glo/Seahorse), and cytolysis at 3–6 h.
3. **Layer 2 — Reduced Systemic Axis & 3D Co-culture:** Caco-2 transwell (TEER) + Kupffer/Hepatocyte + 3D tumor spheroids (LPS/IL-6/PD-L1/TOX dynamics).
4. **Layer 3 — Preclinical In-Vivo Validation (Murine Models):** Orthotopic HCC models / xenografts: stroma microelectrodes (pH), portal LPS, *Akkermansia* reconstitution, tumor control. *Only executed if Layer 1 passes*.
5. **Layer 4 — Clinical Cohort Correlation:** Retrospective & prospective patient biomarkers (stromal pH, serum endotoxin, 16S microbiome, portal IL-6, tumor PD-L1/TOX).

---

### 4. Operationalization Matrix for Latent Parameters ($\phi_{\text{gut}}$)

| Model Parameter | Biological Operable Variable | Standard Measurement Assay | Normal Physiological Range ($\phi_{\text{gut}} \approx 1.0$) | Pathological Regimes ($\phi_{\text{gut}} \le 0.3$) |
| :--- | :--- | :--- | :--- | :--- |
| $\phi_{\text{gut}}$ (Barrier Seal) | Transepithelial Electrical Resistance (TEER) | Epithelial Volt-Ohm Meter (EVOM) | $> 400\,\Omega \cdot \text{cm}^2$ | $< 80\,\Omega \cdot \text{cm}^2$ |
| $\phi_{\text{gut}}$ (Macromolecular Flux) | FITC-Dextran (4 kDa) flux | Fluorescence Spectrometry | $P_{app} < 1 \times 10^{-6}\,\text{cm/s}$ | $P_{app} > 8 \times 10^{-6}\,\text{cm/s}$ |
| $K_{\text{LPS}}$ (Translocated Endotoxin) | Free Lipopolysaccharide (LPS) concentration | Kinetic Chromogenic LAL / rFC assay | $< 0.1\,\text{EU/mL}$ ($< 10\,\text{pg/mL}$) | $1.5\text{--}10.0\,\text{EU/mL}$ ($150\text{--}1000\,\text{pg/mL}$) |
| Microbiome Proxy | Relative abundance of *Akkermansia muciniphila* | qPCR / 16S rRNA / Shotgun Metagenomics | $3.0\%\text{--}5.0\%$ total fecal microbiome | $< 0.01\%$ (undetectable) |
| Portal Cytokines | Interleukin-6 ($\text{IL-6}$) in portal/systemic serum | High-Sensitivity ELISA / Luminex | $< 3.0\,\text{pg/mL}$ | $20.0\text{--}150.0\,\text{pg/mL}$ |

---

### 5. Statistical Rigor & Protocol Registration

* **Pre-Registration:** Target kinetic checkpoints ($t=180\,\text{min}$, $\text{pH}_e=6.20$) frozen prior to wet-lab data collection.
* **Biological vs. Technical Replicates:** Minimum $N=3$ distinct biological donors, $n \ge 3$ technical replicates per condition.
* **Train / Test Dataset Partitioning:** Calibration dataset used strictly for kinetic constant refinement ($V_{\max}, K_m$). **No-refit policy** strictly enforced on independent validation test runs.
* **Quantitative Error Thresholds:** Normalized Root Mean Square Error ($NRMSE \le 15\%$), Coefficient of Determination ($R^2 \ge 0.85$).
