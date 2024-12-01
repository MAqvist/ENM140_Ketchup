import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import random

class BarGraph():
    def __init__(self, data):
        """
        Initialize the graph with concert data over time. Works best with n_concerts <= 10
        
        Parameter:
        ----------
        data : np.array
            A NumPy array of shape (N, T), where:
              - N: Number of concerts.
              - T: Total timesteps (t*N). Say each concert has timestep t = 10 -> T = 10*N
        """
        self._data = data
        self._concerts = np.size(self._data, axis=0)
        self._timesteps = np.size(self._data, axis=1) // self._concerts
        self._timejumps = 1/self._timesteps
    
    def plot_data(self, max_columns=10):
        """
        Plot data for each concert. Each plot shows the number of agents at each timestep,
        including how many are queuing for the next concert.
        
        Parameters:
        ----------
        max_columns : int
            Maximum number of plots to display in a single row.
        """

        colors = get_colors_from_palette("tab20c", self._concerts+1)

        if self._concerts < max_columns:
            max_columns = self._concerts

        rows = (self._concerts + max_columns - 1) // max_columns  # Calculate the number of rows needed
        fig, axes = plt.subplots(rows, max_columns, figsize=(max_columns * 3, rows * 3))
        axes = np.array(axes).reshape(-1)  # Flatten the axes for easy indexing

        bar_width_concert = self._timejumps * 0.8  # Set a smaller width for bars
        bar_width_queue = self._timejumps * 0.8
        offset = bar_width_concert / 3  # Offset to separate bars

        for i, ax in enumerate(axes):
            if i < self._concerts:
                # Extract the relevant timesteps for the current concert
                concert_data = self._data[i, i * self._timesteps:(i + 1) * self._timesteps]
                next_queue = (
                    self._data[i + 1, i * self._timesteps:(i + 1) * self._timesteps]
                    if i + 1 < self._concerts
                    else np.zeros(self._timesteps)
                )
                normalized_time = np.linspace(0, 1, self._timesteps)  # Normalize time from 0 to 1
                
                # Offset positions
                attendance_positions = normalized_time
                queue_positions = normalized_time + offset
                
                # Plot the data for this concert
                ax.set_ylim([0, np.max(self._data) + 1])
                ax.bar(queue_positions, next_queue, label=f'Queue for Concert {i + 2}', width=bar_width_queue, edgecolor='k', color=colors[i+1], alpha=.3)
                ax.bar(attendance_positions, concert_data, label=f'Concert {i + 1} Attendance', width=bar_width_concert, edgecolor='k', color = colors[i])
                
                ax.set_title(f'Concert {i + 1}')
                ax.set_xlabel('Concert time')
                if i == 0: 
                    ax.set_ylabel('Agents')
                ax.legend()
            else:
                ax.axis('off')  # Hide unused subplots

        plt.tight_layout()
        plt.show()

def get_colors_from_palette(palette_name, num_colors):
        """
        Generate a sequence of colors from a Matplotlib color palette.

        Parameters:
        ----------
        palette_name : str
            Name of the Matplotlib color palette (e.g., 'viridis', 'plasma', 'coolwarm').
        num_colors : int
            Number of colors to generate.

        Returns:
        -------
        colors : list
            List of RGBA color values.
        """
        cmap = cm.get_cmap(palette_name, num_colors)  # Get the specified colormap
        return [cmap(i) for i in range(num_colors)]   # Generate colors

def generate_agents(num_agents, concerts, timesteps):
    """
    Generate agents with realistic concert attendance patterns.
    
    Parameters:
    ----------
    num_agents : int
        Number of agents to generate.
    concerts : int
        Number of concerts.
    timesteps : int
        Number of timesteps per concert.
        
    Returns:
    -------
    agents : list of lists
        Each list represents an agent's attendance and queuing behavior.
    """
    agents = []

    for _ in range(num_agents):
        agent = []
        for c in range(concerts):
            start_time = random.randint(0, timesteps - 1) if c == 0 or agent[-1] == c - 1 else 0
            duration = random.randint(1, timesteps - start_time)
            agent += [c] * duration
            
            # Queue for the next concert if there are more concerts left
            if c < concerts - 1:
                queue_time = random.randint(0, timesteps - len(agent) % timesteps)
                agent += [c + 1] * queue_time

        # Ensure no trailing attendance for non-existent concerts
        agent = agent[:concerts * timesteps]
        agents.append(agent)

    return agents

# Example Usage
num_agents = 100
concerts = 3
timesteps = 3
agents = generate_agents(num_agents, concerts, timesteps)


A = np.zeros([concerts, int(timesteps*concerts)])

# Make dataset
for agent in agents:
    t = 0
    for i in agent:
        A[i, t] += 1
        t += 1

hej = BarGraph(A)
hej.plot_data()
