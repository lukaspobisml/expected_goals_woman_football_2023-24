import pandas as pd
from player_minutes import calculate_exact_minutes

# Načítame dáta
data = pd.read_csv('clean_match_events_lean.csv', low_memory=False)

# Spočítame minúty pomocou nášho modulu
minutes_df = calculate_exact_minutes(data)

# Uložimo ich do samostatného datasetu
minutes_df.to_csv('player_total_minutes.csv', index=False)
print('Dataset player_total_minutes.csv bol úspešne vytvorený!')