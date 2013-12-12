from ChemotaxisEnv import ChemotaxisEnv
#from ChemotaxisTask import ChemotaxisTask
from EpisodicChemotaxisTask import ChemotaxisTask
from globals import SCREEN_SIZE
from pybrain.rl.agents.optimization import OptimizationAgent
from pybrain.rl.experiments.episodic import EpisodicExperiment
#from pybrain.rl.learners.directsearch import Reinforce
from pybrain.optimization import HillClimber

from pybrain.tools.shortcuts import buildNetwork
import matplotlib.pyplot as pyplot

MAX_TRIALS = 10
MAX_STEPS = 1200

#all_evals = []
#reward_avgs = [] # keep track of the average fitness per trial
#reward_maxes = [] # keep track of the maximum fitness per trial
#movement = [] # keep track of the seeker's movement
#food_loc = [] # keep track of the location of the food

# pybrain initialization
task = ChemotaxisTask(ChemotaxisEnv(), MAX_STEPS)
module = buildNetwork(2,2,2) # create a feed-forward neural network with 3 layers: 2 input neurons, 2 hidden neurons, and 2 output neurons
#learner = HillClimber(minimize=True, storeAllEvaluations=True, verbose=False)
#agent = OptimizationAgent(module, learner)
#exp = EpisodicExperiment(task, agent)
#exp.doEpisodes(MAX_TRIALS)
learner = HillClimber(task, module, maxEvaluations=MAX_TRIALS, mustMinimize=True, storeAllEvaluations=True, storeAllEvaluated=True, verbose=False)
learner.learn()
# _allEvaluations is a list of the sum of rewards for each trial, i.e. the fitness of each trial's network
# _allEvaluated is a list of the networks for each trial
#for network in learner._allEvaluated:
#    print network.params
reward_avgs = [e/MAX_STEPS for e in learner._allEvaluations]

"""
for i in range(0, MAX_TRIALS):
    exp.doInteractions(MAX_STEPS)
    agent.learn()
    
    print exp.agent.learner.module.params
    
    total_reward = agent.history.getSumOverSequences("reward")[0][0]
    num_rewards = len(agent.history.getField("reward"))
    reward_avgs.append( total_reward / num_rewards )
    
    reward_maxes.append( max(agent.history.getField("reward")) )
    
    movement.append(task.env.movement_tracker)
    food_loc.append(task.env.food.loc)
 
    exp.task.env.reset()
    agent.reset()
"""
# show average reward over trials

pyplot.figure(1)
pyplot.plot(range(1,len(reward_avgs)+1), reward_avgs)
pyplot.ylabel("Average Reward")
pyplot.xlabel("Trial #")

"""
# show maximum reward over trials

pyplot.figure(2)
pyplot.plot(range(1,len(reward_maxes)+1), reward_maxes)
pyplot.ylabel("Maximum Reward")
pyplot.xlabel("Trial #")

# show movement for the last 6 trials

pyplot.figure(3)
NUM_MOVEMENT_PLOTS = 6
for i in range(1,NUM_MOVEMENT_PLOTS+1):
    pyplot.subplot(2,3,i)
    x,y = zip(*movement[NUM_MOVEMENT_PLOTS+1-i]) # last trial is bottom right
    pyplot.scatter(x, y, c='k', marker='.') # path is marked by black points
    pyplot.scatter(food_loc[i][0], food_loc[i][1], c='c', marker='D') # food is marked by a cyan diamond
    pyplot.xlim([0, SCREEN_SIZE])
    pyplot.ylim([0, SCREEN_SIZE])
"""
pyplot.show()