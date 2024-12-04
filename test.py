#%% 
import random
import numpy as np

def generate_random_names(n):
    first_names = ["John", "Jane", "Alex", "Emily", "Chris", "Katie", "Michael", "Sarah", "David", "Laura"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    
    random_names = []
    for _ in range(n):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        random_names.append(f"{first_name} {last_name}")
    
    return random_names

def string_to_color(s):
    random.seed(hash(s))
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


# Example usage
n = 40
names = generate_random_names(n)
# Example usage
for name in names:
    print(f"{name}: {string_to_color(name)}")

n_cols = np.floor(n ** 0.5).astype(int)
n_rows = n // n_cols
if n % n_cols != 0:
    n_rows += 1

print(n_rows, n_cols)

positions = [(i, j) for i in range(n_rows) for j in range(n_cols)]
print(positions)

import matplotlib.pyplot as plt

# Plot stage
plt.figure(figsize=(10, 6))
plt.plot([0, n_cols-1], [n_rows, n_rows], 'k-', lw=4)  # Stage line
plt.text((n_cols-1)/2, n_rows + 0.5, 'Stage', ha='center', va='center', fontsize=30, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))

# Plot names as datapoints
for idx, (i, j) in enumerate(positions):
    if idx < n // n_cols * n_cols:
        x = j
        y = n_rows - 1 - i
        plt.text(x, y, names[idx], ha='center', va='center', fontsize=9, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
        plt.scatter(x, y+.5, s=500, c=string_to_color(names[idx]), edgecolor='black', linewidth=2)

# Center last row
if n % n_cols != 0:
    last_row_start = (n_cols - (n % n_cols)) / 2
    for idx in range(n - (n % n_cols), n):
        x = last_row_start + (idx % n_cols)
        y = 0
        plt.text(x, y, names[idx], ha='center', va='center', fontsize=9, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
        plt.scatter(x, y+.5, s=500, c=string_to_color(names[idx]), edgecolor='black', linewidth=2)

# Add row numbers
for i in range(n_rows):
    plt.text(-0.5, n_rows - 1 - i, f"Row {i+1}", ha='right', va='center', fontsize=9, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))


plt.xlim(-1, n_cols)
plt.ylim(-1, n_rows + 1)
plt.axis('off')
plt.show()
# %%
