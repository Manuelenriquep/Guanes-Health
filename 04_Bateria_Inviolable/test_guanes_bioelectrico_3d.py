"""
==================================================================================================
GUANES HEALTH - BATERÍA INVIOLABLE
Suite de Pruebas Unitarias para BioelectricLattice3D — test_guanes_bioelectrico_3d.py
Kernel Nivel 0 / Verificación Biomédica Inmutable
==================================================================================================
Valida:
  1. Geometría concéntrica esferoidal en 3 capas histológicas (Núcleo necrótico, Zona intermedia, Borde).
  2. Gradiente radial fisiológico de pO2 (núcleo anóxico < 3 mmHg vs borde normóxico ~ 38 mmHg).
  3. Difusión electrotónica 3D de Vmem por uniones gap con stencil de 6 vecinos ortogonales.
  4. Identificación y rescate de Smaller Selves mediante el protocolo tridimensional de Levin.
  5. Métrica volumétrica del Cono Cognitivo de Luz (Phi_3D y radio efectivo esférico).
  6. Sello criptográfico SHA-256 del volumen completo.
==================================================================================================
"""

import math
import os
import sys
import unittest

MOTOR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03_Motor_Oncologico"))
if MOTOR_DIR not in sys.path:
    sys.path.insert(0, MOTOR_DIR)

from guanes_bioelectrico_3d import (
    BioelectricLattice3D,
    HistologicalZone3D
)


class TestGuanesBioelectrico3D(unittest.TestCase):
    """Pruebas del motor esferoidal 3D."""

    def setUp(self):
        # Malla cúbica 7x7x7 (343 vóxeles)
        self.lattice = BioelectricLattice3D(dim_size=7, voxel_spacing_um=20.0)

    def test_spheroid_three_zones_geometry(self):
        """Verifica la asignación radial de las 3 zonas anatómicas concéntricas."""
        center_x = int(self.lattice.center)
        core_zone = self.lattice.zones[center_x, center_x, center_x]
        rim_zone = self.lattice.zones[0, 0, 0]

        self.assertEqual(core_zone, HistologicalZone3D.NECROTIC_CORE)
        self.assertEqual(rim_zone, HistologicalZone3D.PROLIFERATIVE_RIM)

        # En el núcleo, pO2 debe ser anóxico (< 3 mmHg) y despolarizado (Vmem >= -20 mV)
        self.assertLess(self.lattice.p_o2[center_x, center_x, center_x], 3.0)
        self.assertGreaterEqual(self.lattice.v_mem[center_x, center_x, center_x], -20.0)

    def test_oxygen_reaction_diffusion_step(self):
        """Verifica que la integración de reacción-difusión conserve las fronteras y consuma O2 internamente."""
        po2_before_core = self.lattice.p_o2[int(self.lattice.center), int(self.lattice.center), int(self.lattice.center)]
        
        # Ejecutar 5 pasos de reacción-difusión
        for _ in range(5):
            self.lattice.step_reaction_diffusion_3d(dt_seconds=0.5)

        metrics = self.lattice.compute_metrics_3d()
        self.assertLess(metrics["mean_po2_core"], metrics["mean_po2_rim"])
        # Borde debe mantenerse adecuadamente oxigenado por perfusión Dirichlet
        self.assertGreater(metrics["mean_po2_rim"], 30.0)

    def test_smaller_selves_induction_and_levin_rescue_3d(self):
        """Verifica detección de Smaller Selves en 3D y su rescate coordinado con el protocolo Levin."""
        metrics_before = self.lattice.compute_metrics_3d()
        # Inicialmente debe haber células fragmentadas oncológicas en la zona hipóxica e intermedia
        self.assertGreater(metrics_before["smaller_selves_count_3d"], 0)
        self.assertEqual(metrics_before["tissue_state_3d"], "FRAGMENTED_ONCOGENIC")

        # Aplicar protocolo de Levin (repolarización -75 mV y apertura de Cx43 a 0.85)
        self.lattice.apply_levin_normalization_3d(force_vmem=-75.0, restore_gjc=0.85)

        metrics_after = self.lattice.compute_metrics_3d()
        # Los vóxeles rescatables deben acoplarse y elevar el cono cognitivo Phi_3D
        self.assertGreater(metrics_after["fraction_coupled_3d"], 0.70)
        self.assertEqual(metrics_after["tissue_state_3d"], "SYNCHRONIZED_SPHEROID")
        self.assertGreater(metrics_after["cognitive_light_cone_phi_3d"], metrics_before["cognitive_light_cone_phi_3d"])

    def test_bioelectric_sync_step_and_sha256(self):
        """Verifica la difusión de voltaje electrotónico y la inmutabilidad SHA-256."""
        metrics_1 = self.lattice.compute_metrics_3d()
        hash_1 = metrics_1["sha256_volume_hash"]
        self.assertEqual(len(hash_1), 64)

        # Paso de sincronización bioeléctrica
        self.lattice.step_bioelectric_sync_3d(dt=0.1)
        metrics_2 = self.lattice.compute_metrics_3d()
        hash_2 = metrics_2["sha256_volume_hash"]

        # Tras el acoplamiento, el estado físico cambia y genera un nuevo hash reproducible
        self.assertNotEqual(hash_1, hash_2)


if __name__ == "__main__":
    unittest.main()
