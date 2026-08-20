# COMPENDIO DE LITERATURA CIENTÍFICA DE RESPALDO: PROYECTO vONCO-LOGIC
**GUANES HEALTH | DIVISIÓN DE ONCOLOGÍA COMPUTACIONAL Y BIOLOGÍA DE SISTEMAS**  
**ESTADO:** COMPILACIÓN CANÓNICA DE REFERENCIAS DE RESPALDO  
**DOCUMENTO:** `literatura_referencia.md`  

---

## 1. MECANISMOS DE ONCO-SUBVERSIÓN (HALLMARKS OF CANCER)

Este bloque reúne los marcos teóricos y las referencias científicas depositadas en las bases de datos de indexación biomédica (PubMed/PMC) que justifican los parámetros, constantes y restricciones operativas aplicadas en el motor lógico para el fenotipo tumoral (Warburg, senescencia, evasión inmunitaria y bloqueo apoptótico).

### A. Secuestro de la Apoptosis (Bypass de la Vía Intrínseca)
*   **Referencias Clave**: 
    *   **PMC10353994**: *Biophysical characterization of p53/Bcl-2 family interactions at the mitochondrial outer membrane.*
    *   **PMC4590992**: *The Bcl-2 family protein interaction network: targeting the mitochondrial apoptotic gateway.*
*   **Fundamento Fisiológico**: Estas investigaciones detallan cómo las mutaciones en los hotspots del dominio de unión al ADN de p53 (R175, R248, R273) anulan la auditoría genómica celular, impidiendo la activación de transgenes efectores de la vía intrínseca. Asimismo, cuantifican la sobreexpresión constitutiva de hasta 25 veces (x25) de las proteínas antiapoptóticas Bcl-2 y Bcl-xL, las cuales saturan de manera competitiva el bolsillo hidrofóbico BH3, bloqueando mecánicamente la oligomerización de Bax/Bak para la permeabilización mitocondrial (MOMP).

### B. Inmortalidad Replicativa (Evasión de la Senescencia de Hayflick)
*   **Referencias Clave**:
    *   **PMC10684755**: *Transcriptional reactivation of hTERT through somatic promoter mutations in human cancers.*
    *   **PMC4853035**: *The GABP heterotetramer bind de novo consensus motifs in the TERT promoter to drive immortalization.*
*   **Fundamento Fisiológico**: Trabajos de caracterización genética que evidencian las mutaciones recurrentes en el promotor de hTERT en las posiciones -124 G>A (C228T) y -146 G>A (C250T). Estas transiciones de un nucleótido generan el motivo consenso de novo 5'-GGAA-3' que duplica (~2x) la afinidad de unión por el complejo heterotetramérico de transcripción GABP (específicamente la subunidad GABPB1L), induciendo histona acetiltransferasas para descondensar la cromatina y reprogramar la inmortalidad replicativa (manteniendo telómeros constantes en 3920 pb en el simulador frente al umbral senescente fisiológico de 4000 pb).

### C. Reprogramación Metabólica y Cinética de Lactato (Efecto Warburg)
*   **Referencias Clave**:
    *   **PMC4946416**: *Aerobic glycolysis (Warburg Effect) in tumor microenvironments: shunting glucose carbon for rapid biomass expansion.*
    *   **PMC4783224**: *Kinetic and expression analysis of monocarboxylate transporters MCT1 and MCT4 under hypoxia and metabolic stress.*
*   **Fundamento Fisiológico**: Documentación bioenergética que detalla cómo el desvío glucolítico (mediado por la isoforma lenta de piruvato quinasa PKM2 y el transportador de alta afinidad GLUT1) genera un consumo metabólico parasitario de hasta 100 veces el rango normal. Sostiene la parametrización de las constantes de Michaelis-Menten (afinidad $K_m$ de MCT1 de 3.5–5.0 mM para importación/exportación basal y la alta capacidad de eflujo adaptativo de MCT4 inducido por hipoxia con una $K_m$ efectiva de 1.7–5.0 mM medida por FRET), la cual colapsa el pH extracelular estromal (pHe) a rangos ácidos de 6.20 a 6.50.

### D. Angiogénesis e Inestabilidad de Oxígeno (Eje HIF-1α/VEGF)
*   **Referencias Clave**:
    *   **PMC11529905**: *Hypoxia-inducible factors (HIFs) and the vascular endothelial growth factor (VEGF) signaling axis in solid tumors.*
    *   **PMC4656338**: *Molecular mechanisms of prolyl-hydroxylase domain (PHD) inactivation under physiological tumor hypoxia.*
*   **Fundamento Fisiológico**: Modelado del comportamiento del factor de transcripción HIF-1α bajo condiciones de saturación de oxígeno tisular crítica ($\text{O}_2 < 5\%$). Sostiene que la falta de oxígeno inactiva las PHDs, previniendo la degradación mediada por VHL y gatillando la dimerización con HIF-1β para transcribir el factor angiogénico VEGF, induciendo la neovascularización desorganizada del lecho tumoral.

### E. Transición Epitelio-Mesenquimal e Inmunosupresión (Eje PD-L1/EMT)
*   **Referencias Clave**:
    *   **PMC4947415**: *E-cadherin suppression by Snail, Slug, and Twist drives epithelial-to-mesenchymal transition and metastatic dissemination.*
    *   **PMC6174882**: *Reciprocal regulation between PD-L1 expression and EMT programs to sustain tumor immune evasion.*
*   **Fundamento Fisiológico**: Investigación sobre el vínculo directo entre la pérdida de adherencia social intercelular (represión de E-cadherina) y la sobreexpresión del ligando de muerte programada 1 (PD-L1) en la membrana de células metastásicas, induciendo la parálisis por anergia en los linfocitos T CD8+ infiltrantes de tumores (TILs).

---

## 2. VIROLOGÍA Y PUERTOS DE ACCESO MOLECULAR (HTLV-1 / gp46-gp21)

Este bloque documenta las bases virológicas que fundamentan la hipótesis de direccionamiento y fusión selectiva inyectada conceptualmente en el modelo del vector oncolítico (mimetismo electrostático y de acoplamiento estacional).

### A. El Modelo de Multi-Receptor de Entrada
*   **Referencia Canónica**:
    *   **Hoshino H (2012)**. *Cellular Factors Involved in HTLV-1 Entry and Pathogenicity.* Frontiers in Microbiology, 3:222.  
    *DOI: [10.3389/fmicb.2012.00222](https://doi.org/10.3389/fmicb.2012.00222)*
*   **Fundamento Fisiológico**: Este artículo de revisión recopila las bases de la interacción tridimensional entre las glicoproteínas de envoltura del deltaretrovirus y la célula diana. Describe el modelo cooperativo secuencial de tres pasos de entrada:
    1.  *Adhesión Inicial*: Captura electrostática de la subunidad de superficie gp46 mediada por Proteoglicanos de Heparán Sulfato (HSPGs).
    2.  *Docking Estéreo-Específico*: Acoplamiento directo de gp46 al receptor Neuropilina-1 (NRP-1).
    3.  *Gatillo de Fusión*: Asociación física de gp46 al transportador de glucosa GLUT1, concentrado de manera masiva en las membranas tumorales por el Efecto Warburg.

### B. Mimetismo de VEGF165 y el Motivo KKPNR
*   **Referencia Canónica**:
    *   **Lambert S, Bouttier M, Vassy R, et al. (2009)**. *HTLV-1 uses HSPG and neuropilin-1 for entry by molecular mimicry of VEGF165.* Blood, 113(21): 5176-5185.  
    *DOI: [10.1182/blood-2008-04-150342](https://doi.org/10.1182/blood-2008-04-150342)*
*   **Fundamento Fisiológico**: Investigación que demuestra que la envoltura viral imita molecularmente a la isoforma de crecimiento endotelial VEGF165 mediante un motivo peptídico altamente conservado (residuos 90-94, **KKPNR**), logrando el secuestro competitivo del receptor celular NRP-1.

### C. Isomerización de Disulfuros y Fusión por gp21
*   **Referencias Canónicas**:
    *   **Li K, Zhang S, Kronqvist M, et al. (2008)**. *Intersubunit disulfide isomerization controls membrane fusion of human T-cell leukemia virus Env.* Journal of Virology, 82(15): 7135-7143.  
    *DOI: [10.1128/JVI.00442-08](https://doi.org/10.1128/JVI.00442-08)*
    *   **Wallin M, Ekstrom M, Garoff H (2004)**. *Isomerization of the intersubunit disulphide-bond in Env controls retrovirus fusion.* EMBO Journal, 23(1): 54-65.  
    *DOI: [10.1038/sj.emboj.7600012](https://doi.org/10.1038/sj.emboj.7600012)*
*   **Fundamento Fisiológico**: Detalla cómo la unión a GLUT1 desata la isomerización de enlaces disulfuro inter-subunitarios entre gp46 (C225/C228) y gp21 (C401), disociando el complejo y provocando el plegamiento elástico de gp21 en un haz de seis hélices super-estables (6HB coiled-coil) para vencer la repulsión osmótica y fusionar las membranas.

---

## 3. HEPATITIS B Y EL RECEPTOR DE ENTRADA LIVER-SPECIFIC (NTCP / SLC10A1)

Este bloque proporciona la fundamentación biológica de los mecanismos de transporte y regulación del receptor biliar hepático secuestrado por hepadnavirus.

### A. Regulación y Transbordo de Ácidos Biliares
*   **Referencia Canónica**:
    *   **Li Y, Zhou J, Li T (2022)**. *Regulation of the HBV Entry Receptor NTCP and its Potential in Hepatitis B Treatment.* Frontiers in Molecular Biosciences, 9:879817.  
    *DOI: [10.3389/fmolb.2022.879817](https://doi.org/10.3389/fmolb.2022.879817)* | *PMCID: [PMC9039015](https://pmc.ncbi.nlm.nih.gov/articles/PMC9039015/)*
*   **Fundamento Fisiológico**: Revisión exhaustiva sobre la biología del transportador de sodio-taurocolato SLC10A1 (NTCP). Detalla los mecanismos de regulación transcripcional (vía FXR/SHP, HNF-1α, HNF-4α y STAT5), la inhibición transmembrana por citoquinas pro-inflamatorias (IL-6, IL-1β) en respuesta a colestasis, y la ubiquitinación proteasómica que controla su abundancia en la superficie celular.

### B. Identificación como Receptor Viral de HBV
*   **Referencia Canónica**:
    *   **Yan H, Zhong G, Xu G, He W, Jing Z, Gao Z, et al. (2012)**. *Sodium Taurocholate Cotransporting Polypeptide Is a Functional Receptor for Human Hepatitis B and D Virus.* Elife, 1:e00049.  
    *DOI: [10.7554/eLife.00049](https://doi.org/10.7554/eLife.00049)*
*   **Fundamento Fisiológico**: El artículo histórico de descubrimiento que identificó de forma concluyente a la proteína NTCP como el receptor celular responsable de interactuar con el dominio preS1 de la glicoproteína grande de envoltura del virus de la Hepatitis B (HBV) y la Hepatitis D (HDV), mapeando los residuos críticos 157-165 (KGIVISLVL) requeridos para el acoplamiento.

### C. Bloqueo de Entrada y Myrcludex B
*   **Referencia Canónica**:
    *   **Volz T, Allweiss L, M'Barek MB, Warlich M, et al. (2013)**. *The Entry Inhibitor Myrcludex-B Efficiently Blocks Intrahepatic Virus Spreading in Humanized Mice Previously Infected with Hepatitis B Virus.* Journal of Hepatology, 58(5): 861-867.  
    *DOI: [10.1016/j.jhep.2012.12.008](https://doi.org/10.1016/j.jhep.2012.12.008)*
*   **Fundamento Fisiológico**: Valida *in vivo* la eficacia del lipopéptido sintético derivado de preS1 (Myrcludex B / Hepcludex) como un entry inhibitor de NTCP que compite físicamente con los viriones de HBV y HDV para prevenir la de novo infección de hepatocitos sanos.

---
*Fin del compendio de literatura científica de referencia. Documento registrado de forma canónica en los archivos de Guanes Health.*
