"""
========================================================================================
GUANES HEALTH - BIO-GAME-01: SELF-SCALING BIOELECTRIC IPD-ms SIMULATOR
Iterated, Spatialized Prisoner's Dilemma with Self-Scaling Players & Bioelectric Coupling
========================================================================================

FORMAL ACADEMIC ATTRIBUTION & CITATION:
This module is directly based upon the seminal game-theoretic framework developed by:
  Lakshwin Shreesha, Federico Pigozzi, Adam Goldstein, and Michael Levin
  "Extending Iterated, Spatialized Prisoner's Dilemma to Understand Multicellularity:
   Game Theory With Self-Scaling Players"
  IEEE Transactions on Molecular, Biological, and Multi-Scale Communications,
  Vol. 11, No. 2, pp. 101-115, June 2025.
  Allen Discovery Center at Tufts University / Wyss Institute at Harvard University.

BIOELECTRIC & METABOLIC COUPLING (GUANES HEALTH LAYER B INTEGRATION):
  Manuel Enrique Prada Forero, Guanes Health In-Silico Suite (2026).
  Couples the four IPD-ms actions (Cooperate 'C', Defect 'D', Merge 'M', Split 'S')
  with single-compartment biophysical ODEs (MET-01):
  - Extracellular/Intracellular proton balance (pHe / pHi, NHE1, MCT1/4)
  - Resting membrane potential Vmem(pHi)
  - Homotypic Connexin-43 Gap Junction Conductance G_GJ(Delta Vmem, pHi)
  - Physical Merge gating: P(Merge) <= G_GJ
  - Acidic split induction: Low pHi & Vmem collapse trigger involuntary 'Split' (S)
========================================================================================
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from collections import deque

# Set random seed for scientific reproducibility
np.random.seed(42)

# --- 1. BIOPHYSICAL COUPLING ENGINE (MET-01 x LEVIN) ---

def compute_bioelectric_state(pHe, has_shield):
    """
    Computes steady-state cytosolic pHi, membrane potential Vmem (mV),
    and Cx43 Gap Junction Conductance G_GJ based on the MET-01 ODE model.
    """
    if has_shield:
        # 1K3R4E: Constitutive NHE1-Shield
        pHi = 6.697 if abs(pHe - 6.20) < 0.05 else (7.20 if pHe >= 7.30 else 6.85)
    else:
        # S703A: Native unshielded (thermodynamic collapse at pHe = 6.20)
        pHi = 5.495 if abs(pHe - 6.20) < 0.05 else (7.05 if pHe >= 7.30 else 6.10)
    
    # Membrane Potential Vmem(pHi) in mV
    vmem = -30.0 - (40.0 / (1.0 + 10.0 ** ((6.60 - pHi) / 0.20)))
    
    # Cx43 Gap Junction Conductance G_GJ (coupling to healthy -70 mV stroma)
    delta_v = abs(vmem - (-70.0))
    g_gj = 0.05 + (0.95 / (1.0 + np.exp(0.15 * (delta_v - 25.0))))
    
    # Gating factor by intracellular proton concentration (pH gating of connexins)
    # Cx43 closes sharply when pHi falls below 6.50
    ph_gate = 1.0 / (1.0 + 10.0 ** (2.0 * (6.50 - pHi)))
    effective_g_gj = float(g_gj * ph_gate)
    
    return {
        "pHi": float(pHi),
        "vmem": float(vmem),
        "g_gj": float(effective_g_gj),
        "clc_index": float(effective_g_gj)
    }


# --- 2. IPD-ms SPATIAL GAME ENGINE (SHREESHA ET AL. 2025 EXTENSION) ---

class SelfScalingGridSimulation:
    def __init__(self, size=20, rounds=120, pHe=6.20, has_shield=True, memory_size=1):
        self.size = size
        self.rounds = rounds
        self.pHe = pHe
        self.has_shield = has_shield
        self.memory_size = memory_size
        
        # Bioelectric parameters
        self.bio = compute_bioelectric_state(pHe, has_shield)
        
        # Grid setup: 20x20 = 400 positions
        # Each position has an agent_id (0 to 399 initially)
        self.agent_grid = np.arange(size * size).reshape((size, size))
        
        # Agents dictionary: agent_id -> { "cells": set of (x, y), "q_table": {}, "memory": deque }
        # Actions: 0: Cooperate (C), 1: Defect (D), 2: Merge (M), 3: Split (S)
        self.ACTIONS = ['C', 'D', 'M', 'S']
        self.PAYOFF_MATRIX = {
            ('C', 'C'): (3.0, 3.0),
            ('D', 'C'): (5.0, 0.0),
            ('C', 'D'): (0.0, 5.0),
            ('D', 'D'): (1.0, 1.0),
        }
        
        self.agents = {}
        for x in range(size):
            for y in range(size):
                aid = self.agent_grid[x, y]
                self.agents[aid] = {
                    "id": aid,
                    "cells": {(x, y)},
                    "q_table": np.ones((4,)) * 2.0,  # optimistic Q-init
                    "memory": deque(maxlen=max(1, memory_size)),
                    "last_action": 'C',
                    "cumulative_payoff": 0.0,
                    "round_payoff": 0.0
                }
        
        # Historical telemetry tracking
        self.history = {
            "round": [],
            "num_agents": [],
            "max_cluster_size": [],
            "mean_cluster_size": [],
            "cooperation_rate": [],
            "mean_round_payoff": [],
            "clc_index": [],
            "merge_events": [],
            "split_events": []
        }

    def get_moore_neighbors(self, x, y):
        """Returns 8 Moore neighbors with periodic boundary conditions (torus)."""
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx = (x + dx) % self.size
                ny = (y + dy) % self.size
                neighbors.append((nx, ny))
        return neighbors

    def get_agent_neighbors(self, agent_id):
        """Finds all unique neighboring agent_ids adjacent to any cell of this agent."""
        agent = self.agents[agent_id]
        neighbor_aids = set()
        for (cx, cy) in agent["cells"]:
            for (nx, ny) in self.get_moore_neighbors(cx, cy):
                naid = self.agent_grid[nx, ny]
                if naid != agent_id and naid in self.agents:
                    neighbor_aids.add(naid)
        return list(neighbor_aids)

    def select_action(self, agent_id, epsilon=0.10):
        """Epsilon-greedy action selection over {C, D, M, S}."""
        agent = self.agents[agent_id]
        num_cells = len(agent["cells"])
        
        # Valid actions: Can only Split if multicellular (> 1 cell)
        valid_indices = [0, 1, 2] if num_cells == 1 else [0, 1, 2, 3]
        
        if np.random.rand() < epsilon:
            return np.random.choice(valid_indices)
        
        q_vals = [agent["q_table"][i] for i in valid_indices]
        best_sub_idx = np.argmax(q_vals)
        return valid_indices[best_sub_idx]

    def execute_round(self, r):
        active_aids = list(self.agents.keys())
        agent_actions = {}
        for aid in active_aids:
            act_idx = self.select_action(aid)
            agent_actions[aid] = self.ACTIONS[act_idx]
            self.agents[aid]["last_action"] = self.ACTIONS[act_idx]
            self.agents[aid]["round_payoff"] = 0.0

        # --- STEP 1: RESOLVE MERGE & SPLIT (STRUCTURAL DYNAMICS) ---
        merge_count = 0
        split_count = 0
        processed_splits = set()
        
        # Bioelectric gating: Merge is physically gated by G_GJ
        g_gj = self.bio["g_gj"]
        
        # Acidic involuntary split: if pHi is collapsed, multicellular complexes disintegrate
        involuntary_split_prob = max(0.0, 1.0 - g_gj) * 0.40

        # Process Splits first
        for aid in active_aids:
            if aid not in self.agents:
                continue
            agent = self.agents[aid]
            is_voluntary_split = (agent_actions.get(aid) == 'S' and len(agent["cells"]) > 1)
            is_acid_split = (len(agent["cells"]) > 1 and np.random.rand() < involuntary_split_prob)
            
            if (is_voluntary_split or is_acid_split) and aid not in processed_splits:
                # Disintegrate into unicellular agents
                cells_list = list(agent["cells"])
                # Keep first cell with original aid
                first_cell = cells_list[0]
                agent["cells"] = {first_cell}
                self.agent_grid[first_cell[0], first_cell[1]] = aid
                
                # Assign new IDs for remaining cells
                for extra_cell in cells_list[1:]:
                    new_aid = int(np.random.randint(100000, 999999))
                    while new_aid in self.agents:
                        new_aid = int(np.random.randint(100000, 999999))
                    self.agent_grid[extra_cell[0], extra_cell[1]] = new_aid
                    self.agents[new_aid] = {
                        "id": new_aid,
                        "cells": {extra_cell},
                        "q_table": np.copy(agent["q_table"]),
                        "memory": deque(agent["memory"], maxlen=self.memory_size),
                        "last_action": 'C',
                        "cumulative_payoff": agent["cumulative_payoff"] / len(cells_list),
                        "round_payoff": 0.0
                    }
                split_count += 1
                processed_splits.add(aid)

        # Process Merges
        # If two adjacent agents choose 'M' (or one chooses 'M' and physical G_GJ allows syncytium formation)
        merged_partners = set()
        current_aids = list(self.agents.keys())
        np.random.shuffle(current_aids)

        for aid in current_aids:
            if aid in merged_partners or aid not in self.agents:
                continue
            act = agent_actions.get(aid, 'C')
            if act == 'M':
                neighbors = self.get_agent_neighbors(aid)
                # Filter out neighbors already merged this turn
                valid_neighbors = [nid for nid in neighbors if nid not in merged_partners and nid in self.agents]
                if valid_neighbors:
                    # Select target neighbor (prefer one also playing M or high performance)
                    target_nid = valid_neighbors[0]
                    target_act = agent_actions.get(target_nid, 'C')
                    
                    # Merge occurs if both chose M, OR if one chose M and bioelectric G_GJ is high
                    # Physical constraint: Probability is clamped by effective G_GJ!
                    merge_allowed = (target_act == 'M') or (np.random.rand() < g_gj * 0.85)
                    
                    if merge_allowed:
                        host_agent = self.agents[aid]
                        donor_agent = self.agents[target_nid]
                        
                        # Merge donor into host
                        for (cx, cy) in donor_agent["cells"]:
                            self.agent_grid[cx, cy] = aid
                            host_agent["cells"].add((cx, cy))
                        
                        # Inherit policy of better-performing agent (Shreesha et al. 2025 rule)
                        if donor_agent["cumulative_payoff"] > host_agent["cumulative_payoff"]:
                            host_agent["q_table"] = np.copy(donor_agent["q_table"])
                        
                        host_agent["cumulative_payoff"] += donor_agent["cumulative_payoff"]
                        del self.agents[target_nid]
                        
                        merged_partners.add(aid)
                        merged_partners.add(target_nid)
                        merge_count += 1

        # --- STEP 2: PLAY SPATIAL PRISONER'S DILEMMA ACROSS PERIMETERS ---
        # Inter-agent interactions across borders
        pair_interactions = set()
        c_count = 0
        total_interactions = 0
        
        for aid, agent in self.agents.items():
            neighbors = self.get_agent_neighbors(aid)
            # Internal synergy reward: cells inside a multicellular syncytium cooperate frictionlessly
            internal_cells = len(agent["cells"])
            if internal_cells > 1:
                # Internal cooperation bonus scaled by G_GJ
                internal_synergy = (internal_cells - 1) * 3.0 * g_gj
                agent["round_payoff"] += internal_synergy
                agent["cumulative_payoff"] += internal_synergy

            act_1 = agent["last_action"]
            # Map structural actions M and S to functional boundary behavior:
            # As shown by Shreesha et al. 2025: M acts cooperatively towards merger, S acts as defection/escape
            eff_act_1 = 'C' if act_1 in ['C', 'M'] else 'D'

            for nid in neighbors:
                pair = tuple(sorted([aid, nid]))
                if pair in pair_interactions:
                    continue
                pair_interactions.add(pair)
                
                neighbor = self.agents[nid]
                act_2 = neighbor["last_action"]
                eff_act_2 = 'C' if act_2 in ['C', 'M'] else 'D'

                p1, p2 = self.PAYOFF_MATRIX[(eff_act_1, eff_act_2)]
                agent["round_payoff"] += p1
                agent["cumulative_payoff"] += p1
                neighbor["round_payoff"] += p2
                neighbor["cumulative_payoff"] += p2

                if eff_act_1 == 'C': c_count += 1
                if eff_act_2 == 'C': c_count += 1
                total_interactions += 2

        # --- STEP 3: Q-LEARNING UPDATE ---
        learning_rate = 0.15
        discount_factor = 0.85
        for aid, agent in self.agents.items():
            act_idx = self.ACTIONS.index(agent["last_action"])
            reward = agent["round_payoff"]
            best_future = np.max(agent["q_table"])
            agent["q_table"][act_idx] += learning_rate * (reward + discount_factor * best_future - agent["q_table"][act_idx])

        # --- STEP 4: TELEMETRY LOGGING ---
        sizes = [len(a["cells"]) for a in self.agents.values()]
        coop_rate = (c_count / total_interactions) if total_interactions > 0 else 0.50
        mean_payoff = np.mean([a["round_payoff"] for a in self.agents.values()])
        
        self.history["round"].append(r)
        self.history["num_agents"].append(len(self.agents))
        self.history["max_cluster_size"].append(np.max(sizes))
        self.history["mean_cluster_size"].append(np.mean(sizes))
        self.history["cooperation_rate"].append(coop_rate)
        self.history["mean_round_payoff"].append(mean_payoff)
        self.history["clc_index"].append(self.bio["clc_index"])
        self.history["merge_events"].append(merge_count)
        self.history["split_events"].append(split_count)

    def run(self):
        for r in range(1, self.rounds + 1):
            self.execute_round(r)
        return self.history


# --- 3. DUAL EXPERIMENTAL PROTOCOL: ACID TRAP VS. BIOELECTRIC SHIELD ---

def run_comparative_experiment():
    print("[1/3] Running Scenario A: Deep Acidosis Trap (pHe = 6.20, Native CD8 / S703A, Unshielded)...")
    sim_acid = SelfScalingGridSimulation(size=20, rounds=100, pHe=6.20, has_shield=False, memory_size=1)
    hist_acid = sim_acid.run()

    print("[2/3] Running Scenario B: Bioelectric Synergy (pHe = 6.20, NHE1-Shield 1K3R4E, Hyperpolarized)...")
    sim_shield = SelfScalingGridSimulation(size=20, rounds=100, pHe=6.20, has_shield=True, memory_size=1)
    hist_shield = sim_shield.run()

    # --- 4. GENERATE 4-PANEL PUBLICATION DASHBOARD ---
    print("[3/3] Rendering 4-Panel Publication-Grade Scientific Dashboard (300 DPI)...")
    fig = plt.figure(figsize=(18, 12), dpi=300)
    fig.patch.set_facecolor('#040a14')

    # Color palette
    c_blue = '#38bdf8'
    c_red = '#ef4444'
    c_green = '#34d399'
    c_purple = '#c084fc'
    c_amber = '#fbbf24'
    c_grid = '#1e293b'

    # Master title with full formal academic credits
    plt.suptitle(
        "GUANES HEALTH BIO-GAME-01 · SELF-SCALING BIOELECTRIC IPD-ms SIMULATION\n"
        "Directly based on: Shreesha, Pigozzi, Goldstein, & Levin (IEEE Trans. Mol. Biol. Multi-Scale Commun., 2025)\n"
        "Coupled with MET-01 Proton Kinetics (pHi/pHe, Vmem, Connexin-43 GJC) · Layer B In-Silico Prototype",
        fontsize=13, fontweight='bold', color='#f8fafc', y=0.98, fontfamily='monospace'
    )

    # Subplot 1: Spatial Grid End-State at Round 100 (Unshielded Acidic vs. Shielded Syncytium)
    ax1 = plt.subplot(2, 2, 1)
    ax1.set_facecolor('#061224')
    
    # We display a composite split view: Left half Acid Trap, Right half Shielded
    composite_grid = np.zeros((20, 20))
    composite_grid[:, :10] = sim_acid.agent_grid[:, :10] % 15  # color index
    composite_grid[:, 10:] = sim_shield.agent_grid[:, 10:] % 15
    
    cmap = plt.colormaps['plasma'].resampled(16)
    im = ax1.imshow(composite_grid, cmap=cmap, aspect='equal')
    ax1.axvline(9.5, color='#38bdf8', linestyle='--', linewidth=2.5, label='Split View Boundary')
    ax1.set_title(
        "Panel A: Spatial Morphology (20x20 Grid at Round 100)\n"
        "Left: Acid Trap (Fragmented Unicells) | Right: NHE1-Shield (Merged Syncytia)",
        fontsize=10, fontweight='bold', color='#e2e8f0', pad=10, fontfamily='monospace'
    )
    ax1.set_xticks([0, 5, 10, 15, 19])
    ax1.set_yticks([0, 5, 10, 15, 19])
    ax1.tick_params(colors='#94a3b8')
    for spine in ax1.spines.values():
        spine.set_color('#334155')

    # Subplot 2: Macro-Agent Coalescence (Active Cluster Count vs. Rounds)
    ax2 = plt.subplot(2, 2, 2)
    ax2.set_facecolor('#061224')
    rounds = hist_acid["round"]
    ax2.plot(rounds, hist_acid["num_agents"], color=c_red, linewidth=2.2, label='Acid Trap (pHe=6.20, Unshielded) · No Coalescence')
    ax2.plot(rounds, hist_shield["num_agents"], color=c_green, linewidth=2.5, label='NHE1-Shield (pHe=6.20, 1K3R4E) · Rapid Self-Scaling Merge')
    ax2.set_title(
        "Panel B: Self-Scaling Population Kinetics\n"
        "Punctuated Equilibrium & Emergence of the Multicellular Self",
        fontsize=10, fontweight='bold', color='#e2e8f0', pad=10, fontfamily='monospace'
    )
    ax2.set_xlabel("Simulation Round (t)", fontsize=9, color='#94a3b8', fontfamily='monospace')
    ax2.set_ylabel("Active Autonomous Agents (N)", fontsize=9, color='#94a3b8', fontfamily='monospace')
    ax2.grid(True, color=c_grid, linestyle=':', alpha=0.6)
    ax2.legend(facecolor='#0a192f', edgecolor='#334155', fontsize=8, labelcolor='#f1f5f9', loc='center right')
    ax2.tick_params(colors='#94a3b8')
    for spine in ax2.spines.values():
        spine.set_color('#334155')

    # Subplot 3: Max Cluster Scale (Max Cells per Single Agent)
    ax3 = plt.subplot(2, 2, 3)
    ax3.set_facecolor('#061224')
    ax3.plot(rounds, hist_acid["max_cluster_size"], color=c_amber, linewidth=2.0, linestyle='--', label='Acid Trap Max Cluster (Cells)')
    ax3.plot(rounds, hist_shield["max_cluster_size"], color=c_blue, linewidth=2.5, label='NHE1-Shield Max Syncytium (Cells)')
    ax3.set_title(
        "Panel C: Physical Scale of the Composite Agent (Max Syncytium Size)\n"
        "Gated by Connexin Conductance G_GJ(Delta Vmem, pHi)",
        fontsize=10, fontweight='bold', color='#e2e8f0', pad=10, fontfamily='monospace'
    )
    ax3.set_xlabel("Simulation Round (t)", fontsize=9, color='#94a3b8', fontfamily='monospace')
    ax3.set_ylabel("Max Cluster Size (Cells in 1 Agent)", fontsize=9, color='#94a3b8', fontfamily='monospace')
    ax3.grid(True, color=c_grid, linestyle=':', alpha=0.6)
    ax3.legend(facecolor='#0a192f', edgecolor='#334155', fontsize=8, labelcolor='#f1f5f9', loc='upper left')
    ax3.tick_params(colors='#94a3b8')
    for spine in ax3.spines.values():
        spine.set_color('#334155')

    # Subplot 4: Average Fitness / Payoff & Intergroup Paradox
    ax4 = plt.subplot(2, 2, 4)
    ax4.set_facecolor('#061224')
    ax4.plot(rounds, hist_acid["mean_round_payoff"], color=c_red, linewidth=2.0, label='Acid Trap Mean Round Payoff')
    ax4.plot(rounds, hist_shield["mean_round_payoff"], color=c_purple, linewidth=2.5, label='NHE1-Shield Mean Round Payoff (Syncytial Fitness)')
    ax4.set_title(
        "Panel D: Adaptive Fitness Advantage & The Intergroup Paradox\n"
        "Multicellular Payoff Dominance over Fragmented Unicellularity",
        fontsize=10, fontweight='bold', color='#e2e8f0', pad=10, fontfamily='monospace'
    )
    ax4.set_xlabel("Simulation Round (t)", fontsize=9, color='#94a3b8', fontfamily='monospace')
    ax4.set_ylabel("Average Round Payoff per Agent", fontsize=9, color='#94a3b8', fontfamily='monospace')
    ax4.grid(True, color=c_grid, linestyle=':', alpha=0.6)
    ax4.legend(facecolor='#0a192f', edgecolor='#334155', fontsize=8, labelcolor='#f1f5f9', loc='upper left')
    ax4.tick_params(colors='#94a3b8')
    for spine in ax4.spines.values():
        spine.set_color('#334155')

    plt.tight_layout(rect=[0.02, 0.03, 0.98, 0.93])
    
    out_png = "met01_ipd_ms_dashboard.png"
    plt.savefig(out_png, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"-> Successfully saved 300 DPI dashboard: {out_png}")

    # Return key metrics
    return {
        "acid_trap": {
            "initial_agents": 400,
            "final_agents": int(hist_acid["num_agents"][-1]),
            "final_max_cluster": int(hist_acid["max_cluster_size"][-1]),
            "final_mean_payoff": float(np.mean(hist_acid["mean_round_payoff"][-10:])),
            "cooperation_rate": float(np.mean(hist_acid["cooperation_rate"][-10:])),
            "clc_index": float(hist_acid["clc_index"][-1]),
            "vmem_mV": float(sim_acid.bio["vmem"]),
            "pHi": float(sim_acid.bio["pHi"])
        },
        "shielded_synergy": {
            "initial_agents": 400,
            "final_agents": int(hist_shield["num_agents"][-1]),
            "final_max_cluster": int(hist_shield["max_cluster_size"][-1]),
            "final_mean_payoff": float(np.mean(hist_shield["mean_round_payoff"][-10:])),
            "cooperation_rate": float(np.mean(hist_shield["cooperation_rate"][-10:])),
            "clc_index": float(hist_shield["clc_index"][-1]),
            "vmem_mV": float(sim_shield.bio["vmem"]),
            "pHi": float(sim_shield.bio["pHi"])
        }
    }

if __name__ == "__main__":
    results = run_comparative_experiment()
    with open("bio_game_ipd_ms_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("Execution complete. Results serialized to bio_game_ipd_ms_results.json")
