import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    from adjustText import adjust_text
    HAS_ADJUST_TEXT = True
except ImportError:
    HAS_ADJUST_TEXT = False

# Load aggregated scouting data
df = pd.read_csv('forward_scouting_summary.csv')

# Calculate per 90 metrics
df['xg_per_90'] = (df['total_xg'] / df['exact_minutes']) * 90
df['goals_per_90'] = (df['total_goals'] / df['exact_minutes']) * 90

# Filter by minutes (1200 allows elite starters like Khadija Shaw) and shot rate
MIN_MINUTES = 1200
filtered_df = df[
    (df['exact_minutes'] >= MIN_MINUTES) & 
    (df['xg_per_90'] >= 0.1)
].copy()

mean_xg = filtered_df['xg_per_90'].mean()
mean_goals = filtered_df['goals_per_90'].mean()

fig, ax = plt.subplots(figsize=(13, 10), facecolor='#f4f4f4')
ax.set_facecolor('#f4f4f4')

bubble_sizes = filtered_df['total_shots'] * 3.5
scatter = ax.scatter(
    filtered_df['xg_per_90'],
    filtered_df['goals_per_90'],
    s=bubble_sizes,
    color='black',
    alpha=0.6,
    edgecolors='white',
    linewidth=1.5
)

ax.axvline(mean_xg, color='gray', linewidth=1.2, linestyle='--')
ax.axhline(mean_goals, color='gray', linewidth=1.2, linestyle='--')

# Selective label placement
texts = []
for _, row in filtered_df.iterrows():
    is_notable = (
        row['xg_per_90'] > mean_xg * 1.15 or 
        row['goals_per_90'] > mean_goals * 1.15 or 
        row['total_goals'] >= 8
    )
    if is_notable:
        txt = ax.text(
            row['xg_per_90'],
            row['goals_per_90'],
            row['player'],
            fontsize=9,
            fontweight='bold',
            color='#111111'
        )
        texts.append(txt)

if HAS_ADJUST_TEXT and texts:
    adjust_text(
        texts,
        arrowprops=dict(arrowstyle='-', color='gray', lw=0.5, alpha=0.7),
        ax=ax,
        force_text=(0.5, 0.8)
    )

# Padding borders so corner labels don't collide with data points
ax.set_xlim(0.05, filtered_df['xg_per_90'].max() + 0.08)
ax.set_ylim(-0.02, filtered_df['goals_per_90'].max() + 0.12)

# Quadrant descriptions positioned safely in the corners
bbox_props = dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#cccccc', alpha=0.75)

ax.text(
    0.98, 0.98, 
    'High xG per 90, Many Goals per 90\n(Reliable Finishing / Stars)', 
    transform=ax.transAxes, 
    fontsize=8.5, 
    fontstyle='italic', 
    ha='right', 
    va='top', 
    bbox=bbox_props
)
ax.text(
    0.02, 0.98, 
    'Low xG per 90, Many Goals per 90\n(Clinical / Overperforming)', 
    transform=ax.transAxes, 
    fontsize=8.5, 
    fontstyle='italic', 
    ha='left', 
    va='top', 
    bbox=bbox_props
)
ax.text(
    0.02, 0.02, 
    'Low xG per 90, Low Goals per 90\n(Attacking Crisis / Low Output)', 
    transform=ax.transAxes, 
    fontsize=8.5, 
    fontstyle='italic', 
    ha='left', 
    va='bottom', 
    bbox=bbox_props
)
ax.text(
    0.98, 0.02, 
    'High xG per 90, Low Goals per 90\n(Underperforming / Bad Luck)', 
    transform=ax.transAxes, 
    fontsize=8.5, 
    fontstyle='italic', 
    ha='right', 
    va='bottom', 
    bbox=bbox_props
)

ax.set_title(
    f'Player xG vs. Real Goals per 90 (Normalized)\nFiltered by min. {MIN_MINUTES} Minutes & Active Offense | Center Forwards Only',
    fontsize=14, 
    fontweight='bold', 
    pad=15
)
ax.set_xlabel('xG per 90 minutes', fontsize=11, fontweight='bold')
ax.set_ylabel('Goals per 90 minutes', fontsize=11, fontweight='bold')
ax.legend(loc='upper left', frameon=True, facecolor='white', edgecolor='none')

plt.tight_layout()
plt.savefig('xg_vs_goals_per90.png', dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.show()