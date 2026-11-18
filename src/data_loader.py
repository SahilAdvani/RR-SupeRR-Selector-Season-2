"""
data_loader.py - Ingests and cleans official Rajasthan Royals SupeRR Selector datasets.
"""
import os
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data_pack', 'Data Pack')

def load_raw_data(data_dir=DATA_DIR):
    """Loads all CSV tables from the data pack."""
    print("Loading datasets from:", data_dir)
    matches = pd.read_csv(os.path.join(data_dir, 'matches.csv'))
    competitions = pd.read_csv(os.path.join(data_dir, 'competitions.csv'))
    ball_by_ball = pd.read_csv(os.path.join(data_dir, 'ball_by_ball.csv'))
    playing_eleven = pd.read_csv(os.path.join(data_dir, 'playing_eleven.csv'))
    teams = pd.read_csv(os.path.join(data_dir, 'teams.csv'))
    player_mapping = pd.read_csv(os.path.join(data_dir, 'competition_team_player_mapping.csv'))
    
    print(f"Loaded: matches ({len(matches)}), ball_by_ball ({len(ball_by_ball)}), competitions ({len(competitions)})")
    return {
        'matches': matches,
        'competitions': competitions,
        'ball_by_ball': ball_by_ball,
        'playing_eleven': playing_eleven,
        'teams': teams,
        'player_mapping': player_mapping
    }

def merge_match_competition_context(matches, competitions):
    """Enriches matches with competition format, season, and tier weights."""
    m = matches.copy()
    c = competitions[['comp_id', 'comp_name', 'match_format', 'season']].copy()
    m = m.merge(c, on='comp_id', how='left')
    
    # Competition Tier categorization
    def get_comp_tier(row):
        name = str(row['comp_name']).lower()
        if 'ipl' in name or 'indian premier league' in name:
            return 'IPL', 1.25  # Highest quality domestic/franchise league in the world
        elif 'world cup' in name or 't20 world cup' in name:
            return 'T20_WC', 1.20 # Highest international stakes
        elif 'asia cup' in name:
            return 'T20I_TIER1', 1.10
        else:
            return 'T20I_BILATERAL', 1.00 # Standard international bilaterals

    tiers_weights = m.apply(get_comp_tier, axis=1)
    m['comp_tier'] = [tw[0] for tw in tiers_weights]
    m['comp_weight'] = [tw[1] for tw in tiers_weights]
    
    # Knockout stage multiplier
    m['is_knockout'] = m['knock_out'].fillna(False).astype(bool)
    m['match_weight'] = m['comp_weight'] * np.where(m['is_knockout'], 1.15, 1.0)
    
    return m

if __name__ == '__main__':
    data = load_raw_data()
    enriched_matches = merge_match_competition_context(data['matches'], data['competitions'])
    print("Match tier distribution:\n", enriched_matches['comp_tier'].value_counts())

