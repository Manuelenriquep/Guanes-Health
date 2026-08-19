# Especificación Técnica: Vector Viral Oncolítico Auto-Dirigido (vOnco-Logic-v1)
**Clasificación:** ALTAMENTE CONFIDENCIAL / GUANES HEALTH BIOLOGIC
**Versión:** 1.0 (Homeostasis nominal y rescate por inyección de dependencias)

---

### I. ARQUITECTURA CIBERNÉTICA DEL VECTOR

Este diseño representa la convergencia absoluta entre la virología molecular cuantitativa de frontera y la teoría cibernética de sistemas de información. Tratamos la infección viral y el rescate de la apoptosis como un proceso puramente determinista de enrutamiento y procesamiento de señales moleculares.

#### 1. El Puerto de Entrada (Port-Scan y Fusión Determinista)
Para asegurar que el vector viral no amenace el hardware de las células somáticas sanas, explotamos la firma metabólica del tumor como su propio puerto de acceso:
* **Mimetismo del Receptor (NRP-1)**: El virión ha sido pseudotipado con el complejo glicoproteico de envoltura del deltaretrovirus HTLV-1 (gp46/gp21). La glicoproteína gp46 expone el motivo pentapeptídico altamente conservado **KKPNR (aa. 90–94)**, el cual secuestra de forma competitiva al receptor celular **Neuropilina-1 (NRP-1)**, mimetizando a la citoquina VEGF165.
* **El Interruptor de GLUT1**: La unión a NRP-1 provoca un cambio estacional en la región de bisagra rica en prolina (PRR) de gp46, exponiendo un sitio de unión para **GLUT1**. Dado que la célula neoplásica sufre el **Efecto Warburg** y sobreexpresa de manera constitutiva GLUT1 (consumiendo de 10 a 100 veces más glucosa), la célula tumoral presenta una densidad de puertos GLUT1 extremadamente elevada, convirtiéndose en el único hospedador capaz de desencadenar el paso de fusión.
* **La Apertura de la Compuerta (gp21)**: Al enlazarse con GLUT1, se ejecuta la **isomerización del enlace disulfuro inter-subunitario** entre el motivo CXXC de gp46 (C225/C228) y el motivo CX6CC de gp21 (C401). Este reordenamiento disocia a gp46 y proyecta el péptido de fusión hidrofóbico de **gp21** directamente en la bicapa lipídica del tumor a pH neutro, formando un haz de seis hélices (6HB coiled-coil) que inyecta físicamente la cápside viral en el citoplasma celular.

#### 2. El Procesador Lógico Transcripcional (La AND-Gate de Seguridad)
Una vez inyectado, el cassette del genoma viral está gobernado por una compuerta lógica condicional estricta (*AND-gate*) basada en la activación de promotores sintéticos para evitar la transcripción fuera de diana:
* **Insumo de Entrada A (hTERT Mutado)**: Se utiliza como promotor del vector la secuencia reguladora de hTERT, la cual contiene las mutaciones clonales específicas del cáncer en las coordenadas **-124 G>A (C228T) y -146 G>A (C250T)**. Esto recluta con afinidad duplicada (2x) al factor de transcripción aberrante GABP presente solo en células inmortales.
* **Insumo de Entrada B (Elementos HRE)**: Secuencias en tándem HRE que exigen la presencia activa y nuclear del factor **HIF-1α**, estabilizado únicamente por la hipoxia severa y el descontrol logístico interno del tumor.
* *Solo cuando ambos insumos biológicos están activos en el sistema (hTERT+ AND HIF-1α+), la ARN polimerasa se acopla para transcribir el payload de rescate celular.*

#### 3. Firmware de Rescate: Reconexión del Veto FC-BIO-01
Cuando se valida el estado tumoral, el virus transcribe de forma masiva dos transgenes bioingenierizados para revertir el sabotaje oncológico:
1. **p53-WT-mut2 (El Auditor Inmune)**: Introduce un gen supresor p53 modificado en su extremo N-terminal. Esta mutación estérica **impide de forma absoluta el acoplamiento de la ubiquitina ligasa MDM2**. p53 ya no puede ser marcado para degradación por el tumor; se estabiliza, se transloca al núcleo y reactiva la transcripción de las proteínas de reparación genómica y muerte celular.
2. **Péptido BH3-only Sintético (El Desbloqueador de Canales)**: Produce una secuencia peptídica que actúa como mimético de BH3 de ultra-alta afinidad, penetrando en el bolsillo hidrofóbico de las proteínas sobreexpresadas **BCL-2 y BCL-xL (basal de x25)**. Al desplazar competitivamente estos "tapones moleculares", se **liberan físicamente los efectores Bax y Bak**.
* Bax y Bak se oligomerizan de inmediato, ejecutando la **Permeabilización de la Membrana Mitocondrial Externa (MOMP)**. El poro mitocondrial expulsa Citocromo c al citosol, ensamblando el apoptosoma y reactivando la cascada determinista de caspasas efectoras para el apagado ordenado de la célula (apoptosis).

#### 4. Liquidación del Ledger Energético y Efferocitosis (Apagado Limpio)
La inducción de la apoptosis mitocondrial quiebra inmediatamente el balance energético de la célula tumoral:
* El colapso del potencial de membrana mitocondrial anula la síntesis de ATP, desplomando su ledger energético de **10,000 unidades a <10 unidades relativas**.
* Sin energía para alimentar la bomba Na+/K+ ATPasa, el potencial de reposo de la membrana plasmática se despolariza por encima de los **-15 mV**.
* Esto ejecuta el veto fisiológico final de la placa base (**VETO FC-BIO-03**): se transloca de forma activa la **fosfatidilserina a la lámina externa de la membrana plasmática** (la señal \"Eat-Me\" de efferocitosis). Las células dendríticas fagocitan limpiamente la célula tumoral moribunda antes de que ocurra una necrosis desordenada que genere inflamación crónica o escape inmunológico.

---
*Compilado y sellado criptográficamente por el motor de inferencia Guanes Health.*
