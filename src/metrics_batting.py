"""
metrics_batting.py - Evaluates batting baseline vs high-pressure metrics,
scaled by opposition bowling quality, and applies Empirical Bayes shrinkage.
"""
import pandas as pd
import numpy as np

def compute_batting_clutch_metrics(df, min_pressure_balls=30, min_total_balls=100):
    """
    Computes opposition-calibrated batting metrics under baseline and pressure.
    """
    b_df = df[~df['is_wide']].copy()
    b_df['is_dot'] = (b_df['runs'] == 0) & (~b_df['is_wide'])
    b_df['is_boundary'] = b_df['runs'].isin([4, 6])
    b_df['is_dismissal'] = b_df['is_wicket_clean'] & (b_df['dismissed_player_id'] == b_df['striker_id'])
    
    # Opposition bowling quality weight
    if 'bowling_team_weight' in b_df.columns:
        b_df['opp_weight'] = b_df['bowling_team_weight']
    else:
        b_df['opp_weight'] = 1.0

    # 1. Overall Baseline Stats
    baseline = b_df.groupby(['striker_id', 'striker_name']).agg(
        total_balls=('runs', 'count'),
        total_runs=('runs', 'sum'),
        total_dots=('is_dot', 'sum'),
        total_boundaries=('is_boundary', 'sum'),
        mean_base_opp_weight=('opp_weight', 'mean')
    ).reset_index()
    
    baseline['base_sr'] = (baseline['total_runs'] / baseline['total_balls']) * 100.0
    baseline['base_dot_pct'] = (baseline['total_dots'] / baseline['total_balls']) * 100.0
    baseline['base_boundary_pct'] = (baseline['total_boundaries'] / baseline['total_balls']) * 100.0

    # 2. High-Pressure Stats (PSI >= 65)
    pressure = b_df[b_df['is_high_pressure']].groupby(['striker_id', 'striker_name']).agg(
        pressure_balls=('runs', 'count'),
        pressure_runs=('runs', 'sum'),
        pressure_dots=('is_dot', 'sum'),
        pressure_boundaries=('is_boundary', 'sum'),
        mean_press_opp_weight=('opp_weight', 'mean'),
        mean_psi=('PSI', 'mean')
    ).reset_index()
    
    pressure['press_sr'] = (pressure['pressure_runs'] / pressure['pressure_balls']) * 100.0
    pressure['press_dot_pct'] = (pressure['pressure_dots'] / pressure['pressure_balls']) * 100.0
    pressure['press_boundary_pct'] = (pressure['pressure_boundaries'] / pressure['pressure_balls']) * 100.0

    merged = baseline.merge(pressure, on=['striker_id', 'striker_name'], how='inner')
    qualified = merged[
        (merged['pressure_balls'] >= min_pressure_balls) & 
        (merged['total_balls'] >= min_total_balls)
    ].copy()

    # Raw Delta SR
    qualified['delta_sr'] = qualified['press_sr'] - qualified['base_sr']
    qualified['delta_dot_pct'] = qualified['base_dot_pct'] - qualified['press_dot_pct']

    # OPPOSITION QUALITY MULTIPLIER:
    # 1.15 is the Tier 1 international reference point.
    # Facing IPL/Top 6 yields > 1.0 multiplier; Associate attacks yield < 0.90 haircut.
    qualified['opp_quality_factor'] = (qualified['mean_press_opp_weight'] / 1.15).round(3)
    
    qualified['adj_press_sr'] = qualified['press_sr'] * qualified['opp_quality_factor']
    qualified['adj_delta_sr'] = qualified['delta_sr'] * qualified['opp_quality_factor']

    # Empirical Bayes Shrinkage for Adjusted Delta SR (K = 40 balls)
    mu_adj_delta = qualified['adj_delta_sr'].mean()
    K = 40.0
    qualified['shrinkage_weight'] = qualified['pressure_balls'] / (qualified['pressure_balls'] + K)
    qualified['shrunk_delta_sr'] = (qualified['shrinkage_weight'] * qualified['adj_delta_sr']) + ((1 - qualified['shrinkage_weight']) * mu_adj_delta)

    # Standardize components using z-scores
    def zscore(s):
        return (s - s.mean()) / (s.std() + 1e-6)

    z_shrunk_delta_sr = zscore(qualified['shrunk_delta_sr'])
    z_adj_press_sr = zscore(qualified['adj_press_sr'])
    z_dot_suppress = zscore(qualified['delta_dot_pct'] * qualified['opp_quality_factor'])
    z_press_bound = zscore(qualified['press_boundary_pct'] * qualified['opp_quality_factor'])

    raw_cbi = (
        0.40 * z_shrunk_delta_sr +
        0.30 * z_adj_press_sr +
        0.15 * z_dot_suppress +
        0.15 * z_press_bound
    )

    qualified['CBI'] = np.clip(50 + (raw_cbi * 15), 0, 100).round(2)
    return qualified.sort_values(by='CBI', ascending=False).reset_index(drop=True)
