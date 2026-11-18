"""
generate_official_rankings.py - Generates the official Top 10 Batters and Top 10 Bowlers
under pressure based strictly on Round 1 specifications (unrestricted by auction availability),
incorporating Opposition Calibrated Quality and Positional Role Enforcement.
"""
import os
import sys
import pandas as pd
import numpy as np

from data_loader import load_raw_data, merge_match_competition_context
from match_state import compute_cumulative_match_state
from pressure_model import compute_pressure_situation_index
from metrics_batting import compute_batting_clutch_metrics
from metrics_bowling import compute_bowling_clutch_metrics

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_official_rankings():
    print("--- 1. LOADING DATA AND RECONSTRUCTING MATCH STATE ---")
    data = load_raw_data()
    matches = merge_match_competition_context(data['matches'], data['competitions'])
    state = compute_cumulative_match_state(data['ball_by_ball'], matches)

    teams = data['teams'][['team_id', 'team_name']].drop_duplicates()
    state = state.merge(teams, left_on='batting_team_id', right_on='team_id', how='left').rename(columns={'team_name': 'batting_team'}).drop(columns=['team_id'], errors='ignore')
    state = state.merge(teams, left_on='bowling_team_id', right_on='team_id', how='left').rename(columns={'team_name': 'bowling_team'}).drop(columns=['team_id'], errors='ignore')

    print("--- 2. COMPUTING OPPOSITION-WEIGHTED PSI ---")
    psi_df = compute_pressure_situation_index(state, data['teams'])

    pe = data['playing_eleven']
    bbb = data['ball_by_ball']
    mapping = data['player_mapping'][['player_id', 'player_name']].drop_duplicates()

    # 3. PLAYER ROLE EXTRACTION (from playing eleven and career volume)
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

    print("--- 3. COMPUTING OPPOSITION-CALIBRATED CLUTCH METRICS ---")
    # Robust sample size thresholds: >= 80 pressure deliveries, >= 250 total deliveries
    batters = compute_batting_clutch_metrics(psi_df, min_pressure_balls=80, min_total_balls=250)
    bowlers = compute_bowling_clutch_metrics(psi_df, min_pressure_balls=80, min_total_balls=250)

    batters = batters.rename(columns={'striker_id': 'player_id', 'striker_name': 'player_name'}).merge(roles[['player_id', 'player_role', 'median_batting_pos']], on='player_id', how='left')
    bowlers = bowlers.rename(columns={'bowler_id': 'player_id', 'bowler_name': 'player_name'}).merge(roles[['player_id', 'player_role', 'median_batting_pos']], on='player_id', how='left')

    # Positional filter for batters: Must be top/middle order (median_batting_pos <= 7)
    top_10_batters = batters[(batters['player_role'].isin(['Batter', 'All-Rounder'])) & (batters['median_batting_pos'] <= 7)].drop_duplicates(subset=['player_id']).sort_values(by='CBI', ascending=False).head(10).reset_index(drop=True)

    # Positional filter for bowlers: Must be regular bowler
    top_10_bowlers = bowlers[bowlers['player_role'].isin(['Bowler', 'All-Rounder'])].drop_duplicates(subset=['player_id']).sort_values(by='CBoI', ascending=False).head(10).reset_index(drop=True)

    top_10_batters.to_csv(os.path.join(OUTPUT_DIR, 'official_top_10_batters.csv'), index=False)
    top_10_bowlers.to_csv(os.path.join(OUTPUT_DIR, 'official_top_10_bowlers.csv'), index=False)
    batters.to_csv(os.path.join(OUTPUT_DIR, 'all_qualified_batters.csv'), index=False)
    bowlers.to_csv(os.path.join(OUTPUT_DIR, 'all_qualified_bowlers.csv'), index=False)

    print("\n--- OFFICIAL TOP 10 BATTERS UNDER PRESSURE ---")
    print(top_10_batters[['player_name', 'player_role', 'pressure_balls', 'press_sr', 'base_sr', 'delta_sr', 'adj_press_sr', 'opp_quality_factor', 'CBI']].to_string())

    print("\n--- OFFICIAL TOP 10 BOWLERS UNDER PRESSURE ---")
    print(top_10_bowlers[['player_name', 'player_role', 'pressure_balls', 'press_econ', 'base_econ', 'adj_press_econ', 'press_wkt_pct', 'opp_quality_factor', 'CBoI']].to_string())

if __name__ == '__main__':
    generate_official_rankings()
