# Contributing & Peer Critique Guidelines for Guanes Health

We welcome scientific critique, parameter refinement proposals, and computational reproducibility reports from the systems biology, mathematical oncology, and biophysics communities.

---

## What We Are Looking For

1. **Falsification & Critical Feedback:**  
   Identification of unphysical edge cases, mathematical inconsistencies in ODE coupling, or unrealistic assumptions in baseline parameter distributions.
2. **Parameter Refinements (with Literature Citations):**  
   If you have peer-reviewed experimental literature that refines enzyme kinetics ($, {max}$, pKa of PFK-1, NHE1 flux rates, portal IL-6 kinetics), please open an Issue with the citation (DOI) and proposed values.
3. **Reproducibility Issues:**  
   Reports of test failures, numerical instability in ODE integrators under extreme parameter values, or dependency conflicts in clean Python environments.

---

## How to Submit Feedback

* **Open an Issue:** Use GitHub Issues for technical critique, bug reports, and parameter provenance discussions.
* **Pull Requests:** PRs must include:
  - Clear explanation of the mathematical/biophysical rationale.
  - Updates to the corresponding entry in parameter ledgers with source citations (literature | assumed | in-silico-only).
  - Verification that python 04_Bateria_Inviolable/run_tests_pipeline.py passes 100% with no broken invariants.
* **Academic Inquiries / Collaboration:**  
  For formal manuscript review or research inquiries, contact Manuel Enrique Prada Forero at gerente@guanes.biz.
