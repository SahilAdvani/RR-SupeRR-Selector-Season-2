"""
pressure_model.py - Formulates continuous Pressure Situation Index (PSI)
incorporating dynamic match state, tournament leverage, and opposition caliber.
"""
import numpy as np
import pandas as pd

TEAM_WEIGHTS = {
    # Tier 1: IPL Franchises (pinnacle of T20 bowling & batting quality)
    'Chennai Super Kings': 1.25, 'Mumbai Indians': 1.25, 'Kolkata Knight Riders': 1.25,
    'Gujarat Titans': 1.25, 'Sunrisers Hyderabad': 1.25, 'Royal Challengers Bengaluru': 1.25,
    'Rajasthan Royals': 1.25, 'Delhi Capitals': 1.25, 'Lucknow Super Giants': 1.25, 'Punjab Kings': 1.25,
    
    # Tier 1 International: World Cup Winners & Top ICC teams
    'India': 1.20, 'Australia': 1.20, 'England': 1.20, 'South Africa': 1.15,
    'New Zealand': 1.15, 'Pakistan': 1.15, 'West Indies': 1.10,
    
    # Tier 2 International
    'Sri Lanka': 1.00, 'Bangladesh': 0.95, 'Afghanistan': 0.95,
    
    # A-Teams (Emerging Asia Cup / Rising Stars)
    'India A': 0.95, 'Pakistan A': 0.90, 'Sri Lanka A': 0.85, 'Bangladesh A': 0.85, 'Afghanistan A': 0.80,
    
    # Tier 3 International
    'Ireland': 0.80, 'Zimbabwe': 0.75, 'Netherlands': 0.75, 'Scotland': 0.75, 'United States Of America': 0.70,
    
    # Associate / Emerging Nations
    'United Arab Emirates': 0.65, 'Nepal': 0.60, 'Canada': 0.60, 'Oman': 0.60,
    'Hong Kong': 0.55, 'Kuwait': 0.50, 'Singapore': 0.50, 'Japan': 0.45
}

def compute_pressure_situation_index(df, teams_df=None):
    """
    Computes continuous PSI (0 - 100) per delivery.
    """
    data = df.copy()
    
    # Attach team weights if team tables provided
    if teams_df is not None:
        t_map = teams_df[['team_id', 'team_name']].drop_duplicates()
        if 'batting_team' not in data.columns:
            data = data.merge(t_map, left_on='batting_team_id', right_on='team_id', how='left').rename(columns={'team_name': 'batting_team'}).drop(columns=['team_id'], errors='ignore')
        if 'bowling_team' not in data.columns:
            data = data.merge(t_map, left_on='bowling_team_id', right_on='team_id', how='left').rename(columns={'team_name': 'bowling_team'}).drop(columns=['team_id'], errors='ignore')
            
    data['batting_team_weight'] = data['batting_team'].map(TEAM_WEIGHTS).fillna(1.0)
    data['bowling_team_weight'] = data['bowling_team'].map(TEAM_WEIGHTS).fillna(1.0)
    
    # ----------------- 2nd Innings Pressure Calculation -----------------
    rrr = data['rrr'].fillna(8.5)
    wih = data['wickets_in_hand']
    balls_rem = data['balls_remaining']
    
    rrr_factor = np.clip(rrr / 8.5, 0.4, 2.5)
    overs_rem = np.maximum(balls_rem / 6.0, 0.1)
    resource_strain = np.clip((11 - wih) / (overs_rem + 1.0), 0.5, 3.0)
    death_closeness = np.where(balls_rem <= 36, (36 - balls_rem) / 36.0 * 1.5, 0.5)
    
    inn2_raw_pressure = (rrr_factor * 25.0) + (resource_strain * 15.0) + (death_closeness * 20.0)
    
    # ----------------- 1st Innings Pressure Calculation -----------------
    balls_bowled = data['cum_legal_balls']
    overs_bowled = np.maximum(balls_bowled / 6.0, 0.1)
    wkts_lost = 10 - wih
    collapse_rate = wkts_lost / (overs_bowled + 1.0)
    collapse_factor = np.clip(collapse_rate / 0.4, 0.6, 2.5)
    
    phase_weight = np.where(data['phase'] == 'Death', 1.8,
                   np.where(data['phase'] == 'Powerplay', 1.1, 1.0))
    
    inn1_raw_pressure = (collapse_factor * 20.0) + (phase_weight * 22.0)
    
    base_pressure = np.where(data['innings'] == 2, inn2_raw_pressure, inn1_raw_pressure)
    context_multiplier = data['match_weight'].fillna(1.0)
    
    total_psi = base_pressure * context_multiplier
    data['PSI'] = np.clip(total_psi, 0, 100).round(2)
    data['is_high_pressure'] = data['PSI'] >= 65.0
    
    return data
