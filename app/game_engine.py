import numpy as np
import random

class Agent: 
    def __init__(self, name: str, music_taste = 1, strategy = 1, nr_concerts = 3, festival_duration=9):
        self.music_taste = music_taste
        self.position_utility = None
        self.waiting_utility_history = np.zeros(festival_duration)
        self.strategy = strategy
        self.position_utility_history = np.zeros(festival_duration)
        self.concert_history = np.ones(festival_duration, dtype=int)*(nr_concerts-1)
        self.concert_history[0] = 0 #start at first concert 
        self.name = name
        self.position = None
    
class Concert:
    def __init__(self,n_rows, len_rows = 1, music_type = 1, capacity = 5, duration = 2, nr_of_agents = 10):
        self.len_rows = len_rows
        self.music_type = music_type
        self.nr_agents = 0
        self.nr_waiting_agents = 0
        self.capacity = capacity
        self.nr_rows = n_rows
        self.duration = duration #timesteps
        self.agents = np.zeros(nr_of_agents)

    def add_agent(self):
        self.nr_agents += 1

def get_placement_utility(concert):
    placement_factor = 5
    #continuing using sigmoid
    #fullness = concert.nr_agents / concert.capacity
    #sigmoid_x = 1 - fullness
    #k = 10 #steepness of sigomid
    #center = 0.5 #[0,1] with 0.1 happy crowd and 0.9 happy front row
    #utility = placement_factor * 1 / ( 1 + np.exp(-k*(sigmoid_x- center)))

    #stepwise by which row the agent is in, sensitive to concert row length
    dist_from_stage = np.floor((concert.nr_agents) / concert.len_rows)
    utility = placement_factor * (concert.nr_rows - dist_from_stage) / concert.nr_rows
    return utility #, int(dist_from_stage)

def get_waiting_utility():
    waiting_factor = 1
    utility = -1 * waiting_factor
    return utility

def concert_utility2(names, leave_time, previous_round, time_steps_per_concert = 10):
    """
    previous_round: {name: utility_scaler_position}
    """
    wating_utility = get_waiting_utility()

    utility = np.zeros((len(names), time_steps_per_concert+1)) + wating_utility
    utility_factor_for_next_concert = np.zeros(len(names))
    positions = [None] * len(names)

    n = len(names)
    n_cols = np.floor(n ** 0.5).astype(int)
    n_rows = n // n_cols
    if n % n_cols != 0:
        n_rows += 1
        
    next_concert = Concert(capacity=len(names), 
                           duration=time_steps_per_concert,
                           n_rows=n_rows,
                           len_rows=n_cols,
                           nr_of_agents=len(names)
                           )

    pos_counter = 0
    for time in range(time_steps_per_concert+1):
        print(time, leave_time)
        if time in leave_time:
            idx = [i for i, t in enumerate(leave_time) if t == time]
            for i in idx:
                utility[i, :time+1] = previous_round[names[i]]
                utility_factor_for_next_concert[i] = get_placement_utility(next_concert)
                next_concert.add_agent()
                positions[i] = pos_counter

    return utility, utility_factor_for_next_concert, positions

def string_to_color(s):
    random.seed(hash(s))
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
