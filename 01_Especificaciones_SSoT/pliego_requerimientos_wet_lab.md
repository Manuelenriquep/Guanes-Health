# PLIEGO DE REQUERIMIENTOS EXPERIMENTALES Y PROTOCOLO DE VALIDACIÓN WET-LAB
## Transición de Consistencia Lógica (Capa B) a Evidencia Empírica de Sistemas (Capa A)
**Documento de Especificación Técnica - Guanes Health (v1.0)**

---

### 1. OBJETIVO GENERAL
El presente documento define los requerimientos técnicos, metodológicos y de instrumentación científica para la ejecución del bucle de validación experimental en el laboratorio húmedo (*wet-lab*). El objetivo principal es suministrar los datos empíricos de calibración termodinámica, cinética y metabólica necesarios para nutrir y calibrar de forma continua las constantes lógicas de la **Placa Base de Lógica (NS-LBN)** de Guanes Health, migrando de un modelo puramente teórico (Capa B) a un sistema predictivo robusto anclado en la realidad celular y clínica (Capa A).

---

### 2. PAQUETE DE TRABAJO 1 (WP1): CARACTERIZACIÓN TERMODINÁMICA DEL RECEPTOR SINTÉTICO (GPC3 vs. sGPC3)
Este bloque metodológico debe determinar las constantes cinéticas exactas de asociación y disociación del dominio de unión de la célula T reprogramada, evaluando el impacto del pH en el "interruptor de histidinas" y el efecto señuelo del GPC3 soluble.

#### 2.1 Ensayos de Resonancia de Plasmón Superficial (SPR - Biacore)
*   **Procedimiento:** Inmovilizar el antígeno recombinante GPC3 y el fragmento soluble sGPC3 en chips sensores de carboximetildextrano (CM5). Inyectar diluciones seriadas del dominio scFv (ej. clon GC33 modificado con histidinas en regiones CDR) como analito móvil.
*   **Gradiente de pH a evaluar:** Correr curvas de asociación/disociación a valores de pH discretos: `6.00, 6.20, 6.50, 6.80, 7.00, 7.40` utilizando tampones fosfato-citrato a temperatura constante ($37^\circ\text{C}$).
*   **Métricas a extraer (Entregables):**
    *   Constante de asociación ($k_{on}$, $\text{M}^{-1}\text{s}^{-1}$).
    *   Constante de disociación ($k_{off}$, $\text{s}^{-1}$).
    *   Constante de disociación en equilibrio ($K_d = k_{off}/k_{on}$, $\text{M}$ o $\text{nM}$).
    *   Tasa de saturación del scFv por el antígeno soluble señuelo sGPC3 en condiciones de co-presencia de GPC3 unido a membrana.

#### 2.2 Cuantificación del Umbral Mínimo de Activación ($Ag_{threshold}$)
*   **Procedimiento:** Generar líneas celulares de carcinoma hepatocelular (HCC) Huh-7 con expresión controlada de GPC3 mediante promotores inducibles de tetraciclina (sistema Tet-On). Cuantificar rigurosamente la densidad absoluta de receptores GPC3 de membrana por célula mediante citometría de flujo cuantitativa utilizando esferas de calibración (ensayo QIFIkit).
*   **Ensayo de Degranulación:** Co-cultivar las células CAR-T con Huh-7 de densidad antigénica conocida (desde 100 hasta $5 \times 10^5$ moléculas/célula). Medir la desgranulación lisosomal mediante marcaje externo de CD107a.
*   **Métricas a extraer:** Determinar el umbral matemático exacto de densidad de antígeno por micra cuadrada de membrana celular necesario para desencadenar el clivaje proteolítico y la fosforilación de los dominios ITAM de CD3-zeta.

---

### 3. PAQUETE DE TRABAJO 2 (WP2): CINÉTICA METABÓLICA Y HOMEOSTASIS DE PROTONES (NHE1 & MCT4)
Establece los perfiles bioenergéticos que regulan la parálisis citotóxica en el microambiente ácido y la eficacia del escudo metabólico de protones de la célula reprogramada.

#### 3.1 Análisis de Flujo Extracelular en Tiempo Real (Seahorse XF)
*   **Procedimiento:** Utilizar el analizador Seahorse XF24 o XF96 para medir simultáneamente la Tasa de Consumo de Oxígeno (OCR, indicador de fosforilación oxidativa) y la Tasa de Acidificación Extracelular (ECAR, indicador de glucólisis anaeróbica por extrusión de lactato/protones).
*   **Líneas de Ensayo:** Comparar de forma simultánea:
    1.  Células T nativas de control (CD8+ salvajes).
    2.  Células CAR-T convencionales.
    3.  Células CAR-T con sobreexpresión transgénica de NHE1 (intercambiador $\text{Na}^+/\text{H}^+$).
*   **Perturbaciones Farmacológicas:** Evaluar la respuesta bajo la adición secuencial de Oligomicina (bloqueador de ATP sintasa), FCCP (desacoplador mitocondrial), y Antimiocina A/Rotenona (bloqueadores de la cadena respiratoria).
*   **Métricas a extraer:**
    *   Reserva de capacidad mitocondrial y capacidad glucolítica máxima bajo acidosis estromal severa (pH 6.20) en presencia o ausencia del transportador NHE1.
    *   Curva de decaimiento del ATP intracelular bajo exposición crónica a concentraciones variables de lactato extracelular (de 2.0 mM a 40.0 mM).

#### 3.2 Medición Dinámica del pH Intracelular (pHi)
*   **Procedimiento:** Cargar las poblaciones de células T y CAR-T con el éster acetoximetílico de 2',7'-bis-(2-carboxietil)-5-(y-6)-carboxifluoresceína (**BCECF-AM**), una sonda ratiométrica fluorescente sensible al pH intracelular.
*   **Monitoreo:** Someter a las células a un medio extracelular tamponado a pH ácido continuo (pH 6.20). Registrar la fluorescencia mediante espectrofluorometría o microscopía de barrido confocal con calibración por ionóforo de nigericina.
*   **Métricas a extraer:**
    *   Velocidad de acidificación del citosol de la célula T nativa frente a la célula modificada con NHE1.
    *   Tiempo promedio de colapso del gradiente de pH transmembrana ($\Delta pH$) por debajo de pH 6.80.

---

### 4. PAQUETE DE TRABAJO 3 (WP3): VALIDACIÓN ESTEQUIOMÉTRICA DEL FUSIBLE iCASP9
Modelado farmacodinámico in vitro de la inducción de muerte celular de emergencia para definir el perfil de seguridad clínica.

#### 4.1 Ensayos de Homodimerización por Rimiducid (AP1903)
*   **Procedimiento:** Exponer cultivos estables de células CAR-T transducidas con el casete de expresión `iCasp9-FKBP12v` a concentraciones crecientes del inductor bivalente AP1903 (desde 0.01 nM hasta 100 nM).
*   **Métricas a extraer:**
    *   Constante de disociación in vitro de AP1903 por el dominio mutado F36V.
    *   Curva de concentración efectiva media ($\text{EC}_{50}$) para la inducción de la apoptosis celular a las 1, 2, 4, 12 y 24 horas.

#### 4.2 Cinética de Activación de la Cascada de Caspasas
*   **Procedimiento:** Extraer lisados proteicos de células tratadas con AP1903 a diferentes pasos de tiempo (0, 15, 30, 60, 120, 240 minutos). Medir la presencia y actividad de las caspasas 9 y 3/7 activas mediante:
    *   Fluorometría cuantitativa de sustratos de clivaje selectivos (ej. Ac-DEVD-AMC para Caspasa-3).
    *   Análisis de transferencia Western Blot utilizando anticuerpos específicos para fragmentos de clivaje de Caspasa-3 y PARP-1.
*   **Métricas a extraer:** Tiempo de retardo ($t_{lag}$) entre la dimerización alostérica y la activación irreversible de la degradación nuclear.

#### 4.3 Verificación de Evasión de Bloqueo Anti-Apoptósico (Bcl-2 Bypass)
*   **Procedimiento:** Transducir de forma artificial una subpoblación de CAR-T para sobreexpresar de manera constitutiva la proteína antiapoptósica mitocondrial Bcl-2 (clonación lentiviral). Tratar las células recombinantes con AP1903 y realizar ensayos de viabilidad por exclusión de yoduro de propidio (PI) o tinción Annexin V por citometría de flujo.
*   **Métricas a extraer:** Demostrar estadísticamente la ausencia de diferencia significativa en el porcentaje de apoptosis final entre la línea CAR-T normal y la línea CAR-T Bcl-2 sobreexpresada tras inducir el clivaje con AP1903.

---

### 5. PAQUETE DE TRABAJO 4 (WP4): EXTRAVASACIÓN, ADHESIÓN E INFILTRACIÓN ESTROMAL (ORGAN-ON-A-CHIP)
Modelado reológico y biofísico de la migración leucocitaria bajo las barreras de presión intersticial características de los tumores hepáticos sólidos.

#### 5.1 Ensayos de Adhesión bajo Flujo Dinámico (Cámaras de Microfluídica)
*   **Procedimiento:** Cultivar una monocapa densa de células endoteliales sinusoidales hepáticas humanas (HHSEC) estimuladas con TNF-alfa o tratadas con VEGF (para inducir anergia endotelial) en canales de microfluídica. Perfundir células T marcadas fluorescentemente a tasas de esfuerzo de cizalla (*shear stress*) controladas (0.5 a 5.0 dinas/$\text{cm}^2$).
*   **Métricas a extraer:**
    *   Tasa de rodamiento (células/minuto) dependiente de selectinas.
    *   Fuerza crítica de desprendimiento de las uniones mediadas por LFA-1 / ICAM-1.

#### 5.2 Ensayo de Diapédesis y Migración Intersticial en Microgeles 3D
*   **Procedimiento:** Fabricar una barrera endotelial en un chip de microfluídica multicapa que separe un canal de flujo activo de una cámara de colágeno fibrilar 3D reticulado densamente con concentraciones variables de colágeno tipo I (1.5, 3.0, 5.0 mg/mL), emulando la rigidez estromal del HCC. Aplicar un gradiente quimiotáctico controlado de CXCL10 en la cámara profunda del gel, acoplado a una bomba de micropresión para generar una Presión de Fluido Intersticial (IFP) constante de 5.0 a 30.0 mmHg.
*   **Métricas a extraer:**
    *   Índice de Resistencia a la Transmigración en función de la IFP.
    *   Velocidad neta de infiltración espacial (micras/hora) de las células CAR-T nativas frente a las modificadas con sobreexpresión de metaloproteinasas de matriz (MMP-2/9).

---

### 6. PAQUETE DE TRABAJO 5 (WP5): CARTOGRAFÍA BIOELÉCTRICA ($V_{mem}$), ACOPLAMIENTO SINCITIAL ($GJC$) Y CONO DE LUZ COGNITIVO (MARCO DE M. LEVIN / MET-01)
Evalúa experimentalmente la interfaz entre el **Hardware metabólico** (flujo protónico $pHi/pHe$, mutantes NHE1 `S703A` vs. `1K3R4E`, transportadores MCT1/4) y el **Software fisiológico** (potencial de membrana $V_{mem}$, uniones comunicantes *gap junctions* y escala del Cono de Luz Cognitivo).

#### 6.1 Imagenología Ratiométrica Dual en Tiempo Real ($pHi$ + $V_{mem}$: BCECF-AM / DiBAC4(3))
*   **Procedimiento:** Co-cargar co-cultivos de hepatocitos tumorales (Huh-7) y linfocitos CAR-T (comparando `wtNHE1`, mutante defectivo `S703A` [$V_{\max}=10.0, pKa=6.15$] y blindaje constitutivo `1K3R4E` [$V_{\max}=22.0, pKa=6.75$]) con la sonda de pH intracelular **BCECF-AM** y el fluoróforo aniónico sensible al voltaje transmembrana **DiBAC4(3)**.
*   **Perturbación Ácida y Bioeléctrica:** Exponer las cámaras a la transición estromal de $pHe = 7.40$ a $pHe = 6.20$ (compuerta `Gated-6.50`), con y sin activación de hiperpolarización forzada (abridores de canales $K^+$ o estimulación optogenética Arch).
*   **Métricas a extraer:**
    *   Curva acoplada de despolarización celular ($V_{mem}$ de $-70\text{ mV}$ hacia $-30\text{ a }-15\text{ mV}$) en función de la caída de $pHi$.
    *   Verificación experimental de la **Trampa Bioeléctrica del Ácido Estromal**: cuantificar el colapso de ATP y $pHi$ al hiperpolarizar sin pre-acondicionamiento estromal frente al rescate conferido por el mutante `1K3R4E (NHE1)`.

#### 6.2 Cuantificación de Conductancia de Uniones Gap ($GJC$) y Estrategia Bimodal Tumoral
*   **Procedimiento:** Medir la permeabilidad intercelular mediada por Conexina 43 (Cx43) mediante ensayos de recuperación de fluorescencia tras fotoblanqueo (**gap-FRAP** con calceína-AM) y transferencia de trazador (**Lucifer Yellow** / *scrape loading*) en dos regímenes:
    1.  *Fase de Aislamiento Primario:* Borde entre clon oncogénico despolarizado ($V_{mem} \approx -30\text{ mV}$) y monocapa epitelial sana hiperpolarizada ($V_{mem} \approx -70\text{ mV}$).
    2.  *Fase Invasiva/Metastásica:* Frente de invasión en matriz 3D.
*   **Métricas a extraer:**
    *   Conductancia efectiva normalizada ($GJC \in [0.0, 1.0]$) en función del diferencial de voltaje de borde ($\Delta V_{mem}$) y del $pHi$ citosólico.
    *   Umbral crítico de desconexión fisiológica donde el Cono de Luz Cognitivo se contrae al estado unicelular atávico y detona anergia en el CAR-T (caída de CD107a).

#### 6.3 Matriz de Trazabilidad Multiescala (Capas A $\leftrightarrow$ B $\leftrightarrow$ C)

| Capa del Sistema | Función y Alcance Biológico | Módulos y Parámetros Clave | Fuentes y Referencias |
| :--- | :--- | :--- | :--- |
| **Capa C: Gobernanza Bioconductual** *(Software Colectivo)* | Define la escala del "Yo", el Cono de Luz Cognitivo y los *setpoints* de homeostasis anatómica o anergia inmunológica. | • Cono de Luz Cognitivo<br>• Estado de $V_{mem}$ ($-70\text{ mV}$ vs $-30\text{ mV}$)<br>• Compuerta `Gated-6.50`<br>• Colectividad por Gap Junctions ($GJC$) | M. Levin et al. (2014–2026)<br>`Placa_Base_Subversion_y_Normalizacion_5_Niveles.md` |
| **Capa B: Consistencia Lógica** *(Modelado Matemático)* | Procesa el lazo de retroalimentación dinámico entre la carga metabólica y el transporte de protones/fármacos. | • Ecuación de Mookerjee ($PPR_{\text{glyc}}$)<br>• ODEs acopladas de $pHi/pHe$ y $V_{mem}$<br>• Modelo de Hill / Lock de NHE1 (`1K3R4E`)<br>• Farmacodinamia de BAY-8002 | `met01_coupled_proton_ledger.json`<br>`seahorse_deconvolution-v2.py`<br>`simulador_normalizacion_bioelectrica.py` |
| **Capa A: Evidencia Empírica** *(Trazabilidad Wet-Lab)* | Conjunto de datos experimentales reales para la calibración física de las constantes del simulador. | • Archivos planos Seahorse Wave<br>• Titulación de Buffer Power ($BP$)<br>• Curva Dual BCECF-AM / DiBAC4(3)<br>• Ensayos SPR / Biacore (GPC3) y gap-FRAP | `pliego_requerimientos_wet_lab.md`<br>SOPs de Laboratorio |

---

### 7. ENTREGABLES Y FORMATEADOR DE DATOS (TENSORES DE CALIBRACIÓN)
Para que los resultados empíricos se acoplen de manera automatizada a la arquitectura computacional del búnker de simulación, el especialista en inmunología y biofísica de sistemas deberá empaquetar los datos en los siguientes formatos estandarizados:

#### 7.1 Matriz de Constantes Físicas (`physical_constants_ledger.json`)
Un diccionario JSON que contenga las constantes termodinámicas, bioeléctricas y cinéticas críticas validadas con sus respectivos intervalos de confianza estadística (p-valor $< 0.05$).
```json
{
  "scfv_gpc3_kinetics": {
    "ph_6_20": { "kd_nm": 4.25, "std_err": 0.12 },
    "ph_7_40": { "kd_nm": 1250.0, "std_err": 45.3 }
  },
  "safety_fuse": {
    "ap1903_kd_nm": 0.45,
    "clearance_half_life_hours": 3.2
  },
  "metabolic_boundaries": {
    "nhe1_max_flux_protons_sec": 1.25e7,
    "nhe1_1K3R4E_vmax": 22.0,
    "nhe1_1K3R4E_pka": 6.75,
    "atp_viability_limit_relative": 0.20
  },
  "bioelectric_governance_levin": {
    "vmem_healthy_quiescent_mv": -75.0,
    "vmem_tumor_depolarized_mv": -20.0,
    "gjc_healthy_syncytium": 0.85,
    "gjc_isolated_tumor": 0.10
  }
}
```

#### 7.2 Archivos de Curvas de Gradiente (`calibration_curves_gradient.csv`)
Tablas de datos estructurados para cada experimento cinético, lo que permitirá entrenar y calibrar el *Semantic Driver* local para refinar sus estimaciones probabilísticas de pre-activación (`raw`) y alinearlas al 100% con la respuesta molecular real de la Capa A.

---
**APROBACIÓN DE DIRECCIÓN CIENTÍFICA**
*Este documento constituye la especificación canónica y el pliego formal de requerimientos para el reclutamiento del perfil Ph.D. en Inmunología de Sistemas y Biofísica Celular para el búnker de innovación soberana de Guanes Hub.*

