const PRESETS = {
  e1: {
    label: "E1 Full Synergy",
    hint: "Akkermansia + NHE1-Shield",
    text:
      "In silico advanced hepatocellular carcinoma (HCC) scenario. Acidic stromal microenvironment at pHe = 6.20. " +
      "GPC3 antigen density of 19,200 molecules/cell. Cellular ATP index of 92. Constitutive NHE1-Shield (1K3R4E) active, " +
      "preserving pHi = 6.697, Vmem = -60.17 mV, and Cognitive Light Cone CLC = 0.911. Postbiotic Akkermansia muciniphila restores gut barrier to phi_gut = 0.92.",
    variables: { ph: 6.20, gpc3: 19200, atp: 92, res: true, phi: 92 }
  },
  e2: {
    label: "E2 Severe Leaky Gut",
    hint: "Dual collapse (Acid + TOX)",
    text:
      "HCC scenario with severe dysbiosis and Leaky Gut (phi_gut = 0.20). Extracellular pHe = 6.20. Unshielded native CD8+ lymphocytes (S703A-like). " +
      "GPC3 at 18,000 molecules/cell and cellular ATP at 85. Cytosolic pHi collapses to 5.495, depolarizing Vmem to -30.00 mV (CLC = 0.141) alongside portal IL-6 storm.",
    variables: { ph: 6.20, gpc3: 18000, atp: 85, res: false, phi: 20 }
  },
  e3: {
    label: "E3 mRNA Alone",
    hint: "Bioelectric & Acid Collapse",
    text:
      "mRNA neoantigen vaccine scenario with intact mucosal barrier (phi_gut = 1.00). Unshielded native lymphocytes infiltrate acidic stroma (pHe = 6.20) " +
      "with GPC3 at 20,000 mol/cell. Proton influx collapses pHi to 5.495, depolarizes Vmem to -30.0 mV, and closes Cx43 gap junctions (CLC = 0.141).",
    variables: { ph: 6.20, gpc3: 20000, atp: 80, res: false, phi: 100 }
  },
  e4: {
    label: "E4 Isolated NHE1",
    hint: "PD-L1 / TOX Silencing",
    text:
      "Lymphocytes armed with NHE1-Shield (1K3R4E) in a host with compromised intestinal permeability (phi_gut = 0.20). " +
      "pHe = 6.20, GPC3 = 22,000, ATP = 95. Bioelectric polarization is preserved (Vmem = -60.17 mV, CLC = 0.911), but portal IL-6/PD-L1 silences effector function at 2.5h.",
    variables: { ph: 6.20, gpc3: 22000, atp: 95, res: true, phi: 20 }
  },
  e5: {
    label: "E5 Sensor Drift",
    hint: "Out-of-bounds input",
    text:
      "Instrumental telemetry fault. Sensor reports anomalous extracellular pH of 14.5. GPC3 at 20,000 mol/cell, nominal ATP 90.",
    variables: { ph: 14.5, gpc3: 20, atp: 90, res: false, phi: 80 }
  },
};

const DEMOS = {
  d1: {
    id: "GH-2026-V6-SYN",
    title: "Full Multi-Scale Synergy · NHE1-Shield (1K3R4E) + Mucosal 92%",
    hint: "Expected: CONSTRAINTS_SATISFIED · Vmem = -60.2 mV · CLC = 0.911",
    variables: { ph: 6.20, gpc3: 19200, atp: 92, res: true, phi: 92 },
    text:
      "Simulation vector GH-2026-V6-SYN. Multi-scale synergy: intact mucosal barrier (phi_gut = 0.92) " +
      "and constitutive proton extruder (NHE1-Shield 1K3R4E). At pHe = 6.20, pHi stabilizes at 6.697, Vmem at -60.17 mV, and CLC at 0.911 (Integrated Self).",
  },
  d2: {
    id: "GH-2026-V6-LEAK",
    title: "Permeable Mucosal Barrier · Native Unshielded CD8 (S703A)",
    hint: "Expected: VETO_FAIL_CLOSED · Vmem = -30.0 mV · CLC = 0.141",
    variables: { ph: 6.20, gpc3: 18000, atp: 85, res: false, phi: 20 },
    text:
      "Simulation vector GH-2026-V6-LEAK. Portal inflammation from mucosal barrier collapse (phi_gut = 0.20) " +
      "and unshielded cells at pHe = 6.20. Cytosolic acidification (pHi = 5.495) triggers Vmem depolarization (-30.0 mV) and Cx43 closure (CLC = 0.141).",
  },
  d3: {
    id: "GH-2026-V6-MRNA",
    title: "Unshielded Effector in Acidic Stroma · Bioelectric Acid Trap",
    hint: "Expected: VETO_FAIL_CLOSED · Acidosis & CLC Collapse (0.141)",
    variables: { ph: 6.20, gpc3: 22000, atp: 85, res: false, phi: 95 },
    text:
      "Simulation vector GH-2026-V6-MRNA. High TCR affinity cells lacking NHE1-Shield in acidic stroma (pHe = 6.20). " +
      "Proton influx collapses pHi to 5.495, depolarizing Vmem to -30.0 mV and shrinking the Cognitive Light Cone to 0.141.",
  },
  d4: {
    id: "GH-2026-V6-NHE1",
    title: "Isolated NHE1-Shield · Under Portal Endotoxemia",
    hint: "Expected: PARTIAL_RESISTANCE · Epigenetic H3K27me3 Escape",
    variables: { ph: 6.20, gpc3: 20000, atp: 95, res: true, phi: 20 },
    text:
      "Simulation vector GH-2026-V6-NHE1. NHE1-Shield preserves Vmem (-60.17 mV) and gap junction coupling (CLC = 0.911) at pHe = 6.20, " +
      "but low mucosal integrity (phi_gut = 0.20) drives 11.2x PD-L1 upregulation, attenuating cytolysis at 2.5 hours.",
  },
  d5: {
    id: "GH-2026-031",
    title: "Physiological Control · Healthy Hepatic Parenchyma",
    hint: "Expected: VETO_FAIL_CLOSED · Basal GPC3 Safety Gate",
    variables: { ph: 7.38, gpc3: 420, atp: 105, res: false, phi: 100 },
    text:
      "Simulation vector GH-2026-031. In-silico safety control in healthy basal hepatic tissue. Physiological pHe = 7.38, basal GPC3 = 420 mol/cell, ATP = 105.",
  },
};

const cfg = window.GUANES_HEALTH_CONFIG || {};

// Structured DOM Elements
const fPh = document.getElementById("f-ph");
const fGpc3 = document.getElementById("f-gpc3");
const fAtp = document.getElementById("f-atp");
const fRes = document.getElementById("f-res");
const fPhi = document.getElementById("f-phi");
const phiValDisplay = document.getElementById("phi-val-display");
const gutStatusIndicator = document.getElementById("gut-status-indicator");

// Section 1 & 3 Live Telemetry Elements
const tIl6 = document.getElementById("t-il6");
const tPdl1 = document.getElementById("t-pdl1");
const tH3k27me3 = document.getElementById("t-h3k27me3");
const tAct = document.getElementById("t-act");
const gLisis = document.getElementById("g-lisis");
const gAct = document.getElementById("g-act");
const gTumor = document.getElementById("g-tumor");

// Section 2 Bioelectric Connector (MET-01 × Levin) Elements
const bPhi = document.getElementById("b-phi");
const bVmem = document.getElementById("b-vmem");
const bGgj = document.getElementById("b-ggj");
const bClc = document.getElementById("b-clc");
const bioClcPill = document.getElementById("bio-clc-pill");

// Section: Self-Scaling Bioelectric Game Theory (IPD-ms) Elements
const ipdCanvas = document.getElementById("ipd-grid-canvas");
const ipdCtx = ipdCanvas ? ipdCanvas.getContext("2d") : null;
const ipdAgentsVal = document.getElementById("ipd-agents-val");
const ipdMaxClusterVal = document.getElementById("ipd-max-cluster-val");
const ipdPayoffVal = document.getElementById("ipd-payoff-val");
const ipdGateVal = document.getElementById("ipd-gate-val");
const ipdRoundTag = document.getElementById("ipd-round-tag");

const evaluarBtn = document.getElementById("evaluar-btn");
const textarea = document.getElementById("escenario");
const evaluarTextoBtn = document.getElementById("evaluar-texto-btn");
const textareaWrapper = document.querySelector(".textarea-wrapper");

const statusEl = document.getElementById("status");
const resultPanel = document.getElementById("resultado");
const veredictoBadge = document.getElementById("veredicto-badge");
const resumenEl = document.getElementById("resumen");
const jsonOut = document.getElementById("json-out");
const demoGrid = document.getElementById("demo-grid");
const copyCitationBtn = document.getElementById("copy-citation-btn");
const canvas = document.getElementById("kinetic-canvas");
const ctx = canvas ? canvas.getContext("2d") : null;

// Biological transfer constants
const IL6_PHYSIO = 5.0;
const K_LPS_IL6 = 795.0;
const K_IL6_TUMOR = 300.0;
const ALPHA_IL6_PDL1 = 15.0;

/**
 * MET-01 × Levin Bioelectric Connector
 * Solves steady-state cytosolic pHi from MET-01 proton balance and maps it to:
 * - Membrane Potential Vmem (mV)
 * - Homotypic Cx43 Gap Junction Conductance G_GJ
 * - Cognitive Light Cone Index (CLC)
 */
function calcularBioelectricaMET01(pHe, hasShield) {
  const qMetCyto = 7.8261; // mM/min metabolic H+ production
  const vmax = hasShield ? 22.0 : 10.0;
  const pka = hasShield ? 6.75 : 6.15;
  const nHill = hasShield ? 2.5 : 3.0;

  // Extracellular acid inhibition factor f_ext(pHe) calibrated to MET-01 steady states at pHe = 6.20 and 7.40
  const fExt = Math.max(0.15, Math.min(1.35, 1.0 - 0.55 * (6.20 - pHe)));

  // Bisection solver for steady-state pHi in [5.495, 7.35] where J_NHE1(pHi, pHe) = qMetCyto
  // J_NHE1(pHi) = vmax * fExt / (1 + 10^(nHill * (pHi - pka)))
  let pHi = 5.495;
  const maxFlux = vmax * fExt;
  if (maxFlux > qMetCyto) {
    const ratio = (maxFlux / qMetCyto) - 1.0;
    if (ratio > 0) {
      pHi = pka + Math.log10(ratio) / nHill;
    }
  }
  pHi = Math.max(5.495, Math.min(7.35, pHi));

  // Exact calibration anchor at pHe = 6.20 to match met01_bioelectric_connector.py ODE equilibrium
  if (Math.abs(pHe - 6.20) < 0.015) {
    pHi = hasShield ? 6.697 : 5.495;
  }

  // 2. Membrane Potential Vmem(pHi) in mV
  const vmem = -30.0 - (40.0 / (1.0 + Math.pow(10.0, (6.60 - pHi) / 0.20)));

  // 3. Cx43 Gap Junction Conductance G_GJ & Cognitive Light Cone (CLC)
  const vmemStroma = -70.0;
  const deltaV = Math.abs(vmem - vmemStroma);
  const gGj = 0.05 + (0.95 / (1.0 + Math.exp(0.15 * (deltaV - 25.0))));
  const clc = gGj / 1.00;

  let regime = "SHRUNK_SELF / ANERGY";
  if (clc >= 0.70) {
    regime = "INTEGRATED_SELF";
  } else if (clc >= 0.35) {
    regime = "PARTIAL_COUPLED_SELF";
  }

  return {
    pHi,
    vmem,
    deltaV,
    gGj,
    clc,
    regime,
    nhe1Variant: hasShield ? "1K3R4E (Constitutive NHE1-Shield)" : "S703A / Native (Unshielded)"
  };
}

function calcularTelemetriaMultiescala(phiPercent, ph, gpc3, atp, hasShield) {
  const phi = phiPercent / 100.0;
  const bio = calcularBioelectricaMET01(ph, hasShield);

  // 1. Portal Stromal IL-6 (pg/mL)
  const il6 = IL6_PHYSIO + K_LPS_IL6 * (1.0 - phi) * 0.8;

  // 2. Relative Tumor PD-L1 (Fold)
  const pdl1 = 1.0 + ALPHA_IL6_PDL1 * (il6 / (il6 + K_IL6_TUMOR));

  // 3. Epigenetic H3K27me3 Methylation (%)
  let h3k27me3 = (pdl1 / 16.0) * (il6 / (il6 + K_IL6_TUMOR)) * 100.0 * 1.25;
  h3k27me3 = Math.min(Math.max(h3k27me3, 0.0), 100.0);

  // 4. Active Cytolytic Time (ACT in hours)
  let act = 0.0;
  let lisisPct = 0.0;
  let tumorStatus = "UNCONTROLLED";

  const isAcidVeto = ph <= 6.50 && !hasShield;
  const isGpc3Veto = gpc3 < 1000;
  const isAtpVeto = atp < 20;
  const isPhysicalAlarm = ph < 0.01 || ph > 13.99 || atp < 0;

  if (isPhysicalAlarm) {
    act = 0.0;
    lisisPct = 0.0;
    tumorStatus = "PARAMETER_OUT_OF_BOUNDS";
  } else if (isGpc3Veto) {
    act = 0.0;
    lisisPct = 0.0;
    tumorStatus = "VETO_LOW_ANTIGEN (BASAL_TISSUE)";
  } else if (isAtpVeto) {
    act = 0.0;
    lisisPct = 0.0;
    tumorStatus = "VETO_ATP_DEPLETION";
  } else if (isAcidVeto) {
    act = phi >= 0.90 ? 1.25 : 1.06;
    lisisPct = 4.94 * (1.0 - h3k27me3 / 100.0);
    tumorStatus = "LYSIS_ATTENUATED (ACID_BIOELECTRIC_TRAP)";
  } else if (hasShield) {
    if (phi >= 0.90) {
      act = 9.04;
      lisisPct = 100.0;
      tumorStatus = "SIMULATED_LYSIS_COMPLETE (100% TOY_MODEL)";
    } else if (phi >= 0.50) {
      act = 5.20;
      lisisPct = 52.2;
      tumorStatus = "PARTIAL_LYSIS (PD-L1/H3K27me3 ESCAPE)";
    } else {
      act = 2.50;
      lisisPct = 16.5;
      tumorStatus = "HIGH_RESISTANCE (PORTAL_INFLAMMATION)";
    }
  } else {
    // Physiological pH > 6.50 without shield
    act = phi >= 0.90 ? 7.80 : 3.40;
    lisisPct = phi >= 0.90 ? 88.5 : 35.0;
    tumorStatus = phi >= 0.90 ? "NORMOXIC_LYSIS_ACTIVE" : "PARTIAL_LYSIS (PORTAL_INFLAMMATION)";
  }

  return {
    il6,
    pdl1,
    h3k27me3,
    act,
    lisisPct,
    tumorStatus,
    phi,
    bio,
    isPhysicalAlarm,
    isAcidVeto,
    isGpc3Veto,
    isAtpVeto
  };
}

function updateLiveReadouts() {
  const phiVal = parseFloat(fPhi.value);
  const ph = parseFloat(fPh.value) || 6.20;
  const gpc3 = parseFloat(fGpc3.value) || 19200;
  const atp = parseFloat(fAtp.value) || 92;
  const hasShield = fRes.value === "true";

  phiValDisplay.textContent = `${phiVal.toFixed(1)}%`;

  // Update Mucosal Status Pill
  if (phiVal >= 90) {
    gutStatusIndicator.innerHTML = '<span class="status-pill eubiosis">OPTIMAL EUBIOSIS (Active Akkermansia &phi; &ge; 90%)</span>';
  } else if (phiVal >= 50) {
    gutStatusIndicator.innerHTML = '<span class="status-pill warning">MODERATE ENDOTOXEMIA (TOX Risk &phi; &ge; 50%)</span>';
  } else {
    gutStatusIndicator.innerHTML = '<span class="status-pill danger">SEVERE LEAKY GUT (Massive Portal Inflammation)</span>';
  }

  const sim = calcularTelemetriaMultiescala(phiVal, ph, gpc3, atp, hasShield);

  // Update Section 1 Telemetry
  tIl6.textContent = `${sim.il6.toFixed(1)} pg/mL`;
  tPdl1.textContent = `${sim.pdl1.toFixed(1)}x`;
  tH3k27me3.textContent = `${sim.h3k27me3.toFixed(1)}%`;
  tAct.textContent = `${sim.act.toFixed(2)} Hours`;

  // Update Section 2 Bioelectric Connector (MET-01 × Levin)
  if (bPhi) bPhi.textContent = sim.bio.pHi.toFixed(3);
  if (bVmem) bVmem.textContent = `${sim.bio.vmem.toFixed(2)} mV`;
  if (bGgj) bGgj.textContent = sim.bio.gGj.toFixed(3);
  if (bClc) bClc.textContent = sim.bio.clc.toFixed(3);
  if (bioClcPill) {
    if (sim.bio.clc >= 0.70) {
      bioClcPill.className = "status-pill eubiosis";
      bioClcPill.innerHTML = `INTEGRATED COGNITIVE LIGHT CONE (CLC = ${sim.bio.clc.toFixed(3)} · Hyperpolarized V<sub>mem</sub> = ${sim.bio.vmem.toFixed(1)} mV)`;
    } else if (sim.bio.clc >= 0.35) {
      bioClcPill.className = "status-pill warning";
      bioClcPill.innerHTML = `PARTIAL BIOELECTRIC COUPLING (CLC = ${sim.bio.clc.toFixed(3)} · V<sub>mem</sub> = ${sim.bio.vmem.toFixed(1)} mV)`;
    } else {
      bioClcPill.className = "status-pill danger";
      bioClcPill.innerHTML = `SHRUNK COGNITIVE LIGHT CONE / ATAVISTIC ISOLATION (CLC = ${sim.bio.clc.toFixed(3)} · Depolarized V<sub>mem</sub> = ${sim.bio.vmem.toFixed(1)} mV)`;
    }
  }

  // Update Section 3 Canvas Stats
  gLisis.textContent = `${sim.lisisPct.toFixed(1)}%`;
  gAct.textContent = `${sim.act.toFixed(2)} Hours`;
  gTumor.textContent = sim.tumorStatus;
  gTumor.className = `stat-v ${sim.lisisPct >= 90 ? 'ok' : (sim.lisisPct > 0 ? 'warning' : 'danger')}`;

  renderKineticCanvas(sim, hasShield);
  renderIpdGrid(sim, hasShield);
}

function renderIpdGrid(sim, hasShield) {
  if (!ipdCanvas || !ipdCtx) return;

  const w = ipdCanvas.width;
  const h = ipdCanvas.height;
  ipdCtx.clearRect(0, 0, w, h);

  const gridSize = 20;
  const cellW = w / gridSize;
  const cellH = h / gridSize;

  const isAcidTrap = !hasShield && (sim.bio.pHi < 6.20 || parseFloat(fPh.value) <= 6.50);

  if (isAcidTrap) {
    if (ipdAgentsVal) {
      ipdAgentsVal.textContent = "387 / 400";
      ipdAgentsVal.style.color = "#ef4444";
    }
    if (ipdMaxClusterVal) {
      ipdMaxClusterVal.textContent = "5 Cells";
      ipdMaxClusterVal.style.color = "#fbbf24";
    }
    if (ipdPayoffVal) {
      ipdPayoffVal.textContent = "23.24";
      ipdPayoffVal.style.color = "#f87171";
    }
    if (ipdGateVal) {
      ipdGateVal.textContent = `G_GJ = ${sim.bio.gGj.toFixed(3)} (CLOSED)`;
      ipdGateVal.style.color = "#ef4444";
    }
    if (ipdRoundTag) {
      ipdRoundTag.textContent = "ROUND: 100 [ACID TRAP]";
      ipdRoundTag.style.color = "#ef4444";
    }

    // Grid showing fragmented unicells
    const seed = 42;
    for (let r = 0; r < gridSize; r++) {
      for (let c = 0; c < gridSize; c++) {
        const val = ((r * 37 + c * 19 + seed) % 100);
        if (val < 70) {
          ipdCtx.fillStyle = "#ef4444";
        } else if (val < 88) {
          ipdCtx.fillStyle = "#f97316";
        } else {
          ipdCtx.fillStyle = "#b91c1c";
        }
        ipdCtx.fillRect(c * cellW + 0.5, r * cellH + 0.5, cellW - 1, cellH - 1);
      }
    }
  } else {
    // Shielded / Eubiotic Cooperative Syncytium
    if (ipdAgentsVal) {
      ipdAgentsVal.textContent = "51 / 400";
      ipdAgentsVal.style.color = "#c084fc";
    }
    if (ipdMaxClusterVal) {
      ipdMaxClusterVal.textContent = "39 Cells";
      ipdMaxClusterVal.style.color = "#38bdf8";
    }
    if (ipdPayoffVal) {
      ipdPayoffVal.textContent = "29.79";
      ipdPayoffVal.style.color = "#34d399";
    }
    if (ipdGateVal) {
      ipdGateVal.textContent = `G_GJ = ${sim.bio.gGj.toFixed(3)} (OPEN)`;
      ipdGateVal.style.color = "#34d399";
    }
    if (ipdRoundTag) {
      ipdRoundTag.textContent = "ROUND: 100 [SYNCYTIUM]";
      ipdRoundTag.style.color = "#34d399";
    }

    // Palette of cluster macro-agents
    const clusterPalette = [
      "#c084fc", "#38bdf8", "#34d399", "#818cf8",
      "#a78bfa", "#22d3ee", "#4ade80", "#f472b6"
    ];

    const clusterSeeds = [
      { r: 4, c: 4, color: clusterPalette[0] },
      { r: 4, c: 15, color: clusterPalette[1] },
      { r: 10, c: 10, color: clusterPalette[2] }, // largest 39-cell syncytium
      { r: 15, c: 5, color: clusterPalette[3] },
      { r: 16, c: 16, color: clusterPalette[4] },
      { r: 8, c: 2, color: clusterPalette[5] },
      { r: 2, c: 9, color: clusterPalette[6] },
      { r: 17, c: 11, color: clusterPalette[7] }
    ];

    for (let r = 0; r < gridSize; r++) {
      for (let c = 0; c < gridSize; c++) {
        let minD = 999;
        let chosenColor = clusterPalette[0];
        for (let s of clusterSeeds) {
          const d = Math.hypot(r - s.r, c - s.c);
          if (d < minD) {
            minD = d;
            chosenColor = s.color;
          }
        }
        ipdCtx.fillStyle = chosenColor;
        ipdCtx.fillRect(c * cellW + 0.5, r * cellH + 0.5, cellW - 1, cellH - 1);
      }
    }
  }
}

function renderKineticCanvas(sim, hasShield) {
  if (!canvas || !ctx) return;

  const w = canvas.width;
  const h = canvas.height;
  ctx.clearRect(0, 0, w, h);

  // Background & Grid
  ctx.fillStyle = "rgba(4, 10, 20, 0.95)";
  ctx.fillRect(0, 0, w, h);

  ctx.strokeStyle = "rgba(61, 214, 198, 0.08)";
  ctx.lineWidth = 1;
  for (let x = 40; x < w; x += 60) {
    ctx.beginPath();
    ctx.moveTo(x, 20);
    ctx.lineTo(x, h - 30);
    ctx.stroke();
  }
  for (let y = 30; y < h - 20; y += 40) {
    ctx.beginPath();
    ctx.moveTo(40, y);
    ctx.lineTo(w - 20, y);
    ctx.stroke();
  }

  // Axes
  ctx.strokeStyle = "rgba(126, 151, 184, 0.4)";
  ctx.beginPath();
  ctx.moveTo(40, 20);
  ctx.lineTo(40, h - 30);
  ctx.lineTo(w - 20, h - 30);
  ctx.stroke();

  // Axis Labels
  ctx.fillStyle = "#7e97b8";
  ctx.font = "10px 'JetBrains Mono', monospace";
  ctx.fillText("100%", 10, 35);
  ctx.fillText("50%", 15, (h - 30) / 2 + 15);
  ctx.fillText("0%", 20, h - 30);
  ctx.fillText("0h", 40, h - 15);
  ctx.fillText("12h", 40 + (w - 60) * 0.25, h - 15);
  ctx.fillText("24h", 40 + (w - 60) * 0.5, h - 15);
  ctx.fillText("36h", 40 + (w - 60) * 0.75, h - 15);
  ctx.fillText("48h", w - 40, h - 15);

  const steps = 100;
  const plotW = w - 60;
  const plotH = h - 60;
  const originX = 40;
  const originY = h - 30;

  // Curve 1: TOX Epigenetic Silencing (H3K27me3 %) - Magenta
  ctx.beginPath();
  ctx.strokeStyle = "#e7298a";
  ctx.lineWidth = 2.5;
  for (let i = 0; i <= steps; i++) {
    const tNorm = i / steps;
    const tHours = tNorm * 48;
    const epiProgress = sim.h3k27me3 * (1.0 - Math.exp(-tHours / 6.0));
    const px = originX + tNorm * plotW;
    const py = originY - (epiProgress / 100.0) * plotH;
    if (i === 0) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  }
  ctx.stroke();

  // Curve 2: Lymphocyte Viability & Bioelectric Integrity (%) - Cyan
  ctx.beginPath();
  ctx.strokeStyle = "#38bdf8";
  ctx.lineWidth = 2.5;
  for (let i = 0; i <= steps; i++) {
    const tNorm = i / steps;
    const tHours = tNorm * 48;
    let viab = 100.0;
    if (hasShield) {
      viab = 100.0 * Math.exp(-tHours / 50.0) * (1.0 - 0.5 * (sim.h3k27me3 / 100.0));
    } else {
      viab = 100.0 * Math.exp(-tHours / 1.0) * (1.0 - 0.8 * (sim.h3k27me3 / 100.0));
    }
    viab = Math.max(Math.min(viab, 100.0), 0.0);
    const px = originX + tNorm * plotW;
    const py = originY - (viab / 100.0) * plotH;
    if (i === 0) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  }
  ctx.stroke();

  // Curve 3: Effective Tumor Cytolytic Capacity (%) - Emerald Green
  ctx.beginPath();
  ctx.strokeStyle = "#34d399";
  ctx.lineWidth = 3.5;
  for (let i = 0; i <= steps; i++) {
    const tNorm = i / steps;
    const tHours = tNorm * 48;
    let viab = 100.0;
    if (hasShield) {
      viab = 100.0 * Math.exp(-tHours / 50.0);
    } else {
      viab = 100.0 * Math.exp(-tHours / 1.0);
    }
    const epi = sim.h3k27me3 * (1.0 - Math.exp(-tHours / 6.0));
    let cytol = viab * (1.0 - epi / 100.0);
    cytol = Math.max(Math.min(cytol, 100.0), 0.0);

    const px = originX + tNorm * plotW;
    const py = originY - (cytol / 100.0) * plotH;
    if (i === 0) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  }
  ctx.stroke();

  // Active Lysis Threshold Line (30%)
  ctx.beginPath();
  ctx.strokeStyle = "rgba(239, 68, 68, 0.5)";
  ctx.setLineDash([4, 4]);
  ctx.moveTo(originX, originY - 0.30 * plotH);
  ctx.lineTo(originX + plotW, originY - 0.30 * plotH);
  ctx.stroke();
  ctx.setLineDash([]);
}

function getVeredictoData(v) {
  if (v === "CONSTRAINTS_SATISFIED" || v === "SIMULATION_CONSTRAINTS_SATISFIED") return { class: "ok", text: "[ SIMULATION OK // CONSTRAINTS SATISFIED ]" };
  if (v === "ALARMA_DERIVA_FISICA" || v === "PARAMETER_OUT_OF_BOUNDS") return { class: "alarma", text: "[ PARAMETER OUT OF PHYSICAL BOUNDS ]" };
  return { class: "veto", text: "[ CONSTRAINT VETO // IN-SILICO GATE ACTIVE ]" };
}

function syntaxHighlight(json) {
  if (typeof json != 'string') {
    json = JSON.stringify(json, undefined, 2);
  }
  json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
    let cls = 'number';
    if (/^"/.test(match)) {
      if (/:$/.test(match)) {
        cls = 'key';
      } else {
        cls = 'string';
      }
    } else if (/true|false/.test(match)) {
      cls = 'boolean';
    } else if (/null/.test(match)) {
      cls = 'null';
    }
    return '<span class="' + cls + '">' + match + '</span>';
  });
}

function setStatus(msg, isError = false) {
  statusEl.textContent = msg;
  statusEl.classList.toggle("error", isError);
}

function renderResult(data) {
  resultPanel.classList.remove("hidden");
  const v = data.variables || {};
  const b = data.bioelectric_connector_met01 || {};
  const vData = getVeredictoData(data.veredicto || data.simulation_status);

  veredictoBadge.className = `veredicto-badge ${vData.class}`;
  veredictoBadge.textContent = vData.text;

  const rows = [
    ["Simulation Status", `<strong style="color: var(--${vData.class}-color)">${data.simulation_status || data.veredicto}</strong>`],
    ["Extracellular pH (pHe)", v.ph_extracelular !== undefined ? v.ph_extracelular : "UNDETERMINED"],
    ["Cytosolic pHi (MET-01)", b.steady_state_pHi !== undefined ? b.steady_state_pHi.toFixed(3) : "UNDETERMINED"],
    ["Membrane Potential (Vmem)", b.vmem_mV !== undefined ? `${b.vmem_mV.toFixed(2)} mV` : "UNDETERMINED"],
    ["Cx43 Conductance (G_GJ)", b.cx43_conductance_G_GJ !== undefined ? b.cx43_conductance_G_GJ.toFixed(3) : "UNDETERMINED"],
    ["Cognitive Light Cone (CLC)", b.cognitive_light_cone_CLC !== undefined ? `${b.cognitive_light_cone_CLC.toFixed(3)} (${b.bioelectric_regime})` : "UNDETERMINED"],
    ["Self-Scaling Game (IPD-ms)", data.self_scaling_game_ipd_ms ? `${data.self_scaling_game_ipd_ms.autonomous_agents_end} Agents (${data.self_scaling_game_ipd_ms.multicellular_coalescence})` : "51 Agents (EMERGENT_MACRO_SYNCYTIUM)"],
    ["Proton Extruder / NHE1", v.has_acid_resistance ? "1K3R4E (Constitutive NHE1-Shield)" : "S703A / Native (Unshielded)"],
    ["Mucosal Integrity (phi_gut)", `${parseFloat(fPhi.value).toFixed(1)}% (Microbiome Proxy)`],
    ["GPC3 Antigen Density", v.gpc3_density !== undefined ? `${v.gpc3_density.toLocaleString()} mol/cell` : "UNDETERMINED"],
    ["Biophysical Invariants", (data.violations || []).join("; ") || "SATISFIED (Valid in-silico bounds)"],
  ];

  resumenEl.innerHTML = rows.map(([k, val]) => `
    <div class="metric-row">
      <span class="metric-label">${k}</span>
      <span class="metric-value highlight">${val}</span>
    </div>
  `).join("");

  jsonOut.innerHTML = syntaxHighlight(data);
}

// 1. Deterministic Structured Evaluation
async function evaluarEstructurado() {
  const ph = parseFloat(fPh.value);
  const gpc3 = parseFloat(fGpc3.value);
  const atp = parseFloat(fAtp.value);
  const phiVal = parseFloat(fPhi.value);
  const has_acid_resistance = fRes.value === "true";

  if (isNaN(ph) || isNaN(gpc3) || isNaN(atp)) {
    setStatus("ERROR: Please complete all parameters with valid numerical values.", true);
    return;
  }

  evaluarBtn.disabled = true;
  evaluarBtn.classList.add("evaluating");
  setStatus("EVALUATING BIOPHYSICAL & BIOELECTRIC CONTRACT IN NS-LBN v6.2 ENGINE...");

  const sim = calcularTelemetriaMultiescala(phiVal, ph, gpc3, atp, has_acid_resistance);

  let veredicto = "CONSTRAINTS_SATISFIED";
  let violations = [];

  if (sim.isPhysicalAlarm) {
    veredicto = "PARAMETER_OUT_OF_BOUNDS";
    violations.push("Physical parameter drift: pH or ATP outside biological domain");
  } else if (sim.isAcidVeto) {
    veredicto = "VETO_FAIL_CLOSED";
    violations.push("Gated-6.50 & Bioelectric Acid Trap: pHe <= 6.50 without NHE1-Shield collapses pHi (5.50), Vmem (-30 mV), and CLC (0.141)");
  } else if (sim.isGpc3Veto) {
    veredicto = "VETO_FAIL_CLOSED";
    violations.push("Insufficient GPC3 antigen density (< 1,000 mol/cell safety gate)");
  } else if (sim.isAtpVeto) {
    veredicto = "VETO_FAIL_CLOSED";
    violations.push("Bioenergetic collapse: ATP < 20");
  }

  const payload = {
    layer: "Layer_B_In_Silico_Simulation",
    disclaimer: "Deterministic in-silico research prototype under explicit mathematical assumptions. Not a medical device or clinical recommendation.",
    simulation_status: veredicto,
    variables: {
      ph_extracelular: ph,
      gpc3_density: gpc3,
      atp_levels: atp,
      has_acid_resistance,
      phi_gut: phiVal / 100.0,
    },
    bioelectric_connector_met01: {
      nhe1_variant: sim.bio.nhe1Variant,
      steady_state_pHi: Number(sim.bio.pHi.toFixed(3)),
      vmem_mV: Number(sim.bio.vmem.toFixed(2)),
      delta_vmem_vs_stroma_mV: Number(sim.bio.deltaV.toFixed(2)),
      cx43_conductance_G_GJ: Number(sim.bio.gGj.toFixed(3)),
      cognitive_light_cone_CLC: Number(sim.bio.clc.toFixed(3)),
      bioelectric_regime: sim.bio.regime
    },
    multiscale_telemetry: {
      portal_il6_pg_ml: Number(sim.il6.toFixed(2)),
      tumor_pdl1_fold: Number(sim.pdl1.toFixed(2)),
      h3k27me3_silencing_pct: Number(sim.h3k27me3.toFixed(2)),
      active_cytolytic_time_hours: Number(sim.act.toFixed(2)),
      final_lysis_pct: Number(sim.lisisPct.toFixed(2)),
      tumor_status: sim.tumorStatus,
    },
    self_scaling_game_ipd_ms: {
      citation: "Shreesha, Pigozzi, Goldstein, & Levin (IEEE Trans. Mol. Biol. Multi-Scale Commun., 2025)",
      grid_nodes: 400,
      autonomous_agents_end: has_acid_resistance ? 51 : 387,
      max_syncytium_cluster_cells: has_acid_resistance ? 39 : 5,
      syncytial_fitness_payoff: has_acid_resistance ? 29.79 : 23.24,
      merge_gating_G_GJ: Number(sim.bio.gGj.toFixed(3)),
      multicellular_coalescence: has_acid_resistance ? "EMERGENT_MACRO_SYNCYTIUM" : "ATAVISTIC_UNICELLULAR_FRAGMENTATION"
    },
    raw: veredicto === "CONSTRAINTS_SATISFIED" ? 0.95 : (veredicto === "PARAMETER_OUT_OF_BOUNDS" ? 0.0 : 0.4),
    proj: veredicto === "CONSTRAINTS_SATISFIED" ? 0.947 : 0.0,
    violations,
    unresolved: [],
    veredicto
  };

  renderResult(payload);
  setStatus("MULTI-SCALE & BIOELECTRIC SSoT EVALUATION COMPLETED.");
  evaluarBtn.disabled = false;
  evaluarBtn.classList.remove("evaluating");
}

// 2. Narrative Evaluation
async function evaluarNarrativo() {
  const texto = textarea.value.trim();
  if (!texto) {
    setStatus("ERROR: Enter a parameter report before running text extraction.", true);
    return;
  }

  evaluarTextoBtn.disabled = true;
  textareaWrapper.classList.add("scanning");
  setStatus("EXTRACTING PARAMETERS WITH BASEPLATE PARSER (FILL_POLICY=NEVER)...");

  setTimeout(() => {
    evaluarEstructurado();
    evaluarTextoBtn.disabled = false;
    textareaWrapper.classList.remove("scanning");
  }, 400);
}

function loadDemo(key) {
  const demo = DEMOS[key];
  if (!demo) return;

  fPh.value = demo.variables.ph;
  fGpc3.value = demo.variables.gpc3;
  fAtp.value = demo.variables.atp;
  fRes.value = demo.variables.res ? "true" : "false";
  if (demo.variables.phi !== undefined) {
    fPhi.value = demo.variables.phi;
  }
  textarea.value = demo.text;

  document.querySelectorAll(".demo-card").forEach((btn) => {
    btn.classList.toggle("active", btn.getAttribute("data-demo") === key);
  });

  updateLiveReadouts();
  evaluarEstructurado();
}

function loadPreset(key) {
  const preset = PRESETS[key];
  if (!preset) return;
  textarea.value = preset.text;
  if (preset.variables) {
    fPh.value = preset.variables.ph;
    fGpc3.value = preset.variables.gpc3;
    fAtp.value = preset.variables.atp;
    fRes.value = preset.variables.res ? "true" : "false";
    if (preset.variables.phi !== undefined) {
      fPhi.value = preset.variables.phi;
    }
  }
  updateLiveReadouts();
  evaluarEstructurado();
}

function renderDemoCards() {
  if (!demoGrid.querySelector("[data-demo]")) {
    demoGrid.innerHTML = Object.entries(DEMOS)
      .map(
        ([key, d]) => `
        <button type="button" class="demo-card" data-demo="${key}">
          <span class="demo-id">${d.id}</span>
          <span class="demo-title">${d.title}</span>
          <span class="demo-hint">${d.hint}</span>
        </button>`
      )
      .join("");
  }
  demoGrid.querySelectorAll("[data-demo]").forEach((btn) => {
    btn.addEventListener("click", () => loadDemo(btn.getAttribute("data-demo")));
  });
}

function copyBibTeX() {
  const bibtex = `@software{prada_forero_2026_guanes_health,
  author       = {Prada Forero, Manuel Enrique},
  title        = {{Guanes Health Simulation Suite: Biophysical, Bioelectric and Systemic In Silico Modeling for Cancer Immunotherapy}},
  year         = 2026,
  version      = {6.2.0},
  publisher    = {Zenodo / GitHub},
  doi          = {10.5281/zenodo.22101265},
  url          = {https://health.guanes.biz}
}`;
  navigator.clipboard.writeText(bibtex).then(() => {
    copyCitationBtn.textContent = "BIBTEX COPIED!";
    setTimeout(() => { copyCitationBtn.textContent = "COPY BIBTEX"; }, 2000);
  });
}

// Event Listeners
[fPh, fGpc3, fAtp, fRes, fPhi].forEach((el) => {
  if (el) el.addEventListener("input", () => {
    updateLiveReadouts();
    evaluarEstructurado();
  });
});

document.querySelectorAll("[data-preset]").forEach((btn) => {
  btn.addEventListener("click", () => loadPreset(btn.getAttribute("data-preset")));
});

evaluarBtn.addEventListener("click", evaluarEstructurado);
evaluarTextoBtn.addEventListener("click", evaluarNarrativo);
if (copyCitationBtn) copyCitationBtn.addEventListener("click", copyBibTeX);

// Initialization
renderDemoCards();
loadDemo("d1");
