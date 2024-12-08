import matplotlib.pyplot as plt
import numpy as np
import random
import db_handler as dbh

def string_to_color(s):
    random.seed(hash(s))
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def concert_fig(names, leave_times):
    # shape of audience
    n = len(names)
    n_cols = np.floor(n ** 0.5).astype(int)
    n_rows = n // n_cols
    if n % n_cols != 0:
        n_rows += 1
    possible_positions = [(i, j) for i in range(n_rows) for j in range(n_cols)]
    
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot stage
    ax.plot([0, n_cols-1], [n_rows, n_rows], 'k-', lw=4)  # Stage line
    ax.text((n_cols-1)/2, n_rows + 0.5, 'Stage', ha='center', va='center', fontsize=30, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))

    positions = sorted(range(len(leave_times)), key=lambda i: leave_times[i])

    # Plot names as datapoints
    for idx, (i, j) in enumerate(possible_positions):
        if idx < n // n_cols * n_cols:
            x = j
            y = n_rows - 1 - i
            ax.text(x, y, names[positions[idx]], ha='center', va='center', fontsize=9, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
            ax.scatter(x, y+.5, s=500, c=string_to_color(names[positions[idx]]), edgecolor='black', linewidth=2)
    
    # Center last row
    if n % n_cols != 0:
        last_row_start = (n_cols - (n % n_cols)) / 2
        for idx in range(n - (n % n_cols), n):
            x = last_row_start + (idx % n_cols)
            y = 0
            ax.text(x, y, names[positions[idx]], ha='center', va='center', fontsize=9, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
            ax.scatter(x, y+.5, s=500, c=string_to_color(names[positions[idx]]), edgecolor='black', linewidth=2)
    
    # Add row numbers
    for i in range(n_rows):
        ax.text(-0.5, n_rows - 1 - i, f"Row {i+1}", ha='right', va='center', fontsize=9, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))

    ax.set_xlim(-1, n_cols)
    ax.set_ylim(-1, n_rows + 1)
    ax.axis('off')
    ax.set_title("Concert Audience for the Next Concert")
    return fig, positions

def plot_cumulative_utility(names, utility):
    fig, ax = plt.subplots()
    for i, name in enumerate(names):
        ax.plot(range(len(utility[i])), np.cumsum(utility[i]), label=name, color=string_to_color(name))
    
    ax.set_xticks(range(len(utility[i])))
    ax.set_xticklabels(range(1, len(utility[i])+1))
    ax.set_xlabel("Time")
    ax.set_ylabel("Utility")
    ax.legend()
    ax.grid()
    ax.set_title("Utility for this concert")
    return fig

def utility_for_next_concert(round_num, name):
    utility = dbh.get_utility_nexts(round_num, name)

    if utility:
        return float(utility[0])
    else:
        return 0.0