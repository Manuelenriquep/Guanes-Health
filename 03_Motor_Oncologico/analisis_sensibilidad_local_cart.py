# -*- coding: utf-8 -*-
"""
Barrido local 1D/2D del esqueleto CAR-T / HCC (Capa B).

Rangos ±20% = asumidos en ledger_parametros_cart_hcc.md (no literatura).
No es análisis de Sobol ni manuscrito listo.
"""

import os
import sys

import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

_MOTOR = os.path.abspath(os.path.dirname(__file__))
if _MOTOR not in sys.path:
    sys.path.insert(0, _MOTOR)

from simulador_cart_hcc_interaccion import SimuladorCARTInteraccion, UMBRAL_GPC3

# Rangos exploratorios declarados (ledger); no intervalos de confianza empíricos
DELTA_DENS = 0.20
DELTA_KLISIS = 0.20
K_LISIS_NOM = 0.005
DENS_NOM = 5000.0
PHE_NOM = 6.20


def visuales_dir():
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "02_Simulaciones_Visuales")
    )


def viabilidad_terminal(ph_e=PHE_NOM, densidad=DENS_NOM, k_lisis=K_LISIS_NOM):
    """Viabilidad tumoral modelada a t=72 h."""
    sim = SimuladorCARTInteraccion()
    hist = sim.simular_intervalo(
        ph_e=ph_e, densidad_antigeno=densidad, k_lisis=k_lisis
    )
    return float(hist["viabilidad_tumor"][-1])


def barrido_phe(n=21, ph_min=6.0, ph_max=7.4, densidad=DENS_NOM, k_lisis=K_LISIS_NOM):
    phe = np.linspace(ph_min, ph_max, n)
    viab = np.array([viabilidad_terminal(ph_e=float(p), densidad=densidad, k_lisis=k_lisis) for p in phe])
    return phe, viab


def barrido_densidad(n=21, d_min=500.0, d_max=10000.0, ph_e=PHE_NOM, k_lisis=K_LISIS_NOM):
    dens = np.linspace(d_min, d_max, n)
    viab = np.array([viabilidad_terminal(ph_e=ph_e, densidad=float(d), k_lisis=k_lisis) for d in dens])
    return dens, viab


def envolvente_asumida(ph_e=PHE_NOM, n_grid=5):
    """
    Envolvente min/mediana/max sobre rejilla ±20% en densidad y k_lisis.
    Etiqueta: rango asumido Capa B (ledger), no IC de literatura.
    """
    dens_vals = np.linspace(DENS_NOM * (1 - DELTA_DENS), DENS_NOM * (1 + DELTA_DENS), n_grid)
    k_vals = np.linspace(K_LISIS_NOM * (1 - DELTA_KLISIS), K_LISIS_NOM * (1 + DELTA_KLISIS), n_grid)
    muestras = []
    for d in dens_vals:
        for k in k_vals:
            muestras.append(viabilidad_terminal(ph_e=ph_e, densidad=float(d), k_lisis=float(k)))
    arr = np.array(muestras)
    return {
        "n": int(arr.size),
        "min": float(arr.min()),
        "mediana": float(np.median(arr)),
        "max": float(arr.max()),
        "ph_e": ph_e,
        "nota": "envolvente ±20% asumido (ledger); no IC empírico",
    }


def mapa_phe_densidad(n_ph=11, n_d=11):
    phe = np.linspace(6.0, 7.4, n_ph)
    dens = np.linspace(500.0, 10000.0, n_d)
    z = np.zeros((n_d, n_ph))
    for i, d in enumerate(dens):
        for j, p in enumerate(phe):
            z[i, j] = viabilidad_terminal(ph_e=float(p), densidad=float(d))
    return phe, dens, z


def generar_figura(out_name="sensibilidad_local_cart_hcc.png"):
    phe, v_phe = barrido_phe()
    dens, v_dens = barrido_densidad()
    env = envolvente_asumida()
    phe2, dens2, z = mapa_phe_densidad()

    fig, axs = plt.subplots(1, 3, figsize=(12, 3.6))
    fig.suptitle(
        "Barrido local CAR-T/HCC (Capa B) — rangos asumidos, no wet-lab",
        fontsize=11,
    )

    axs[0].plot(phe, v_phe * 100.0, color="#1f4e79", lw=2)
    axs[0].axvline(PHE_NOM, color="gray", ls="--", lw=1)
    axs[0].set_xlabel("pHe")
    axs[0].set_ylabel("Viabilidad tumoral terminal (%)")
    axs[0].set_title("1D: pHe")
    axs[0].set_ylim(0, 105)

    axs[1].plot(dens, v_dens * 100.0, color="#1f4e79", lw=2)
    axs[1].axvline(UMBRAL_GPC3, color="#c0392b", ls="--", lw=1, label="veto GPC3")
    axs[1].set_xlabel("Densidad GPC3 (moléc./cél., modelo)")
    axs[1].set_title("1D: densidad")
    axs[1].set_ylim(0, 105)
    axs[1].legend(fontsize=8)

    im = axs[2].imshow(
        z * 100.0,
        origin="lower",
        aspect="auto",
        extent=[phe2[0], phe2[-1], dens2[0], dens2[-1]],
        cmap="viridis_r",
        vmin=0,
        vmax=100,
    )
    axs[2].set_xlabel("pHe")
    axs[2].set_ylabel("Densidad GPC3")
    axs[2].set_title("2D: pHe × densidad")
    fig.colorbar(im, ax=axs[2], fraction=0.046, pad=0.04, label="%")

    fig.tight_layout()
    os.makedirs(visuales_dir(), exist_ok=True)
    out = os.path.join(visuales_dir(), out_name)
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out, env


if __name__ == "__main__":
    path, env = generar_figura()
    print(f"[+] Figura: {path}")
    print(
        f"[+] Envolvente asumida @ pHe={env['ph_e']}: "
        f"min={env['min']*100:.2f}%  mediana={env['mediana']*100:.2f}%  "
        f"max={env['max']*100:.2f}%  (n={env['n']})"
    )
    print(f"    {env['nota']}")
