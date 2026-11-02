# ⚡ GUANES HEALTH: MAPA DE ECUACIONES DIFERENCIALES
## Electrofisiología Multiescala: Poisson-Nernst-Planck (PNP), Teoría de Cables Tisular & Redes de Hopfield No Neuronales

**Versión:** 1.0.0 (Formalismo Matemático & Derivación)  
**Clasificación:** SSoT — Especificación Matemática para el Simulador  
**Arquitecto Principal & Fundador:** Manuel Enrique Prada Forero  
**Marco Computacional:** Electroquímica Fisiológica / Sistemas Dinámicos No Lineales / Inferencia Activa  

---

## 1. Visión General del Sistema Multiescala

El simulador computacional traduce la **Placa Base Lógica en Tres Capas** a un sistema acoplado de ecuaciones diferenciales ordinarias y en derivadas parciales (EDOs/EDPs) estructurado en tres escalas espaciotemporales:

```
┌────────────────────────────────────────────────────────────────────────┐
│ ESCALA MACROSCÓPICA / TISULAR: TEORÍA DE CABLES 2D/3D (EDP)            │
│  • Difusión electrotónica en el sincitio de conexinas (Cx43)           │
│  • Acoplamiento transjuncional no lineal V_j y red de telocitos        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Corrientes de acoplamiento I_gap
┌───────────────────────────────────▼────────────────────────────────────┐
│ ESCALA CELULAR: CIRCUITO EQUIVALENTE Y BALANCE DE CARGA (EDO)          │
│  • C_m * (dV_mem / dt) = - (I_ion + I_bombas + I_gap + I_ext)          │
│  • Atractores multiestables de reposo y bifurcaciones de fase          │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Flujos iónicos J_k
┌───────────────────────────────────▼────────────────────────────────────┐
│ ESCALA NANOSCÓPICA / MEMBRANA: POISSON-NERNST-PLANCK (PNP)            │
│  • Transporte electrodifusivo de iones a través de canales y poros     │
│  • Distribución del campo eléctrico y carga espacial transmembrana    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Escala Nanoscópica: Ecuaciones de Poisson-Nernst-Planck (PNP)

El transporte de cada especie iónica $k \in \{\text{K}^+, \text{Na}^+, \text{Cl}^-, \text{Ca}^{2+}, \text{H}^+\}$ a través del poro de la membrana y el microambiente pericelular se rige por el acoplamiento electrodifusivo.

### 2.1. Ecuación de Nernst-Planck (Conservación y Flujo Iónico)
El vector de densidad de flujo molar $\mathbf{J}_k$ ($\text{mol}/(\text{m}^2\cdot\text{s})$) combina difusión browniana (gradiente de concentración) y deriva electroforética (gradiente de potencial):

$$\mathbf{J}_k = - D_k \left( \nabla c_k + \frac{z_k F}{RT} c_k \nabla \phi \right)$$

Donde:
* $c_k(\mathbf{x}, t)$: Concentración local de la especie iónica $k$ ($\text{mol}/\text{m}^3$).
* $D_k$: Coeficiente de difusión del ion dentro del canal o solución ($\text{m}^2/\text{s}$).
* $z_k$: Valencia eléctrica del ion ($+1$ para $\text{K}^+, \text{Na}^+, \text{H}^+$; $-1$ para $\text{Cl}^-$; $+2$ para $\text{Ca}^{2+}$).
* $F$: Constante de Faraday ($96\,485.33\text{ C}/\text{mol}$).
* $R$: Constante universal de los gases ($8.314\text{ J}/(\text{mol}\cdot\text{K})$).
* $T$: Temperatura fisiológica ($310.15\text{ K} = 37^\circ\text{C}$).
* $\phi(\mathbf{x}, t)$: Potencial electrostático local ($\text{V}$).

La ecuación de continuidad impone la conservación de masa iónica:

$$\frac{\partial c_k}{\partial t} = - \nabla \cdot \mathbf{J}_k + \mathcal{R}_k$$

*(Donde $\mathcal{R}_k$ representa tasas de reacción o amortiguamiento químico citosólico).*

### 2.2. Ecuación de Poisson (Campo Electrostático Autoinducido)
La distribución del potencial eléctrico $\phi$ está determinada por la densidad total de carga neta:

$$\nabla \cdot \big( \varepsilon(\mathbf{x}) \nabla \phi \big) = - \rho(\mathbf{x}) = - \left( F \sum_k z_k c_k + \rho_{\text{fija}} \right)$$

Donde:
* $\varepsilon(\mathbf{x}) = \varepsilon_r \varepsilon_0$: Permitividad dieléctrica del medio ($\varepsilon_r \approx 2\text{ a } 4$ en bicapa lipídica, $\varepsilon_r \approx 80$ en citosol/fluido extracelular).
* $\rho_{\text{fija}}$: Densidad de carga estática de las cadenas laterales de proteínas del poro y fosfolípidos de membrana.

### 2.3. Reducción a Régimen Cuasi-Estacionario: Límite Goldman-Hodgkin-Katz (GHK)
Bajo la hipótesis de campo eléctrico constante dentro de una membrana de espesor $d$ ($\nabla \phi \approx \Delta V / d = V_{mem}/d$), la integración analítica unidimensional de la ecuación de Nernst-Planck conduce a la **densidad de corriente iónica GHK ($I_k$)**:

$$I_k = P_k z_k^2 \frac{F^2 V_{mem}}{RT} \left[ \frac{c_{k,i} - c_{k,e} \exp\left( - \frac{z_k F V_{mem}}{RT} \right)}{1 - \exp\left( - \frac{z_k F V_{mem}}{RT} \right)} \right]$$

Donde $P_k$ es la permeabilidad efectiva ($\text{m}/\text{s}$), el objetivo directo de modulación farmacológica por cócteles ionotrópicos.

---

## 3. Escala Celular: Dinámica de Membrana y Circuitos Multiestables

Para cada célula individual $i$, el potencial de membrana $V_i \equiv V_{mem,i}$ evoluciona según la conservación de carga sobre la capacitancia de membrana $C_m$ ($\approx 1\text{ }\mu\text{F}/\text{cm}^2$):

$$C_m \frac{d V_i}{d t} = - \left( I_{\text{pasivo}}(V_i) + I_{\text{voltaje}}(V_i, \mathbf{w}) + I_{\text{bombas}} + I_{\text{gap},i} \right)$$

### 3.1. Corrientes Iónicas Pasivas y Dependientes de Voltaje
$$I_{\text{pasivo}} = g_{K,\text{leak}}(V_i - E_K) + g_{Na,\text{leak}}(V_i - E_{Na}) + g_{Cl,\text{leak}}(V_i - E_{Cl})$$

Donde los potenciales de reversión de Nernst son:
$$E_k = \frac{RT}{z_k F} \ln \left( \frac{[k]_e}{[k]_{i}} \right)$$

Para canales dependientes de voltaje (vg. $Na_v 1.5, K_v$), incorporamos variables de compuerta tipo Hodgkin-Huxley somático $\mathbf{w} = (m, h, n)$:
$$I_{\text{voltaje}} = \bar{g}_{Na} m^3 h (V_i - E_{Na}) + \bar{g}_K n^4 (V_i - E_K)$$
$$\frac{dw}{dt} = \frac{w_\infty(V_i) - w}{\tau_w(V_i)}, \quad w \in \{m, h, n\}$$

### 3.2. Bombas Electrogénicas No Lineales
1. **Bomba $\text{Na}^+/\text{K}^+$-ATPasa:**
   Genera una corriente efluyente neta hiperpolarizante modelada mediante cinética de Hill:
   $$I_{\text{NaK}} = I_{\text{NaK,max}} \cdot \left( \frac{[\text{Na}^+]_i}{[\text{Na}^+]_i + K_{m,\text{Na}}} \right)^3 \cdot \left( \frac{[\text{K}^+]_e}{[\text{K}^+]_e + K_{m,\text{K}}} \right)^2 \cdot f_{\text{voltaje}}(V_i)$$

2. **Bomba $\text{H}^+$-V-ATPasa y Antiportador NHE1:**
   $$I_{\text{NHE1}} \propto \frac{1}{1 + 10^{pH_i - pK_a}} \cdot \frac{1}{1 + 10^{pK_b - pH_e}}$$
   *(Regula el escape de protones y consolida el escudo pericelular ácido del tumor).*

### 3.3. Dinámica Intracelular de Concentraciones
El volumen citosólico $\text{Vol}_i$ integra los flujos iónicos netos:
$$\frac{d [k]_i}{dt} = - \frac{A_{\text{mem}}}{z_k F \cdot \text{Vol}_i} I_{k,\text{total}} + \sum_{j \in \mathcal{N}_i} \frac{J_{k,\text{gap}}^{j \to i}}{\text{Vol}_i}$$

---

## 4. Escala Tisular: Teoría de Cables Multidimensional & Sincitio Conexinas (Cx43)

### 4.1. Formalismo Discreto de Red (Red de Células Acopladas)
Las células somáticas están interconectadas en una topología reticular (2D o 3D) mediante *gap junctions*. La corriente total que la célula $i$ intercambia con sus vecinas $\mathcal{N}_i$ es:

$$I_{\text{gap},i} = \sum_{j \in \mathcal{N}_i} g_{ij}(V_i, V_j, pH_e) \cdot (V_i - V_j)$$

### 4.2. Conductancia Transjuncional No Lineal de Conexinas $g_{ij}(V_j)$
La conductancia de una *gap junction* (Cx43) depende del **voltaje transjuncional** $V_j \equiv V_i - V_j$. Se modela formalmente mediante una **distribución de Boltzmann doble**:

$$g_{ij}(V_j) = g_{\text{res}} + \frac{g_{\text{max}} - g_{\text{res}}}{1 + \exp\left( \pm A \cdot (|V_i - V_j| - V_0) \right)} \cdot \Phi(pH_e)$$

Donde:
* $g_{\text{res}}$: Conductancia residual mínima en estado cerrado.
* $g_{\text{max}}$: Conductancia en estado completamente abierto (sano, $V_j \approx 0$).
* $V_0$: Voltaje transjuncional en el que la conductancia cae a la mitad ($\approx 30\text{ a } 45\text{ mV}$ para Cx43).
* $\Phi(pH_e)$: Función sigmoidal de bloqueo por acidosis:
  $$\Phi(pH_e) = \frac{1}{1 + \exp\left( - \frac{pH_e - pH_{\text{crit}}}{\Delta pH} \right)}$$
  *(Si $pH_e \le 6.20$, $\Phi \to 0$: el tumor queda eléctricamente aislado).*

### 4.3. Límite Continuo: Ecuación de Cable Tisular Bidimensional (EDP)
En el límite continuo espacial ($\Delta x \to 0$), el tejido se describe como un medio bidominio o cable bidimensional generalizado:

$$C_m \frac{\partial V}{\partial t} = \nabla \cdot \big( \mathbf{G}_{\text{gap}}(\mathbf{x}, V) \nabla V \big) - I_{\text{iónico}}(V) + I_{\text{ext}}$$

En coordenadas cartesianas 2D para un tejido isotrópico:

$$C_m \frac{\partial V}{\partial t} = \frac{\partial}{\partial x} \left( \sigma_x(V) \frac{\partial V}{\partial x} \right) + \frac{\partial}{\partial y} \left( \sigma_y(V) \frac{\partial V}{\partial y} \right) - I_{\text{iónico}}(V)$$

Donde la conductividad del sincitio $\sigma(V)$ representa la densidad de conexinas activas ($\text{Cx43}$).

---

## 5. El Isomorfismo de Hopfield: Redes No Neuronales y Función de Energía

### 5.1. Mapeo Dinámico
Identificamos formalmente la red bioeléctrica con una **Red Neuronal Recurrente Continua de Hopfield**:

| Red Neuronal de Hopfield | Sincitio Bioeléctrico Tisular |
| :--- | :--- |
| **Neurona $i$ / Estado $u_i$** | Célula somática $i$ / Potencial intracelular $V_i$ |
| **Función de activación $s_i = g(u_i)$** | Corriente neta / Estado de apertura de canales |
| **Peso sináptico $W_{ij}$** | Conductancia intercelular de conexinas $g_{ij}$ |
| **Potencial de reposo o umbral $\theta_i$** | Potencial de reversión GHK intrínseco $E_{\text{rev},i}$ |

### 5.2. Función de Energía de Lyapunov (Función Objetivo del Tejido)
Para una matriz de acoplamiento simétrica ($g_{ij} = g_{ji}$), definimos la función escalar de energía bioeléctrica:

$$\mathcal{E}(\mathbf{V}) = - \frac{1}{2} \sum_{i} \sum_{j \in \mathcal{N}_i} g_{ij} (V_i - V_j)^2 - \sum_i \int_0^{V_i} I_{\text{iónico}}(V') dV'$$

Por el teorema de estabilidad de Lyapunov:
$$\frac{d\mathcal{E}}{dt} = \sum_i \frac{\partial \mathcal{E}}{\partial V_i} \frac{dV_i}{dt} = - \sum_i C_m \left( \frac{dV_i}{dt} \right)^2 \le 0$$

* **Atractor Saludable:** Mínimo global de $\mathcal{E}$ ($\delta S = 0$, $V_i \approx -65\text{ mV} \; \forall i$).
* **Foco Tumoral:** Mínimo local patológico desacoplado ($g_{ij} \approx 0, V_{\text{tumor}} \approx -20\text{ mV}$).

---

## 6. Formulación de Inferencia Activa & Repolarización FDA (Espacio de Control)

El objetivo del simulador es encontrar el vector de intervención farmacológica $\mathbf{u}(t) = [u_{\text{minoxidil}}, u_{\text{lidocaina}}, u_{\text{isotretinoina}}, u_{\text{amilorida}}]$ que minimice la Energía Libre Variacional $\mathcal{F}$:

$$\mathcal{F}(t) = \frac{1}{2} \sum_{i \in \text{Tumor}} \big( V_i(t) - V_{\text{sano}}^* \big)^2 + \lambda \sum_{i \in \text{Borde}} (1 - \text{Cx43}_i(t))^2 + \gamma \|\mathbf{u}(t)\|^2$$

Sujeto a:
$$\begin{aligned}
P_K(t) &= P_{K,0} \cdot \big( 1 + \kappa_1 \cdot u_{\text{minoxidil}}(t) \big) \\
P_{Na}(t) &= P_{Na,0} \cdot \big( 1 - \kappa_2 \cdot u_{\text{lidocaina}}(t) \big) \\
g_{\text{max},\text{Cx43}}(t) &= g_{\text{base}} \cdot \big( 1 + \kappa_3 \cdot u_{\text{isotretinoina}}(t) \big) \\
J_{\text{NHE1}}(t) &= J_{\text{NHE1},0} \cdot \big( 1 - \kappa_4 \cdot u_{\text{amilorida}}(t) \big)
\end{aligned}$$

---

## 7. Resumen de Ecuaciones para Implementación en Código

```python
# Pseudo-código del núcleo numérico para el solver (RK4 / Heun / Crank-Nicolson):

def dV_dt_sistema(V, conc, t, params, farmacos_fda):
    # 1. Modular permeabilidades con fármacos FDA
    P_K = params.P_K * (1 + params.k_minox * farmacos_fda.minoxidil)
    P_Na = params.P_Na * (1 - params.k_lido * farmacos_fda.lidocaina)
    
    # 2. Corrientes iónicas transmembrana GHK locales
    I_GHK = calcular_corriente_ghk(V, conc, P_K, P_Na, params.P_Cl)
    I_Bombas = calcular_corriente_NaK_ATPasa(V, conc)
    
    # 3. Corrientes de conexinas Cx43 (Laplaciano discreto no lineal)
    V_diff = V[:, np.newaxis] - V[np.newaxis, :]  # V_j = V_i - V_j
    g_gap = calcular_conductancia_boltzmann_cx43(V_diff, params.pHe, farmacos_fda.isotretinoina)
    I_gap = np.sum(g_gap * V_diff, axis=1)
    
    # 4. Derivada del potencial de membrana
    dV = (- (I_GHK + I_Bombas + I_gap)) / params.C_m
    
    # 5. Dinámica de concentraciones iónicas
    dConc = actualizar_concentraciones(I_GHK, I_Bombas, params.Volumen)
    
    return dV, dConc
```

---

> **Atestado:** Este mapa de ecuaciones unifica formalmente el transporte nanoscópico (PNP), la electrodinámica tisular (Cables 2D) y la memoria morfológica (Hopfield) para la ejecución en el motor computacional de Guanes Health.
