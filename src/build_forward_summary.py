import pandas as pd
import numpy as np

# Load clean events and pre-computed minutes from data/
data = pd.read_csv('data/clean_match_events_lean.csv', low_memory=False)
player_mins = pd.read_csv('data/player_total_minutes.csv')

# Filter shots for Center Forwards
shots = data[(data['type'] == 'Shot') & (data['position'] == 'Center Forward')].copy()
shots['is_goal'] = np.where(shots['shot_outcome'] == 'Goal', 1, 0)

# Aggregate offensive metrics
summary = shots.groupby(['player', 'team', 'position']).agg(
    total_shots=('type', 'count'),
    total_goals=('is_goal', 'sum'),
    total_xg=('shot_statsbomb_xg', 'sum')
).reset_index()

# Merge with minutes played
summary = pd.merge(summary, player_mins[['player', 'exact_minutes']], on='player', how='inner')

# Save lightweight dataset into data/
summary.to_csv('data/forward_scouting_summary.csv', index=False)
print(f"Done! Saved {len(summary)} forwards to data/forward_scouting_summary.csv")