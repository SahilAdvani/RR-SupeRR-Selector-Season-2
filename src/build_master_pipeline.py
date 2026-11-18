"""
build_master_pipeline.py - Orchestrates end-to-end data processing with:
1. Opposition Calibrated Quality weights
2. Role-Enforced Positional Filtering (preventing tailenders in batting lists)
3. Dual-Skill All-Rounder Evaluation (evaluating batting & bowling simultaneously)
4. Strict 2026 Recency & Retirement Filtering
"""
import os
import sys
import pandas as pd
import numpy as np

from data_loader import load_raw_data, merge_match_competition_context
from match_state import compute_cumulative_match_state
from pressure_model import compute_pressure_situation_index, TEAM_WEIGHTS
from metrics_batting import compute_batting_clutch_metrics
from metrics_bowling import compute_bowling_clutch_metrics

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_master_pipeline():
    print("--- 1. LOADING AND PREPARING DATASETS ---")
    data = load_raw_data()
    matches = merge_match_competition_context(data['matches'], data['competitions'])
    state = compute_cumulative_match_state(data['ball_by_ball'], matches)
    
    # Attach teams to state
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

    # 4. RECENT ACTIVITY & 2026 IPL PERFORMANCE (Dual-Skill)
    comps = data['competitions']
    m_df = psi_df.merge(matches[['match_id', 'comp_name', 'season']].drop_duplicates(), on='match_id')

    pe_m = pe[pe['is_played'] == True].merge(matches[['match_id', 'season', 'comp_name']], on='match_id')
    matches_2026 = pe_m[pe_m['season'] == '2026'].groupby('player_id')['match_id'].nunique().rename('matches_2026').reset_index()
    ipl_2026_matches = pe_m[pe_m['comp_name'] == 'IPL 2026'].groupby('player_id')['match_id'].nunique().rename('ipl26_caps').reset_index()

    ipl_2026_balls = m_df[(m_df['comp_name'] == 'IPL 2026')].copy()
    bat_2026 = ipl_2026_balls[~ipl_2026_balls['is_wide']].groupby('striker_id').agg(
        ipl26_runs=('runs', 'sum'),
        ipl26_balls=('runs', 'count')
    ).reset_index()
    bat_2026['ipl26_sr'] = (bat_2026['ipl26_runs'] / bat_2026['ipl26_balls']) * 100

    bowler_runs_mask = ~ipl_2026_balls['extras_type'].str.lower().isin(['byes', 'legbyes']).fillna(False)
    ipl_2026_balls['bowler_runs'] = (ipl_2026_balls['runs'] + ipl_2026_balls['extras1_runs'].fillna(0) + ipl_2026_balls['extras_2_runs'].fillna(0)).where(bowler_runs_mask, 0)
    bowler_wkt_mask = ipl_2026_balls['is_wicket'].fillna(False) & ~ipl_2026_balls['dismissal_type'].str.lower().isin(['runout', 'run out', 'retire out', 'obstructing the field', 'obstracting the field']).fillna(False)
    ipl_2026_balls['is_bowler_wkt'] = bowler_wkt_mask

    bowl_2026 = ipl_2026_balls.groupby('bowler_id').agg(
        ipl26_balls=('over_ball_num', 'count'),
        ipl26_runs_conceded=('bowler_runs', 'sum'),
        ipl26_wickets=('is_bowler_wkt', 'sum')
    ).reset_index()
    bowl_2026['ipl26_econ'] = (bowl_2026['ipl26_runs_conceded'] / (bowl_2026['ipl26_balls'] / 6.0))

    m_comp = data['player_mapping'].merge(comps, on='comp_id')
    ipl_2026 = m_comp[(m_comp['season'] == '2026') & (m_comp['comp_name_x'] == 'IPL 2026')][['player_id', 'player_name', 'team_name']].drop_duplicates().rename(columns={'team_name': 'ipl_2026_team'})
    ipl_played_ever = m_comp[m_comp['comp_name_x'].str.contains('IPL', case=False, na=False)]['player_id'].unique()
    pak_players = data['player_mapping'][data['player_mapping']['team_name'].str.contains('Pakistan', case=False, na=False)]['player_name'].unique()

    print("--- 3. COMPUTING OPPOSITION-CALIBRATED CLUTCH METRICS ---")
    batters = compute_batting_clutch_metrics(psi_df, min_pressure_balls=30, min_total_balls=100)
    bowlers = compute_bowling_clutch_metrics(psi_df, min_pressure_balls=30, min_total_balls=100)

    # 5. DUAL-SKILL RETENTION & CLASSIFICATION
    def enrich_master(df, p_id_col, p_name_col):
        d = df.rename(columns={p_id_col: 'player_id', p_name_col: 'player_name'})
        d = d.merge(roles[['player_id', 'player_role', 'median_batting_pos']], on='player_id', how='left')
        d = d.merge(ipl_2026, on=['player_id', 'player_name'], how='left')
        d = d.merge(matches_2026, on='player_id', how='left')
        d = d.merge(ipl_2026_matches, on='player_id', how='left')
        d = d.merge(bat_2026, left_on='player_id', right_on='striker_id', how='left')
        d = d.merge(bowl_2026, left_on='player_id', right_on='bowler_id', how='left')
        
        d['matches_2026'] = d['matches_2026'].fillna(0).astype(int)
        d['ipl26_caps'] = d['ipl26_caps'].fillna(0).astype(int)
        d['ipl26_runs'] = d['ipl26_runs'].fillna(0).astype(int)
        d['ipl26_sr'] = d['ipl26_sr'].fillna(0.0)
        d['ipl26_wickets'] = d['ipl26_wickets'].fillna(0).astype(int)
        d['ipl26_econ'] = d['ipl26_econ'].fillna(99.0)
        d['has_played_ipl'] = d['player_id'].isin(ipl_played_ever)
        d['is_pakistani'] = d['player_name'].isin(pak_players)
        
        def get_cat(r):
            if r['is_pakistani']:
                return 'Ineligible (Pakistani)'
            if r['matches_2026'] == 0:
                return 'Retired / Inactive (0 matches in 2026)'
            if r['ipl_2026_team'] == 'Rajasthan Royals':
                return 'Current RR Squad Player'
            if pd.isna(r['ipl_2026_team']):
                if r['has_played_ipl']:
                    return 'Existing IPL player, potentially available'
                else:
                    return 'Domestic / Int player without IPL contract'
            else: # In 2026 IPL squad
                # DUAL-SKILL RETENTION CHECK:
                bat_retained = (r['ipl26_runs'] >= 250) or (r['ipl26_caps'] >= 8 and r['ipl26_sr'] >= 145)
                bowl_retained = (r['ipl26_wickets'] >= 10) or (r['ipl26_caps'] >= 8 and r['ipl26_econ'] <= 8.5)
                
                if r['player_role'] == 'All-Rounder':
                    if bat_retained or bowl_retained:
                        return 'Existing IPL player, unlikely to be released'
                elif r['player_role'] == 'Batter':
                    if bat_retained:
                        return 'Existing IPL player, unlikely to be released'
                else: # Bowler
                    if bowl_retained:
                        return 'Existing IPL player, unlikely to be released'
                        
                if r['ipl26_caps'] <= 3:
                    return 'Emerging player with limited IPL exposure'
                else:
                    return 'Existing IPL player, potentially available'
        d['situation_category'] = d.apply(get_cat, axis=1)
        return d

    b_master = enrich_master(batters, 'striker_id', 'striker_name')
    bo_master = enrich_master(bowlers, 'bowler_id', 'bowler_name')

    # Export Master CSVs
    b_master.to_csv(os.path.join(OUTPUT_DIR, 'batters_auction_master.csv'), index=False)
    bo_master.to_csv(os.path.join(OUTPUT_DIR, 'bowlers_auction_master.csv'), index=False)

    # 6. ACTIONABLE SHORTLISTS WITH ROLE ENFORCEMENT
    actionable_cats = ['Emerging player with limited IPL exposure', 'Domestic / Int player without IPL contract', 'Existing IPL player, potentially available']
    
    # Batters List: MUST BE BATTER OR BATTING ALL-ROUNDER (median_batting_pos <= 7)
    top_10_batters = b_master[
        (b_master['player_role'].isin(['Batter', 'All-Rounder'])) & 
        (b_master['median_batting_pos'] <= 7) &
        (b_master['situation_category'].isin(actionable_cats))
    ].sort_values(by='CBI', ascending=False).drop_duplicates(subset=['player_id']).head(10).reset_index(drop=True)

    # Bowlers List: MUST BE BOWLER OR BOWLING ALL-ROUNDER
    top_10_bowlers = bo_master[
        (bo_master['player_role'].isin(['Bowler', 'All-Rounder'])) &
        (bo_master['situation_category'].isin(actionable_cats))
    ].sort_values(by='CBoI', ascending=False).drop_duplicates(subset=['player_id']).head(10).reset_index(drop=True)

    # Retained Benchmarks
    bench_batters = b_master[b_master['situation_category'] == 'Existing IPL player, unlikely to be released'].sort_values(by='CBI', ascending=False).head(5).reset_index(drop=True)
    bench_bowlers = bo_master[bo_master['situation_category'] == 'Existing IPL player, unlikely to be released'].sort_values(by='CBoI', ascending=False).head(5).reset_index(drop=True)

    top_10_batters.to_csv(os.path.join(OUTPUT_DIR, 'top_10_actionable_batters.csv'), index=False)
    top_10_bowlers.to_csv(os.path.join(OUTPUT_DIR, 'top_10_actionable_bowlers.csv'), index=False)
    bench_batters.to_csv(os.path.join(OUTPUT_DIR, 'benchmark_batters.csv'), index=False)
    bench_bowlers.to_csv(os.path.join(OUTPUT_DIR, 'benchmark_bowlers.csv'), index=False)

    print("\nMaster Pipeline Finished Successfully!")
    print(f"Actionable Batters (Role-Enforced): {len(top_10_batters)}")
    print(f"Actionable Bowlers (Role-Enforced): {len(top_10_bowlers)}")

if __name__ == '__main__':
    run_master_pipeline()
