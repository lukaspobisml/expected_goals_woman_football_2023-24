Women's Football Scouting: Advanced Finishing & xG AnalysisAn end-to-end data analytics and scouting project evaluating attacking profiles, finishing efficiency, and chance creation for Center Forwards across women's football competitions using StatsBomb open-data event format.📌 Project Overview & ObjectivesTraditional goal tallies often mask underlying performance due to small sample sizes, tactical variances, and conversion luck. This project decouples finishing form from chance creation by:Normalizing shot volumes and expected metrics via true playing minutes derived directly from match substitution events.Comparing Total Expected Goals ($xG$) vs. Actual Goals across seasons.Evaluating Per 90 metrics ($xG/90$ vs. $\text{Goals}/90$) to assess true productivity rates.Quantifying Finishing Efficiency ($G - xG$) through diverging bar charts to isolate clinical finishers from players experiencing temporary conversion slumps.🛠️ Data Pipeline & ArchitectureTo avoid expensive recalculations and eliminate reliance on heavy raw event datasets during visualization, the pipeline uses a decoupled, modular design across data/, src/, and results/:Exact Playing Time Mining (src/player_minutes.py):Parses match actions and substitution events (type == 'Substitution') to track true pitch time for both starting players and substitutes.Outputs a persistent lookup table: data/player_total_minutes.csv.Scouting Summary Aggregation (src/build_forward_summary.py):Isolates center forward actions and aggregates total shots, goals, and cumulative $xG$ from data/clean_match_events_lean.csv.Merges with data/player_total_minutes.csv to output data/forward_scouting_summary.csv (~a few KB), making all visualization scripts completely independent of massive event logs.Sample Reliability Filters:Position: Center ForwardPlaying Time: Minimum 1,200 minutes played (ensures regular starters and high-impact attackers like Khadija Shaw are captured while filtering out micro-samples).Shot Threshold: Minimum 30 shots or active offensive output ($xG/90 \ge 0.1$).Dynamic Label Placement & Collision Avoidance:Integrated adjustText with directional pointer lines and expanded plot margins (set_xlim, set_ylim) to prevent collisions between player labels, bar values, and quadrant category cards.📊 Key Visualizations & Scouting Insights1. Normalized Striker Quadrants ($xG \text{ per } 90 \text{ vs. } \text{Goals per } 90$)The Outlier / Elite Volume:Khadija Monifa Shaw stands out as the sample's most dominant attacker, creating top-tier shot quality per 90 while maintaining a conversion rate well above expectation.Lea Schüller and Sophia Olivia Wilson consistently lead high-volume threat creation, remaining persistent offensive focal points against deep defensive structures.Role Profiling:Quadrants clearly distinguish between primary high-volume outlets, clinical poachers operating on lower volume, and forwards suffering from finishing slumps.2. Finishing Efficiency (Diverging Bar Chart: $G - xG$)Clinical Overperformers ($G > xG$):Khadija Monifa Shaw leads the dataset ($+8.74$), followed by Ana Marcos Moral ($+4.50$) and Elisabeth Terland ($+4.32$), showcasing elite conversion rates from low-to-medium difficulty chances.Market Opportunity / Underperformers ($G < xG$):Alessia Russo and Valentina Giacinti register negative finishing deltas despite generating consistent baseline numbers.Scouting Insight: Often driven by variance or temporary finishing runs. Forwards in this bracket represent prime recruitment opportunities before positive regression to the mean restores their goal output.3. Absolute Volume Quadrants (Total $xG$ vs. Goals Scored)Displays absolute season-long production with bubble sizes representing total shot volume, highlighting the overall offensive workload and presence of each striker.📁 Repository Structure├── data/
│   ├── clean_match_events_lean.csv    # Lean match events (local source)
│   ├── forward_scouting_summary.csv   # Pre-aggregated forward dataset (portable)
│   ├── match_events.csv               # Raw StatsBomb event dump
│   ├── matches_data.csv               # Match metadata
│   └── player_total_minutes.csv       # Pre-calculated minutes played cache
├── results/
│   ├── best_xg_performers.png         # Diverging bar chart (Finishing efficiency: G - xG)
│   ├── xg_vs_goals_per90.png          # Normalized per 90 quadrant scatter plot
│   └── xg_vs_goals.png                # Total volume quadrant scatter plot
├── src/
│   ├── best_xG_performers.py          # Script generating G - xG bar chart
│   ├── build_forward_summary.py       # Script creating aggregated forward dataset
│   ├── calculate_minutes.py           # Playing time extraction runner
│   ├── datadownload.py                # Raw dataset download script
│   ├── dataprocessingagent.py         # Data processing agent utility
│   ├── goals_vs_xG_per90.py           # Script generating per-90 scatter plot
│   ├── goals_vs_xG.py                 # Script generating total volume scatter plot
│   └── player_minutes.py              # Playing time computation module
├── .gitignore                         # Git tracking ignore rules
└── README.md                          # Project documentation
🚀 Getting StartedPrerequisitespip install pandas numpy matplotlib adjustText
Reproducing VisualizationsRun the scripts from the project root directory. Since data/forward_scouting_summary.csv is pre-aggregated, all visualizations generate instantly and save directly to results/:# 1. (Optional) Rebuild aggregated forward summary from raw clean data
python src/build_forward_summary.py

# 2. Generate Normalized Per 90 quadrant
python src/goals_vs_xG_per90.py

# 3. Generate Finishing Efficiency (G - xG) bar chart
python src/best_xG_performers.py

# 4. Generate Total xG vs. Goals volume quadrant
python src/goals_vs_xG.py
