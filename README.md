# Women's Football Scouting: Advanced Finishing & xG Analysis

An end-to-end data scouting project analyzing attacking performance and finishing efficiency for **Center Forwards** across women's football competitions using the StatsBomb event data format.

---

## 📌 Project Overview & Objectives

Traditional goal totals often misrepresent pure attacking ability due to team quality, variance, and small-sample luck. This project separates finishing luck from chance creation by analyzing:
- **Expected Goals (xG) vs. Actual Goals**: Quantifying raw volume against conversion quality.
- **Finishing Efficiency ($G - xG$)**: Identifying clinical finishers versus underperforming strikers.
- **Per 90 Normalization via Event Mining**: Accurately deriving exact on-pitch minutes from match event actions and substitutions rather than defaulting to inaccurate static 90-minute assumptions.

---

## 🛠️ Data Pipeline & Methodology

1. **Exact Playing Time Extraction (`src/player_minutes.py`)**:
   - Parses match actions and substitution events (`type == 'Substitution'`) to track true pitch time for both starters and bench players.
   - Saves a lightweight cache (`data/player_total_minutes.csv`) to decouple heavy minute calculation from visualization workflows.
2. **Scouting Summary Aggregation (`src/build_forward_summary.py`)**:
   - Isolates center forward actions and aggregates total shots, goals, and cumulative xG.
   - Exports an optimized summary dataset (`data/forward_scouting_summary.csv`), allowing downstream visualization scripts to execute instantly.
3. **Scouting Thresholds (Sample Reliability)**:
   - **Position**: `Center Forward`
   - **Playing Time**: Minimum 1,200 minutes played to capture regular starters (including elite performers like Khadija Shaw).
   - **Shot Volume**: Minimum 30 total shots or $xG \ge 0.1$ per 90.
4. **Presentation-Grade Visual Standards**:
   - Implements `adjustText` with automated pointer lines to eliminate overlapping labels.
   - Uses padded plot boundaries (`set_xlim`, `set_ylim`) so corner quadrant annotations and bar chart value labels remain fully legible without clipping.

---

## 📊 Key Visualizations & Findings

### 1. Striker Quadrant Analysis ($xG \text{ per } 90 \text{ vs. } \text{Goals per } 90$)
![xG vs Goals per 90](results/xg_vs_goals_per90.png)

- **The Outlier / Elite Volume**:
  - **Khadija Monifa Shaw** stands out as the sample's most dominant attacker, creating elite shot quality per 90 while consistently outscoring expected output.
  - **Lea Schüller** and **Sophia Olivia Wilson** rank among the highest volume creators, consistently generating quality opportunities against deep defensive blocks.
- **Quadrant Archetypes**:
  - Separates high-volume creators from clinical, lower-volume finishers and forwards navigating goal droughts.

---

### 2. Finishing Efficiency (Diverging Bar Chart: $G - xG$)
![Finishing Efficiency](results/best_xg_performers.png)

- **Clinical Overperformers ($G > xG$)**:
  - **Khadija Monifa Shaw** leads the dataset (+8.74 goals above expectation), followed by **Ana Marcos Moral** (+4.50) and **Elisabeth Terland** (+4.32), showcasing elite conversion rates from low-to-medium difficulty chances.
- **Market Opportunities / Underperformers ($G < xG$)**:
  - **Alessia Russo** and **Valentina Giacinti** register negative finishing deltas despite generating consistent underlying shot volume.
  - *Scouting Insight*: Often driven by variance or temporary finishing slumps. Strikers with sound underlying generation metrics represent undervalued transfer targets primed for positive regression to the mean.

---

## 📁 Repository Structure

```text
├── data/
│   ├── clean_match_events_lean.csv    # Filtered match events (local raw data)
│   ├── forward_scouting_summary.csv   # Aggregated forward statistics
│   ├── match_events.csv               # Raw StatsBomb event dump
│   ├── matches_data.csv               # Match metadata
│   └── player_total_minutes.csv       # Pre-computed playing time cache
├── results/
│   ├── best_xg_performers.png         # Diverging bar chart (Finishing efficiency G - xG)
│   ├── xg_vs_goals_per90.png          # Normalized per-90 quadrant scatter plot
│   └── xg_vs_goals.png                # Total volume quadrant scatter plot
├── src/
│   ├── best_xG_performers.py          # Script generating G - xG bar chart
│   ├── build_forward_summary.py       # Script creating aggregated forward dataset
│   ├── calculate_minutes.py           # Playing time extraction runner
│   ├── datadownload.py                # Dataset download utility
│   ├── dataprocessingagent.py         # Data processing helper
│   ├── goals_vs_xG_per90.py           # Script generating per-90 scatter plot
│   ├── goals_vs_xG.py                 # Script generating total volume scatter plot
│   └── player_minutes.py              # Playing time computation module
├── .gitignore                         # Git ignore configuration
└── README.md                          # Project documentation