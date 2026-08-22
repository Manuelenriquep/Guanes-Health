# -*- coding: utf-8 -*-
"""
Demo de divergencia: clasificador estático (proxy) vs instrumento Guanes (Gated-6.50).

Misma firma genómica “IO-elegible”; el matcher administrativo sigue diciendo sí
mientras el estroma ácido (pHe ≤ 6.50) anula la eficiencia CD8 *en el modelo*.

Capa B / ilustrativo — no es evidencia clínica ni auditoría de MatchMiner u otros.
"""
from __future__ import annotations

import argparse
import os
import sys

_MOTOR_DIR = os.path.abspath(os.path.dirname(__file__))
if _MOTOR_DIR not in sys.path:
    sys.path.insert(0, _MOTOR_DIR)

from inmuno_utils import PH_VETO_CD8, calcular_eficiencia_cd8


def clasificador_estatico(firma_io_elegible: bool) -> float:
    """
    Proxy de matching administrativo: firma fija → eficacia nominal 1.0.
    Ignora pHe (diseño intencional del contraste).
    """
    return 1.0 if firma_io_elegible else 0.0


def eficiencia_instrumento_placa(pHe: float, firma_io_elegible: bool) -> float:
    """Match genómico *y* veto Gated-6.50 (Capa B)."""
    if not firma_io_elegible:
        return 0.0
    return float(calcular_eficiencia_cd8(pHe))


def comparar_en_pHe(pHe: float, firma_io_elegible: bool = True) -> dict:
    estatico = clasificador_estatico(firma_io_elegible)
    placa = eficiencia_instrumento_placa(pHe, firma_io_elegible)
    return {
        "pHe": float(pHe),
        "firma_io_elegible": bool(firma_io_elegible),
        "eficacia_estatica": estatico,
        "eficacia_placa": placa,
        "diverge": abs(estatico - placa) > 1e-12,
    }


def barrido_pHe(
    pHe_min: float = 6.00,
    pHe_max: float = 7.40,
    paso: float = 0.05,
    firma_io_elegible: bool = True,
) -> list:
    if paso <= 0:
        raise ValueError("paso debe ser > 0")
    filas = []
    n = int(round((pHe_max - pHe_min) / paso))
    for i in range(n + 1):
        pHe = round(pHe_min + i * paso, 10)
        if pHe > pHe_max + 1e-9:
            break
        filas.append(comparar_en_pHe(pHe, firma_io_elegible))
    return filas


def visuales_dir() -> str:
    path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "02_Simulaciones_Visuales")
    )
    os.makedirs(path, exist_ok=True)
    return path


def imprimir_tabla(filas: list, destacado: float = PH_VETO_CD8) -> None:
    print("pHe     estatico   placa     diverge")
    print("------  ---------  --------  -------")
    for f in filas:
        marca = " <-- veto CD8" if abs(f["pHe"] - destacado) < 1e-9 else ""
        print(
            f"{f['pHe']:5.2f}   "
            f"{f['eficacia_estatica']:7.2f}    "
            f"{f['eficacia_placa']:6.2f}   "
            f"{'SI' if f['diverge'] else 'no'}{marca}"
        )


def generar_figura(filas: list, salida: str | None = None) -> str:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    pHe = [f["pHe"] for f in filas]
    est = [f["eficacia_estatica"] for f in filas]
    placa = [f["eficacia_placa"] for f in filas]

    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=140)
    ax.plot(pHe, est, color="#5c6b73", linewidth=2.2, label="Matcher estático (proxy)")
    ax.plot(
        pHe,
        placa,
        color="#0b6e4f",
        linewidth=2.6,
        label="Instrumento Guanes (Gated-6.50)",
    )
    ax.axvline(
        PH_VETO_CD8,
        color="#c0392b",
        linestyle="--",
        linewidth=1.2,
        label=f"Veto pHe = {PH_VETO_CD8:.2f}",
    )
    ax.fill_between(
        pHe,
        est,
        placa,
        where=[e != p for e, p in zip(est, placa)],
        color="#0b6e4f",
        alpha=0.12,
        interpolate=True,
    )
    ax.set_xlabel("pHe estromal (modelo)", fontsize=11)
    ax.set_ylabel("Eficacia IO nominal (fracción 0–1)", fontsize=11)
    ax.set_ylim(-0.05, 1.15)
    ax.set_xlim(min(pHe), max(pHe))
    ax.grid(True, linestyle="--", alpha=0.45)
    ax.legend(loc="lower right", frameon=False)
    ax.set_title(
        "Divergencia instrumentada: firma fija vs. veto ácido (Capa B)",
        fontsize=12,
        pad=10,
    )
    fig.text(
        0.5,
        0.02,
        "Ilustración del modelo — no es predicción clínica ni auditoría de repos externos.",
        ha="center",
        fontsize=8,
        color="#444444",
    )
    fig.tight_layout(rect=[0, 0.05, 1, 1])

    if salida is None:
        salida = os.path.join(
            visuales_dir(), "divergencia_estatico_vs_placa_gated_650.png"
        )
    fig.savefig(salida, bbox_inches="tight")
    plt.close(fig)
    return salida


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Contraste: matcher estático (firma IO) vs eficiencia CD8 Gated-6.50."
        )
    )
    parser.add_argument("--no-plot", action="store_true", help="Solo tabla en consola")
    parser.add_argument(
        "--pHe",
        type=float,
        default=None,
        help="Si se indica, solo compara ese pHe (sin barrido)",
    )
    args = parser.parse_args(argv)

    print("=== Divergencia estatico vs placa (Capa B; Gated-6.50) ===")
    print("Paciente toy: firma IO-elegible = True (match administrativo fijo).\n")

    if args.pHe is not None:
        fila = comparar_en_pHe(args.pHe, firma_io_elegible=True)
        imprimir_tabla([fila])
        if fila["diverge"]:
            print(
                "\n[+] Divergencia: el matcher sigue en 1.0; "
                "el instrumento anula o reduce la eficacia modelada."
            )
        else:
            print(
                "\n[=] Sin divergencia en este pHe "
                "(ambos alineados en el toy model)."
            )
        return 0

    filas = barrido_pHe()
    imprimir_tabla(filas)

    bajo_veto = [f for f in filas if f["pHe"] <= PH_VETO_CD8 + 1e-12]
    assert all(f["eficacia_placa"] == 0.0 for f in bajo_veto)
    assert all(f["eficacia_estatica"] == 1.0 for f in bajo_veto)
    print(
        f"\n[+] Bajo pHe <= {PH_VETO_CD8:.2f}: estatico=1.0 y placa=0.0 "
        f"({len(bajo_veto)} puntos) - divergencia maxima del contraste."
    )

    if not args.no_plot:
        path = generar_figura(filas)
        print(f"[+] Figura: {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
