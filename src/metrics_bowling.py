"""
metrics_bowling.py - Evaluates bowling baseline vs high-pressure metrics,
scaled by opposition batting lineup quality, and applies Empirical Bayes shrinkage.
"""
import pandas as pd
import numpy as np

def compute_bowling_clutch_metrics(df, min_pressure_balls=30, min_total_balls=100):
    """
    Computes opposition-calibrated bowling metrics under baseline and pressure.
    """
    b_df = df.copy()
    
    # Opposition batting quality weight
    if 'batting_team_weight' in b_df.columns:
        b_df['opp_weight'] = b_df['batting_team_weight']
    else:
        b_df['opp_weight'] = 1.0

    bowler_runs_mask = ~b_df['extras_type'].str.lower().isin(['byes', 'legbyes']).fillna(False)
    b_df['bowler_runs_conceded'] = np.where(bowler_runs_mask, b_df['runs'] + b_df['extras1_runs'] + b_df['extras_2_runs'], 0)
    
    bowler_wkt_mask = b_df['is_wicket_clean'] & ~b_df['dismissal_type'].str.lower().isin(['runout', 'run out', 'retire out', 'obstructing the field', 'obstracting the field']).fillna(False)
    b_df['is_bowler_wicket'] = bowler_wkt_mask
    b_df['is_bowler_dot'] = (b_df['bowler_runs_conceded'] == 0) & b_df['is_legal_ball']
    b_df['is_bowler_boundary'] = b_df['runs'].isin([4, 6])

    # 1. Overall Baseline Stats
    baseline = b_df.groupby(['bowler_id', 'bowler_name']).agg(
        total_balls=('is_legal_ball', 'sum'),
        total_runs_conceded=('bowler_runs_conceded', 'sum'),
        total_wickets=('is_bowler_wicket', 'sum'),
        total_dots=('is_bowler_dot', 'sum'),
        mean_base_opp_weight=('opp_weight', 'mean')
    ).reset_index()
    
    baseline['base_econ'] = (baseline['total_runs_conceded'] / (baseline['total_balls'] / 6.0))
    baseline['base_wkt_pct'] = (baseline['total_wickets'] / baseline['total_balls']) * 100.0
    baseline['base_dot_pct'] = (baseline['total_dots'] / baseline['total_balls']) * 100.0

    # 2. High-Pressure Stats (PSI >= 65)
    pressure = b_df[b_df['is_high_pressure']].groupby(['bowler_id', 'bowler_name']).agg(
        pressure_balls=('is_legal_ball', 'sum'),
        pressure_runs_conceded=('bowler_runs_conceded', 'sum'),
        pressure_wickets=('is_bowler_wicket', 'sum'),
        pressure_dots=('is_bowler_dot', 'sum'),
        mean_press_opp_weight=('opp_weight', 'mean'),
        mean_psi=('PSI', 'mean')
    ).reset_index()
    
    pressure['press_econ'] = (pressure['pressure_runs_conceded'] / (pressure['pressure_balls'] / 6.0))
    pressure['press_wkt_pct'] = (pressure['pressure_wickets'] / pressure['pressure_balls']) * 100.0
    pressure['press_dot_pct'] = (pressure['pressure_dots'] / pressure['pressure_balls']) * 100.0

    merged = baseline.merge(pressure, on=['bowler_id', 'bowler_name'], how='inner')
    qualified = merged[
        (merged['pressure_balls'] >= min_pressure_balls) & 
        (merged['total_balls'] >= min_total_balls)
    ].copy()

    cohort_econ_shift = pressure['press_econ'].median() - baseline['base_econ'].median()
    qualified['raw_delta_econ'] = (qualified['base_econ'] + cohort_econ_shift) - qualified['press_econ']
    qualified['raw_delta_wkt'] = qualified['press_wkt_pct'] - qualified['base_wkt_pct']

    # OPPOSITION QUALITY MULTIPLIER:
    qualified['opp_quality_factor'] = (qualified['mean_press_opp_weight'] / 1.15).round(3)
    
    # Bowlers bowling against IPL/Tier 1 batting lineups receive credit; against associates, high economy is penalized
    qualified['adj_delta_econ'] = qualified['raw_delta_econ'] * qualified['opp_quality_factor']
    qualified['adj_press_wkt_pct'] = qualified['press_wkt_pct'] * qualified['opp_quality_factor']
    qualified['adj_press_econ'] = qualified['press_econ'] / qualified['opp_quality_factor']

    # Empirical Bayes Shrinkage for Delta Economy (K = 40 balls)
    mu_adj_delta = qualified['adj_delta_econ'].mean()
    K = 40.0
    qualified['shrinkage_weight'] = qualified['pressure_balls'] / (qualified['pressure_balls'] + K)
    qualified['shrunk_delta_econ'] = (qualified['shrinkage_weight'] * qualified['adj_delta_econ']) + ((1 - qualified['shrinkage_weight']) * mu_adj_delta)

    def zscore(s):
        return (s - s.mean()) / (s.std() + 1e-6)

    z_shrunk_delta_econ = zscore(qualified['shrunk_delta_econ'])
    z_press_econ_inv = -1.0 * zscore(qualified['adj_press_econ'])
    z_press_wkt = zscore(qualified['adj_press_wkt_pct'])
    z_press_dot = zscore(qualified['press_dot_pct'] * qualified['opp_quality_factor'])

    raw_cboi = (
        0.35 * z_shrunk_delta_econ +
        0.25 * z_press_econ_inv +
        0.25 * z_press_wkt +
        0.15 * z_press_dot
    )

    qualified['CBoI'] = np.clip(50 + (raw_cboi * 15), 0, 100).round(2)
    return qualified.sort_values(by='CBoI', ascending=False).reset_index(drop=True)
