# Reporte Técnico BIO-GAME-01: Teoría de Juegos con Jugadores de Autoescala (IPD-ms) Acoplada a la Bioelectricidad y pH Estromal (MET-01)

> **Cita Académica Principal y Reconocimiento Formal:**  
> Este desarrollo computacional es una extensión directa del marco teórico y experimental publicado por:  
> **Lakshwin Shreesha, Federico Pigozzi, Adam Goldstein y Michael Levin**  
> *"Extending Iterated, Spatialized Prisoner's Dilemma to Understand Multicellularity: Game Theory With Self-Scaling Players"*  
> **IEEE Transactions on Molecular, Biological, and Multi-Scale Communications**, Vol. 11, N.º 2, pp. 101–115, junio de 2025.  
> *Allen Discovery Center at Tufts University / Wyss Institute for Biologically Inspired Engineering at Harvard University.*

---

## I. Resumen Ejecutivo y Marco Teórico Unificado

El dilema clásico de la cooperación biológica asume una población de agentes con fronteras físicas inmutables ($N$ células fijas). En el trabajo pionero de **Shreesha et al. (2025)**, este paradigma se supera al permitir que los agentes ejecuten dos acciones adicionales además de Cooperar ($C$) o Defeccionar ($D$):
1. **Fusión (*Merge*, $M$):** Dos agentes adyacentes unifican sus cuerpos celulares en un único individuo compuesto, compartiendo espacio físico, recompensas y heredando la política cognitiva del agente de mayor desempeño.
2. **División (*Split*, $S$):** Un agente multicelular compuesto se desintegra en sus subunidades unicelulares elementales.

### La Innovación Biofísica de Guanes Health (Capa B)
En el modelo puramente formal de teoría de juegos, la acción *Merge* ocurre por aprendizaje por refuerzo ($Q$-learning). En la **biología somática real**, dos células no pueden fusionarse funcionalmente si no existe un **puente bioeléctrico conductor**: las **Uniones Gap (*Gap Junctions*, Cx43)**.

En el módulo **`BIO-GAME-01`** (`bio_game_ipd_ms_simulator.py`), conectamos formalmente la cinemática de juegos con la biofísica del transportador de protones **MET-01**:
$$\mathcal{P}(\text{Merge}) \le G_{GJ}(\Delta V_{mem}, pH_i)$$
$$G_{GJ}(\Delta V_{mem}) = 0.05 + \frac{0.95}{1 + \exp\left(0.15 \cdot (|V_{mem} - (-70.0)| - 25.0)\right)} \cdot \left[ \frac{1}{1 + 10^{2.0 \cdot (6.50 - pH_i)}} \right]$$

---

## II. Resultados Cuantitativos del Experimento Comparativo (100 Rondas, Cuadrícula $20 \times 20 = 400$ Nodos)

Ejecutamos dos escenarios en condiciones estromales tumorales idénticas de acidosis profunda ($pH_e = 6.20$):

| Métrica del Sistema (Ronda 100) | Escenario A: Trampa Ácida (CD8 Nativo / S703A) | Escenario B: Sinergia Bioeléctrica (NHE1-Shield 1K3R4E) | Delta / Factor de Cambio |
| :--- | :---: | :---: | :---: |
| **Agentes Autónomos Activos ($N$)** | **387** (Fraccionamiento atávico) | **51** (Fusión sincitial masiva) | **-86.8% agentes** (Autoescala) |
| **Escala Máxima del Macro-Agente** | **5 células** (Incapacidad de escala) | **39 células** (Sincitio extendido) | **+7.8x mayor escala física** |
| **Recompensa Media por Ronda** | **23.24** | **29.79** | **+28.2% ventaja adaptativa** |
| **Potencial de Membrana ($V_{mem}$)** | **-30.00 mV** (Despolarizado) | **-60.14 mV** (Hiperpolarizado) | **-30.14 mV más polarizado** |
| **$pH_i$ Citosólico de Equilibrio** | **5.495** (Acidosis citosólica) | **6.697** (Protegido por NHE1) | **+1.20 unidades de pH** |
| **Índice del Cono de Luz Cognitivo ($CLC$)** | **0.001** (Anergia / Aislamiento) | **0.649** (Yo Multicelular Integrado) | **+649x mayor integración** |

---

## III. Análisis de los 4 Paneles del Dashboard (`met01_ipd_ms_dashboard.png`)

### Panel A: Morfología Espacial (Cuadrícula $20 \times 20$ en la Ronda 100)
- **Mitad Izquierda (Trampa Ácida sin Escudo):** El colapso del $pH_i$ a 5.495 cierra las conexinas por acidez ($\mathcal{P}_{\text{Merge}} \approx 0$). Los agentes permanecen como partículas unicelulares fragmentadas (387 agentes independientes), compitiendo a escala atávica.
- **Mitad Derecha (NHE1-Shield 1K3R4E):** Al sostener $pH_i = 6.697$ y $V_{mem} = -60.14\text{ mV}$, las uniones gap permanecen abiertas. Los agentes ejecutan $Merge$ en cascada, autoorganizándose en grandes dominios multicelulares unificados (hasta 39 células continuas por macro-agente).

### Panel B: Cinética Poblacional de Autoescala (Equilibrio Puntuado)
- Replica con exactitud el patrón descubierto por **Shreesha, Pigozzi, Goldstein y Levin (2025)**: la curva de población desciende no de forma lineal, sino a través de **mesetas y caídas abruptas (equilibrio puntuado)** a medida que coalescen sub-agentes en unidades mayores.

### Panel C: Escala Física del Compuesto
- En la trampa de acidosis estromal, la fragmentación involuntaria inducida por acidez disuelve cualquier intento de cooperación física (tope de 5 células).
- Con el blindaje iónico, la escala del individuo compuesto crece progresivamente hasta abarcar el 10% del tejido en un solo macro-organismo coordinado.

### Panel D: Ventaja Adaptativa (*Fitness*) y Paradoja Intergrupal
- Los macro-agentes multicelulares obtienen una aptitud promedio significativamente superior ($29.79$ vs $23.24$) debido a la compartición de recompensas internas sin fricción.
- **La Paradoja Intergrupal:** Al igual que en el paper de Levin et al., la formación de un gran colectivo multicelular genera una barrera periférica donde la interacción con agentes no fusionados se estabiliza en defección mutua o cooperación limitada, reflejando fielmente la frontera inmunológica de un tumor sólido frente al estroma circundante.

---

## IV. Atribución Académica y Declaración Ética

Este software se proporciona bajo la licencia de investigación de código abierto de Guanes Health y debe ser citado formalmente en cualquier derivado científico o computacional:

```bibtex
@article{shreesha2025extending,
  author    = {Shreesha, Lakshwin and Pigozzi, Federico and Goldstein, Adam and Levin, Michael},
  title     = {Extending Iterated, Spatialized Prisoner's Dilemma to Understand Multicellularity: Game Theory With Self-Scaling Players},
  journal   = {IEEE Transactions on Molecular, Biological, and Multi-Scale Communications},
  volume    = {11},
  number    = {2},
  pages     = {101--115},
  year      = {2025},
  publisher = {IEEE},
  doi       = {10.1109/TMBMC.2025.XXXXXXX}
}

@software{prada_forero_2026_biogame01,
  author    = {Prada Forero, Manuel Enrique},
  title     = {Guanes Health BIO-GAME-01: Biophysical & Bioelectric Coupling of Self-Scaling Game Theory for Cancer Research},
  year      = {2026},
  version   = {6.2.0},
  publisher = {Zenodo / GitHub},
  doi       = {10.5281/zenodo.22101265},
  url       = {https://health.guanes.biz}
}
```
