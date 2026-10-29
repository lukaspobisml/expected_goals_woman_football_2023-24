import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    from adjustText import adjust_text
    HAS_ADJUST_TEXT = True
except ImportError:
    HAS_ADJUST_TEXT = False

# 1. Load data
df = pd.read_csv('data/forward_scouting_summary.csv')

# 2. Compute per 90 metrics
df['xg_per_90'] = (df['total_xg'] / df['exact_minutes']) * 90
df['goals_per_90'] = (df['total_goals'] / df['exact_minutes']) * 90

# 3. Filter sample
MIN_MINUTES = 1200
filtered_df = df[
    (df['exact_minutes'] >= MIN_MINUTES) & 
    (df['xg_per_90'] >= 0.1)
].copy()

mean_xg = filtered_df['xg_per_90'].mean()
mean_goals = filtered_df['goals_per_90'].mean()

# 4. Canvas setup
fig, ax = plt.subplots(figsize=(13, 9.5), facecolor='#f4f4f4')
ax.set_facecolor('#f4f4f4')

# 5. Square Root Scaling functions
forward_transform = lambda x: np.sqrt(np.maximum(x, 0))
inverse_transform = lambda x: x**2

ax.set_xscale('function', functions=(forward_transform, inverse_transform))
ax.set_yscale('function', functions=(forward_transform, inverse_transform))

ax.set_xticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6])

# 6. Scatter points
bubble_sizes = filtered_df['total_shots'] * 3.6
scatter = ax.scatter(
    filtered_df['xg_per_90'],
    filtered_df['goals_per_90'],
    s=bubble_sizes,
    color='black',
    alpha=0.65,
    edgecolors='white',
    linewidth=1.4
)

# Reference lines
ax.axvline(mean_xg, color='#7f8c8d', linewidth=1.1, linestyle='--', label=f'Average xG/90 ({mean_xg:.2f})')
ax.axhline(mean_goals, color='#7f8c8d', linewidth=1.1, linestyle='--', label=f'Average Goals/90 ({mean_goals:.2f})')

# 7. Labels
texts = []
for _, row in filtered_df.iterrows():
    is_notable = (
        row['xg_per_90'] > mean_xg * 1.05 or 
        row['goals_per_90'] > mean_goals * 1.05 or 
        row['total_goals'] >= 7
    )
    if is_notable:
        txt = ax.text(
            row['xg_per_90'],
            row['goals_per_90'],
            row['player'],
            fontsize=8.5,
            fontweight='bold',
            color='#1a1a1a'
        )
        texts.append(txt)

if HAS_ADJUST_TEXT and texts:
    adjust_text(
        texts,
        arrowprops=dict(arrowstyle='->', color='#95a5a6', lw=0.6, alpha=0.8),
        ax=ax,
        expand_text=(1.3, 1.5),
        force_text=(0.7, 1.0)
    )

# Generous limits so Shaw stays well clear of the top-right box
ax.set_xlim(0.06, 0.95)
ax.set_ylim(-0.01, 1.65)

# Quadrant labels
bbox_props = dict(boxstyle='round,pad=0.35', facecolor='white', edgecolor='#dcdde1', alpha=0.85)

ax.text(0.98, 0.98, 'High xG/90, Many Goals/90\n(Elite Volume & Finishing)', 
        transform=ax.transAxes, fontsize=8.5, fontstyle='italic', ha='right', va='top', bbox=bbox_props)
ax.text(0.02, 0.98, 'Low xG/90, Many Goals/90\n(Clinical / Overperforming)', 
        transform=ax.transAxes, fontsize=8.5, fontstyle='italic', ha='left', va='top', bbox=bbox_props)
ax.text(0.02, 0.02, 'Low xG/90, Low Goals/90\n(Low Threat & Output)', 
        transform=ax.transAxes, fontsize=8.5, fontstyle='italic', ha='left', va='bottom', bbox=bbox_props)
ax.text(0.98, 0.02, 'High xG/90, Low Goals/90\n(Underperforming / Unlucky)', 
        transform=ax.transAxes, fontsize=8.5, fontstyle='italic', ha='right', va='bottom', bbox=bbox_props)

# Titles, axes and legend
ax.set_title(
    f'Player xG vs. Real Goals per 90 (Power Scaled)\nFiltered by min. {MIN_MINUTES} Minutes & Active Offense | Center Forwards Only',
    fontsize=13, fontweight='bold', pad=14
)
ax.set_xlabel('xG per 90 minutes (Square Root Scale)', fontsize=11, fontweight='bold')
ax.set_ylabel('Goals per 90 minutes (Square Root Scale)', fontsize=11, fontweight='bold')
ax.legend(loc='lower left', bbox_to_anchor=(0.18, 0.02), frameon=True, facecolor='white', edgecolor='none')

plt.tight_layout()
plt.savefig('results/xg_vs_goals_per90.png', dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.show()