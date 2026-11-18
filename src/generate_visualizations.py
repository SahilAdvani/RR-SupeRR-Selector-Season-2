"""
generate_visualizations.py - Generates publication-grade figures for the Ensemble Clutch Models.
"""
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from data_loader import load_raw_data, merge_match_competition_context
from match_state import compute_cumulative_match_state
from pressure_model import compute_pressure_situation_index

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs')
FIGURES_DIR = os.path.join(OUTPUT_DIR, 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)

def plot_psi_distribution(df):
    plt.figure(figsize=(9, 4.8))
    palette = {'Powerplay': '#2b5c8f', 'Middle': '#d97724', 'Death': '#b82525'}
    
    for phase, color in palette.items():
        subset = df[df['phase'] == phase]['PSI'].dropna()
        sns.kdeplot(subset, label=f'{phase} Overs', color=color, fill=True, alpha=0.3, linewidth=2)
    
    plt.axvline(65, color='black', linestyle='--', linewidth=1.5, label='High-Pressure Cutoff (PSI=65)')
    plt.title('Pressure Situation Index (PSI) Distribution Across Match Phases', fontsize=13, weight='bold', pad=12)
    plt.xlabel('Pressure Situation Index (0 - 100)', fontsize=11)
    plt.ylabel('Density', fontsize=11)
    plt.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'psi_distribution.png'))
    plt.close()
    print("Saved psi_distribution.png")

def plot_batting_clutch_quadrant(top_batters, all_batters):
    plt.figure(figsize=(10, 6.8))
    
    # Background qualified cohort
    plt.scatter(
        all_batters['base_sr'], all_batters['raw_press_sr'],
        s=all_batters['press_balls'] * 0.4,
        c='#CBD5E1', alpha=0.45, edgecolors='none', label='Qualified T20 Batters Cohort'
    )

    # Top 10 Batters
    scatter = plt.scatter(
        top_batters['base_sr'], top_batters['raw_press_sr'],
        s=top_batters['press_balls'] * 1.3,
        c=top_batters['Ensemble_CBI'], cmap='viridis', alpha=0.9, edgecolors='black', linewidth=1.2, label='Top 10 Consensus Clutch Batters'
    )
    cbar = plt.colorbar(scatter)
    cbar.set_label('Royals Consensus Clutch Index (CBI)', fontsize=10)
    
    for _, row in top_batters.iterrows():
        plt.annotate(row['player_name'], (row['base_sr'], row['raw_press_sr']), xytext=(6, 4), textcoords='offset points', fontsize=9, weight='bold', color='#1E3A8A')
        
    lims = [125, 210]
    plt.plot(lims, lims, '--', color='gray', alpha=0.6, label='Baseline Parity (ΔSR = 0)')
    
    plt.title('Batting Clutch Matrix: Baseline SR vs. High-Pressure SR (Size ~ High-Pressure Balls)', fontsize=13, weight='bold', pad=14)
    plt.xlabel('Baseline Strike Rate (Overall Career)', fontsize=11)
    plt.ylabel('High-Pressure Strike Rate (PSI ≥ 65)', fontsize=11)
    plt.legend(loc='upper left', frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'batting_clutch_quadrant.png'))
    plt.close()
    print("Saved batting_clutch_quadrant.png")

def plot_bowling_clutch_quadrant(top_bowlers, all_bowlers):
    plt.figure(figsize=(10, 6.8))
    
    # Background qualified cohort
    plt.scatter(
        all_bowlers['base_econ'], all_bowlers['raw_press_econ'],
        s=all_bowlers['press_balls'] * 0.4,
        c='#CBD5E1', alpha=0.45, edgecolors='none', label='Qualified T20 Bowlers Cohort'
    )

    # Top 10 Bowlers
    scatter = plt.scatter(
        top_bowlers['base_econ'], top_bowlers['raw_press_econ'],
        s=top_bowlers['press_balls'] * 1.3,
        c=top_bowlers['Ensemble_CBoI'], cmap='magma', alpha=0.9, edgecolors='black', linewidth=1.2, label='Top 10 Consensus Clutch Bowlers'
    )
    cbar = plt.colorbar(scatter)
    cbar.set_label('Royals Consensus Clutch Index (CBoI)', fontsize=10)
    
    for _, row in top_bowlers.iterrows():
        plt.annotate(row['player_name'], (row['base_econ'], row['raw_press_econ']), xytext=(6, 4), textcoords='offset points', fontsize=9, weight='bold', color='#991B1B')
        
    lims = [5.5, 11.5]
    plt.plot(lims, lims, '--', color='gray', alpha=0.6, label='Baseline Parity')
    
    plt.title('Bowling Clutch Matrix: Baseline Econ vs. High-Pressure Econ (Size ~ High-Pressure Balls)', fontsize=13, weight='bold', pad=14)
    plt.xlabel('Baseline Economy (Overall Career)', fontsize=11)
    plt.ylabel('High-Pressure Economy (Lower is Better, PSI ≥ 65)', fontsize=11)
    plt.legend(loc='lower right', frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'bowling_clutch_quadrant.png'))
    plt.close()
    print("Saved bowling_clutch_quadrant.png")

def generate_all_visualizations():
    data = load_raw_data()
    matches = merge_match_competition_context(data['matches'], data['competitions'])
    state = compute_cumulative_match_state(data['ball_by_ball'], matches)
    
    teams = data['teams'][['team_id', 'team_name']].drop_duplicates()
    state = state.merge(teams, left_on='batting_team_id', right_on='team_id', how='left').rename(columns={'team_name': 'batting_team'}).drop(columns=['team_id'], errors='ignore')
    state = state.merge(teams, left_on='bowling_team_id', right_on='team_id', how='left').rename(columns={'team_name': 'bowling_team'}).drop(columns=['team_id'], errors='ignore')
    
    psi_df = compute_pressure_situation_index(state, data['teams'])
    plot_psi_distribution(psi_df)
    
    top_b = pd.read_csv(os.path.join(OUTPUT_DIR, 'official_top_10_batters.csv'))
    all_b = pd.read_csv(os.path.join(OUTPUT_DIR, 'all_qualified_batters.csv'))
    plot_batting_clutch_quadrant(top_b, all_b)
    
    top_bo = pd.read_csv(os.path.join(OUTPUT_DIR, 'official_top_10_bowlers.csv'))
    all_bo = pd.read_csv(os.path.join(OUTPUT_DIR, 'all_qualified_bowlers.csv'))
    plot_bowling_clutch_quadrant(top_bo, all_bo)
    print("All visualizations created successfully!")

if __name__ == '__main__':
    generate_all_visualizations()
