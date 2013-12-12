__author__ = 'Daniel Horowitz, dhorowitz@oxy.edu'

from ChemotaxisEnv import ChemotaxisEnv
from globals import toPygame#, SCREEN_SIZE
from pybrain.rl.environments import EpisodicTask

class ChemotaxisTask(EpisodicTask):
	def __init__(self, env=None, maxsteps=1000):
		"""
		:key env: (optional) an instance of a ChemotaxisEnv (or a subclass thereof)
		:key maxsteps: maximal number of steps (default: 1000)
		"""
		if env == None:
			env = ChemotaxisEnv()
		self.env = env
		
		EpisodicTask.__init__(self, env)
		self.N = maxsteps
		self.t = 0
		
		#self.actor_limits = [(0,1), (0,1)] # scale (-1,1) to motor neurons
		self.sensor_limits = [(0,1), (0,1)] # scale sensor neurons to (-1,1)

	def reset(self):
		EpisodicTask.reset(self)
		self.t = 0

	def performAction(self, action):
		self.t += 1
		EpisodicTask.performAction(self, action)

	def isFinished(self):
		if self.t >= self.N:
			# maximal timesteps
			return True
		return False
		
	def getReward(self):
		""" The reward is equal to the chemical signal of the food at the seeker's location,
        which is the inverse square of the distance between those locations. """
		return self.env.calcSignal(toPygame(self.env.seeker.body.position))

	def setMaxLength(self, n):
		self.N = n
