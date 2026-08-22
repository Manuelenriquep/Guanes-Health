# Contraste de instrumento: match estático vs placa (Gated-6.50)

**Ámbito:** demo de atracción / cribado de hipótesis in silico.  
**Estado:** operativo (Capa B).  
**Complementa:** [`placa_base_instrumento_investigacion.md`](./placa_base_instrumento_investigacion.md), [`ssot_framework_map-v3.md`](./ssot_framework_map-v3.md).

---

## Tesis (permitida)

Un matcher genómico-administrativo (proxy) puede declarar a un paciente “IO-elegible” con firma fija mientras el **instrumento de placa** anula la eficacia CD8 modelada si `pHe ≤ 6.50` (política canónica Gated-6.50).

Eso demuestra **divergencia de instrumentos**, no superioridad clínica ni auditoría de MatchMiner / Onco-Logic / TRONCO / Awesome Cancer AI.

| Capa | Uso aquí |
|------|----------|
| A | Acidosis estromal como mecanismo de literatura (ancla cualitativa) |
| B | `clasificador_estatico` vs `calcular_eficiencia_cd8` |
| C | Calibración empírica del umbral / cinética — `UNRESOLVED` |
| D | “Predice fracaso clínico de inmunoterapia” — **prohibido** |

---

## Artefactos

| Rol | Archivo |
|-----|---------|
| Demo CLI + figura | `03_Motor_Oncologico/demo_divergencia_estatico_vs_placa.py` |
| Test de anclaje | `04_Bateria_Inviolable/test_divergencia_estatico_vs_placa.py` |
| Política CD8 | `03_Motor_Oncologico/inmuno_utils.py` |
| Figura | `02_Simulaciones_Visuales/divergencia_estatico_vs_placa_gated_650.png` |

Comando:

```bash
py "03_Motor_Oncologico/demo_divergencia_estatico_vs_placa.py"
```

---

## Fail-closed del contraste

- `pHe ≤ 6.50` → eficacia placa = 0; estático (con firma) = 1 → **diverge**.
- `pHe = 7.35` → ambos = 1 → **no diverge**.
- Sin firma IO → ambos = 0.

La placa es herramienta de investigación; no es la célula.
