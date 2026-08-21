# -*- coding: utf-8 -*-
"""
GUANES HEALTH - Barrido estocastico O2 -> HIF-1a -> VEGF (Capa B)

Proceso Ornstein-Uhlenbeck para O2 intersticial, cinetica HIF-1a y fraccion
de tiempo sobre umbral HRE como proxy de activacion transcripcional VEGF.

Salida: 02_Simulaciones_Visuales/analisis_estocastico_oxigeno.png
"""

import math
import os

import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def simular_oxigeno_estocastico(mu, sigma, theta=0.5, dt=0.1, tiempo_total=72.0, rng=None):
    """Ornstein-Uhlenbeck: dO2 = theta*(mu - O2)*dt + sigma*dW."""
    if rng is None:
        rng = np.random.default_rng()
    pasos = int(tiempo_total / dt)
    o2 = np.zeros(pasos)
    o2[0] = mu

    for t in range(1, pasos):
        dW = rng.normal(0.0, math.sqrt(dt))
        o2[t] = o2[t - 1] + theta * (mu - o2[t - 1]) * dt + sigma * dW
        o2[t] = max(0.0, o2[t])

    return o2


def calcular_acumulacion_hif1a(o2_profile, dt=0.1, k_syn=2.0, k_deg=0.8):
    """Cinetica HIF-1a con estabilizacion sigmoidea bajo hipoxia (~5%)."""
    pasos = len(o2_profile)
    hif1a = np.zeros(pasos)

    for t in range(1, pasos):
        o2_actual = o2_profile[t]
        factor_estabilizacion = 1.0 / (1.0 + math.exp(1.5 * (o2_actual - 5.0)))
        dHIF = (k_syn * factor_estabilizacion - k_deg * hif1a[t - 1]) * dt
        hif1a[t] = max(0.0, hif1a[t - 1] + dHIF)

    return hif1a


def evaluar_produccion_vegf(hif1a_profile, umbral_hre=0.8):
    """Porcentaje de tiempo con HIF-1a >= umbral HRE (proxy VEGF)."""
    tiempo_activo = np.sum(hif1a_profile >= umbral_hre)
    return (tiempo_activo / len(hif1a_profile)) * 100.0


def vegf_en_punto(mu, sigma, monte_carlo_runs=5, seed=42):
    """Promedio Monte Carlo de activacion VEGF (%) en un punto (mu, sigma)."""
    rng = np.random.default_rng(seed)
    resultados = []
    for _ in range(monte_carlo_runs):
        o2_profile = simular_oxigeno_estocastico(mu, sigma, rng=rng)
        hif1a_profile = calcular_acumulacion_hif1a(o2_profile)
        resultados.append(evaluar_produccion_vegf(hif1a_profile))
    return float(np.mean(resultados))


def visuales_dir():
    path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "02_Simulaciones_Visuales")
    )
    os.makedirs(path, exist_ok=True)
    return path


def ejecutar_barrido_parametrico(resolucion=50, monte_carlo_runs=5, seed=42):
    print("[*] Barrido parametrico estocastico O2 vs volatilidad...")

    mus = np.linspace(1.0, 12.0, resolucion)
    sigmas = np.linspace(0.1, 5.0, resolucion)
    vegf_map = np.zeros((resolucion, resolucion))

    # Semilla por celda para reproducibilidad estable del mapa
    for i, sigma in enumerate(sigmas):
        for j, mu in enumerate(mus):
            cell_seed = seed + i * resolucion + j
            vegf_map[i, j] = vegf_en_punto(
                mu, sigma, monte_carlo_runs=monte_carlo_runs, seed=cell_seed
            )

    print("[+] Barrido completado. Generando mapa...")

    plt.figure(figsize=(10, 8))
    X, Y = np.meshgrid(mus, sigmas)

    cp = plt.contourf(X, Y, vegf_map, levels=20, cmap="YlOrRd")
    cbar = plt.colorbar(cp)
    cbar.set_label(
        "Activacion Transcripcional de VEGF (%)", fontsize=11, fontweight="bold"
    )

    contours = plt.contour(
        X,
        Y,
        vegf_map,
        levels=[10.0, 50.0, 90.0],
        colors="black",
        linewidths=1.2,
        linestyles="dashed",
    )
    plt.clabel(contours, inline=True, fmt="%1.0f%%", fontsize=10, colors="black")

    plt.text(
        2.0,
        1.0,
        "HIPOXIA\nPERMANENTE\n(VEGF > 90%)",
        color="darkred",
        fontsize=9,
        fontweight="bold",
        ha="center",
    )
    plt.text(
        9.0,
        4.0,
        "HIPOXIA\nINTERMITENTE\n(Bypass Estocastico)",
        color="orange",
        fontsize=9,
        fontweight="bold",
        ha="center",
    )
    plt.text(
        9.5,
        0.8,
        "NORMOXIA\nSEGURA",
        color="darkgreen",
        fontsize=9,
        fontweight="bold",
        ha="center",
    )

    plt.title(
        "MAPEO ESTOCASTICO DE RESISTENCIA: DINAMICA HIF-1a / VEGF",
        fontsize=12,
        fontweight="bold",
        pad=15,
    )
    plt.xlabel(
        r"Saturacion Media de Oxigeno Intersticial ($\mu$ - %)",
        fontsize=11,
        fontweight="bold",
    )
    plt.ylabel(
        r"Amplitud de Fluctuaciones Estocasticas ($\sigma$ - %)",
        fontsize=11,
        fontweight="bold",
    )
    plt.grid(True, alpha=0.3, linestyle=":")

    out_path = os.path.join(visuales_dir(), "analisis_estocastico_oxigeno.png")
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[OK] Visualizacion: {out_path}")
    return vegf_map


if __name__ == "__main__":
    ejecutar_barrido_parametrico()
