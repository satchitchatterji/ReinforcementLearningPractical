from processing_py import *
from random import uniform
from extras import Vector

class Scene:
	"""
	Simple scene that is drawn on the screen, consisting
	of the ground, a target, and an arbitrary number of rockets.
	This needs to be drawn and updated if you want to control this
	with a keyboard (since key inputs are tied to the draw panel).
	It is initialised with a window width and height, and rockets
	can be added to a scene with the add_rocket function.

	TODO: Since gravity is tied to the scene, a window is created
	(the window is tied to the App class instance), so if something
	like a rocket training sequence is needed, a window has to exist,
	which is not idea. So in the future, try to disentange the window
	with the controlling/updating of the rocket (maybe with the MVC paradigm?) 
	"""

	########## Initialisations ##########

	def __init__(self, width, height, init_target_val = 'random', is_drawn = True):
		
		self.is_drawn = is_drawn
		# decide whether or not to draw the scene incl rockets onto the screen
		# if the control is automated, the movements will be far far faster
		# if this is false.
		if self.is_drawn:
			self.app = App(width, height)

		self.width = width
		self.height = height
		self.ground_height = 20 # height of the ground from the bottom of window
		self.rockets = [] # list of rockets associated with screen

		self.gravity = Vector(0, 0.01) # gravity of scene

		self.target_size = 100 # width of target drawn to screen
		self.target_lims = (0, self.width-self.target_size) # limits of where the target is initialised
		self.init_target(init_target_val)


	def init_target(self, init_val = 'random'):
		if init_val == 'random':
			self.target_pos = uniform(*self.target_lims) # generate initial target position	
		elif type(init_val) == int:
			self.target_pos = init_val
			
		else:
			print('Target initialization failed, reverting to zero.')
			self.target_pos = 0

		self.target_center = Vector(self.target_pos+self.target_size/2, self.height-self.ground_height) # center x-coord of target
	
	########## Rocket-specific functions ##########

	def add_rocket(self, rocket):
		"""
		Associate rocket with this scene
		"""
		self.rockets.append(rocket)

	def draw_rockets(self):
		"""
		Draws rocket(s) to the screen if
		the list of rockets is not empty
		"""
		if self.rockets:
			for rocket in self.rockets:
				rocket.draw()

	########## Draw scene ##########

	def draw_background(self):
		"""
		Draws draws background. For now, it is just black.
		"""
		self.app.background(0,0,0)

	def draw_ground(self, col=(33,179,47)):
		"""
		Draw ground onto scene. For now, it is a green rectangle
		at the bottom of the screen with height := ground_height
		"""
		self.app.fill(*col)
		self.app.rect(0, self.height-self.ground_height, self.width, self.ground_height)

	def draw_target(self, col=(255,0,0)):
		"""
		Draw target onto scene. For now, it is a red rectangle
		at the bottom of the screen on the ground with height := ground_height
		and width := target_size
		"""
		self.app.fill(*col)
		self.app.ellipse(self.target_center.x, self.height-self.ground_height, 10,10)
		self.app.rect(self.target_pos, self.height-self.ground_height, self.target_size, self.ground_height)


	def draw(self):
		"""
		Draw all necessary elements of the scene (background,
		ground, target, rockets) and refresh the window. This
		is meant to be called at each time frame. Rockets are
		updated OUTISDE of this scene (though it could be better
		to add it here? Lemme know).
		"""
		if not self.is_drawn:
			return

		self.draw_background()
		self.draw_ground()
		self.draw_target()
		self.draw_rockets()
		self.app.redraw()
		
		# At each time step, check if the user closed the window, and
		# stop the program in that case. This is necessary since if you
		# just close the window, the program keeps running in the 
		# background (this is because the window is a Java applet which is)
		# initialised by the py program, but runs independently.
		# Also find a safer way to do this maybe?
		if self.app.isDead._flag:
			exit()