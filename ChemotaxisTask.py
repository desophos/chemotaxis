from ChemotaxisEnv import ChemotaxisEnv
from globals import toPygame
from pybrain.rl.environments import Task

class ChemotaxisTask(Task):

    def __init__(self, env=ChemotaxisEnv()):
        """
        :key env: (optional) an instance of a ChemotaxisEnv (or a subclass thereof)
        """
        Task.__init__(self, env)
        
        self.actor_limits = [(-10,10), (-10,10)] # limit motor neurons
        self.sensor_limits = [(0,1), (0,1)] # no limit on sensor neurons

    def performAction(self, action):
        """ A filtered mapping towards performAction of the underlying environment. """
        self.env.performAction(action)

    def getReward(self):
        """ The reward is equal to the chemical signal of the food at the seeker's location,
        which is the inverse square of the distance between those locations. """
        return self.env.calcSignal(toPygame(self.env.seeker.body.position))