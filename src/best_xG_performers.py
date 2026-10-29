import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load aggregated scouting data from data/
df = pd.read_csv('data/forward_scouting_summary.csv')

# Filter sample
MIN_MINUTES = 1200
filtered_df = df[
    (df['exact_minutes'] >= MIN_MINUTES) & 
    (df['total_shots'] >= 30)
].copy()

# Calculate finishing delta
filtered_df['diff_xg'] = filtered_df['total_goals'] - filtered_df['total_xg']
filtered_df = filtered_df.sort_values(by='diff_xg', ascending=True).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(12, 10), facecolor='#f4f4f4')
ax.set_facecolor('#f4f4f4')

colors = ['#2ecc71' if x >= 0 else '#e74c3c' for x in filtered_df['diff_xg']]
bars = ax.barh(
    filtered_df['player'],
    filtered_df['diff_xg'],
    color=colors,
    alpha=0.85,
    edgecolor='white',
    linewidth=0.8
)

ax.axvline(0, color='black', linewidth=1.2, linestyle='-')

# Dynamic margin to avoid clipping labels
min_val = filtered_df['diff_xg'].min()
max_val = filtered_df['diff_xg'].max()
ax.set_xlim(min_val - 1.2, max_val + 1.2)

ax.set_title(
    f'Total Finishing Efficiency (Goals minus xG)\nCenter Forwards with min. {MIN_MINUTES} Minutes',
    fontsize=14, fontweight='bold', pad=15
)
ax.set_xlabel('Total Goals minus xG (G - xG)', fontsize=11, fontweight='bold')
ax.set_ylabel('Player', fontsize=11, fontweight='bold')

for bar in bars:
    width = bar.get_width()
    offset = 0.2 if width >= 0 else -0.2
    ax.text(
        width + offset,
        bar.get_y() + bar.get_height() / 2,
        f'{width:+.2f}',
        va='center',
        ha='left' if width >= 0 else 'right',
        fontsize=8,
        fontweight='bold',
        color='#222222'
    )

plt.tight_layout()
plt.savefig('results/best_xg_performers.png', dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.show()