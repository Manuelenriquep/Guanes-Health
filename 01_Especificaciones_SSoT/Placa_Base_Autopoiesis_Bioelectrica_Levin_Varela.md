# Placa Base de Autopoiesis Bioeléctrica & Redes Relacionales (v7.0)
**Acoplamiento de la Biología Bioeléctrica (Levin) y la Teoría de la Autopoiesis (Maturana & Varela)**  
**División de Biofísica de Sistemas, Morfogénesis Computacional y Modelado In Silico — Guanes Health**

---

### Demarcación Epistemológica y Principio de Rigor Científico

Este documento formaliza la integración matemática y computacional entre la **Biología Bioeléctrica** (Michael Levin) y la **Teoría de la Autopoiesis** (Humberto Maturana y Francisco Varela) dentro del marco de la termodinámica de sistemas fuera del equilibrio y la inferencia activa (Karl Friston).

> **Aviso de Rigor Epistemológico (Capa B — In Silico Toy Model):**  
> Este marco de trabajo no es una herramienta de diagnóstico clínico directo, ni un dispositivo médico regulado, ni una ontologización de metáforas biológicas. Constituye una especificación técnica de ingeniería de sistemas biológicos que describe un prototipo determinista libre de heurísticas arbitrarias (`IMPUTATION_POLICY = NONE` / Fail-Closed). Cualquier propuesta derivada debe someterse al protocolo de falsación en laboratorio húmedo (*wet-lab*).

---

## 1. Fundamentos: Los Cinco Pilares de la Intersección

```
+---------------------------------------------------------------------------------------------------------+
|                                PLACA BASE DE AUTOPOIESIS BIOELÉCTRICA                                   |
+---------------------------------------------------------------------------------------------------------+
|                                                                                                         |
|  [PILAR 1: MEMBRANA, BOMBEOS IÓNICOS Y DOBLE ESCALA TEMPORAL]                                           |
|     - Borde Automantenido: Cierre operacional que evita la lisis por equilibrio de Gibbs-Donnan.        |
|     - Escala Rápida (Interactiva, tau ~ 10^-3 a 10^0 s): Bombeo iónico activo (Na+/K+-ATPasa, NHE1).   |
|     - Escala Lenta (Constitutiva, tau ~ 10^3 a 10^5 s): Síntesis, transporte y reciclaje de canales.    |
|                                                                                                         |
|  [PILAR 2: CAUSALIDAD TERMODINÁMICA - CICLO TRABAJO-CONSTRICCIÓN (T-C)]                                  |
|     - Circularidad Causal: "El trabajo genera constricciones que canalizan nuevo trabajo útil".         |
|     - Potencial Transmembrana (Vmem): Constricción dinámica que guía el transporte secundario.          |
|                                                                                                         |
|  [PILAR 3: INFORMACIÓN SEMÁNTICA Y UMBRALES DE VIABILIDAD]                                              |
|     - Información Semántica (SI): Fracción informacional entorno-agente acoplada a la viabilidad V >= 0|
|     - Umbrales Fail-Closed: ATP < 20% activa veto irreversible a lisis (Estado S3).                     |
|                                                                                                         |
|  [PILAR 4: REDES RELACIONALES, BIO-LOCI, ENTROPÍA DE FLUJO (H_flux) E IRREDUCIBILIDAD (I)]              |
|     - Bio-locus: Comunidad de células unidas por uniones gap Cx43 que operan como macro-agente.        |
|     - Entropía de Flujo: H_flux = - sum_i p_i ln(p_i) sobre la corriente electrometabólica.             |
|     - Irreducibilidad: I = 1/2 sum_i |p_i - 1/N| -> Distancia al desacoplamiento entrópico.             |
|                                                                                                         |
|  [PILAR 5: AUTOPOIESIS MULTICELULAR Y CONO DE LUZ COGNITIVO (LEVIN)]                                    |
|     - Resolución a la objeción de Varela: El colectivo celular forma un individuo de 2° orden cuando     |
|       la integración relacional interna excede la fuga con el entorno (Phi^r > 0.25).                  |
|                                                                                                         |
+---------------------------------------------------------------------------------------------------------+
```

---

## 2. Fisiología de la Membrana y el Ciclo Trabajo-Constricción (T-C)

### 2.1 Cierre Operacional y Borde Automantenido
Un sistema vivo no es meramente un conjunto de reacciones químicas dentro de una vesícula estática. Es una **red de procesos de producción que regenera continuamente la propia barrera física que lo delimita**.

En las células animales, la concentración de macromoléculas no difusibles cargadas negativamente en el citoplasma genera una presión osmótica destructiva (**Efecto Gibbs-Donnan**). Sin trabajo termodinámico continuo, entrarían agua e iones hasta reventar la membrana.
El bombeo activo ($\text{Na}^+/\text{K}^+$-ATPasa, extrusión de protones por NHE1) no es un mero "intercambio de nutrientes": es el **proceso de trabajo interactivo necesario para mantener el borde mismo en el espacio**.

### 2.2 Doble Escala Temporal
El automantenimiento requiere desacoplar dos escalas dinámicas:
1. **Escala Interactiva ($\tau_{\text{fast}} \approx 10^{-3} - 10^0\text{ s}$):**
   Gasto continuo de Gibbs $(\Delta G_{\text{ATP}} \approx 50\text{ kJ/mol})$ en gradientes electroquímicos de membrana:
   $$\dot{W}_{\text{int}} = \Delta G_{\text{ATP}} \cdot J_{\text{pump}}(V_{\text{mem}}, \text{pH}_i, [\text{ATP}])$$
2. **Escala Constitutiva ($\tau_{\text{slow}} \approx 10^3 - 10^5\text{ s}$):**
   Síntesis, plegamiento e inserción de las compuertas de membrana $C(t)$ (conexinas Cx43, bombas iónicas, transportadores):
   $$\frac{dC}{dt} = \eta_{\text{synth}} \cdot W_{\text{const}}([\text{ATP}]) - \gamma_{\text{turnover}} \cdot C(t)$$

### 2.3 Clausura de Constricciones
La energía libre liberada por el catabolismo no se disipa al azar: es canalizada por las **constricciones materiales** (canales iónicos, bombas). A su vez, los gradientes iónicos creados son los que proporcionan la fuerza electromotriz para generar nuevas constricciones:
$$\text{Trabajo } W \xrightarrow{\text{construye}} \text{Constricciones } C \xrightarrow{\text{canalizan}} \text{Trabajo Útil } W$$

---

## 3. Información Semántica y Umbral de Viabilidad

A diferencia de la información de Shannon sintáctica (que cuenta bits sin importar el significado), la **Información Semántica (SI)** se define formalmente como:
$$SI(S; E) = \mathcal{V}(\text{acoplado}) - \mathcal{V}(\text{desacoplado / scrambled})$$
donde $\mathcal{V}(\sigma) \in [-1, 1]$ es la **función de viabilidad termodinámica**:
$$\mathcal{V}(\sigma) = 0.4 \left(\frac{[\text{ATP}] - 20}{80}\right) + 0.35 \left(\frac{-V_{\text{mem}} - 20}{70}\right) + 0.25 \left(\frac{\text{pH}_i - 6.50}{0.90}\right)$$

### Cortafuegos Fail-Closed
- Si $[\text{ATP}] < 20\% \implies \mathcal{V} = -1.0 \implies \text{Veto Inmediato (Lisis)}$
- Si $V_{\text{mem}} > -20\text{ mV} \implies$ Despolarización mitótica o muerte.
- Si $\text{pH}_i < 6.50 \implies$ Inactivación alostérica de PFK-1 por protones ($n_{\text{Hill}} = 4.0$).

---

## 4. Redes Relacionales: El Bio-Locus y su Matriz de Transición $T_k$

### 4.1 Definición de Bio-Locus
Un **Bio-locus** es una red relacional $\mathcal{G} = (\mathcal{V}_{BL}, \mathcal{E}_{BL})$ donde las células están unidas mediante uniones gap de alta conductancia:
$$g_{ij} = G_{GJ}(\Delta V_{ij}, \overline{\text{pH}}_{i, j}) = g_0 \cdot \frac{1}{1 + \exp\left(\frac{|\Delta V_{ij}| - 25.0}{5.0}\right)} \cdot \frac{1}{1 + 10^{4.0(6.60 - \overline{\text{pH}}_i)}}$$

### 4.2 Matriz de Transición Markoviana $T_k$
El comportamiento dinámico del bio-locus evoluciona en un espacio de 4 microestados discretos:
- **$S_0$ (Homeostático Polarizado):** $V_{\text{mem}} \le -60\text{ mV}$, $G_{GJ} \ge 0.8$, $[\text{ATP}] \ge 60\%$.
- **$S_1$ (Adaptativo / Estrés):** Compensación metabólica activa, acoplamiento preservado.
- **$S_2$ (Despolarizado / Ameboide / Neoplásico):** Cierre de compuertas gap junction, despolarización crítica, fenotipo atávico aislado.
- **$S_3$ (Veto Metabólico / Lisis / Necrosis):** Atractor absorbente fail-closed ($T_{33} = 1.0$).

La matriz $T_k$ es generada deterministamente bajo las condiciones locales y sistémicas:
$$T_k = \begin{pmatrix} 
T_{00} & T_{01} & T_{02} & T_{03} \\
T_{10} & T_{11} & T_{12} & T_{13} \\
T_{20} & T_{21} & T_{22} & T_{23} \\
0 & 0 & 0 & 1
\end{pmatrix}$$

Donde $T_{20}$ y $T_{21}$ están fuertemente catalizados por el cóctel de **repolarización ionotrópica FDA** (Minoxidil, Lidocaína, Isotretinoína, Amilorida).

---

## 5. Métrica de Entropía de Flujo ($H_{\text{flux}}$) e Irreducibilidad ($\mathcal{I}$)

### 5.1 Entropía de Flujo ($H_{\text{flux}}$)
Dado el flujo electrometabólico intercelular entre células $i$ y $j$:
$$F_{ij} = g_{ij} |V_i - V_j| + D_{\text{met}} |\text{pH}_i - \text{pH}_j|$$
El flujo total saliente de cada célula es $F_i = \sum_{j \ne i} F_{ij}$.  
La distribución normalizada de flujo es $p_i = \frac{F_i}{\sum_k F_k}$.

La **Entropía de Flujo** mide el desorden en la circulación de señales del colectivo:
$$H_{\text{flux}} = -\sum_{i=1}^N p_i \ln p_i, \quad h_{\text{flux}} = \frac{H_{\text{flux}}}{\ln N} \in [0, 1]$$

### 5.2 Métrica de Irreducibilidad ($\mathcal{I}$)
Compara la distribución observada $p_i$ con la distribución uniforme $u_i = 1/N$ esperada de una población puramente desintegrada:
$$\mathcal{I}(\text{bio-locus}) = \frac{1}{2}\sum_{i=1}^N \left| p_i - \frac{1}{N} \right| \in [0, 1]$$

### 5.3 Índice de Integración Agencial ($\Phi^r$) y Cono de Luz Cognitivo (CLC)
$$\Phi^r = \mathcal{I} \cdot \bar{G}_{GJ} \cdot \left(\frac{[\overline{\text{ATP}}] - 20}{80}\right)$$

- **$\Phi^r \ge 0.25$:** Estado **Integrated Self** (El colectivo actúa como un macro-agente soberano con memoria morfogenética unificada).
- **$\Phi^r < 0.25$:** Estado **Decoupled Ameboid** (Aislamiento fenotípico tumoral; cada célula compite egoístamente por su propio gradiente).

### 5.4 Simulación In Silico de Knockout (KO)
Al suprimir selectivamente el nodo $k$, la variación de entropía $\Delta H_{\text{flux}}^{(k)} = |H_{\text{flux}}(\text{WT}) - H_{\text{flux}}(\text{KO}_k)|$ cuantifica la indispensabilidad autopoiética de dicho componente dentro de la placa base del tejido.

---

## 6. Certificación Forense Criptográfica (Ley 527 de 1999)

Toda evaluación in silico del Bio-locus emite un hash criptográfico **SHA-256** inmutable calculado sobre la tupla:
$$\text{Certificado} = \text{SHA-256}\Big(\text{ID}, N, \overline{V_{\text{mem}}}, \overline{[\text{ATP}]}, H_{\text{flux}}, \mathcal{I}, \Phi^r, \text{Timestamp}\Big)$$
Garantizando auditoría no repudiable y reproducibilidad determinista libre de sesgos heurísticos.
