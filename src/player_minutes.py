import numpy as np
import pandas as pd


def calculate_exact_minutes(data: pd.DataFrame) -> pd.DataFrame:
  df = data.copy()
  match_player_minutes = []

  for match_id in df['match_id'].dropna().unique():
    match_df = df[df['match_id'] == match_id]

    active_players = (
        match_df[match_df['player'].notna() & match_df['position'].notna()][
            ['player', 'team', 'position']
        ]
        .drop_duplicates()
        .to_dict('records')
    )

    for p_info in active_players:
      p = p_info['player']
      t = p_info['team']
      pos = p_info['position']

      player_events = match_df[match_df['player'] == p]
      first_min = player_events['minute'].min()
      mins = 90 if first_min <= 5 else (90 - first_min)

      player_sub_out = match_df[
          (match_df['type'].astype(str).str.contains('Sub', case=False, na=False))
          & (match_df['player'] == p)
      ]
      if not player_sub_out.empty:
        sub_min = player_sub_out.iloc[0].get('minute')
        if not pd.isna(sub_min):
          mins = sub_min

      match_player_minutes.append({
          'match_id': match_id,
          'player': p,
          'team': t,
          'position': pos,
          'minutes_played': max(1, min(90, mins)),
      })

  if not match_player_minutes:
    return pd.DataFrame(columns=['player', 'team', 'exact_minutes'])

  minutes_df = pd.DataFrame(match_player_minutes)
  total_minutes = (
      minutes_df.groupby(['player', 'team'])['minutes_played']
      .sum()
      .reset_index()
  )
  total_minutes.rename(columns={'minutes_played': 'exact_minutes'}, inplace=True)

  return total_minutes