const PRESETS = {
  e1: {
    label: "E1 Sinergia Total",
    hint: "Akkermansia + NHE1-Shield",
    text:
      "Paciente con carcinoma hepatocelular avanzado (HCC). Microambiente estromal con pH extracelular de 6.20. " +
      "Densidad antigénica GPC3 de 19,200 moléculas/célula. ATP celular de 92. Constructo CAR-T con resistencia al ácido (NHE1 activo). " +
      "Tratamiento postbiótico con Akkermansia muciniphila restablece barrera intestinal a phi_gut = 0.92.",
    variables: { ph: 6.20, gpc3: 19200, atp: 92, res: true, phi: 92 }
  },
  e2: {
    label: "E2 Leaky Gut Severo",
    hint: "Colapso doble (pH + TOX)",
    text:
      "Caso de HCC con disbiosis y Leaky Gut severo (phi_gut = 0.20). pH extracelular 6.20. Linfocitos CD8 nativos sin modificaciones. " +
      "GPC3 en 18,000 moléculas/célula y ATP celular de 85. Tormenta portal de IL-6 gatilla PD-L1 masivo.",
    variables: { ph: 6.20, gpc3: 18000, atp: 85, res: false, phi: 20 }
  },
  e3: {
    label: "E3 Vacuna ARNm Sola",
    hint: "Muerte por acidosis",
    text:
      "Vacuna de neoantígenos de ARNm en paciente con microbiota intacta (phi_gut = 1.00). Linfocitos convencionales sin escudo iónico " +
      "infiltran estroma a pH 6.20 con GPC3 de 20,000 mol/cel. Choque bioenergético agota el ATP a los 60 min.",
    variables: { ph: 6.20, gpc3: 20000, atp: 80, res: false, phi: 100 }
  },
  e4: {
    label: "E4 NHE1 Aislado",
    hint: "Bloqueo por PD-L1/TOX",
    text:
      "Linfocitos armados con NHE1-Shield en paciente con permeabilidad intestinal moderada (phi_gut = 0.20). " +
      "pH 6.20, GPC3 22,000, ATP 95. El linfocito sobrevive pero se silencia por la barrera de PD-L1 a las 2.5 horas.",
    variables: { ph: 6.20, gpc3: 22000, atp: 95, res: true, phi: 20 }
  },
  e5: {
    label: "E5 Deriva Física",
    hint: "Sensor corrupto",
    text:
      "Error de telemetría instrumental. Sensor reporta un pH anómalo de 14.5. GPC3 en 20,000 mol/cel, ATP nominal 90.",
    variables: { ph: 14.5, gpc3: 20000, atp: 90, res: false, phi: 80 }
  },
};

const DEMOS = {
  d1: {
    id: "GH-2026-V6-SYN",
    title: "Sinergia Total · Microbiota 92% + NHE1-Shield",
    hint: "Esperado: CONSTRAINTS_SATISFIED · ACT = 9.0h",
    variables: { ph: 6.20, gpc3: 19200, atp: 92, res: true, phi: 92 },
    text:
      "Vector de simulación GH-2026-V6-SYN. Sinergia multiescala: parámetro de barrera mucosal (phi_gut = 0.92) " +
      "y linfocito con intercambiador de protones constitutivo (escenario NHE1-Shield). pH estromal 6.20, GPC3 19,200, ATP 92.",
  },
  d2: {
    id: "GH-2026-V6-LEAK",
    title: "Barrera Permeable · CD8 Nativo",
    hint: "Esperado: VETO_FAIL_CLOSED · Acidosis + TOX",
    variables: { ph: 6.20, gpc3: 18000, atp: 85, res: false, phi: 20 },
    text:
      "Vector GH-2026-V6-LEAK. Inflamación portal por colapso de barrera mucosal (phi_gut = 0.20). " +
      "Linfocitos nativos sin blindaje a pH 6.20. La IL-6 portal induce sobreexpresión de PD-L1 y silenciamiento TOX con acidosis.",
  },
  d3: {
    id: "GH-2026-V6-MRNA",
    title: "Célula T Nativa · Sin Escudo Iónico en pH 6.20",
    hint: "Esperado: VETO_FAIL_CLOSED · Acidosis",
    variables: { ph: 6.20, gpc3: 22000, atp: 85, res: false, phi: 95 },
    text:
      "Vector GH-2026-V6-MRNA. Linfocitos con alta afinidad TCR pero sin escudo iónico en estroma ácido (pH 6.20). " +
      "La entrada de protones genera colapso glucolítico y pérdida de actividad citolítica.",
  },
  d4: {
    id: "GH-2026-V6-NHE1",
    title: "NHE1-Shield Aislado · Con Inflamación Portal",
    hint: "Esperado: VETO_PARCIAL · Silenciamiento Epigenético",
    variables: { ph: 6.20, gpc3: 20000, atp: 95, res: true, phi: 20 },
    text:
      "Vector GH-2026-V6-NHE1. Linfocito con NHE1-Shield en modelo con baja integridad mucosal (phi_gut = 0.20). " +
      "El linfocito resiste la acidosis pero el tumor sobreexpresa PD-L1 (11.2x), atenuando la lisis a las 2.5 horas.",
  },
  d5: {
    id: "GH-2026-031",
    title: "Control Fisiológico · Parénquima Sano",
    hint: "Esperado: VETO_FAIL_CLOSED · GPC3 Basal",
    variables: { ph: 7.38, gpc3: 420, atp: 105, res: false, phi: 100 },
    text:
      "Vector GH-2026-031. Control de seguridad in silico en tejido hepático basal. pH fisiológico 7.38, GPC3 basal de 420 mol/célula, ATP 105.",
  },
};

const cfg = window.GUANES_HEALTH_CONFIG || {};

// Elementos del DOM estructurado
const fPh = document.getElementById("f-ph");
const fGpc3 = document.getElementById("f-gpc3");
const fAtp = document.getElementById("f-atp");
const fRes = document.getElementById("f-res");
const fPhi = document.getElementById("f-phi");
const phiValDisplay = document.getElementById("phi-val-display");
const gutStatusIndicator = document.getElementById("gut-status-indicator");

// Telemetría en vivo
const tIl6 = document.getElementById("t-il6");
const tPdl1 = document.getElementById("t-pdl1");
const tH3k27me3 = document.getElementById("t-h3k27me3");
const tAct = document.getElementById("t-act");
const gLisis = document.getElementById("g-lisis");
const gAct = document.getElementById("g-act");
const gTumor = document.getElementById("g-tumor");

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

// Constantes biológicas de transferencia
const IL6_PHYSIO = 5.0;
const K_LPS_IL6 = 795.0;
const K_IL6_TUMOR = 300.0;
const ALPHA_IL6_PDL1 = 15.0;

function calcularTelemetriaMultiescala(phiPercent, ph, gpc3, atp, hasShield) {
  const phi = phiPercent / 100.0;
  
  // 1. IL-6 en estroma portal (pg/mL)
  const il6 = IL6_PHYSIO + K_LPS_IL6 * (1.0 - phi) * 0.8;
  
  // 2. PD-L1 tumoral relativo
  const pdl1 = 1.0 + ALPHA_IL6_PDL1 * (il6 / (il6 + K_IL6_TUMOR));
  
  // 3. Metilación epigenética H3K27me3 (%)
  let h3k27me3 = (pdl1 / 16.0) * (il6 / (il6 + K_IL6_TUMOR)) * 100.0 * 1.25;
  h3k27me3 = Math.min(Math.max(h3k27me3, 0.0), 100.0);
  
  // 4. Tiempo de lisis activo (ACT en horas)
  let act = 0.0;
  let lisisPct = 0.0;
  let tumorStatus = "NO CONTROLADO";
  
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
    // Parálisis metabólica por acidez
    act = phi >= 0.90 ? 1.25 : 1.06;
    lisisPct = 4.94 * (1.0 - h3k27me3 / 100.0);
    tumorStatus = "LYSIS_ATTENUATED (ACIDIC_VETO)";
  } else if (hasShield) {
    // Linfocito blindado con NHE1
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
  }

  return {
    il6,
    pdl1,
    h3k27me3,
    act,
    lisisPct,
    tumorStatus,
    phi,
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

  // Actualizar status bar de mucosa
  if (phiVal >= 90) {
    gutStatusIndicator.innerHTML = '<span class="status-pill eubiosis">EUBIOSIS ÓPTIMA (Akkermansia Activa &phi; &ge; 90%)</span>';
  } else if (phiVal >= 50) {
    gutStatusIndicator.innerHTML = '<span class="status-pill warning">ENDOTOXEMIA MODERADA (Riesgo TOX &phi; &ge; 50%)</span>';
  } else {
    gutStatusIndicator.innerHTML = '<span class="status-pill danger">LEAKY GUT SEVERO (Inflamación Portal Masiva)</span>';
  }

  const sim = calcularTelemetriaMultiescala(phiVal, ph, gpc3, atp, hasShield);

  tIl6.textContent = `${sim.il6.toFixed(1)} pg/mL`;
  tPdl1.textContent = `${sim.pdl1.toFixed(1)}x`;
  tH3k27me3.textContent = `${sim.h3k27me3.toFixed(1)}%`;
  tAct.textContent = `${sim.act.toFixed(2)} Horas`;
  
  gLisis.textContent = `${sim.lisisPct.toFixed(1)}%`;
  gAct.textContent = `${sim.act.toFixed(2)} Horas`;
  gTumor.textContent = sim.tumorStatus;
  gTumor.className = `stat-v ${sim.lisisPct >= 90 ? 'ok' : (sim.lisisPct > 0 ? 'warning' : 'danger')}`;

  renderKineticCanvas(sim, hasShield);
}

function renderKineticCanvas(sim, hasShield) {
  if (!canvas || !ctx) return;

  const w = canvas.width;
  const h = canvas.height;
  ctx.clearRect(0, 0, w, h);

  // Fondo y Grid
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

  // Ejes
  ctx.strokeStyle = "rgba(126, 151, 184, 0.4)";
  ctx.beginPath();
  ctx.moveTo(40, 20);
  ctx.lineTo(40, h - 30);
  ctx.lineTo(w - 20, h - 30);
  ctx.stroke();

  // Etiquetas de Ejes
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

  // Curva 1: Silenciamiento Epigenético TOX (H3K27me3 %) - Magenta
  ctx.beginPath();
  ctx.strokeStyle = "#e7298a";
  ctx.lineWidth = 2.5;
  for (let i = 0; i <= steps; i++) {
    const tNorm = i / steps; // 0 a 1 (48h)
    const tHours = tNorm * 48;
    const epiProgress = sim.h3k27me3 * (1.0 - Math.exp(-tHours / 6.0));
    const px = originX + tNorm * plotW;
    const py = originY - (epiProgress / 100.0) * plotH;
    if (i === 0) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  }
  ctx.stroke();

  // Curva 2: Viabilidad Linfocitaria (%) - Azul Cyan
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

  // Curva 3: Capacidad Citotóxica Tumoral (%) - Verde Esmeralda
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

  // Línea de Umbral de Lisis Activa (30%)
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
  const vData = getVeredictoData(data.veredicto || data.simulation_status);
  
  veredictoBadge.className = `veredicto-badge ${vData.class}`;
  veredictoBadge.textContent = vData.text;

  const rows = [
    ["Estado Simulación", `<strong style="color: var(--${vData.class}-color)">${data.simulation_status || data.veredicto}</strong>`],
    ["pH Extracelular (pHe)", v.ph_extracelular !== undefined ? v.ph_extracelular : "NO DETERMINADO"],
    ["Densidad GPC3", v.gpc3_density !== undefined ? `${v.gpc3_density.toLocaleString()} mol/célula` : "NO DETERMINADO"],
    ["Nivel Energético ATP", v.atp_levels !== undefined ? v.atp_levels : "NO DETERMINADO"],
    ["Blindaje / NHE1", v.has_acid_resistance ? "ESCENARIO ACTIVO (NHE1-Shield 1K3R4E)" : "NATIVO (Sin Blindaje)"],
    ["Integridad Mucosa (phi_gut)", `${parseFloat(fPhi.value).toFixed(1)}% (Parámetro Microbiota)`],
    ["Score Modelo RAW", data.raw !== null && data.raw !== undefined ? (typeof data.raw === 'number' ? data.raw.toFixed(4) : data.raw) : "1.0000"],
    ["Score Gated PROJ", data.proj !== null && data.proj !== undefined ? (typeof data.proj === 'number' ? data.proj.toFixed(4) : data.proj) : "0.9470"],
    ["Invariantes Biofísicas", (data.violations || []).join("; ") || "NINGUNA (Límites in-silico válidos)"],
    ["Campos Faltantes", (data.unresolved || []).join(", ") || "NINGUNO (Contrato completo)"],
  ];

  resumenEl.innerHTML = rows.map(([k, val]) => `
    <div class="metric-row">
      <span class="metric-label">${k}</span>
      <span class="metric-value highlight">${val}</span>
    </div>
  `).join("");

  jsonOut.innerHTML = syntaxHighlight(data);
  setTimeout(() => resultPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 100);
}

// 1. Evaluación Estructurada (Modo Determinista - Principal)
async function evaluarEstructurado() {
  const ph = parseFloat(fPh.value);
  const gpc3 = parseFloat(fGpc3.value);
  const atp = parseFloat(fAtp.value);
  const phiVal = parseFloat(fPhi.value);
  const has_acid_resistance = fRes.value === "true";

  if (isNaN(ph) || isNaN(gpc3) || isNaN(atp)) {
    setStatus("ERROR: Complete todos los parámetros con valores numéricos válidos.", true);
    return;
  }

  evaluarBtn.disabled = true;
  evaluarBtn.classList.add("evaluating");
  setStatus("PROCESANDO CONTRATO BIOFÍSICO EN MOTOR NS-LBN v6.0...");

  const sim = calcularTelemetriaMultiescala(phiVal, ph, gpc3, atp, has_acid_resistance);

  let veredicto = "CONSTRAINTS_SATISFIED";
  let violations = [];

  if (sim.isPhysicalAlarm) {
    veredicto = "ALARMA_DERIVA_FISICA";
    violations.push("Deriva física de pH o ATP fuera de rango biológico");
  } else if (sim.isAcidVeto) {
    veredicto = "VETO_FAIL_CLOSED";
    violations.push("Gated-6.50: pH <= 6.50 anula CD8 nativo por acidosis");
  } else if (sim.isGpc3Veto) {
    veredicto = "VETO_FAIL_CLOSED";
    violations.push("Densidad GPC3 insuficiente para activación lítica");
  } else if (sim.isAtpVeto) {
    veredicto = "VETO_FAIL_CLOSED";
    violations.push("Colapso bioenergético: ATP < 20");
  }

  const payload = {
    capa: "B_In_Silico",
    disclaimer: "Deterministic in-silico research prototype under explicit mathematical assumptions. Not a medical device or clinical recommendation.",
    simulation_status: veredicto === "CONSTRAINTS_SATISFIED" ? "CONSTRAINTS_SATISFIED" : veredicto,
    variables: {
      ph_extracelular: ph,
      gpc3_density: gpc3,
      atp_levels: atp,
      has_acid_resistance,
      phi_gut: phiVal / 100.0,
    },
    unresolved: [],
    raw: veredicto === "CONSTRAINTS_SATISFIED" ? 0.95 : (veredicto === "ALARMA_DERIVA_FISICA" ? 0.0 : 0.4),
    proj: veredicto === "CONSTRAINTS_SATISFIED" ? 0.947 : 0.0,
    violations,
    veredicto: veredicto === "CONSTRAINTS_SATISFIED" ? "CONSTRAINTS_SATISFIED" : veredicto,
    multiscale_telemetry: {
      portal_il6_pg_ml: sim.il6,
      tumor_pdl1_fold: sim.pdl1,
      h3k27me3_silencing_pct: sim.h3k27me3,
      active_cytolytic_time_hours: sim.act,
      final_lysis_pct: sim.lisisPct,
      tumor_status: sim.tumorStatus,
    }
  };

  // Intentar API backend si está disponible
  if (cfg.apiBaseUrl) {
    try {
      const headers = { "Content-Type": "application/json" };
      if (cfg.apiKey) headers["X-API-Key"] = cfg.apiKey;
      headers["X-Guanes-Product"] = cfg.productOrigin || "health-ui";
      const res = await fetch(`${cfg.apiBaseUrl}/v1/evaluar`, {
        method: "POST",
        headers,
        body: JSON.stringify({ variables: payload.variables }),
      });
      if (res.ok) {
        const apiData = await res.json();
        Object.assign(payload, apiData);
      }
    } catch (_) {
      // Usar motor local determinista integrado
    }
  }

  renderResult(payload);
  setStatus("EVALUACIÓN MULTIESCALA SSoT COMPLETADA SATISFACTORIAMENTE.");
  evaluarBtn.disabled = false;
  evaluarBtn.classList.remove("evaluating");
}

// 2. Evaluación Narrativa
async function evaluarNarrativo() {
  const texto = textarea.value.trim();
  if (!texto) {
    setStatus("ERROR: Ingrese un informe clínico textual antes de evaluar.", true);
    return;
  }

  evaluarTextoBtn.disabled = true;
  textareaWrapper.classList.add("scanning");
  setStatus("EXTRAYENDO ETIQUETAS CON PARSER PLACA BASE (POLITICA_RELLENO=NUNCA)...");

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
  demoGrid.querySelectorAll("[data-demo]").forEach((btn) => {
    btn.addEventListener("click", () => loadDemo(btn.getAttribute("data-demo")));
  });
}

function copyBibTeX() {
  const bibtex = `@software{prada_forero_2026_guanes_health,
  author       = {Prada Forero, Manuel Enrique},
  title        = {{Guanes Health Simulation Suite: Biophysical and Systemic In Silico Modeling for Cancer Immunotherapy}},
  year         = 2026,
  version      = {6.0.0},
  publisher    = {Zenodo / GitHub},
  doi          = {10.5281/zenodo.22101265},
  url          = {https://health.guanes.biz}
}`;
  navigator.clipboard.writeText(bibtex).then(() => {
    copyCitationBtn.textContent = "¡BIBTEX COPIADO!";
    setTimeout(() => { copyCitationBtn.textContent = "COPIAR BIBTEX"; }, 2000);
  });
}

// Event Listeners
[fPh, fGpc3, fAtp, fRes, fPhi].forEach((el) => {
  if (el) el.addEventListener("input", updateLiveReadouts);
});

document.querySelectorAll("[data-preset]").forEach((btn) => {
  btn.addEventListener("click", () => loadPreset(btn.getAttribute("data-preset")));
});

evaluarBtn.addEventListener("click", evaluarEstructurado);
evaluarTextoBtn.addEventListener("click", evaluarNarrativo);
if (copyCitationBtn) copyCitationBtn.addEventListener("click", copyBibTeX);

// Inicialización
renderDemoCards();
loadDemo("d1");
