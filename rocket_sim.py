from processing_py import *
from scene import Scene
from rocket import Rocket
from controller import RocketController
from FNN import ControllerNetwork

from datetime import datetime


"""
Welcome to the rocket simulation!
Try and land the virtual rocket on the red pad.
Don't fall to hard or tilt too much though!

First, change you name on line 37!

Use these keys to control the rocket:
	KEY   ->   BEHAVIOUR
	'w'   ->   Turn engine on
	' '   ->   Turn engine off <space>
	's'   ->   Stop rotation
	'a'   ->   Rotate anticlockwise (turn left)
	'd'   ->   Rotate anticlockwise (turn right)
	'r'   ->   Reset all values of rocket (pos, vel, acc)

You can play another game directly by pressing 'r'.
Right after you land, the target is reset, so don't worry
if it suddenly jumps away, your success/failure was duly recorded.

You can just close the pop up panel when you are done playing.

Thanks for playing!
"""

##### CHANGE YOUR NAME HERE #####

player_name = 'satchit'

subdir = 'saved_runs'

scene = Scene(1000, 1000)
rocket = Rocket(scene, start_pos='random')
controller = RocketController(rocket, physical_control=True)

saved_data = False

while(True):

	if rocket.is_dead:
		if not saved_data:
			print('Rocket has landed!')
			print(f'Landing was a {"success" if rocket.check_success() else "failure"}!')

			cur_time = datetime.now()
			test_time = cur_time.strftime('%Y%m%dT%H%M%S')
			# controller.save_to_file(f'{subdir}/{player_name}_save_{test_time}.csv')
			
			saved_data = True

	controller.control()
	rocket.update()

	if len(controller.physical_history)>=1 and not rocket.is_dead:
		saved_data = False

			
	scene.draw()