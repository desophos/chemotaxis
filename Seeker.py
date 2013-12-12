from pymunk import pygame_util
import pygame
import pymunk
from globals import SCREEN_SIZE
from math import pi

class Seeker(pygame.sprite.Sprite):
	STEP_TIME = 0.1
	RADIUS = 5
	SENSOR_RADIUS = 2
	VELOCITY_LIMIT = 5
	ANGULAR_VELOCITY_LIMIT = pi/16
	WALL_WIDTH = 2.0
	amin = 0
	amax = 0

	def __init__(self):
		
		# pygame init
		
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([10, 10])

		# pymunk init
		self.space = pymunk.Space()
		
		self.walls = [
					pymunk.Segment(self.space.static_body, (0,0+self.WALL_WIDTH), (SCREEN_SIZE, 0+self.WALL_WIDTH), self.WALL_WIDTH), # bottom
					pymunk.Segment(self.space.static_body, (0,0), (0, SCREEN_SIZE), self.WALL_WIDTH), # left
					pymunk.Segment(self.space.static_body, (0, SCREEN_SIZE), (SCREEN_SIZE, SCREEN_SIZE), self.WALL_WIDTH), # top
					pymunk.Segment(self.space.static_body, (SCREEN_SIZE-self.WALL_WIDTH, 0), (SCREEN_SIZE-self.WALL_WIDTH, SCREEN_SIZE), self.WALL_WIDTH) # right
					]
		
		def collision(space, arbiter, *args, **kwargs):
			""" make seeker bounce off walls """
			self.body.velocity.x = -self.body.velocity.x
			self.body.velocity.y = -self.body.velocity.y
			self.body.angle += pi
		
		c = 1
		for wall in self.walls:
			self.space.add_collision_handler(0, c, begin=collision)
			wall.collision_type = c
			c += 1
			wall.friction = 1.0
			wall.group = 1
			wall.color = pygame.color.THECOLORS["black"]
			
		self.space.add(self.walls)
		
		self.force_l = pymunk.Body(1,1)
		self.force_r = pymunk.Body(1,1)
		self.force_line_l = pymunk.Segment(self.force_l, (0,0), (0,0), 1)
		self.force_line_r = pymunk.Segment(self.force_r, (0,0), (0,0), 1)
		
		self.force_space = pymunk.Space()
		self.force_space.add(self.force_line_l, self.force_line_r)

		self.body = pymunk.Body(mass=5, moment=1000) # tweak these to decrease spinning out of control
		self.body.velocity_limit = self.VELOCITY_LIMIT
		self.body.angular_velocity_limit = self.ANGULAR_VELOCITY_LIMIT

		self.body_shape = pymunk.Circle(self.body, self.RADIUS, (0, 0))
		self.sensor_left = pymunk.Circle(self.body, self.SENSOR_RADIUS, (-self.RADIUS, 0))
		self.sensor_right = pymunk.Circle(self.body, self.SENSOR_RADIUS, (self.RADIUS, 0))
		
		self.body_shape.collision_type = 0
		
		self.body_shape.color = pygame.color.THECOLORS["black"]
		self.sensor_left.color = pygame.color.THECOLORS["red"]
		self.sensor_right.color = pygame.color.THECOLORS["red"]
		
		self.space.add(self.body, self.body_shape, self.sensor_left, self.sensor_right)
		
		self.reset()

	def orientate_sensors(self, left_sensor_relative_pos, right_sensor_relative_pos):
		self.space.remove(self.sensor_left, self.sensor_right)
		
		self.sensor_left = pymunk.Circle(self.body, self.SENSOR_RADIUS, left_sensor_relative_pos)
		self.sensor_right = pymunk.Circle(self.body, self.SENSOR_RADIUS, right_sensor_relative_pos)
		
		self.space.add(self.sensor_left, self.sensor_right)
		
	def update_force_lines(self, force_l_start, force_l_end, force_r_start, force_r_end):
		self.force_space.remove(self.force_line_l, self.force_line_r)
		
		self.force_line_l = pymunk.Segment(self.force_l, force_l_start, force_l_end, 1)
		self.force_line_r = pymunk.Segment(self.force_r, force_r_start, force_r_end, 1)
		
		self.force_space.add(self.force_line_l, self.force_line_r)

	def position_body(self, pos=None):
		from random import random

		if not pos:
			pos_range = SCREEN_SIZE-self.WALL_WIDTH # lower maximum
			pos = random()*pos_range + self.WALL_WIDTH # raise minimum
			self.body.position = (pos, pos)
		else:
			self.body.position = pos

	def reset_velocity(self):
		self.body.velocity = (0,0)
		self.body.angular_velocity = 0

	def update(self, surface):
		#lx,ly,rx,ry = self.calcSensorPositions()

		self.space.step(self.STEP_TIME)
			
		# wrap sloppily around edges
		#if (self.body.position.x < 0):
		#	self.position_body((SCREEN_SIZE, self.body.position.y))
		#if (self.body.position.x > SCREEN_SIZE):
		#	self.position_body((0, self.body.position.y))
		#if (self.body.position.y < 0):
		#	self.position_body((self.body.position.x, SCREEN_SIZE))
		#if (self.body.position.y > SCREEN_SIZE):
		#	self.position_body((self.body.position.x, 0))

		#print self.body.position

		pygame_util.draw(surface, self.space)
		pygame_util.draw(surface, self.force_space)

	def reset(self):
		self.position_body()
		self.reset_velocity()

	def calcRelativeSensorPositions(self):
		""" Calculate locations of sensors using the magic of trigonometry. """
		from math import sin, cos
		
		lx = self.RADIUS * sin(self.body.angle)
		ly = self.RADIUS * -cos(self.body.angle)
		rx = self.RADIUS * -sin(self.body.angle)
		ry = self.RADIUS * cos(self.body.angle)

		return lx, ly, rx, ry

	def calcAbsoluteSensorPositions(self):
		lx, ly, rx, ry = self.calcRelativeSensorPositions()
		
		lx += self.body.position[0]
		ly += self.body.position[1]
		rx += self.body.position[0]
		ry += self.body.position[1]

		return lx, ly, rx, ry

	def constrain_angle(self, angle):
		""" keep angle between 0 and 2*pi """
		if angle > 2*pi:
			angle = angle - 2*pi
		elif angle < 0:
			angle = 2*pi - angle
			
		return angle

	def move_body(self, la, ra):
		""" apply forces to the seeker's body """
		from math import sin, cos
		
		print la, ra
		
		self.body.angle = self.constrain_angle(self.body.angle)
		
		lx, ly, rx, ry = self.calcRelativeSensorPositions()
		
		self.orientate_sensors((lx,ly), (rx,ry))
		
		self.body.reset_forces()
		
		a = self.body.angle
		
		# break down forces into their x and y components
		force_lx = la * cos(a)
		force_ly = la * sin(a)
		force_rx = ra * cos(a)
		force_ry = ra * sin(a)
		
		# apply forces at the sensor locations in the direction of the seeker
		self.body.apply_force((force_lx, force_ly), (lx, ly))
		self.body.apply_force((force_rx, force_ry), (rx, ry))
		
		lx, ly, rx, ry = self.calcAbsoluteSensorPositions()
		
		self.update_force_lines((lx, ly), (lx+force_lx, ly+force_ly), (rx, ry), (rx+force_rx, ry+force_ry))