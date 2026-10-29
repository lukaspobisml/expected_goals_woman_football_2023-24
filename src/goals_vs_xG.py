import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    from adjustText import adjust_text
    HAS_ADJUST_TEXT = True
except ImportError:
    HAS_ADJUST_TEXT = False

# Load aggregated scouting data from data/
df = pd.read_csv('data/forward_scouting_summary.csv')

# Filter by minutes and shot sample
MIN_MINUTES = 1200
filtered_df = df[
    (df['exact_minutes'] >= MIN_MINUTES) & 
    (df['total_shots'] >= 30)
].copy()

mid_xg = (filtered_df['total_xg'].min() + filtered_df['total_xg'].max()) / 2
mid_goals = (filtered_df['total_goals'].min() + filtered_df['total_goals'].max()) / 2

fig, ax = plt.subplots(figsize=(12, 9), facecolor='#f4f4f4')
ax.set_facecolor('#f4f4f4')

scatter = ax.scatter(
    filtered_df['total_xg'],
    filtered_df['total_goals'],
    s=filtered_df['total_shots'] * 0.8,
    color='black',
    alpha=0.7,
    edgecolors='white',
    linewidth=1.5
)

ax.axvline(mid_xg, color='gray', linewidth=1, linestyle='--')
ax.axhline(mid_goals, color='gray', linewidth=1, linestyle='--')

# Selective label placement
texts = []
for _, row in filtered_df.iterrows():
    texts.append(
        ax.text(
            row['total_xg'],
            row['total_goals'],
            row['player'],
            fontsize=9,
            fontweight='bold',
            color='#222222'
        )
    )    

if HAS_ADJUST_TEXT and texts:
    adjust_text(
        texts,
        arrowprops=dict(arrowstyle='-', color='gray', lw=0.5, alpha=0.7),
        ax=ax
    )

ax.text(0.95, 0.93, 'High xG, Many Goals\nReliable Finishing', transform=ax.transAxes,
        fontsize=9, fontstyle='italic', ha='right', va='top', bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.5))
ax.text(0.05, 0.93, 'Low xG, Many Goals\n(Above Average Finishing / Luck)', transform=ax.transAxes,
        fontsize=9, fontstyle='italic', ha='left', va='top', bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.5))
ax.text(0.05, 0.07, 'Low xG, Low Goals\n(Attacking Crisis)', transform=ax.transAxes,
        fontsize=9, fontstyle='italic', ha='left', va='bottom', bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.5))
ax.text(0.95, 0.07, 'High xG, Low Goals\n(Missed Chances / Bad Luck)', transform=ax.transAxes,
        fontsize=9, fontstyle='italic', ha='right', va='bottom', bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.5))

ax.set_title(
    f'Player xG vs. Real Goals (Centered at Average)\nPoint Size Represents Number of Shots | min. {MIN_MINUTES} Minutes',
    fontsize=14, fontweight='bold', pad=15
)
ax.set_xlabel('Total xG', fontsize=11, fontweight='bold')
ax.set_ylabel('Goals Scored', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('results/xg_vs_goals.png', dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.show()