import pandas as pd
import ast
import os

def safe_parse_coords(val):
    """
    Bezpečne naparsuje súradnice z formátu [x, y] alebo stringu na dvojicu floatov.
    Ošetrí NaN, None, prázdne stringy a neočakávané formáty.
    """
    if pd.isna(val) or val is None:
        return None, None
    
    if isinstance(val, (list, tuple)):
        coords = val
    elif isinstance(val, str):
        val_stripped = val.strip()
        if not val_stripped:
            return None, None
        try:
            coords = ast.literal_eval(val_stripped)
        except Exception:
            return None, None
    else:
        return None, None
    
    if isinstance(coords, (list, tuple)) and len(coords) >= 2:
        try:
            return float(coords[0]), float(coords[1])
        except (ValueError, TypeError):
            return None, None
            
    return None, None

def is_boolean_like(series):
    """
    Zistí, či stĺpec obsahuje booleovské alebo True/False hodnoty.
    """
    if pd.api.types.is_bool_dtype(series):
        return True
        
    non_na = series.dropna()
    if non_na.empty:
        return False
        
    unique_vals = set(non_na.unique())
    
    # Množiny reprezentujúce booleovské stavy
    bool_sets = [
        {True, False}, {True}, {False},
        {1.0, 0.0}, {1.0}, {0.0},
        {1, 0}, {1}, {0},
        {'True', 'False'}, {'True'}, {'False'},
        {'true', 'false'}, {'true'}, {'false'}
    ]
    return any(unique_vals.issubset(s) for s in bool_sets)

def count_true_values(series):
    """
    Spočíta výskyty hodnôt reprezentujúcich True.
    """
    return series.isin([True, 1, 1.0, 'True', 'true']).sum()

def main():
    input_file = 'clean_match_events_full.csv'
    output_file = 'clean_match_events_lean.csv'
    
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Vstupný súbor '{input_file}' neexistuje v aktuálnom adresári.")
        
    # Načítanie celého súboru
    df = pd.read_csv(input_file, low_memory=False)
    original_cols = list(df.columns)
    original_cols_count = len(original_cols)
    original_rows_count = len(df)
    
    # 1. Spracovanie a rozbalenie súradníc z pôvodných polí (ak existujú a nie sú rozbalené)
    coord_mappings = {
        'location': ('location_x', 'location_y'),
        'pass_end_location': ('pass_end_location_x', 'pass_end_location_y'),
        'shot_end_location': ('shot_end_location_x', 'shot_end_location_y')
    }
    
    for src, (tgt_x, tgt_y) in coord_mappings.items():
        if src in df.columns:
            parsed = df[src].apply(safe_parse_coords)
            df[tgt_x] = parsed.apply(lambda x: x[0] if x is not None else None)
            df[tgt_y] = parsed.apply(lambda x: x[1] if x is not None else None)
        else:
            # Ak zdrojový stĺpec nie je, zaistíme, že existujúce _x a _y sú aspoň pretypované na float
            for col in (tgt_x, tgt_y):
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

    # Identifikácia stĺpcov na vymazanie na základe nízkeho počtu True hodnôt
    dropped_due_to_scarcity = []
    for col in df.columns:
        if is_boolean_like(df[col]):
            true_count = count_true_values(df[col])
            if true_count < 50:
                dropped_due_to_scarcity.append(col)
                
    # Explicitne zmazané balastné stĺpce podla zadania
    explicit_drops = ['related_events', 'tactics', 'index', 'timestamp']
    
    # Spojenie zoznamov na vymazanie
    to_drop = set(dropped_due_to_scarcity + [col for col in explicit_drops if col in df.columns])
    
    # Odstránenie z df
    df_filtered = df.drop(columns=[col for col in to_drop if col in df.columns])
    
    # 2. Výber a zachovanie len relevantných metrík podľa zadania
    keep_cols_spec = [
        # Kontext
        'match_id', 'period', 'minute', 'second', 'team', 'player', 'position', 'type', 'play_pattern',
        # Súradnice
        'location_x', 'location_y', 'pass_end_location_x', 'pass_end_location_y', 'shot_end_location_x', 'shot_end_location_y',
        # Tlak a aktivita
        'under_pressure', 'counterpress',
        # Prihrávky
        'pass_length', 'pass_angle', 'pass_height', 'pass_body_part', 'pass_outcome', 'pass_recipient', 'pass_shot_assist', 'pass_cross',
        # Strely
        'shot_statsbomb_xg', 'shot_outcome', 'shot_type', 'shot_technique', 'shot_body_part'
    ]
    
    # Vo finálnom datasete ponecháme iba tie stĺpce, ktoré prežili predchádzajúci filter a sú v špecifikácii
    final_keep_cols = [col for col in keep_cols_spec if col in df_filtered.columns]
    df_lean = df_filtered[final_keep_cols].copy()
    
    # Určenie všetkých vymazaných stĺpcov oproti pôvodnému súboru
    deleted_cols = sorted(list(set(original_cols) - set(df_lean.columns)))
    
    # 3. Uloženie
    df_lean.to_csv(output_file, index=False)
    
    # Výstupy do konzoly
    print("--- DETEKCIA A ODSTRÁNENIE STĹPCOV ---")
    print(f"Počet stĺpcov odstránených kvôli nízkej frekvencii True (< 50): {len(set(dropped_due_to_scarcity))}")
    print(f"Stĺpce s nízkou frekvenciou True: {sorted(dropped_due_to_scarcity)}")
    print(f"Explicitne zmazané balastné stĺpce: {[c for c in explicit_drops if c in original_cols]}")
    print("\n--- KOMPLETNÝ ZOZNAM VYMAZANÝCH STĹPCOV ---")
    print(f"Celkovo vymazaných stĺpcov: {len(deleted_cols)}")
    print(deleted_cols)
    
    print("\n--- ŠTATISTIKY PROCESU ---")
    print(f"Pôvodný počet stĺpcov: {original_cols_count}")
    print(f"Finálny počet stĺpcov: {len(df_lean.columns)}")
    print(f"Finálny počet riadkov: {len(df_lean)}")
    print(f"Súbor úspešne uložený do: '{output_file}'")

if __name__ == '__main__':
    main()