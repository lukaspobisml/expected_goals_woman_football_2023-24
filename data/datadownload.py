import pandas as pd
from statsbombpy import sb

target_leagues = [
    {"competition_id": 37, "season_id": 281},  # WSL
    {"competition_id": 131, "season_id": 281}, # Serie A
    {"competition_id": 135, "season_id": 281}, # Bundesliga
    {"competition_id": 182, "season_id": 281}, # Liga F
    {"competition_id": 49, "season_id": 107},  # NWSL
]

print("Sťahujem zoznam zápasov...")
all_matches = []
for league in target_leagues:
    matches_df = sb.matches(competition_id=league["competition_id"], season_id=league["season_id"])
    all_matches.append(matches_df)

combined_matches = pd.concat(all_matches, ignore_index=True)
combined_matches = combined_matches.drop_duplicates(subset=['match_id'])
combined_matches.to_csv("matches_data.csv", index=False)
print("Zoznam zápasov bol uložený.")

print("Sťahujem udalosti (events) zápasov...")
sample_match_ids = combined_matches['match_id'].tolist()

all_events = []
for m_id in sample_match_ids:
    try:
        match_events = sb.events(match_id=m_id)
        all_events.append(match_events)
    except Exception as e:
        print(f"Chyba pri sťahovaní zápasu {m_id}: {e}")

if all_events:
    combined_events = pd.concat(all_events, ignore_index=True)
    
    # OPRAVA: Duplicity budeme kontrolovať iba podľa unikátneho ID udalosti ('id'),
    # čím sa vyhneme chybám so stĺpcami obsahujúcimi slovníky (dict).
    if 'id' in combined_events.columns:
        combined_events = combined_events.drop_duplicates(subset=['id'])
    else:
        combined_events = combined_events.drop_duplicates()
    
    # Uloženie vyčistených eventov
    combined_events.to_csv("match_events.csv", index=False)
    print(f"Úspešne spracovaných a uložených {len(combined_events)} udalostí do 'match_events.csv'.")

print("Hotovo! Dáta sú úspešne spracované.")
