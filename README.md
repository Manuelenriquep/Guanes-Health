# Guanes Health

An early computational oncology prototype exploring deterministic, state-based modeling of tumor disruption and therapeutic restoration.

## Overview

Guanes Health is a small Python project built around a simple question:

**Can selected oncological behaviors be represented as explicit failures of cellular control logic, and can therapeutic interventions be modeled as deterministic state-restoration rules?**

This repository does not present a clinical system, a validated scientific simulator, or a production-ready platform. It is an early computational prototype designed to make that question concrete, inspectable, and testable in code.

Its current value lies in scope discipline rather than scale: a narrow model, explicit assumptions, deterministic behavior, and basic automated tests.

## Origin

The project did not begin inside computational oncology.

It began with work on a different problem: applying a "motherboard" or "baseboard" (*placa base*) style of reasoning to document engineering. That approach focused on structure, control surfaces, assertion layers, failure conditions, and deterministic handling of ambiguity in high-stakes information workflows.

After seeing how powerful that framing could be as a **research instrument**, I began exploring whether a similar methodology could help think about biological systems. I spent time researching cancer biology, tumor metabolism, apoptosis, immune evasion, and related control mechanisms through that lens.

**Important:** the placa is a tool for organizing hypotheses and inspectable state. It is **not** a claim that a living cell *is* a silicon motherboard. Biology remains stochastic; the placa remains an engineering abstraction. See `01_Especificaciones_SSoT/placa_base_instrumento_investigacion.md`.

The result was not certainty, but conviction: there seemed to be enough structural coherence in the *method* to justify a computational prototype.

Guanes Health is the first small implementation of that intuition.

## Thesis

The thesis behind this repository is modest in implementation, but ambitious in direction:

some biological problems may become easier to reason about when they are expressed not only as biochemical narratives, but also as constrained systems with inspectable state transitions, failure modes, and restoration paths.

The current prototype treats a narrow cellular scenario as a deterministic model with:

- a healthy baseline state,
- a tumor state defined by simplified metabolic, apoptotic, and immune-evasion conditions,
- an intervention layer that compares isolated immunotherapy against a combined restoration protocol.

This is a computational abstraction, not a claim that biology can be reduced to software metaphors. The purpose is to create a structure that can be criticized, revised, or rejected on technical grounds.

## What Exists in This Repository

At the moment, this repository contains an early deterministic simulation written in Python.

It includes:

- a minimal healthy-cell model,
- a minimal tumor-cell model,
- a restoration module simulating isolated and combined intervention paths,
- fail-closed validation for invalid or physically inconsistent inputs,
- a small automated unit test suite.

This makes the project more than a written concept, but still far from a mature scientific system.

## Design Principles

The current codebase follows a few strict principles:

- **Determinism:** identical inputs should produce identical outputs.
- **Inspectability:** assumptions should be visible in code, not hidden in rhetoric.
- **Fail-closed behavior:** invalid states should halt execution rather than pass silently.
- **Minimal scope:** the model should remain small enough to audit directly.
- **Testability:** core claims of the prototype should be expressible as automated tests.

These constraints are intentional. If the abstraction cannot remain coherent at small scale, it does not yet deserve to grow.

## What This Repository Does Not Claim

This project does **not** currently claim:

- clinical validity,
- experimental validation,
- molecular simulation fidelity,
- pharmacokinetic or pharmacodynamic realism,
- integration with biological datasets,
- regulatory-grade guarantees,
- a complete or final theory of oncological control.

Those are future research and engineering questions, not present accomplishments.

## Why Publish It Publicly

This repository is public because early ideas improve when they are exposed to serious scrutiny.

Publishing the prototype forces precision. It makes assumptions legible. It allows critique to attach to code rather than to vague ambition. It also creates a record of what exists today, what is only hypothesized, and what still needs to be earned through deeper work.

If the underlying idea has value, it should become clearer under criticism, not weaker.

## Repository Structure

- `AGENTS.md`  
  Binding contract for AI collaborators (placa = instrument; no clinical overclaim).

- `01_Especificaciones_SSoT/`  
  Operational SSoT. Start at `00_INDICE.md`. Includes epistemology of the *placa* and the three-agent pipeline contract. Broad narrative of the method belongs in a future book, not here.

- `02_Simulaciones_Visuales/`  
  Charts from model runs (illustrative, not clinical evidence).

- `03_Motor_Oncologico/`  
  Core Python prototype (`placa_*.py` = model artifacts, not biological identity claims).

- `04_Bateria_Inviolable/`  
  Unit tests covering the main modeled scenarios.

## Running the Prototype

From the repository root:

```bash
py "03_Motor_Oncologico/parche_restauracion.py"
```

This runs the current deterministic demonstration and prints the healthy baseline, the isolated immunotherapy path, and the combined restoration scenario.

## Running the Tests

From the repository root:

```bash
py -m unittest discover -s "04_Bateria_Inviolable" -v
```

The current test suite is intentionally small and focused on the main modeled scenarios.

## License

This repository is distributed under the `Guanes Health Source-Available License v1.1`.

The code is public for inspection, private study, and non-commercial evaluation. Commercial use, redistribution, sublicensing, and productization require prior written permission from the author. See `LICENSE` for details.

Commercial licensing inquiries: `gerente@guanes.biz`

## What Feedback Would Be Most Valuable

The most valuable feedback at this stage is direct and technical.

I am especially interested in critique on:

- whether the abstraction is coherent,
- whether the modeled states are too crude to be meaningful,
- whether the deterministic framing clarifies or distorts the biology,
- whether the current implementation has a credible path toward stronger formalism and reproducibility.

## Method vs. book

- **This repo:** runnable prototype, tests, licenses, and operational SSoT (instruments, fail-closed, agent contracts).
- **Book (separate):** public exposition of the broader idea. Not maintained inside this repository.

## Status

**Current stage:** early public prototype maximized for inspectable operation under a source-available license.

Evaluate it as a formalized hypothesis under construction: small in code, limited in claims, deliberate in structure.

## Author

Manuel Enrique Prada Forero
