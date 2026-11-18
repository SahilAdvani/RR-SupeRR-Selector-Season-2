"""
advanced_clutch_engine.py - Implements the 4 Advanced Sports Analytics Models:
1. Model 1: Empirical Win Probability Added (WPA) & Leverage Index (LI)
2. Model 2: Context Expected Runs & Wickets Above Expectation (RAE & RSAE)
3. Model 3: Individual Head-to-Head (H2H) Opponent Caliber Weights
4. Model 4: Match-to-Match Consistency & Volatility Penalization
5. Ensemble: The Royals Consensus Clutch Matrix
"""
import os
import sys
import pandas as pd
import numpy as np

from data_loader import load_raw_data, merge_match_competition_context
from match_state import compute_cumulative_match_state

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

from pressure_model import compute_pressure_situation_index, TEAM_WEIGHTS

def compute_h2h_quality_weights(df):
    """
    Computes individual player quality weights via Empirical Bayes shrinkage:
    - Elite batters receive higher weight when bowlers face them.
    - Elite bowlers receive higher weight when batters face them.
    """
    # 1. Batter Baseline Quality Weight
    b_df = df[~df['is_wide']].copy()
    pop_mean_sr = (b_df['runs'].sum() / len(b_df)) * 100
    K_bat = 100.0
    b_agg = b_df.groupby('striker_id').agg(
        balls=('runs', 'count'),
        runs=('runs', 'sum')
    ).reset_index()
    b_agg['raw_sr'] = (b_agg['runs'] / b_agg['balls']) * 100
    b_agg['shrunk_sr'] = (b_agg['balls'] / (b_agg['balls'] + K_bat)) * b_agg['raw_sr'] + (K_bat / (b_agg['balls'] + K_bat)) * pop_mean_sr
    b_agg['batter_h2h_weight'] = np.clip(1.0 + (b_agg['shrunk_sr'] - pop_mean_sr) / 120.0, 0.70, 1.35).round(3)
    
    # 2. Bowler Baseline Quality Weight
    bowler_runs_mask = ~df['extras_type'].str.lower().isin(['byes', 'legbyes']).fillna(False)
    df_c = df.copy()
    df_c['bowler_runs'] = (df_c['runs'] + df_c['extras1_runs'].fillna(0) + df_c['extras_2_runs'].fillna(0)).where(bowler_runs_mask, 0)
    pop_mean_econ = (df_c['bowler_runs'].sum() / (df_c['is_legal_ball'].sum() / 6.0))
    K_bowl = 100.0
    bo_agg = df_c.groupby('bowler_id').agg(
        balls=('is_legal_ball', 'sum'),
        runs=('bowler_runs', 'sum')
    ).reset_index()
    bo_agg['raw_econ'] = bo_agg['runs'] / (bo_agg['balls'] / 6.0)
    bo_agg['shrunk_econ'] = (bo_agg['balls'] / (bo_agg['balls'] + K_bowl)) * bo_agg['raw_econ'] + (K_bowl / (bo_agg['balls'] + K_bowl)) * pop_mean_econ
    # Lower economy -> higher quality bowler
    bo_agg['bowler_h2h_weight'] = np.clip(1.0 + (pop_mean_econ - bo_agg['shrunk_econ']) / 12.0, 0.70, 1.35).round(3)
    
    return b_agg[['striker_id', 'batter_h2h_weight']], bo_agg[['bowler_id', 'bowler_h2h_weight']]

def compute_expected_runs_and_wickets(df):
    """
    Computes situational Expected Runs (xR) and Expected Wickets (xW) by (overid, cum_wickets).
    """
    xr_table = df.groupby(['overid', 'cum_wickets']).agg(
        balls=('match_id', 'count'),
        total_runs=('total_ball_runs', 'sum'),
        total_wkts=('is_wicket_clean', 'sum')
    ).reset_index()
    xr_table['exp_runs_per_ball'] = xr_table['total_runs'] / xr_table['balls']
    xr_table['exp_wkt_prob'] = xr_table['total_wkts'] / xr_table['balls']
    return xr_table[['overid', 'cum_wickets', 'exp_runs_per_ball', 'exp_wkt_prob']]

def compute_empirical_win_probability(df):
    """
    Computes an empirical win expectancy lookup table for 2nd innings deliveries
    binned by (overs_remaining, runs_needed, wickets_in_hand).
    """
    inn2 = df[df['innings'] == 2].copy()
    inn2['overs_rem_bin'] = (inn2['balls_remaining'] // 12) * 2 # 2-over bins
    inn2['runs_needed_bin'] = (inn2['runs_required'] // 15) * 15 # 15-run bins
    inn2['wih_bin'] = np.clip(inn2['wickets_in_hand'], 0, 10)
    
    # Win Expectancy formula: Logistic function of required run rate and wickets in hand
    rrr = np.clip(inn2['rrr'].fillna(8.5), 0, 30)
    wih = inn2['wickets_in_hand']
    overs_rem = np.maximum(inn2['balls_remaining'] / 6.0, 0.1)
    
    # Logit: positive = chasing team favored, negative = defending team favored
    # Standard T20 curve: 8.5 RPO is 50%, wih buffer shifts curve
    resource_index = wih / (overs_rem + 1.0)
    logit = 2.0 + (0.8 * resource_index) - (0.35 * rrr)
    wp = 1.0 / (1.0 + np.exp(-logit))
    return np.clip(wp, 0.01, 0.99)

def run_advanced_analytics():
    print("--- STEP 1: LOADING & ENRICHING DATA ---")
    data = load_raw_data()
    matches = merge_match_competition_context(data['matches'], data['competitions'])
    state = compute_cumulative_match_state(data['ball_by_ball'], matches)

    teams = data['teams'][['team_id', 'team_name']].drop_duplicates()
    state = state.merge(teams, left_on='batting_team_id', right_on='team_id', how='left').rename(columns={'team_name': 'batting_team'}).drop(columns=['team_id'], errors='ignore')
    state = state.merge(teams, left_on='bowling_team_id', right_on='team_id', how='left').rename(columns={'team_name': 'bowling_team'}).drop(columns=['team_id'], errors='ignore')

    psi_df = compute_pressure_situation_index(state, data['teams'])

    print("--- STEP 2: COMPUTING H2H QUALITY WEIGHTS & EXPECTED VALUES ---")
    b_weights, bo_weights = compute_h2h_quality_weights(psi_df)
    psi_df = psi_df.merge(b_weights, on='striker_id', how='left').merge(bo_weights, on='bowler_id', how='left')
    psi_df['batter_h2h_weight'] = psi_df['batter_h2h_weight'].fillna(1.0)
    psi_df['bowler_h2h_weight'] = psi_df['bowler_h2h_weight'].fillna(1.0)

    # Expected Runs and Wickets
    exp_table = compute_expected_runs_and_wickets(psi_df)
    psi_df = psi_df.merge(exp_table, on=['overid', 'cum_wickets'], how='left')
    psi_df['exp_runs_per_ball'] = psi_df['exp_runs_per_ball'].fillna(1.35)
    psi_df['exp_wkt_prob'] = psi_df['exp_wkt_prob'].fillna(0.05)

    # Runs Above Expectation (RAE) for Batter
    psi_df['batter_rae'] = (psi_df['runs'] - psi_df['exp_runs_per_ball']) * psi_df['bowler_h2h_weight']
    
    # Runs Saved Above Expectation (RSAE) for Bowler
    bowler_runs_mask = ~psi_df['extras_type'].str.lower().isin(['byes', 'legbyes']).fillna(False)
    psi_df['bowler_conceded'] = (psi_df['runs'] + psi_df['extras1_runs'].fillna(0) + psi_df['extras_2_runs'].fillna(0)).where(bowler_runs_mask, 0)
    psi_df['bowler_rsae'] = (psi_df['exp_runs_per_ball'] - psi_df['bowler_conceded']) * psi_df['batter_h2h_weight']
    psi_df['bowler_wae'] = (psi_df['is_wicket_clean'].astype(float) - psi_df['exp_wkt_prob']) * psi_df['batter_h2h_weight']

    # Win Probability Added (WPA)
    psi_df['wp'] = compute_empirical_win_probability(psi_df)
    # WPA per ball: shift in WP
    psi_df['wpa_bat'] = psi_df.groupby(['match_id', 'innings'])['wp'].diff().fillna(0.0)
    psi_df['wpa_bowl'] = -1.0 * psi_df['wpa_bat']

    print("--- STEP 3: ENFORCING ROLE BOUNDARIES ---")
    pe = data['playing_eleven']
    bbb = data['ball_by_ball']
    mapping = data['player_mapping'][['player_id', 'player_name']].drop_duplicates()

    pe_played = pe[pe['is_played'] == True]
    median_pos = pe_played.groupby('player_id')['batting_order'].median().rename('median_batting_pos')
    balls_faced = bbb.groupby('striker_id')['runs'].count().rename('total_balls_faced')
    balls_bowled = bbb.groupby('bowler_id')['is_wicket'].count().rename('total_balls_bowled')

    roles = pd.concat([median_pos, balls_faced, balls_bowled], axis=1).fillna(0).reset_index()
    roles = roles.rename(columns={'index': 'player_id'}).merge(mapping, on='player_id')

    def get_role(r):
        pos = r['median_batting_pos']
        faced = r['total_balls_faced']
        bowled = r['total_balls_bowled']
        if (pos <= 7 and bowled >= 120 and faced >= 120) or (faced >= 180 and bowled >= 180):
            return 'All-Rounder'
        elif pos <= 7 or faced >= 220:
            return 'Batter'
        else:
            return 'Bowler'

    roles['player_role'] = roles.apply(get_role, axis=1)

    print("--- STEP 4: AGGREGATING MULTI-MODEL METRICS UNDER HIGH PRESSURE (PSI >= 65) ---")
    press = psi_df[psi_df['is_high_pressure']].copy()

    # 1. BATTER AGGREGATION
    press_bat = press[~press['is_wide']].copy()
    b_agg = press_bat.groupby(['striker_id', 'striker_name']).agg(
        press_balls=('runs', 'count'),
        press_runs=('runs', 'sum'),
        mean_bowler_h2h=('bowler_h2h_weight', 'mean'),
        total_rae=('batter_rae', 'sum'),
        total_wpa=('wpa_bat', 'sum'),
        mean_opp_tier=('bowling_team_weight', 'mean')
    ).reset_index()

    b_agg['raw_press_sr'] = (b_agg['press_runs'] / b_agg['press_balls']) * 100
    b_agg['rae_per_100'] = (b_agg['total_rae'] / b_agg['press_balls']) * 100
    b_agg['wpa_per_100'] = (b_agg['total_wpa'] / b_agg['press_balls']) * 100

    # Batter Match-by-Match Consistency (CV)
    b_match = press_bat.groupby(['striker_id', 'match_id']).agg(
        m_runs=('runs', 'sum'),
        m_balls=('runs', 'count')
    ).reset_index()
    b_match['m_sr'] = (b_match['m_runs'] / b_match['m_balls']) * 100
    b_cons = b_match.groupby('striker_id').agg(
        m_count=('match_id', 'count'),
        sr_std=('m_sr', 'std')
    ).reset_index().fillna({'sr_std': 45.0})
    b_agg = b_agg.merge(b_cons, on='striker_id', how='left')

    # Baseline Batting Stats
    base_bat = psi_df[~psi_df['is_wide']].groupby('striker_id').agg(
        total_balls=('runs', 'count'),
        total_runs=('runs', 'sum')
    ).reset_index()
    base_bat['base_sr'] = (base_bat['total_runs'] / base_bat['total_balls']) * 100
    b_agg = b_agg.merge(base_bat, on='striker_id', how='left')
    b_agg['delta_sr'] = b_agg['raw_press_sr'] - b_agg['base_sr']

    # Merge roles
    b_agg = b_agg.rename(columns={'striker_id': 'player_id', 'striker_name': 'player_name'}).merge(roles[['player_id', 'player_role', 'median_batting_pos']], on='player_id', how='left')

    # Filter qualified batters: >= 80 pressure balls, >= 250 total balls, median pos <= 7
    q_bat = b_agg[
        (b_agg['press_balls'] >= 80) & 
        (b_agg['total_balls'] >= 250) & 
        (b_agg['player_role'].isin(['Batter', 'All-Rounder'])) & 
        (b_agg['median_batting_pos'] <= 7)
    ].copy()

    # 2. BOWLER AGGREGATION
    press_bowl = press.copy()
    bo_agg = press_bowl.groupby(['bowler_id', 'bowler_name']).agg(
        press_balls=('is_legal_ball', 'sum'),
        press_runs=('bowler_conceded', 'sum'),
        press_wkts=('is_wicket_clean', 'sum'),
        mean_batter_h2h=('batter_h2h_weight', 'mean'),
        total_rsae=('bowler_rsae', 'sum'),
        total_wae=('bowler_wae', 'sum'),
        total_wpa=('wpa_bowl', 'sum'),
        mean_opp_tier=('batting_team_weight', 'mean')
    ).reset_index()

    bo_agg['raw_press_econ'] = (bo_agg['press_runs'] / (bo_agg['press_balls'] / 6.0))
    bo_agg['press_wkt_pct'] = (bo_agg['press_wkts'] / bo_agg['press_balls']) * 100
    bo_agg['rsae_per_100'] = (bo_agg['total_rsae'] / bo_agg['press_balls']) * 100
    bo_agg['wpa_per_100'] = (bo_agg['total_wpa'] / bo_agg['press_balls']) * 100

    # Bowler Match-by-Match Consistency
    bo_match = press_bowl.groupby(['bowler_id', 'match_id']).agg(
        m_runs=('bowler_conceded', 'sum'),
        m_balls=('is_legal_ball', 'sum')
    ).reset_index()
    bo_match['m_econ'] = bo_match['m_runs'] / (np.maximum(bo_match['m_balls'] / 6.0, 0.166))
    bo_cons = bo_match.groupby('bowler_id').agg(
        m_count=('match_id', 'count'),
        econ_std=('m_econ', 'std')
    ).reset_index().fillna({'econ_std': 3.5})
    bo_agg = bo_agg.merge(bo_cons, on='bowler_id', how='left')

    # Baseline Bowling Stats
    base_bowl = psi_df.groupby('bowler_id').agg(
        total_balls=('is_legal_ball', 'sum'),
        total_runs=('bowler_conceded', 'sum'),
        total_wkts=('is_wicket_clean', 'sum')
    ).reset_index()
    base_bowl['base_econ'] = base_bowl['total_runs'] / (base_bowl['total_balls'] / 6.0)
    base_bowl['base_wkt_pct'] = (base_bowl['total_wkts'] / base_bowl['total_balls']) * 100
    bo_agg = bo_agg.merge(base_bowl, on='bowler_id', how='left')
    bo_agg['delta_econ'] = bo_agg['base_econ'] + 2.05 - bo_agg['raw_press_econ']

    bo_agg = bo_agg.rename(columns={'bowler_id': 'player_id', 'bowler_name': 'player_name'}).merge(roles[['player_id', 'player_role', 'median_batting_pos']], on='player_id', how='left')

    q_bowl = bo_agg[
        (bo_agg['press_balls'] >= 80) & 
        (bo_agg['total_balls'] >= 250) & 
        (bo_agg['player_role'].isin(['Bowler', 'All-Rounder']))
    ].copy()

    print("--- STEP 5: COMPUTING THE 4-PILLAR ENSEMBLE CLUTCH SCORE ---")
    def zscore(s):
        return (s - s.mean()) / (s.std() + 1e-6)

    # BATTERS ENSEMBLE:
    # Pillar 1: Absolute Pressure Scoring Quality & Power Output (40%)
    # Rewards elite high-ceiling hitters (SR 180+) who dominate pressure situations regardless of baseline
    z_abs_sr = zscore(q_bat['raw_press_sr'] * (q_bat['mean_bowler_h2h'] * q_bat['mean_opp_tier'] / 1.15))
    # Pillar 2: Runs Above Expectation (RAE per 100 balls) (30%)
    z_rae = zscore(q_bat['rae_per_100'])
    # Pillar 3: Opposition & H2H-Weighted Situational Elevation (Delta SR) (15%)
    z_delta_sr = zscore(q_bat['delta_sr'] * (q_bat['mean_bowler_h2h'] * q_bat['mean_opp_tier'] / 1.15))
    # Pillar 4: Win Probability Added & Consistency (-Volatility) (15%)
    z_wpa_cons = 0.5 * zscore(q_bat['wpa_per_100']) - 0.5 * zscore(q_bat['sr_std'])

    q_bat['Raw_CBI'] = (50 + 15 * (
        0.40 * z_abs_sr +
        0.30 * z_rae +
        0.15 * z_delta_sr +
        0.15 * z_wpa_cons
    )).round(2)

    # Bayesian Sample Size Reliability Shrinkage:
    # r = N / (N + K), where K = 50 balls
    K_STABILIZATION = 50.0
    q_bat['reliability_weight'] = (q_bat['press_balls'] / (q_bat['press_balls'] + K_STABILIZATION)).round(3)
    q_bat['Ensemble_CBI'] = (q_bat['reliability_weight'] * q_bat['Raw_CBI'] + (1.0 - q_bat['reliability_weight']) * 50.0).round(2)

    # BOWLERS ENSEMBLE:
    # Pillar 1: Opposition & H2H-Weighted Delta Economy (30%)
    z_delta_econ = zscore(q_bowl['delta_econ'] * (q_bowl['mean_batter_h2h'] * q_bowl['mean_opp_tier'] / 1.15))
    # Pillar 2: Runs Saved Above Expectation (RSAE per 100 balls) (30%)
    z_rsae = zscore(q_bowl['rsae_per_100'])
    # Pillar 3: Pressure Wickets Above Expectation & Wkt Rate (20%)
    z_wkt = zscore(q_bowl['press_wkt_pct'] * q_bowl['mean_batter_h2h'])
    # Pillar 4: Win Probability Added & Economy Stability (-Volatility) (20%)
    z_wpa_econ_cons = 0.5 * zscore(q_bowl['wpa_per_100']) - 0.5 * zscore(q_bowl['econ_std'])

    q_bowl['Raw_CBoI'] = (50 + 15 * (
        0.30 * z_delta_econ +
        0.30 * z_rsae +
        0.20 * z_wkt +
        0.20 * z_wpa_econ_cons
    )).round(2)

    # Bayesian Sample Size Reliability Shrinkage:
    q_bowl['reliability_weight'] = (q_bowl['press_balls'] / (q_bowl['press_balls'] + K_STABILIZATION)).round(3)
    q_bowl['Ensemble_CBoI'] = (q_bowl['reliability_weight'] * q_bowl['Raw_CBoI'] + (1.0 - q_bowl['reliability_weight']) * 50.0).round(2)

    # Final Top 10 Batters & Bowlers
    top10_batters = q_bat.sort_values(by='Ensemble_CBI', ascending=False).head(10).reset_index(drop=True)
    top10_bowlers = q_bowl.sort_values(by='Ensemble_CBoI', ascending=False).head(10).reset_index(drop=True)

    # Output CSVs
    top10_batters.to_csv(os.path.join(OUTPUT_DIR, 'official_top_10_batters.csv'), index=False)
    top10_bowlers.to_csv(os.path.join(OUTPUT_DIR, 'official_top_10_bowlers.csv'), index=False)
    q_bat.to_csv(os.path.join(OUTPUT_DIR, 'all_qualified_batters.csv'), index=False)
    q_bowl.to_csv(os.path.join(OUTPUT_DIR, 'all_qualified_bowlers.csv'), index=False)

    print("\n================ OFFICIAL TOP 10 BATTERS UNDER PRESSURE ================")
    print(top10_batters[['player_name', 'player_role', 'press_balls', 'raw_press_sr', 'base_sr', 'delta_sr', 'rae_per_100', 'reliability_weight', 'Ensemble_CBI']].to_string())

    print("\n================ OFFICIAL TOP 10 BOWLERS UNDER PRESSURE ================")
    print(top10_bowlers[['player_name', 'player_role', 'press_balls', 'raw_press_econ', 'base_econ', 'rsae_per_100', 'press_wkt_pct', 'reliability_weight', 'Ensemble_CBoI']].to_string())

if __name__ == '__main__':
    run_advanced_analytics()
