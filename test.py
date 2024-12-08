#%% 
import random
import numpy as np
import matplotlib.pyplot as plt

def generate_random_names(n):
    first_names = ["John", "Jane", "Alex", "Emily", "Chris", "Katie", "Michael", "Sarah", "David", "Laura"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    
    random_names = []
    for _ in range(n):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        random_names.append(f"{first_name[0]}. {last_name}")
    
    return random_names

def string_to_color(s):
    random.seed(hash(s))
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

for img_idx in range(5):
    
    n = 19
    names = generate_random_names(n)

    n_cols = np.floor(n ** 0.5).astype(int)
    n_rows = n // n_cols
    if n % n_cols != 0:
        n_rows += 1
    
    positions = [(i, j) for i in range(n_rows) for j in range(n_cols)]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot([0, n_cols-1], [n_rows, n_rows], 'k-', lw=4)  # Stage line
    ax.text((n_cols-1)/2, n_rows + 0.5, 'Stage', ha='center', va='center', fontsize=30, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
    
    for idx, (i, j) in enumerate(positions):
        if idx < n // n_cols * n_cols:
            x = j
            y = n_rows - 1 - i
            ax.text(x, y, names[idx], ha='center', va='center', fontsize=9, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
            ax.scatter(x, y+.5, s=500, c=string_to_color(names[idx]), edgecolor='black', linewidth=2)
    
    if n % n_cols != 0:
        last_row_start = (n_cols - (n % n_cols)) / 2
        for idx in range(n - (n % n_cols), n):
            x = last_row_start + (idx % n_cols)
            y = 0
            ax.text(x, y, names[idx], ha='center', va='center', fontsize=9, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
            ax.scatter(x, y+.5, s=500, c=string_to_color(names[idx]), edgecolor='black', linewidth=2)
    
    for i in range(n_rows):
        ax.text(-0.5, n_rows - 1 - i, f"Row {i+1}", ha='right', va='center', fontsize=9, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
    
    ax.set_xlim(-1, n_cols)
    ax.set_ylim(-1, n_rows + 1)
    ax.axis('off')
    folder_name = 'figures'
    import os
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    plt.savefig(f'figures/concert_{img_idx+1}.png')
    plt.close(fig)




#%%
fig, axs = plt.subplots(1, 5, figsize=(25, 6))  # Increased figure width and height for clarity

n = 19
names = generate_random_names(n)

for img_idx, ax in enumerate(axs):

    random.shuffle(names)

    n_cols = np.floor(n ** 0.5).astype(int)
    n_rows = n // n_cols
    if n % n_cols != 0:
        n_rows += 1
    
    positions = [(i, j) for i in range(n_rows) for j in range(n_cols)]

    ax.plot([0, n_cols-1], [n_rows, n_rows], 'k-', lw=4)  # Stage line
    ax.text((n_cols-1)/2, n_rows + 0.5, 'Stage', ha='center', va='center', fontsize=30, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
    
    for idx, (i, j) in enumerate(positions):
        if idx < n // n_cols * n_cols:
            x = j
            y = n_rows - 1 - i
            ax.text(x, y, names[idx], ha='center', va='center', fontsize=9, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
            ax.scatter(x, y+.5, s=500, c=string_to_color(names[idx]), edgecolor='black', linewidth=2)
    
    if n % n_cols != 0:
        last_row_start = (n_cols - (n % n_cols)) / 2
        for idx in range(n - (n % n_cols), n):
            x = last_row_start + (idx % n_cols)
            y = 0
            ax.text(x, y, names[idx], ha='center', va='center', fontsize=9, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
            ax.scatter(x, y+.5, s=500, c=string_to_color(names[idx]), edgecolor='black', linewidth=2)
    
    for i in range(n_rows):
        ax.text(-0.5, n_rows - 1 - i, f"Row {i+1}", ha='right', va='center', fontsize=9, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
    
    ax.set_xlim(-1, n_cols)
    ax.set_ylim(-1, n_rows + 1)
    ax.axis('off')

fig.tight_layout()  # Adjust layout to allow space for the arrow
folder_name = 'figures'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
plt.savefig(f'figures/concert_combined.png')
plt.close(fig)


