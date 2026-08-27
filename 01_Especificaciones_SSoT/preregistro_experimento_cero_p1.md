# PRE-REGISTRO EXPERIMENTAL: PROTOCOLO DE FALSACIÓN P1 (EXPERIMENTO CERO)
## Demarcación Bioenergética de Linfocitos T en Acidosis Tumoral
**Especificación Técnica SSoT - Guanes Health v6.0**  
*Autor: Manuel Enrique Prada Forero (`gerente@guanes.biz`)*  
*Estatus:* **Diseño Congelado Pre-Datos (No-Refit Policy)**  
*Fecha de Congelación:* 26 de Agosto, 2026  
*Nota de Demarcación:* Este documento establece el contrato metodológico y estadístico previo a la recolección de datos empíricos. La existencia de este pre-registro no implica que el ensayo haya sido ejecutado.

---

### 1. Marco de Falsación y Regla de Decisión del Modelo

El objetivo de este protocolo es evaluar si el colapso bioenergético predicho por el módulo de inhibición alostérica de PFK-1 en acidosis estromal ($\text{pH}_e = 6.20$) se sostiene empíricamente en linfocitos T humanos primarios CD8+.

* **$H_0$ (Falsación del Mecanismo / Kill Switch):**  
  $$\frac{[\text{ATP}]_{\text{pH } 6.20, 180\,\text{min}}}{[\text{ATP}]_{\text{pH } 7.40, 180\,\text{min}}} > 0.25$$  
  *Interpretación:* Si tras 180 minutos de exposición a $\text{pH}_e = 6.20$, los linfocitos T viables retienen más del $25\%$ del ATP intracelular del control neutro, **la hipótesis de parálisis glucolítica severa inducida por acidosis queda formalmente falsada**. Se descarta la topología PFK-1/acidosis de Guanes Health v6.0 y se suspende el avance a ensayos P2/P3/P4.

* **$H_1$ (Consistencia Cualitativa con el Modelo):**  
  $$\frac{[\text{ATP}]_{\text{pH } 6.20, 180\,\text{min}}}{[\text{ATP}]_{\text{pH } 7.40, 180\,\text{min}}} < 0.50 \quad \text{con } p < 0.05 \text{ (Mixed Model)}$$  
  *Interpretación:* Existe una caída bioenergética estadísticamente significativa y biológicamente relevante atribuible a la acidosis extracelular.

* **Predicción Numérica Puntual (In Silico v6.0):**  
  $$[\text{ATP}]_{\text{pH } 6.20, 180\,\text{min}} < 0.05 \cdot [\text{ATP}]_{\text{pH } 7.40, 180\,\text{min}}$$  
  *Nota:* El valor $< 5.0\%$ es la deducción puntual de las constantes de referencia de v6.0. Obtener valores entre $5\%$ y $25\%$ confirma el mecanismo pero exige recalibración de $\beta_i$ y $n_{\text{PFK}}$ en dataset de entrenamiento.

---

### 2. Endpoints y Jerarquía de Medición

Para evitar fallos por conjunción de variables (*AND gates*), los criterios se estratifican en:

#### 2.1 Endpoint Primario (Decisivo para $H_0 / H_1$)
* **$[\text{ATP}]$ Intracelular Relativo a $t = 180\,\text{min}$:**  
  Medido mediante luminiscencia (CellTiter-Glo) y rigurosamente **normalizado por contaje de células viables** (o contenido proteico total mediante BCA/Bradford) en las mismas alícuotas:
  $$\text{ATP}_{\text{norm}} = \frac{\text{RLU}}{\text{Células Viables}}$$

#### 2.2 Endpoints Secundarios (Caracterización Cinética y Mecanística)
1. **$\text{pH}_i$ Citosólico Dinámico:** Cinética de acidificación intracelular medida por ratiometría fluorescente BCECF-AM a $t \in \{0, 30, 60, 120, 180\}\,\text{min}$.
2. **Perfil Cinético Temporal de ATP:** Curva completa de decaimiento temporal en los 5 pasos de muestreo.
3. **Viabilidad Celular Concurrente:** Exclusión de fluoróforos (Calceína-AM / Ioduro de Propidio o Ensayo de Caspasa-3/7) para desacoplar el colapso metabólico de la citólisis/necrosis inespecífica aguda.

---

### 3. Parámetros In Silico Congelados (SSoT v6.0)

Las siguientes constantes quedan bloqueadas sin reajuste (*No-Refit*):

| Constante | Símbolo | Valor Congelado | Unidad | Proveniencia |
| :--- | :---: | :---: | :---: | :--- |
| $\text{pKa}$ Alostérico de PFK-1 | $\text{pKa}_{\text{PFK}}$ | 6.80 | pH units | Literature (Ui 1966, Kemp 1983) |
| Coeficiente de Hill de PFK-1 | $n_{\text{PFK}}$ | 4.0 | adimensional | Asumido (Homotetrámero) |
| Capacidad Buffer Citosólica | $\beta_i$ | 30.0 | $\text{mM / pH unit}$ | Literature (Swietach 2014) |
| Tasa de Producción Glucolítica | $k_{\text{glyco}}$ | 0.05 | $\text{min}^{-1}$ | In-silico baseline |
| Tasa de Gasto Basal de ATP | $k_{\text{basal\_drain}}$ | 0.05 | $\text{min}^{-1}$ | In-silico baseline |

---

### 4. Diseño Experimental y Controles de Calidad

#### 4.1 Muestra Biológica y Réplicas
* **Población:** Linfocitos T humanos primarios CD8+ aislados de PBMC de donantes sanos.
* **Tamaño Muestral:** $N \ge 3$ donantes biológicos independientes.
* **Réplicas Técnicas:** $n = 3$ pozos independientes por punto temporal, donante y condición ($3 \times 3 = 9$ mediciones técnicas por condición temporal).

#### 4.2 Condiciones de Cultivo
* Buffer RPMI-1640 modificado sin bicarbonato, suplementado con HEPES ($10\,\text{mM}$) y MES ($10\,\text{mM}$) a $37^\circ\text{C}$:
  * Condición Control: $\text{pH}_e = 7.40 \pm 0.02$.
  * Condición Acidosis: $\text{pH}_e = 6.20 \pm 0.02$.
* **Puntos Temporales:** $t \in \{0, 30, 60, 120, 180\}\,\text{minutos}$.

#### 4.3 Controles Obligatorios Anti-Sesgo
1. **Control de Deriva de pH:** Medición potenciométrica del $\text{pH}_e$ del sobrenadante al inicio ($t=0$) y al final ($t=180\,\text{min}$) de cada corrida. Deriva admisible máxima: $\Delta \text{pH}_e \le 0.05$ unidades.
2. **Control Positivo Metabólico:** Inclusión de pocillos control con Oligomicina ($1\,\mu\text{M}$) o 2-Desoxiglucosa (2-DG, $50\,\text{mM}$) a pH 7.40 para confirmar que el ensayo de luciferasa responde a la depleción energética en el rango dinámico esperado.
3. **Desacoplamiento de P2:** Este protocolo excluye expresamente inhibidores de NHE1 (Cariporide/EIPA) y modificaciones transgénicas para evitar solapamiento de hipótesis.

---

### 5. Análisis Estadístico Pre-Especificado

* **Transformación:** Las concentraciones relativas de ATP se analizarán en escala logarítmica ($\log_{10}(\text{ATP}_{\text{norm}})$) para estabilizar la varianza.
* **Modelo Estadístico:** Modelo lineal de efectos mixtos (*Linear Mixed-Effects Model*):
  $$\log(\text{ATP}_{ijk}) = \mu + \text{pH}_i + \text{Tiempo}_j + (\text{pH} \times \text{Tiempo})_{ij} + u_k + \epsilon_{ijk}$$
  Donde $u_k \sim \mathcal{N}(0, \sigma_u^2)$ representa el efecto aleatorio del donante biológico $k$, y $\text{pH}_i$, $\text{Tiempo}_j$ son factores fijos.
* **Nivel de Significancia:** $\alpha = 0.05$ (dos colas).

---

### 6. Matriz de Decisión y Destino del Modelo

```
                              [ RESULTADO EXPERIMENTAL P1 ]
                                            │
               ┌────────────────────────────┼────────────────────────────┐
               ▼                            ▼                            ▼
      ATP_180 < 5%                5% <= ATP_180 <= 25%             ATP_180 > 25%
   (Predicción v6.0)              (Caída Significativa)           (Hipótesis Nula H0)
               │                            │                            │
               ▼                            ▼                            ▼
      ✅ ÉXITO TOTAL              ⚠️ RECALIBRACIÓN              ❌ FALSADO
  Mecanismo y constantes       Mecanismo válido; ajustar     Topología PFK-1 refutada.
   validados en Capa 1.       beta_i / n_PFK en train-set.   Suspender avance a P2-P4.
  Habilitado paso a P2.          Congelar test-set v6.1.     Rediseñar motor biofísico.
```
