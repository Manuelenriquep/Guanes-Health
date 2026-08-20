# -*- coding: utf-8 -*-
"""
GUANES HEALTH - SCRIPT DE ANÁLISIS PARAMÉTRICO DE RESISTENCIA ADAPTATIVA (MCT2)
Este script ejecuta un barrido multidimensional del espacio de estados biológicos
para caracterizar la viabilidad tumoral residual en función de:
1. El retraso temporal de la inmunoterapia anti-PD-1 (Eje X, de 0 a 24 horas).
2. La tasa de sobreexpresión máxima de MCT2 (Eje Y, de x1 a x20).

Genera un mapa de calor tridimensional de alta resolución para el control de calidad in silico.
"""

import math
import numpy as np
import os
import sys

# Configurar matplotlib para ejecución headless
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def simular_punto_limite(retraso_inmuno, mct2_max, dt=0.1, tiempo_total=72.0):
    """
    Ejecuta una corrida temporal única para una combinación de parámetros biofísicos.
    Retorna la viabilidad tumoral residual final en t = 72.0 h.
    """
    pasos = int(tiempo_total / dt)
    tiempo = np.linspace(0, tiempo_total, pasos)
    
    # Inicialización del perfil tumoral
    viabilidad = 1.0
    atp_nivel = 10000.0
    t_metabolico = 12.0
    t_inmunoterapia = t_metabolico + retraso_inmuno
    
    # Parámetros del microambiente
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
            # Activación adaptativa de la sobreexpresión de MCT2
            mct2_expresion = 1.0 + (mct2_max - 1.0) * (1 - math.exp(-0.1 * (t - t_metabolico)))
            
            # Colapso mitigado de pHi (rescate celular)
            pHi_minimo = max(5.50, 5.75 + 0.85 * (1 - 1.0 / mct2_expresion))
            decay_pHi = (7.20 - pHi_minimo) * (1 - math.exp(-0.4 * (t - t_metabolico)))
            pHi = max(pHi_minimo, 7.20 - decay_pHi)
            
            # Acidosis estromal extracelular residual (bloqueo de lavado)
            pHe_maximo = min(7.35, 7.35 - 0.75 * (1 - 1.0 / mct2_expresion))
            lavado_pHe = (pHe_maximo - 6.20) * (1 - math.exp(-0.25 * (t - t_metabolico)))
            pHe = min(pHe_maximo, 6.20 + lavado_pHe)
            
            # Eficiencia de linfocitos CD8+ bajo gradiente de protones
            if pHe > 7.0:
                eficiencia_cd8_basal = (pHe - 7.0) / (7.35 - 7.0)
            else:
                eficiencia_cd8_basal = 0.0
            eficiencia_cd8 = min(1.0, eficiencia_cd8_basal)
            
        # Aplicación secuencial de inmunoterapia anti-PD-1
        if t >= t_inmunoterapia:
            efectividad_PD1 = 1.0 if pHe >= 7.30 else (pHe - 6.0) / (7.35 - 6.0)
            efectividad_PD1 = max(0.0, efectividad_PD1)
            
            fuerza_citotoxica = eficiencia_cd8 * efectividad_PD1
            depuracion = (viabilidad - 0.0) * (1 - math.exp(-0.5 * fuerza_citotoxica * dt))
            viabilidad = max(0.0, viabilidad - depuracion)
        else:
            if pHi < 5.80:
                # Daño por autólisis ácida interna pasiva
                viabilidad = max(0.2, viabilidad - 0.01 * dt)
            else:
                viabilidad = 1.0
                
    return viabilidad * 100.0  # Retornar porcentaje de viabilidad

def ejecutar_barrido():
    print("[*] Iniciando barrido paramétrico del espacio de estados...")
    
    # Definir grillas de parámetros
    retrasos = np.linspace(0.0, 24.0, 50)       # Retraso inmunoterapia (0 a 24 horas)
    mct2_valores = np.linspace(1.0, 20.0, 50)   # Tasa de sobreexpresión (1x a 20x)
    
    # Matriz para almacenar resultados de viabilidad
    grilla_viabilidad = np.zeros((len(mct2_valores), len(retrasos)))
    
    for i, mct2_val in enumerate(mct2_valores):
        for j, ret_val in enumerate(retrasos):
            grilla_viabilidad[i, j] = simular_punto_limite(ret_val, mct2_val)
            
    print("[+] Barrido completado con éxito. Generando visualización...")
    
    # Configuración estética del gráfico (Estilo científico limpio)
    plt.figure(figsize=(10, 8), dpi=150)
    
    # Crear mapa de calor de contorno relleno (contourf) para gradientes suaves
    X, Y = np.meshgrid(retrasos, mct2_valores)
    contour = plt.contourf(X, Y, grilla_viabilidad, levels=30, cmap="coolwarm", vmin=0, vmax=100)
    
    # Agregar líneas de nivel de referencia
    lines = plt.contour(X, Y, grilla_viabilidad, levels=[10, 50, 90], colors="black", linewidths=0.5, linestyles="dashed")
    plt.clabel(lines, inline=True, fmt="%d%%", fontsize=8)
    
    # Colorbar de viabilidad tumoral residual
    cbar = plt.colorbar(contour)
    cbar.set_label("Viabilidad Tumoral Residual final (%)", fontsize=11, fontweight="bold", labelpad=10)
    
    # Etiquetas y título estrictamente biológicos
    plt.xlabel("Retraso de Inmunoterapia anti-PD-1 tras Bloqueo Metabólico (horas)", fontsize=11, fontweight="bold")
    plt.ylabel("Tasa de sobreexpresión compensatoria máxima de MCT2 (x)", fontsize=11, fontweight="bold")
    plt.title("Mapa de Escape Adaptativo Tumoral por Sobreexpresión de MCT2\n(Simulación multiescala de constantes de frontera a t = 72.0 h)", fontsize=12, fontweight="bold", pad=15)
    
    # Anotaciones explicativas de las Cohortes de simulación
    plt.annotate("Cohorte C estándar\n(Zona de aclaramiento)", xy=(12.0, 1.0), xytext=(15.0, 4.0),
                 arrowprops=dict(facecolor="black", shrink=0.05, width=0.5, headwidth=4),
                 fontsize=9, bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8, ec="black", lw=0.5))
                 
    plt.annotate("Zona de Escape Clonal\n(Resistencia metabólica)", xy=(6.0, 15.0), xytext=(8.0, 11.0),
                 arrowprops=dict(facecolor="black", shrink=0.05, width=0.5, headwidth=4),
                 fontsize=9, bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8, ec="black", lw=0.5))

    plt.tight_layout()
    
    # Rutas de salida en scratch
    output_png = "/workspace/scratch/analisis_parametrico_mct2.png"
    plt.savefig(output_png, dpi=150, bbox_inches="tight")
    plt.close()
    
    print(f"[✔] ÉXITO: Imagen exportada correctamente a {output_png}")

if __name__ == "__main__":
    ejecutar_barrido()
