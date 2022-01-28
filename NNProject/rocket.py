import os
import math
import numpy as np
from random import uniform
from extras import Vector, normalize
from copy import copy

class Rocket:

	"""
	A simplistic rocket model, that, given a Scene object,
	can have a thrust and rotate. Its position can be intialised
	at a known (x,y) position or randomly initialised within the
	boundaries of the scene. 

	"""

	########## Initialisation ##########

	def __init__(self, scene, start_pos = 'random'):

		self.scene = scene

		self.draw_pos = Vector(0,0) # the position where the rocket image is drawn (top left position)
		self.center_pos = Vector(0,0) # the center position of the image (can be understood as the rocket's position)
		self.vel = Vector(0, 0) # velocity vector of the rocket
		self.thrust = Vector(0, 0) # thrust/acceleration vector of the rocket
		self.rotation = 0 # current rotation angle (in radian) of the rocket, with respect to vertical
		self.engine_on = False # whether or not the rocket is accelerating
		self.fuel = 100 # the fuel in the rocket, the engine cannot turn on if 0

		self.is_dead = False # if the rocket has crashed or landed, it is dead

		# rocket image data, numbers are only wrt the image itself
		self.img_height = 100
		self.img_width = 0.7*self.img_height

		# fire image data, numbers are only wrt the image itself
		self.fire_img_width = 0.25 * self.img_width
		self.fire_img_height = 10/9 * self.fire_img_width

		self.BASE_DIR = os.path.dirname(os.path.abspath(__file__)).upper()

		# load the images
		if self.scene.is_drawn:
			self.rocket_img_path = self.BASE_DIR+'/rocket.png'
			self.rocket_img = self.scene.app.loadImage(self.rocket_img_path)
			self.fire_img_path = self.BASE_DIR+'/fire.png'
			self.fire_img = self.scene.app.loadImage(self.fire_img_path)

		# a few constants that tend not to change over the lifetime of the rocket
		# these need not be constants, but it makes sense that they are 
		self.consts = {}
		self.consts["rotation_speed"] = 0.02 # angular velocity is constant while turning
		self.consts["thrust"] = 0.02 # acceleration is constant per time second
		self.consts["init_lims_x"] = (0, self.scene.width) # initialization boundary (wrt width of scene)
		self.consts["init_lims_y"] = (0, self.scene.height/2) # initialization boundary (wrt upper half of scene)
		self.consts["init_pos"] = self.get_start_pos(start_pos) # get the initial position of the rocket
		self.consts["fuel_consumption"] = 0.5; # amount of fuel consumed per time step

		# reset position, velocity, thrust, rotation, and add self to scene
		self.reset_all()		
		self.scene.add_rocket(self)

		# data accessible of rocket, see method self::get_data 
		# for the list of values currently exported
		self.data = {}
		self.score_mult = np.array([-1, 0, 0, 0]) # relative importance of distance, vel, rot, fuel
		self._score = None

	def get_start_pos(self, init = 'random'):
		"""
		Generates starting positon of rocket.
		switch init:
			case 'center': return (center of screen, placed upon ground)
			case 'air_center' : return (center of screen, placed in air)
			case 'random': return (random, random) within init_limits
			case type(init)==Vector: return init
			default: return (0,0)
		"""
		if init == 'center':
			return Vector(self.scene.width/2 - self.img_width/2, 
						  self.scene.height - self.scene.ground_height - self.img_height)
		elif init == 'air_center':
			return Vector(self.scene.width/2 - self.img_width/2, self.img_height)
		elif init == 'random':
			x = uniform(*self.consts["init_lims_x"]) - self.img_width/2
			y = uniform(*self.consts["init_lims_y"])
			return Vector(x, y)
		elif type(init) == Vector:
			return init
		else:
			return Vector(0,0)


	########## Reset object ##########

	def reset_rotation(self):
		"""
		Set the rocket upright (vertical)
		"""
		self.rotation = 0

	def reset_position(self):
		"""
		Re-place rocket wherever it was initially initialised
		"""
		self.draw_pos = self.consts["init_pos"]
		self.update_center_pos()

	def reset_movement(self):
		"""
		Reset acceleration, velocity, turn engine off
		"""
		self.thrust.zeros()
		self.vel.zeros()
		self.engine_on = False
	
	def reset_all(self):
		"""
		Resets position, movement, and rotation of rocket
		"""
		self.is_dead = False
		self.fuel = 100
		self.reset_position()
		self.reset_movement()
		self.reset_rotation()


	########## Updation functions ##########

	def control_engine(self, turn_on=True):
		if turn_on:
			if self.fuel > 0:
				self.engine_on = True
		else:
			self.engine_on = False

	def update_center_pos(self):
		"""
		Update the center position of the rocket with respect to the
		drawing position of the image onto the scene. This should be 
		ideally done the opposite way, updating the draw position wrt
		the center position, but this is the way it's done now. Since 
		the center pos and draw pos are a contant distance (center of
		the image and the top left), it doesn't really matter that much
		in the long run, but may be updated in the future. 
		"""
		self.center_pos.x = self.draw_pos.x + self.img_width/2
		self.center_pos.y = self.draw_pos.y + self.img_height/2

	def update_fire_coords(self):
		"""
		Updates where the fire should be drawn with respect to the image.
		These numbers are specific to the rocket.png and fire.png images.
		"""
		self.fire_x = 0.38*self.img_width - self.img_width/2
		self.fire_y = 0.94*self.img_height - self.img_height/2


	def update_thrust(self):
		"""
		Update the thrust of the rocket if the engine is on, else set the thrust
		to zero. The magnitude of the thrust vector is constant in this simulation
		but it does not have to be. Components are calculated with trig, as usual.
		Because the y-position on screen gets larger the more towards the bottom
		of the screen you go, the thrust is negative (we want the rocket to go
		up the screen, so reduce its y-value over time).
		"""
		if self.engine_on:
			self.thrust.x = -self.consts["thrust"]*math.cos(self.rotation+math.pi/2)
			self.thrust.y = -self.consts["thrust"]*math.sin(self.rotation+math.pi/2)

			self.fuel -= self.consts["fuel_consumption"]
			if self.fuel < 0:
				self.fuel = 0
				self.control_engine(turn_on=False)

		else:
			self.thrust.zeros()

	def update_velocity(self):
		"""
		Update the velocity of the rocket. There are two forces that affect
		the velocity of the rocket here: gravity and thrust. These accelerate
		the rocket over time.
		"""
		self.vel += self.scene.gravity
		self.vel += self.thrust

	def update_position(self):
		"""
		Update the position of the rocket by adding on the velocity vector
		for one time step.
		"""
		self.draw_pos += self.vel

		# check for collision with the ground
		# if so, reset velocity and thrust.
		if self.draw_pos.y + self.img_height > self.scene.height - self.scene.ground_height:
			self.draw_pos.y = self.scene.height - self.scene.ground_height - self.img_height
			# self.reset_movement()
			self.is_dead = True

		self.update_center_pos()
		
	def update(self):
		"""
		Functionally updates the acceleration, velocity and position of rocket.
		"""
		if self.is_dead:
			return

		self.update_thrust()
		self.update_velocity()
		self.update_position()


	########## Visualisation ##########

	def draw(self):
		"""
		This function enables the rocket to be drawn on screen.

		It is a little involved and needs a little knowledge of Processing 3
		or the processing api being used to draw it, but let me know if you'd
		like me to extend this comment to include more information about it,
		or ask me directly if you're curious -satchit
		"""

		if not self.scene.is_drawn:
			return

		self.scene.app.pushMatrix()
		self.scene.app.translate(self.center_pos.x, self.center_pos.y)
		self.scene.app.rotate(self.rotation)

		if self.engine_on:
			self.update_fire_coords()
			self.fire_img = self.scene.app.loadImage(self.fire_img_path)
			self.scene.app.image(self.fire_img, self.fire_x, self.fire_y, self.fire_img_width, self.fire_img_height)
		

		self.rocket_img = self.scene.app.loadImage(self.rocket_img_path) 
		self.scene.app.image(self.rocket_img, -self.img_width/2, -self.img_height/2, self.img_width, self.img_height)
		self.scene.app.ellipse(0, 0, 10, 10)

		self.scene.app.popMatrix()


	########## Scoring System ##########

	def get_relative_rotation(self):
		return min(abs(self.rotation), abs(2*math.pi-self.rotation))

	def get_tared_out_distance(self): 
		# min distance score is now 0, not 50
		return abs(self.img_height/2 - self.center_pos.dist(self.scene.target_center))

	def calc_score(self, recalc=True):
		distance = self.get_tared_out_distance()
		vel = self.vel.mag()
		rot = self.get_relative_rotation()
		fuel = 100-self.fuel
		dependables = np.array([distance, vel, rot, fuel])
		self._score = np.dot(dependables, self.score_mult)

	def set_score(self, val):
		self._score = val

	def score(self, recalc=False):
		# update data
		self.get_data()

		if recalc or self._score is None:
			self.calc_score()

		return self._score

	def check_success(self):
		return (self.is_dead
			and (self.get_relative_rotation() < np.pi/12) 
			and (self.vel.mag() < 2)
			and (abs(self.center_pos.x - self.scene.target_center.x) < self.scene.target_size/2)
			and (abs(self.center_pos.y - self.scene.target_center.y) < self.img_height+10)
			)

	########## Data export ##########

	def get_data(self):
		"""
		Export the quasi-physical data of the rocket as a dictionary.
		The variables being exported are self-explanitory 
		"""
		self.data['x_pos'] = self.center_pos.x
		self.data['y_pos'] = self.center_pos.y
		self.data['x_vel'] = self.vel.x
		self.data['y_vel'] = self.vel.y
		self.data['x_thrust'] = self.thrust.x
		self.data['y_thrust'] = self.thrust.y
		self.data['rotation'] = self.get_relative_rotation()
		self.data['engine'] = self.engine_on
		self.data['x_target'] = self.scene.target_center.x
		self.data['y_target'] = self.scene.target_center.y
		self.data['fuel'] = self.fuel

		return self.data

	def get_data_list(self, normalized=False):
		ls = list(self.get_data().values())
		if normalized:
			ls = list(normalize(ls))
		return ls

	def __lt__(self, other):
		return self.score() < other.score()