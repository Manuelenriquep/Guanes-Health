# -*- coding: utf-8 -*-
"""
GUANES HEALTH - DESTINO 2: ESCAPE METABOLICO Y CIERRE POR BLOQUEO MCT2

Modos:
  --comparativo  Escape libre vs triple bloqueo completo (mapa v3)
  --umbral       Bloqueo incompleto: frontera de control (default, destino 2)

Umbral (default):
  Eje X: retraso anti-PD-1 tras MCT1/4 (0-24 h)
  Eje Y: MCT2 funcional residual bajo bloqueo incompleto (0.3x-8.0x)
  Pregunta: cual es el maximo MCT2 residual que aun mantiene aclaramiento
  (>=99% del espacio con viabilidad <10%)?
"""

import argparse
import math
import os

import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


MCT2_FUNCIONAL_INHIBIDO = 0.5
UMBRAL_ACLARAMIENTO = 10.0  # % viabilidad
FRACCION_CONTROL = 99.0  # % del espacio parametrico


def simular_punto_limite(
    retraso_inmuno,
    mct2_max=15.0,
    inhibicion_mct2=False,
    mct2_funcional=None,
    dt=0.1,
    tiempo_total=72.0,
):
    """Viabilidad tumoral residual (%) a t = tiempo_total."""
    pasos = int(tiempo_total / dt)
    tiempo = np.linspace(0, tiempo_total, pasos)

    viabilidad = 1.0
    t_metabolico = 12.0
    t_inmunoterapia = t_metabolico + retraso_inmuno

    pHi = 7.20
    pHe = 6.20
    mct2_expresion = 1.0
    eficiencia_cd8 = 0.0

    for t in tiempo:
        if t < t_metabolico:
            pHe = 6.20
            pHi = 7.20
            mct2_expresion = 1.0
            eficiencia_cd8 = 0.0
        else:
            if mct2_funcional is not None:
                # Bloqueo incompleto: nivel funcional fijado (fuga farmacologica)
                mct2_expresion = float(mct2_funcional)
            elif inhibicion_mct2:
                mct2_expresion = MCT2_FUNCIONAL_INHIBIDO
            else:
                mct2_expresion = 1.0 + (mct2_max - 1.0) * (
                    1 - math.exp(-0.1 * (t - t_metabolico))
                )

            pHi_minimo = max(5.50, 5.75 + 0.85 * (1 - 1.0 / mct2_expresion))
            decay_pHi = (7.20 - pHi_minimo) * (
                1 - math.exp(-0.4 * (t - t_metabolico))
            )
            pHi = max(pHi_minimo, 7.20 - decay_pHi)

            pHe_maximo = min(7.35, 7.35 - 0.75 * (1 - 1.0 / mct2_expresion))
            lavado_pHe = (pHe_maximo - 6.20) * (
                1 - math.exp(-0.25 * (t - t_metabolico))
            )
            pHe = min(pHe_maximo, 6.20 + lavado_pHe)

            if pHe > 7.0:
                eficiencia_cd8 = min(1.0, (pHe - 7.0) / (7.35 - 7.0))
            else:
                eficiencia_cd8 = 0.0

        if t >= t_inmunoterapia:
            efectividad_PD1 = (
                1.0 if pHe >= 7.30 else (pHe - 6.0) / (7.35 - 6.0)
            )
            efectividad_PD1 = max(0.0, efectividad_PD1)
            fuerza = eficiencia_cd8 * efectividad_PD1
            depuracion = viabilidad * (1 - math.exp(-0.5 * fuerza * dt))
            viabilidad = max(0.0, viabilidad - depuracion)
        else:
            if pHi < 5.80:
                viabilidad = max(0.2, viabilidad - 0.01 * dt)
            else:
                viabilidad = 1.0

    return viabilidad * 100.0


def fraccion_aclaramiento(grilla, umbral=UMBRAL_ACLARAMIENTO):
    return float(np.mean(grilla < umbral) * 100.0)


def visuales_dir():
    path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "02_Simulaciones_Visuales")
    )
    os.makedirs(path, exist_ok=True)
    return path


# ---------------------------------------------------------------------------
# Modo --comparativo (mapa v3)
# ---------------------------------------------------------------------------
def ejecutar_barrido_comparativo(n=50):
    print("[*] Barrido A: escape MCT2 libre")
    print("[*] Barrido B: triple bloqueo completo (MCT2=0.5)")

    retrasos = np.linspace(0.0, 24.0, n)
    mct2_valores = np.linspace(1.0, 20.0, n)
    X, Y = np.meshgrid(retrasos, mct2_valores)

    grilla_escape = np.zeros((n, n))
    grilla_triple = np.zeros((n, n))
    for i, mct2_val in enumerate(mct2_valores):
        for j, ret in enumerate(retrasos):
            grilla_escape[i, j] = simular_punto_limite(
                ret, mct2_max=mct2_val, inhibicion_mct2=False
            )
            grilla_triple[i, j] = simular_punto_limite(
                ret, mct2_max=mct2_val, inhibicion_mct2=True
            )

    frac_e = fraccion_aclaramiento(grilla_escape)
    frac_t = fraccion_aclaramiento(grilla_triple)
    print(f"[+] Escape libre:    aclaramiento = {frac_e:.1f}%")
    print(f"[+] Triple bloqueo: aclaramiento = {frac_t:.1f}%")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6.5), dpi=150)
    for ax, grilla, titulo in (
        (
            axes[0],
            grilla_escape,
            f"A) Escape MCT2 libre\n(aclaramiento {frac_e:.1f}%)",
        ),
        (
            axes[1],
            grilla_triple,
            f"B) Triple bloqueo completo\n(aclaramiento {frac_t:.1f}%)",
        ),
    ):
        c = ax.contourf(X, Y, grilla, levels=30, cmap="coolwarm", vmin=0, vmax=100)
        lines = ax.contour(
            X, Y, grilla, levels=[10, 50, 90], colors="k", linewidths=0.5, linestyles="--"
        )
        ax.clabel(lines, inline=True, fmt="%d%%", fontsize=7)
        ax.set_xlabel("Retraso anti-PD-1 (h)", fontsize=9, fontweight="bold")
        ax.set_ylabel("Techo genetico MCT2 (x)", fontsize=9, fontweight="bold")
        ax.set_title(titulo, fontsize=10, fontweight="bold")

    fig.suptitle(
        "Escape metabolico vs cierre por triple bloqueo (t=72 h)",
        fontsize=12,
        fontweight="bold",
    )
    fig.colorbar(c, ax=axes.ravel().tolist(), shrink=0.85, pad=0.02).set_label(
        "Viabilidad residual (%)", fontweight="bold"
    )
    out = os.path.join(visuales_dir(), "analisis_parametrico_mct2-v3.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] {out}")


# ---------------------------------------------------------------------------
# Modo --umbral (destino 2): bloqueo incompleto
# ---------------------------------------------------------------------------
def ejecutar_barrido_umbral(n_ret=40, n_mct2=40):
    """
    Pregunta destino 2: con MCT1/4 activo, cuanto MCT2 residual tolera el modelo
    antes de perder el control del espacio (retraso x funcional).
    """
    print("[*] Destino 2: frontera de control bajo bloqueo MCT2 incompleto")

    retrasos = np.linspace(0.0, 24.0, n_ret)
    # 0.3 = bloqueo fuerte; ~2+ = fuga que reabre escape; 8 = casi libre
    mct2_residual = np.linspace(0.3, 8.0, n_mct2)
    X, Y = np.meshgrid(retrasos, mct2_residual)

    grilla = np.zeros((n_mct2, n_ret))
    for i, mct2_f in enumerate(mct2_residual):
        for j, ret in enumerate(retrasos):
            grilla[i, j] = simular_punto_limite(
                ret, mct2_funcional=mct2_f
            )

    # Fraccion de aclaramiento por cada nivel de MCT2 residual (colapsando retrasos)
    fracs = np.array(
        [fraccion_aclaramiento(grilla[i : i + 1, :]) for i in range(n_mct2)]
    )
    vmax_por_nivel = grilla.max(axis=1)

    # Umbral: mayor MCT2 residual con control casi total
    control_mask = (fracs >= FRACCION_CONTROL) & (vmax_por_nivel < UMBRAL_ACLARAMIENTO)
    if np.any(control_mask):
        idx_umbral = int(np.where(control_mask)[0][-1])
        mct2_umbral = float(mct2_residual[idx_umbral])
    else:
        idx_umbral = None
        mct2_umbral = None

    print(f"[+] Aclaramiento global del mapa: {fraccion_aclaramiento(grilla):.1f}%")
    if mct2_umbral is not None:
        print(
            f"[+] Umbral de control: MCT2 funcional residual <= {mct2_umbral:.2f}x "
            f"mantiene >= {FRACCION_CONTROL:.0f}% aclaramiento"
        )
    else:
        print("[!!] Ningun nivel de bloqueo en la grilla alcanza control total")

    # Cohorte C (retraso=12 h): curva 1D viabilidad vs MCT2 residual
    ret_c = 12.0
    curva_c = np.array(
        [simular_punto_limite(ret_c, mct2_funcional=m) for m in mct2_residual]
    )

    fig, axes = plt.subplots(1, 2, figsize=(14, 6.2), dpi=150)

    ax0 = axes[0]
    c0 = ax0.contourf(X, Y, grilla, levels=30, cmap="coolwarm", vmin=0, vmax=100)
    lines = ax0.contour(
        X, Y, grilla, levels=[10, 50, 90], colors="k", linewidths=0.6, linestyles="--"
    )
    ax0.clabel(lines, inline=True, fmt="%d%%", fontsize=7)
    if mct2_umbral is not None:
        ax0.axhline(
            mct2_umbral,
            color="lime",
            linewidth=1.8,
            linestyle="-",
            label=f"Umbral control <= {mct2_umbral:.2f}x",
        )
        ax0.legend(loc="upper right", fontsize=8)
    ax0.set_xlabel("Retraso anti-PD-1 tras MCT1/4 (h)", fontsize=9, fontweight="bold")
    ax0.set_ylabel("MCT2 funcional residual (x)", fontsize=9, fontweight="bold")
    ax0.set_title(
        "A) Espacio de escape bajo bloqueo incompleto",
        fontsize=10,
        fontweight="bold",
    )
    fig.colorbar(c0, ax=ax0, fraction=0.046, pad=0.04).set_label(
        "Viabilidad residual (%)", fontsize=8
    )

    ax1 = axes[1]
    ax1.plot(mct2_residual, curva_c, color="#1f4e79", linewidth=2.2, label="Cohorte C (dt=12 h)")
    ax1.axhline(UMBRAL_ACLARAMIENTO, color="gray", linestyle="--", linewidth=1, label="Umbral 10%")
    if mct2_umbral is not None:
        ax1.axvline(mct2_umbral, color="lime", linewidth=1.6, label=f"Control <= {mct2_umbral:.2f}x")
    ax1.fill_between(
        mct2_residual,
        0,
        curva_c,
        where=(curva_c < UMBRAL_ACLARAMIENTO),
        color="#4a90d9",
        alpha=0.25,
        label="Zona aclaramiento",
    )
    ax1.set_xlabel("MCT2 funcional residual (x)", fontsize=9, fontweight="bold")
    ax1.set_ylabel("Viabilidad residual a t=72 h (%)", fontsize=9, fontweight="bold")
    ax1.set_title(
        "B) Dosis-respuesta del bloqueo (Cohorte C)",
        fontsize=10,
        fontweight="bold",
    )
    ax1.set_ylim(-2, 105)
    ax1.legend(fontsize=8, loc="upper left")
    ax1.grid(True, alpha=0.3)

    fig.suptitle(
        "Destino 2: frontera de cierre del escape metabolico MCT2\n"
        "(bloqueo incompleto; salida de modelo a t = 72.0 h)",
        fontsize=12,
        fontweight="bold",
        y=1.02,
    )
    out = os.path.join(visuales_dir(), "analisis_umbral_bloqueo_mct2-v1.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] {out}")
    return mct2_umbral


def main():
    parser = argparse.ArgumentParser(description="Analisis parametrico MCT2 (destino 2)")
    parser.add_argument(
        "--comparativo",
        action="store_true",
        help="Mapa escape libre vs triple bloqueo completo",
    )
    parser.add_argument(
        "--umbral",
        action="store_true",
        help="Frontera de control bajo bloqueo incompleto (default)",
    )
    args = parser.parse_args()

    if args.comparativo and not args.umbral:
        ejecutar_barrido_comparativo()
    else:
        # Default destino 2
        ejecutar_barrido_umbral()
        if args.comparativo:
            ejecutar_barrido_comparativo()


if __name__ == "__main__":
    main()
