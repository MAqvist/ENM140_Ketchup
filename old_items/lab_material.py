import nashpy as nash
import nashpy.repeated_games as create_repeated_games
import numpy as np
from bigtree import Node


#prisoners dilemma
A = np.array([[3, 0], [5, 1]])
B = np.array([[3, 5], [0, 1]])

#matching pennies
A = np.array([[1, -1], [-1, 1]])

#rock paper scissors
A = np.array([[0,-1, 1], [1, 0, -1], [-1, 1, 0]])

#2x3 game
A = np.array([[1,1,-1],[2,-1,0]])
B = np.array([[1./2,-1,-1./2], [-1,3,2]])

#hawk-dove
A = np.array([[-2, 6], [0, 3]])
B = np.array([[-2, 0], [6, 3]])

#big mokey-little monkey

BMlm_root = Node("root")
C = Node("C", parent=BMlm_root)
W = Node("W", parent=BMlm_root)
Cc = Node("Cc", payoff=[5,3], parent=C)
Cw = Node("Cw", payoff= [4,4], parent=C)
Wc = Node("Wc", payoff=[9,1], parent=W)
Ww = Node("Ww", payoff = [0,0], parent=W)

#exotic bMlm

root = Node("root")
C = Node("C", parent=root, payoff=[1,2])
M = Node("M", parent=root, payoff=[3,4])
W = Node("W", parent=root)
Wc = Node("Wc", payoff=[9,1], parent=W)
Ww = Node("Ww", parent=W)
WwC = Node("WwC", payoff=[4,5], parent=Ww)
WwW = Node("WwW", parent=Ww)
WwWc = Node("WwWc", payoff=[2,3], parent=WwW)
WwWw = Node("WwWw", parent=WwW)
WwWwC = Node("WwWwC", payoff=[7,8], parent=WwWw)
WwWwW = Node("WwWwW", payoff=[9,10], parent=WwWw)

#create a game ith payoff matrices
my_game = nash.Game(A, B)
#if constant sum, you cn create it just with once matrix
my_game = nash.Game(A)

#check for best response
sigma_r = np.array([0, 1])
sigma_c = np.array([1, 0])
print(my_game.is_best_response(sigma_r, sigma_c))

#2D and 3D plots for 2 players- 2 actions games
from gt_utils.two_pa.plot_utils.plots import UtilityPloter
utility_plotter = UtilityPloter(my_game)
fig_objects = utility_plotter.make_2d_plots(player=1) #utility of player 1 vs probability of player 2 of playing the first action
fig_objects = utility_plotter.make_3d_plots(player=1) ##utility of player 1 vs probability of player 1 of playing the first action and probability of player 2 of playing the first action

#compute all Nash equilibria with support enumeration
equilibria = my_game.support_enumeration()
for eq in equilibria:
    print(eq)
    
#if constant sum, you can use the linear program feature
my_game.linear_program()

#extensive form games
from gt_utils.extensive.extensive import ExtensiveFormGame

BMlm_game = ExtensiveFormGame(BMlm_root)

#print the game tree
BMlm_root.show(attr_list=["payoff"])
BMlm_root.hshow()

#extensive -> normal form
pure_strategies = BMlm_game.enumerate_pure_strategies()
u1, u2 = BMlm_game.get_normal_form() #creates a naspy game object in ExtensiceFormGame.nashpy_game

#create a repeated version of the game
repeated_game = create_repeated_games.obtain_repeated_game(game=my_game, repetitions=2) 
#get corresponding strategies
strategies = create_repeated_games.obtain_strategy_space(A=A, repetitions=2) 

#replicator dynamics
y0 = np.array([0.05, 0.95])#initial population
timepoints = np.linspace(0, 10, 1500)
population_1, population_2 = my_game.replicator_dynamics(y0=y0, timepoints=timepoints).T