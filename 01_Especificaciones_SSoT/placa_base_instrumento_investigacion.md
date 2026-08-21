# PLACA BASE COMO INSTRUMENTO DE INVESTIGACIÓN
**DOCUMENTO DE ALINEACIÓN EPISTEMOLÓGICA (SSoT)**  
**Ámbito:** Guanes Health · motor oncológico in silico · metodología de placas  
**Estado:** normativo para lenguaje interno y para agentes colaboradores  
**Complementa:** `vector_viral_oncolitico_modelo-v2.md`

---

## 1. Tesis operativa (la correcta)

La **Placa Base** en Guanes Health es una **herramienta de investigación**: un artefacto de ingeniería de sistemas para ordenar hipótesis, estados, vetos, fallos y restauraciones de forma inspectable y testeable.

No es una afirmación de que la célula humana *sea* una placa de silicio, ni de que la biología esté gobernada por compuertas digitales binarias.

| Afirmación permitida | Afirmación prohibida |
|----------------------|----------------------|
| “Usamos una placa para modelar restricciones y estados celulares.” | “La célula es una placa base.” |
| “El cáncer se representa *en el modelo* como fallos de control.” | “El cáncer es malware literal.” |
| “La metáfora ayuda a diseñar experimentos in silico.” | “La metáfora valida terapias o sustituye wet-lab.” |
| “Fail-closed en el código protege coherencia del simulador.” | “Fail-closed demuestra fisiología real.” |

---

## 2. Por qué existe la confusión (y cómo evitarla)

El método de placas nació en **ingeniería documental** (estructura, aserciones, fail-closed, manejo de ambigüedad). Luego se **trasladó** a biología como lente de investigación.

Si un agente o colaborador **recibe** un archivo llamado `placa_base_sana` / `placa_base_cancer` o un entregable titulado “placa base de la célula”, es previsible —pero **incorrecto**— que asuma ontología (“la célula = placa”) en lugar de instrumento (“la placa modela aspectos de la célula”).

**Regla para agentes:** el nombre del artefacto describe el *instrumento*, no la identidad del sistema vivo. Ante duda, este documento prevalece sobre retórica generada en chat.

---

## 3. Capas de verdad (mismas reglas que el vector v2)

| Capa | Contenido en el dominio de placas | Ejemplo |
|------|-----------------------------------|---------|
| **A. Biología de fondo** | Hechos/mecanismos de literatura | pHe ácido tumoral; eje BCL-2; GLUT1 |
| **B. Modelo de placa** | Variables, vetos, umbrales del simulador | `ATP_WARBURG = 10000` (unidades relativas del modelo) |
| **C. Abierto** | No decidido aún | Backbone viral; calibración empírica de constantes |
| **D. Prohibido afirmar** | Validación clínica / “la célula es digital” | Eficacia terapéutica humana; ontología silicio↔célula |

Las constantes de `placa_sana.py` / `placa_cancer.py` son **Capa B** salvo que exista trazabilidad explícita a literatura (Capa A) en una tabla fuente. Inventario del núcleo: [`ledger_parametros_nucleo.md`](./ledger_parametros_nucleo.md). Madurez de artefactos: [`madurez_artefactos_motor.md`](./madurez_artefactos_motor.md). Mapa operativo: [`ssot_framework_map-v3.md`](./ssot_framework_map-v3.md).

---

## 4. Qué hace fabulosa a la placa (sin ego)

Como instrumento, la placa aporta:

1. **Modularidad** — homeostasis, sabotaje tumoral, restauración y vector como módulos criticables por separado.  
2. **Inspectabilidad** — supuestos en código y SSoT, no solo en prosa.  
3. **Fail-closed** — estados inválidos abortan; no se “inventa” coherencia silenciosa.  
4. **Puente interdisciplinario** — ingenieros y biólogos comparten un mapa de control sin pretender identidad física.  
5. **Cribado de hipótesis** — reduce espacio de búsqueda *computacional*; no certifica candidatos clínicos.

Eso basta para justificar el método. No hace falta convertir la metáfora en metafísica.

---

## 5. Contrato de lenguaje (obligatorio en docs y código)

- Preferir: *modelo de placa*, *artefacto de placa*, *instrumento de restricción lógica*, *estado modelado*.  
- Evitar como ontología: *“la célula es una placa”*, *“compuertas de silicio en vivo”*, *“malware celular”* salvo como **metáfora pedagógica explícitamente marcada**.  
- Si se usa metáfora, una frase de anclaje debe seguirla: *“esto es analogía de ingeniería; la biología real es estocástica.”*  
- Nombres de archivo `placa_*.py` se conservan por continuidad histórica; su docstring debe declarar **instrumento / modelo**, no identidad biológica.

---

## 6. Relación con el resto del SSoT

- **Hallmarks y biofísica** → `vector_viral_oncolitico_modelo-v2.md` §2 (Capa A parametrizada + Capa B del sim).  
- **Vector** → misma especificación §3 (hipótesis; backbone/safety UNRESOLVED).  
- **Wet-lab** → §4 (la placa no sustituye validación experimental).  
- **Implementación** → `03_Motor_Oncologico/placa_sana.py`, `placa_cancer.py`, `parche_restauracion.py`.

---

## 7. Resumen en una línea

**La placa base es una herramienta de investigación fabulosa precisamente porque no pretende ser la célula.**

---
*Documento de alineación epistemológica. Prevalece sobre interpretaciones ontológicas de la metáfora en chats o borradores de agentes.*
