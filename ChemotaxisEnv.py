from Food import Food
from Seeker import Seeker
from globals import SCREEN_SIZE, toPygame
from pybrain.rl.environments.environment import Environment
import pygame

class ChemotaxisEnv(Environment):
	"""
	Experiment adapted from "Evolving Dynamical Neural Networks for Adaptive Behavior" (Beer & Gallagher, 1992)
	
	An seeker is enclosed in a square box with a food item inside.
	This food item emits a chemical signal whose intensity falls off
	as the inverse square of the distance from the food.
	The intensity of the chemical signal within the environment varies
	five orders of magnitude from the item to the far corners of the box, i.e. at a distance of root(2).
	We wish the seeker to find and remain in the vicinity of the food item,
	starting from arbitrary locations and orientations within the environment.

	To accomplish this task, the seeker is endowed with a circular body with a diameter of .01.
	The seeker possesses chemical sensors that can directly sense
	the intensity of the chemical signal at their location.
	These sensors are symmetrically placed about the center line of the body.
	In addition, the seeker has two effectors located on opposite sides of its body.
	These effectors can apply forces that move the body forward and rotate it.
	In the simplified physics of this environment,
	the velocity of movement is proportional to the force applied.

	State space (continuous):
		food		location of food item as a coordinate pair from (0,0) to (100,100)
		seeker.loc	location of the center of the seeker
		seeker.dir	angle of the seeker in radians from the positive x-axis, i.e. east=0
	Action space (continuous):
		l			output signal of the left effector neuron
		r			output signal of the right effector neuron
	"""
	
	def __init__(self):
		# pygame initialization

		self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
		pygame.mouse.set_visible(0)

		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((255, 255, 255))
		
		self.food = Food()
		self.food_sprite = pygame.sprite.RenderPlain(self.food) # create sprite group for the food

		self.seeker = Seeker()
		self.seeker_sprite = pygame.sprite.RenderPlain(self.seeker) # create sprite group for the seeker

		self._draw()

		# pybrain initialization
		self.action = [0.0, 0.0]
		
		self.reset()

	def _draw(self):
		#self.seeker_sprite.update(self.background)
		self.screen.blit(self.background, (0, 0))
		self.food.update()
		self.food_sprite.draw(self.screen)
		self.seeker.update(self.screen) # we don't need to draw this here because we draw it with pymunk
		pygame.display.flip()

	def _calcDistance(self, loc1, loc2):
		""" Calculates the Euclidean distance between two coordinate pairs. """
		from math import sqrt
		return sqrt((loc2[0] - loc1[0]) ** 2 + (loc2[1] - loc1[1]) ** 2)

	def calcSignal(self, loc):
		""" Calculates the chemical signal at a specific location, which is
		the inverse square of the distance between the given location and the food. """

		dist = self._calcDistance(self.food.loc, loc)
		if dist == 0:
			return 1
		else:
			return 1/dist # why does changing the reward magnitude change the sensor-delta magnitude?

	def getSensors(self):
		""" the currently visible state of the world (the observation may be
			stochastic - repeated calls returning different values)

			:rtype: by default, this is assumed to be a numpy array of doubles
		"""
		# get sensor locations
		lx, ly, rx, ry = self.seeker.calcAbsoluteSensorPositions()

		# return the strength of the chemical signals at the seeker's left and right sensors
		return [ self.calcSignal(toPygame((lx, ly))), self.calcSignal(toPygame((rx, ry))) ]

	def performAction(self, action):
		""" perform an action on the world that changes its internal state (maybe
			stochastically).
			:key action: an action that should be executed in the Environment.
			:type action: by default, this is assumed to be a numpy array of doubles
			
			action[0] is the left motor/effector neuron output, action[1] is the right
		"""

		self.seeker.move_body(action[0], action[1])

		self.movement_tracker.append(toPygame(self.seeker.body.position))

		# redraw
		self._draw()

	def reset(self):
		""" Reinitializes the environment with the food in a random location
			and the seeker with a random direction in a random location.
		"""
		from random import random
		self.movement_tracker = []
		self.food.setLocation((random()*SCREEN_SIZE, random()*SCREEN_SIZE))
		self.seeker.reset()