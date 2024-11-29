import numpy as np
import matplotlib.pyplot as plt

class graph():
    def __init__(self, data):
        """
        Initialize the graph with concert data over time.
        
        Parameter:
        ----------
        data : np.array
            A NumPy array of shape (N, T), where:
              - N: Number of concerts.
              - T: Total timesteps (t*N). Say each concert has timestep t = 10 -> T = 10*N
        """
        self.data = data
        self.concerts = np.size(self.data, axis=0)
        self.timesteps = np.size(self.data, axis=1) // self.concerts
        self.timejumps = 1/self.timesteps

    def plot_data(self):
        """
        Plot the data for the concerts.
        """
        T = np.linspace(0, self.concerts, int(self.concerts/self.timejumps)+1)
        concert_timeranges = np.arange(self.concerts)

        print(T)
        
        for c in range(self.concerts):
            plt.plot(T[0,:], A[0])



concerts = 3
timesteps = 2

agents = []

agents.append([0, 0, 1, 1, 2, 2]) # Is only at active concerts
agents.append([0, 1, 1, 1, 2, 2]) # Leaves after half first concerts, then queue for the second concert and stays for the full amount. Stays for last concert
agents.append([2, 2, 2, 2, 2, 2]) # Only queues at last concerts and stay that whole concert

A = np.zeros([concerts, int(timesteps*concerts)])

# Make dataset
for agent in agents:
    t = 0
    for i in agent:
        A[i, t] += 1
        t += 1

print(A)


hej = graph(A)
hej.plot_data()