"""
match_state.py - Reconstructs ball-by-ball dynamic match state, target calculations,
wickets in hand, and runs required.
"""
import pandas as pd
import numpy as np

def compute_cumulative_match_state(bbb, matches):
    """
    Computes exact situational state for each ball:
    - cumulative score in innings
    - cumulative wickets fallen
    - legal balls bowled & legal balls remaining
    - target score and required run rate (for 2nd innings)
    - current run rate (CRR)
    """
    df = bbb.copy()
    
    # Sort strictly chronologically within each match and innings
    df = df.sort_values(by=['match_id', 'innings', 'overid', 'over_ball_num']).reset_index(drop=True)
    
    # Total runs conceded on this ball: batter runs + extras
    # In BBB: 'runs' is batter runs. 'extras1_runs' + 'extras_2_runs' are extras.
    df['extras1_runs'] = df['extras1_runs'].fillna(0).astype(int)
    df['extras_2_runs'] = df['extras_2_runs'].fillna(0).astype(int)
    df['total_ball_runs'] = df['runs'] + df['extras1_runs'] + df['extras_2_runs']
    
    # Is it a legal ball? (Wides and No-balls / Overstep are NOT legal balls for over completion)
    df['is_wide'] = df['extras_type'].str.lower().eq('wide').fillna(False)
    df['is_noball'] = df['extras_type'].str.lower().isin(['overstep', 'no ball', 'noball']).fillna(False)
    df['is_legal_ball'] = ~(df['is_wide'] | df['is_noball'])
    
    # Wicket count
    df['is_wicket_clean'] = df['is_wicket'].fillna(False).astype(bool)
    
    # Group by match and innings to compute cumulative progressions
    match_inn = df.groupby(['match_id', 'innings'])
    
    df['cum_runs'] = match_inn['total_ball_runs'].cumsum()
    df['cum_wickets'] = match_inn['is_wicket_clean'].cumsum()
    df['cum_legal_balls'] = match_inn['is_legal_ball'].cumsum()
    
    # Innings 1 max legal balls is typically 120 (unless revised)
    # Merge revised overs from matches
    match_meta = matches[['match_id', 'first_inn_revised_overs', 'second_inn_revised_overs', 'revised_target', 'match_weight', 'comp_tier', 'is_knockout']].copy()
    df = df.merge(match_meta, on='match_id', how='left')
    
    # Determine total allotted overs per innings
    df['allotted_overs'] = np.where(
        df['innings'] == 1,
        df['first_inn_revised_overs'].fillna(20.0),
        df['second_inn_revised_overs'].fillna(20.0)
    )
    # Ensure standard minimum 20 if 0 or NaN
    df['allotted_overs'] = np.where(df['allotted_overs'] <= 0, 20.0, df['allotted_overs'])
    df['total_allotted_balls'] = (df['allotted_overs'] * 6).astype(int)
    
    df['balls_remaining'] = np.maximum(0, df['total_allotted_balls'] - df['cum_legal_balls'])
    df['wickets_in_hand'] = np.maximum(0, 10 - df['cum_wickets'])
    
    # Current Run Rate (CRR)
    df['overs_bowled'] = df['cum_legal_balls'] / 6.0
    df['crr'] = np.where(df['overs_bowled'] > 0, df['cum_runs'] / df['overs_bowled'], 0.0)
    
    # Calculate Innings 1 final score to establish Target for Innings 2
    inn1_totals = df[df['innings'] == 1].groupby('match_id')['cum_runs'].max().rename('inn1_final_score')
    df = df.merge(inn1_totals, on='match_id', how='left')
    
    # Target score: revised_target if present, else inn1_final_score + 1
    df['target_score'] = np.where(
        df['revised_target'].notna() & (df['revised_target'] > 0),
        df['revised_target'],
        df['inn1_final_score'] + 1
    )
    
    # Runs required in Innings 2
    df['runs_required'] = np.where(
        df['innings'] == 2,
        np.maximum(0, df['target_score'] - df['cum_runs']),
        np.nan
    )
    
    # Required Run Rate (RRR)
    overs_rem = df['balls_remaining'] / 6.0
    df['rrr'] = np.where(
        (df['innings'] == 2) & (overs_rem > 0),
        df['runs_required'] / overs_rem,
        np.nan
    )
    # Cap RRR to sensible maximum for numerical stability (e.g. 36)
    df['rrr'] = df['rrr'].clip(lower=0.0, upper=36.0)
    
    # Define Match Phase: Powerplay (overs 1-6), Middle (7-15), Death (16-20)
    df['phase'] = pd.cut(
        df['overid'],
        bins=[0, 6, 15, 25],
        labels=['Powerplay', 'Middle', 'Death'],
        right=True
    )
    
    return df

if __name__ == '__main__':
    from data_loader import load_raw_data, merge_match_competition_context
    data = load_raw_data()
    matches = merge_match_competition_context(data['matches'], data['competitions'])
    state_df = compute_cumulative_match_state(data['ball_by_ball'], matches)
    print("Match state computed successfully! Sample 2nd innings:")
    sample = state_df[state_df['innings'] == 2][['match_id', 'overid', 'cum_runs', 'wickets_in_hand', 'target_score', 'runs_required', 'rrr', 'balls_remaining']].head(10)
    print(sample)

