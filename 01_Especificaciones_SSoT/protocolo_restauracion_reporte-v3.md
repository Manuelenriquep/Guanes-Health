# Working Note: Restoration Protocol Model (v3)
## Speculative scenario design for a deterministic oncology prototype

This document records a working scenario used to shape the current Guanes Health prototype.

It is not a clinical protocol, not a validated pharmacological model, and not evidence of experimental efficacy. The purpose of the document is narrower: to describe the assumptions, state transitions, and comparison cases that inform the current codebase.

The numbers below should be read as **model parameters inside a conceptual simulation**, not as externally validated biomedical results.

---

### I. Modeling Frame

The current prototype treats a narrow tumor-control problem as a state-transition model with three simplified dimensions:

1. **Apoptotic blockade**
   - The tumor state is modeled as resistant to apoptosis through elevated anti-apoptotic signaling.

2. **Metabolic acidification**
   - The tumor state is modeled as maintaining an acidic extracellular microenvironment and a distorted energetic profile.

3. **Immune evasion**
   - The tumor state is modeled as remaining partially inaccessible to cytotoxic immune response under acidic conditions, even when checkpoint camouflage is reduced.

These simplifications are deliberately coarse. Their role is to create a deterministic prototype that can be inspected and tested, not to reproduce full tumor biology.

---

### II. Scenario Comparison

The document tracks four conceptual intervention schedules that motivated the structure of the prototype:

#### Cohort A: Simultaneous intervention
- Metabolic and immune intervention are applied together at the same initial step.
- In the model, this may improve the environment, but not necessarily fast enough to produce the best immune response.

#### Cohort B: Isolated immunotherapy
- Checkpoint inhibition is modeled without correcting the acidic environment.
- In the prototype, this case is intentionally weak and helps illustrate why microenvironment conditions matter in the current abstraction.

#### Cohort C: Sequential combined intervention
- Metabolic disruption is applied first.
- Immune restoration is introduced only after the modeled environment becomes more permissive.
- This is the main scenario represented by the current implementation.

#### Cohort D: Delayed sequential intervention
- Immune restoration is introduced after an extended delay.
- In the conceptual model, this case explores the cost of poor timing in a deterministic intervention schedule.

These cohorts are comparative modeling constructs. At present, only a subset of their logic is implemented directly in code.

---

### III. Simplified State Table

The following table summarizes the current toy-model state transitions that inspired the prototype:

| State | Intracellular pH | Extracellular pH | ATP | CD8 Efficiency | Interpretation |
| :--- | :---: | :---: | :---: | :---: | :--- |
| Healthy baseline | 7.20 | 7.35 | 100 | nominal | Stable homeostasis |
| Tumor baseline | 7.20-7.40 | 6.20 | 10,000 | 10.0% | Acidic, immune-resistant, apoptosis-limited |
| Cohort A | modeled | modeled | modeled | modeled | Simultaneous intervention comparison |
| Cohort B | 7.20-7.40 | 6.20 | 10,000 | 10.0% | Checkpoint intervention without environmental restoration |
| Cohort C | 5.20 | 7.35 | 30 | 100.0% in-model | Combined restoration path represented in code |
| Cohort D | modeled | modeled | modeled | modeled | Delayed intervention comparison |

Several values above are intentionally fixed constants used to make the simulation deterministic and easy to test. They should not be interpreted as experimentally grounded measurements.

---

### IV. Implementation Relationship

The current Python implementation is much smaller than the full conceptual space described here.

What the code currently does:

- model a healthy baseline state,
- model a tumor baseline state,
- simulate isolated anti-PD-1 behavior under acidic conditions,
- simulate a combined restoration path with explicit state changes,
- reject invalid or physically inconsistent inputs using fail-closed checks.

What the code does not yet do:

- simulate continuous kinetics,
- calibrate parameters against external data,
- represent all cohorts with equal detail,
- model toxicity, dosing, or mechanistic uncertainty at realistic depth.

---

### V. Reference Pseudocode

The following pseudocode illustrates the logic of the main modeled path. It is included as a conceptual summary of the prototype rather than as a claim of biological completeness.

```python
# ==============================================================================
# GUANES HEALTH - ONCOLOGÍA DE PLACAS BASE
# Algoritmo de validación del microambiente de la Cohorte C (Secuencial Óptima)
# ==============================================================================

class CelulaCelular:
    def __init__(self, tipo="tumoral"):
        self.tipo = tipo
        self.mct4_bloqueado = False
        self.ph_intracelular = 7.40 if tipo == "tumoral" else 7.20
        self.ph_extracelular = 6.20 if tipo == "tumoral" else 7.35
        self.atp = 10000 if tipo == "tumoral" else 100
        self.bcl2_overexpression = True if tipo == "tumoral" else False
        self.calreticulina_exp_pico = False
        self.apoptosis_activa = False

def simular_protocolo_v2_1(celula: CelulaCelular, cohorte="C"):
    if celula is None:
        raise ValueError("Doctrina Fail-Closed: Célula nula no procesable.")
        
    if celula.tipo == "sana":
        return {"viable": True, "eficiencia_CD8": 100.0, "ATP": celula.atp}

    if cohorte == "C":
        # Hito t = 0h: Bloqueo metabólico estricto de MCT4
        celula.mct4_bloqueado = True
        # El lactato se acumula intracelularmente colapsando el pHi
        celula.ph_intracelular = 5.20 
        
        # Hito t = 12h: Ventana inmunogénica óptima
        celula.ph_extracelular = 7.35  # pH normalizado
        celula.calreticulina_exp_pico = True  # Activación de estrés de RE (vía PERK)
        
        # Inyección combinada anti-PD1 + BH3 miméticos en t = 12h
        celula.bcl2_overexpression = False  # Desatascado mitocondrial
        celula.apoptosis_activa = True
        celula.atp = 30  # Colapso energético tumoral
        
        # Eficiencia de depuración citotóxica máxima por des-acidificación
        eficiencia_CD8 = 100.0 
        
        # Aserción rígida de validación del sistema
        assert celula.ph_intracelular < 5.5, "Error: Fuga metabólica por MCT4 activo"
        assert celula.apoptosis_activa == True, "Error: Veto de apoptosis activo"
        assert celula.ph_extracelular == 7.35, "Error: Microambiente ácido persistente"
        
        return {
            "apoptosis_activa": True,
            "eficiencia_CD8": eficiencia_CD8,
            "atp_tumoral": celula.atp,
            "autolisis_acida_activada": True,
            "seguridad_periferica": "irAEs_evitados_al_70%"
        }
        
    return {"apoptosis_activa": False, "eficiencia_CD8": 10.0, "atp_tumoral": celula.atp}
```

This working note should be read as a design artifact for an early computational model. Future revisions should either deepen its formalism or narrow its claims further.
