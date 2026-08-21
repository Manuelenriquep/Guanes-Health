# Protocolo operativo de tres agentes

**Ámbito:** trabajo sobre este repositorio (código + SSoT).  
**No es el libro:** aquí solo el contrato mínimo para que los agentes no rompan la epistemología.

Complementa: `placa_base_instrumento_investigacion.md`.

---

## Pipeline

```
Agente Célula  →  placa sana (instrumento)
Agente Cáncer  →  placa tumoral (instrumento)
        ↓
Agente Oncólogo  →  razona intervención / riesgos / huecos
        ↓
Código + tests  →  único lugar donde una afirmación del modelo se “cierra”
```

---

## Roles

### 1. Agente Célula
- **Entrada:** literatura / hechos de homeostasis (Capa A) + constantes ya en `placa_sana.py`.
- **Salida:** propuesta de estado, umbrales o vetos para la **placa sana**.
- **Prohibido:** afirmar que la célula *es* una placa; inventar terapias.

### 2. Agente Cáncer
- **Entrada:** hallmarks / sabotaje (Capa A) + constantes en `placa_cancer.py` / SSoT v2 §2.
- **Salida:** propuesta de fallos de control para la **placa tumoral**.
- **Prohibido:** ontología silicio↔biología; eficacia clínica.

### 3. Agente Oncólogo
- **Entrada obligatoria:** las dos placas (o sus exports) + este protocolo + `placa_base_instrumento_investigacion.md`.
- **Salida:** hipótesis de intervención, secuencias, riesgos, ítems `UNRESOLVED`.
- **Prohibido (regla de puerta):**
  - Leer las placas como “la realidad es digital”.
  - Afirmar cura, 100% selectividad, o validación wet-lab inexistente.
  - Rellenar `backbone_id` / `safety_switch_id` u otros huecos por ego.

---

## Capas (recordatorio)

| Capa | Uso |
|------|-----|
| A | Biología de fondo (citable) |
| B | Estado del modelo / placa |
| C | Abierto / UNRESOLVED |
| D | Prohibido afirmar (clínica, ontología digital) |

---

## Fail-closed

Si faltan hechos, anexos o decisión de ingeniería: **no completar con ficción**. Marcar `UNRESOLVED` o abortar la afirmación.

---

## Implementación en este repo

| Artefacto | Archivo |
|-----------|---------|
| Placa sana | `03_Motor_Oncologico/placa_sana.py` |
| Placa tumoral | `03_Motor_Oncologico/placa_cancer.py` |
| Capa “oncólogo” mínima (restauración modelada) | `03_Motor_Oncologico/parche_restauracion.py` |
| Pruebas | `04_Bateria_Inviolable/` |

Los nombres `placa_*` son históricos; significan **instrumento de modelado**.

Madurez (canónico vs experimental vs histórico): [`madurez_artefactos_motor.md`](./madurez_artefactos_motor.md).  
Trazabilidad A→B del núcleo: [`ledger_parametros_nucleo.md`](./ledger_parametros_nucleo.md).
