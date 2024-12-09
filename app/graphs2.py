import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import random
import utilities as ut

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
    
    def plot_data(self, max_columns=5):
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

        bar_width_concert = self._timejumps * 0.8
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

class SeminarGraph():
    def __init__(self, names, responses, timesteps, concert_number):
        responses = np.array(responses)/timesteps
        print(responses)
        self._names = np.array(names, dtype=str)
        self._responses = np.array(responses, dtype=float)
        self._timesteps = timesteps
        self._attendees = np.array(self._timesteps)
        self._concert_number = concert_number
        self.__sort_lists()
    
    def __sort_lists(self):
        idx_sorted = np.argsort(self._responses)
        name_sorted = np.array([self._names[i] for i in idx_sorted])
        response_sorted = np.array([self._responses[i] for i in idx_sorted])

        self._names = name_sorted
        self._responses = response_sorted

    def create_plot_data(self):
        self._xx = np.arange(0, self._timesteps+1)
        self._yy = np.ones(len(self._xx)) * len(self._names)
        y_offset = np.zeros(len(self._xx))
        for response in self._responses:
            self._yy[int(response*(self._timesteps)):] -= 1

        fig, ax = plt.subplots()

        ax.bar(0, len(self._names), color='grey', alpha=.4)
        for i in range(0, len(self._xx)):
            ax.bar(self._xx[i], self._yy[i-1],color='grey', alpha=.4)

        ax.bar(self._xx[:-1], self._yy[:-1], color='cornflowerblue', edgecolor='k')

        for idx, leaver in enumerate(self._responses):
            i = int(leaver*self._timesteps)-1
            if i >= 10:
                break
            x = (leaver*self._timesteps)
            y = (self._yy[i+1])+.5+y_offset[i]
            print(int(leaver*self._timesteps))
            ax.scatter(x, y, s=128, edgecolors='k', c=string_to_color(self._names[idx]))
            ax.text(x+.5, y, self._names[idx], verticalalignment='center')
            y_offset[i] += 1
            
        ax.set_xticks(np.arange(0, self._timesteps+1))
        ax.set_xlim([-.9, self._timesteps+2.5])
        ax.set_ylabel('Attendees')
        ax.set_xlabel('Timestep')
        ax.set_title('Concert {}'.format(self._concert_number))
        
        return fig

def string_to_color(s):
    random.seed(hash(s))
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

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
# num_agents = 100
# concerts = 3
# timesteps = 3
# agents = generate_agents(num_agents, concerts, timesteps)


# A = np.zeros([concerts, int(timesteps*concerts)])

# # Make dataset
# for agent in agents:
#     t = 0
#     for i in agent:
#         A[i, t] += 1
#         t += 1

# hej = BarGraph(A)
# hej.plot_data()

def plot_cumulative_utility(names, utility_total, current_round, n_time_steps):
    fig, ax = plt.subplots()

    # Calculate total utility for each player
    total_utilities = {name: sum(np.concatenate(utility_total[name])) for name in names}

    # Get the top 7 players with the highest utilities
    top_7_names = sorted(total_utilities, key=total_utilities.get, reverse=True)[:7]

    # Plot for the top 7 players
    for name in top_7_names:
        ax.plot(range(0, len(np.concatenate(utility_total[name]))), 
                np.cumsum(utility_total[name]), 
                label=name, 
                color=ut.string_to_color(name))

    ax.set_xticks(np.arange(0, int(current_round)*n_time_steps, n_time_steps))
    ax.set_xticklabels(range(1, int(current_round)+1))
    ax.set_xlabel("Concert Number")
    ax.set_ylabel("Cumulative Utility")
    ax.legend()
    ax.grid()
    ax.set_title("Cumulative Utility for Top 7 Players")
    return fig

names = ['lucas', 'august', 'malte', 'mathilda', 'diddy', 'tits', 'tats', 'johan', 'stefan', 'claes', 'erik', 'svenne', 'miklos', 'jasmin', 'gunilla','ingrid']
responses = [0.9, 0.2, 0.2, 1., .5, .8, .0, .7, .7, .7, .8, .8, .9, 1, 1, 1]

sem = SeminarGraph(names, responses, 10, 2)
sem.create_plot_data()

# Seminar
# Addera kombinerad barplot med isch scatter vem som sticker på tidsteg t
