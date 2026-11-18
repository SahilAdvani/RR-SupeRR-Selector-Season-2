"""
generate_slide_visualizations.py
Creates bespoke, high-definition presentation graphics for the 15-slide SupeRR Selector deck.
Uses Seaborn + Matplotlib with custom theme styling matching the Rajasthan Royals branding:
- Primary Pink: #E91E63 / Royal Blue: #1E3A8A / Dark Navy: #0B132B / Accent Gold: #D97706
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs', 'figures')
os.makedirs(OUTPUT_DIR, exist_ok=True)

RR_PINK = '#E91E63'
RR_BLUE = '#1E3A8A'
RR_DARK = '#0B132B'
RR_GOLD = '#F59E0B'
RR_GRAY = '#64748B'

# Load data
q_bat = pd.read_csv('outputs/all_qualified_batters.csv')
q_bowl = pd.read_csv('outputs/all_qualified_bowlers.csv')
top_bat = pd.read_csv('outputs/official_top_10_batters.csv')
top_bowl = pd.read_csv('outputs/official_top_10_bowlers.csv')

# -------------------------------------------------------------
# 1. Slide 4: Pressure Phase Distribution & Threshold (PSI Curves)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
# Generate synthetic PSI curves across overs for 3 match states
overs = np.linspace(1, 20, 200)
psi_chase_high = 40 + 55 / (1 + np.exp(-(overs - 13) / 1.8))
psi_chase_low = 30 + 35 / (1 + np.exp(-(overs - 14) / 2.5))
psi_inn1 = 25 + 40 / (1 + np.exp(-(overs - 15) / 2.0))

ax.plot(overs, psi_chase_high, color=RR_PINK, lw=3, label='Steep Chase (RRR >= 11.5, 4+ Wickets Down)')
ax.plot(overs, psi_chase_low, color=RR_BLUE, lw=2.5, ls='--', label='Controlled Chase (RRR ~ 8.5, 2 Wickets Down)')
ax.plot(overs, psi_inn1, color=RR_GOLD, lw=2.5, ls='-.', label='1st Innings Top-Order Crisis (3 wkts in PP)')

ax.axhline(65, color=RR_DARK, lw=2, ls=':', label='High-Pressure Clutch Zone Threshold (PSI >= 65.0)')
ax.fill_between(overs, 65, 100, color=RR_PINK, alpha=0.12, label='Clutch Zone (Top 15.5% Decisions)')

ax.set_title("Dynamic Pressure Situation Index (PSI) Trajectories Across Overs", fontsize=14, fontweight='bold', pad=12, color=RR_DARK)
ax.set_xlabel("Match Over (1 to 20)", fontsize=11, fontweight='bold', color=RR_DARK)
ax.set_ylabel("Pressure Situation Index (0 to 100)", fontsize=11, fontweight='bold', color=RR_DARK)
ax.set_xlim(1, 20)
ax.set_ylim(20, 100)
ax.legend(frameon=True, facecolor='white', framealpha=0.95, fontsize=9.5, loc='upper left')
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'slide4_psi_trajectories.png'))
plt.close()

# -------------------------------------------------------------
# 2. Slide 6: Batting High Absolute Power vs Delta SR
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
scatter = ax.scatter(q_bat['base_sr'], q_bat['raw_press_sr'], c=q_bat['Ensemble_CBI'], cmap='coolwarm', s=q_bat['press_balls']*0.8, alpha=0.75, edgecolors='black', lw=0.5)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Final CBI Score (Bayesian Shrunk)', fontsize=10, fontweight='bold')

# Diagonal line
ax.plot([110, 200], [110, 200], color='gray', ls='--', lw=1.5, label='Equal Rate Line (Press SR = Base SR)')

# Annotate Top 10 Batters
for _, r in top_bat.iterrows():
    ax.annotate(r['player_name'], (r['base_sr'], r['raw_press_sr']),
                xytext=(5, 5), textcoords='offset points', fontsize=8.5, fontweight='bold', color=RR_DARK)

ax.set_title("Batting High-Ceiling Output vs Baseline: Resolving the Delta Bias", fontsize=14, fontweight='bold', pad=12, color=RR_DARK)
ax.set_xlabel("Baseline Career Strike Rate (Normal Situations)", fontsize=11, fontweight='bold', color=RR_DARK)
ax.set_ylabel("Pressure Strike Rate (PSI >= 65)", fontsize=11, fontweight='bold', color=RR_DARK)
ax.legend(loc='lower right', frameon=True)
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'slide6_batter_power_vs_baseline.png'))
plt.close()

# -------------------------------------------------------------
# 3. Slide 7: Bowler Economy Suppression vs Baseline
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
scatter = ax.scatter(q_bowl['base_econ'], q_bowl['raw_press_econ'], c=q_bowl['Ensemble_CBoI'], cmap='viridis_r', s=q_bowl['press_balls']*0.6, alpha=0.8, edgecolors='black', lw=0.5)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Final CBoI Score (Bayesian Shrunk)', fontsize=10, fontweight='bold')

ax.plot([6, 11], [6, 11], color='red', ls='--', lw=1.5, label='Par Suppression Line')

for _, r in top_bowl.iterrows():
    ax.annotate(r['player_name'], (r['base_econ'], r['raw_press_econ']),
                xytext=(5, 4), textcoords='offset points', fontsize=8.5, fontweight='bold', color=RR_DARK)

ax.set_title("Bowler Economy Under Pressure vs Baseline: Isolating Elite Choke Assets", fontsize=14, fontweight='bold', pad=12, color=RR_DARK)
ax.set_xlabel("Baseline Career Economy (All Situations)", fontsize=11, fontweight='bold', color=RR_DARK)
ax.set_ylabel("Pressure Economy (PSI >= 65)", fontsize=11, fontweight='bold', color=RR_DARK)
ax.legend(loc='lower right', frameon=True)
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'slide7_bowler_suppression.png'))
plt.close()

# -------------------------------------------------------------
# 4. Slide 8: Bayesian Shrinkage Illustration (k=50)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 4.8), dpi=300)
n_balls = np.linspace(10, 500, 300)
reliability = n_balls / (n_balls + 50)

ax.plot(n_balls, reliability, color=RR_PINK, lw=3, label='Reliability Weight r = N / (N + 50)')
ax.axvline(80, color=RR_GRAY, ls=':', lw=1.5, label='Min Qualification Floor (80 balls, r=0.615)')
ax.axvline(250, color=RR_BLUE, ls='--', lw=1.5, label='Medium Veteran Sample (250 balls, r=0.833)')
ax.axvline(420, color=RR_GOLD, ls='-.', lw=1.5, label='Elite Sample (420 balls: Bumrah, Pathirana, r=0.894)')

ax.set_title("Bayesian Reliability Curve: Regressing Small-Sample Noise Towards Population Mean", fontsize=13, fontweight='bold', pad=12, color=RR_DARK)
ax.set_xlabel("High-Pressure Deliveries (Faced or Bowled)", fontsize=11, fontweight='bold', color=RR_DARK)
ax.set_ylabel("Reliability Factor (r)", fontsize=11, fontweight='bold', color=RR_DARK)
ax.set_ylim(0, 1.0)
ax.legend(loc='lower right', frameon=True)
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'slide8_bayesian_reliability.png'))
plt.close()

# -------------------------------------------------------------
# 5. Slide 9: Top 10 Batters Horizontal Bar Chart (Final CBI)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
sorted_bat = top_bat.sort_values(by='Ensemble_CBI', ascending=True)
bars = ax.barh(sorted_bat['player_name'], sorted_bat['Ensemble_CBI'], color=RR_PINK, edgecolor=RR_DARK, lw=0.8, alpha=0.9)

for bar in bars:
    w = bar.get_width()
    ax.text(w - 3.8, bar.get_y() + bar.get_height()/2, f"{w:.2f}", ha='center', va='center', color='white', fontweight='bold', fontsize=9.5)

ax.set_title("Official Top 10 Batters Under Pressure (Final Consensus CBI)", fontsize=14, fontweight='bold', pad=12, color=RR_DARK)
ax.set_xlabel("Consensus Clutch Batting Index (CBI Score)", fontsize=11, fontweight='bold', color=RR_DARK)
ax.set_xlim(50, 70)
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'slide9_top10_batters_bar.png'))
plt.close()

# -------------------------------------------------------------
# 6. Slide 11: Top 10 Bowlers Horizontal Bar Chart (Final CBoI)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
sorted_bowl = top_bowl.sort_values(by='Ensemble_CBoI', ascending=True)
bars = ax.barh(sorted_bowl['player_name'], sorted_bowl['Ensemble_CBoI'], color=RR_BLUE, edgecolor=RR_DARK, lw=0.8, alpha=0.9)

for bar in bars:
    w = bar.get_width()
    ax.text(w - 3.8, bar.get_y() + bar.get_height()/2, f"{w:.2f}", ha='center', va='center', color='white', fontweight='bold', fontsize=9.5)

ax.set_title("Official Top 10 Bowlers Under Pressure (Final Consensus CBoI)", fontsize=14, fontweight='bold', pad=12, color=RR_DARK)
ax.set_xlabel("Consensus Clutch Bowling Index (CBoI Score)", fontsize=11, fontweight='bold', color=RR_DARK)
ax.set_xlim(50, 72)
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'slide11_top10_bowlers_bar.png'))
plt.close()

print("All slide visualizations generated successfully in outputs/figures/!")
