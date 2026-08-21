# Compendio bibliográfico: ecosistema acoplado (Escenario 4)

Soporte de literatura y anclaje de parámetros del modelo onco-hepático.  
Guanes Health — investigación *in silico*.

**Nota:** las citas respaldan biología de fondo (Capa A). Los umbrales numéricos del código son Capa B (modelo), no calibración clínica.

---

## 1. Marco del Escenario 4 (co-intervención modelada)

El Escenario 4 combina, en el simulador, Myrcludex B + inmunoterapia (Cohorte C) + atenuación del eje IL-6/STAT3 (proxy \(\beta_{PD\text{-}L1}=0.1\)). Es una hipótesis de diseño secuencial, no un protocolo clínico.

Bajo infección por HBV y tumor adyacente, el modelo acopla tres tensiones:

1. **Entrada viral**: HBV usa NTCP (SLC10A1) basolateral [3].
2. **Inflamación paracrina**: IL-6 puede reprimir NTCP en hepatocito y, en el clon tumoral, empujar STAT3 → PD-L1 [3, 4].
3. **Microambiente ácido**: eflujo de protones (p. ej. MCT4) puede deprimir citotoxicidad CD8+ modelada a pHe bajo [5].

### Interrupción síncrona de acoplamientos (en el modelo)

El aclaramiento tumoral *simulado* en Escenario 4 aparece cuando se cortan a la vez esos acoplamientos:

- **Myrcludex B (10 nM)**: bloqueo preferente de entrada viral vs transporte biliar (Ki modeladas 1 nM vs 100 nM), para limitar colestasis / depleción de GSH (`VETO FC-HEP-01`).
- **Atenuación IL-6/STAT3**: mantiene PD-L1 por debajo del umbral de saturación anti-PD-1 (150× en Capa B).
- **Cohorte C**: normalización de pHe modelado (~7.35) antes de anti-PD-1, para no disparar el veto de escudo ácido.

---

## 2. COMPENDIO DE LITERATURA DE RESPALDO (CRÉDITOS ACADÉMICOS)

A continuación, se catalogan de forma rigurosa las investigaciones biomédicas, artículos de revisión y ensayos clínicos indexados en el ecosistema científico que otorgan validez biológica a las ecuaciones cinéticas, aserciones y parámetros de frontera integrados en nuestro simulador multiescala:

### **A. Virología Molecular y Receptores de Entrada (HBV / NTCP / Myrcludex B)**

*   **[Yan et al., 2012]**  
    *Yan H, Zhong G, Xu G, He W, Jing Z, Gao Z, et al.*  
    **Sodium Taurocholate Cotransporting Polypeptide Is a Functional Receptor for Human Hepatitis B and D Virus.**  
    *Elife, 2012; 1:e00049. DOI: 10.7554/eLife.00049*  
    * **Aporte Científico**: Descubrimiento histórico de la proteína NTCP (SLC10A1) como el receptor basolateral exclusivo utilizado por la glicoproteína grande de superficie (LHB) de HBV y HDV para la entrada celular. Mapeó de forma tridimensional la interacción específica del dominio **preS1** con los residuos 157 a 165 (KGIVISLVL) de NTCP, localizando la posición de susceptibilidad crítica de especie en el residuo 158.

*   **[Li et al., 2022]**  
    *Li Y, Zhou J, Li T.*  
    **Regulation of the HBV Entry Receptor NTCP and its Potential in Hepatitis B Treatment.**  
    *Frontiers in Molecular Biosciences, 2022; 9:879817. PMCID: PMC9039015. DOI: 10.3389/fmolb.2022.879817*  
    * **Aporte Científico**: Sostiene la dinámica reguladora de NTCP por la vía inflamatoria paracrina. Documenta de forma cuantitativa la cascada de señalización **IL-6 \\(\rightarrow\\) JNK** que inactiva los factores de transcripción enriquecidos en hígado **HNF-1α y HNF-4α**, resultando en una represión del promotor transcripcional de hasta el 98% en hepatocitos primarios humanos (PHH). Asimismo, detalla la regulación post-traduccional del receptor y su tasa de recambio en la membrana sinusoidal.

*   **[Volz et al., 2013]**  
    *Volz T, Allweiss L, M'Barek MB, Warlich M, et al.*  
    **The Entry Inhibitor Myrcludex-B Efficiently Blocks Intrahepatic Virus Spreading in Humanized Mice Previously Infected with Hepatitis B Virus.**  
    *Journal of Hepatology, 2013; 58(5): 861-867. DOI: 10.1016/j.jhep.2012.12.008*  
    * **Aporte Científico**: Valida el mecanismo farmacodinámico del entry inhibitor Myrcludex B (Hepcludex), un lipopéptido sintético derivado de preS1. Demuestra cómo satura competitivamente a NTCP para frenar la infección *de novo*, justificando en el simulador las constantes de selectividad y el diferencial estequiométrico que previene la colestasis detergente mitocondrial por acumulación de taurocolato basolateral.

### **B. Inmunología del Microambiente Estromal y Regulación por pH**

*   **[placa-base-logica-inmunologica-v2.md - Especificación Técnica]**  
    *Guanes Health - Documento de Diseño Inmunológico v2.0.*  
    * **Aporte Científico**: Describe el **Veto del Escudo Ácido (FC-BIO-2.1)**, parametrizando que la desgranulación lítica de perforinas y granzimas por linfocitos CD8+ TILs queda completamente excluida a un pH estromal extracelular local \\(pHe \le 6.50\\) debido a la parálisis mecánica de filamentos de actina y el colapso de los gradientes iónicos de calcio dependientes de carga.

*   **[Hoshino H, 2012]**  
    *Hoshino H.*  
    **Cellular Factors Involved in HTLV-1 Entry and Pathogenicity.**  
    *Frontiers in Microbiology, 2012; 3:222. DOI: 10.3389/fmicb.2012.00222*  
    * **Aporte Científico**: Describe el modelo de multi-receptor coordinado (HSPGs, NRP-1 y GLUT1) que permite la fusión a pH extracelular neutro del deltaretrovirus mediante el mimetismo molecular del motivo peptídico KKPNR con VEGF165, y la isomerización de enlaces disulfuro de gp21 (seis hélices super-estables 6HB).

### **C. Reprogramación Metabólica y Mecanismos de Escape de Cáncer**

*   **[Frontiers | Cellular Factors Involved in HTLV-1 Entry and Pathogenicity]**  
    * **Aporte Científico**: Justifica la hiper-expresión de los transportadores GLUT1 asociados al Efecto Warburg en células con reprogramación metabólica acelerada, lo que concentra de manera masiva los receptores de entrada y propaga selectivamente el vector en el microambiente tumoral.

*   **[placa-base-hepatocito.md - Especificación de Zonación]**  
    *Guanes Health - Documento de Diseño del Hepatocito v1.0.*  
    * **Aporte**: Ancla el gradiente sinusoidal de oxígeno (Zona 1 periportal vs Zona 3 pericentral) y la modulación de transportadores biliares según oxigenación local (base de densidad NTCP en el modelo).

---

## 3. Límites

Herramienta de cribado de hipótesis *in silico*. Las dinámicas numéricas del repo **no** están calibradas como predictores clínicos. Toda hipótesis relevante requiere validación experimental independiente.

Cribado de hipótesis sobre instrumento de placa — no consejo médico ni evidencia clínica.

