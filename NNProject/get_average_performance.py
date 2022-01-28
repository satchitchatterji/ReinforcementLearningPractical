import pickle

from random import uniform

from scene import Scene
from rocket import Rocket
from controller import RocketController
from FNN import ControllerNetwork
from MLP_wrapper import MLP_wrapper
from extras import Vector
import numpy as np
import matplotlib.pyplot as plt
import os

from MLP_tensorflow import neural_network_model

save_plots=False
save_path='flight_paths'
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

# distance, vel, rot, fuel
score_weights = [1,0,0,0]

# if your saved controllers (MLPs) are not pickled, then
# these need to be changed appropriately; also change
# the starts with and ends with.
# files = [x.replace('.pickle','').replace('sorted_cn_list_','') for x in os.listdir('tests') if x.endswith('.pickle')]

# If you just want to test a single controller, 
# you can just write 'files = [whatever]',
# if there is a whatever.pickle saved in your tests folder.

# You don't even need to have it pickled. Put whatever string
# you want in file_ref and change the line with 'cn=...' to
# do control stuff. The file ref is used for saving images otherwise
# so you can just write files = ['abc'] and it'll run.

files = ['abc']

for file_ref in files:
	print(f'file_ref = {file_ref}')
	
	# try:
	# put your own controller here
	# ideally it should have a get_decision method
	# so that it'll just be plug and play by
	# changing just one line of code.
	# Else, feel free to change the code as you need to.
	
	# cn = pickle.load(open(f'tests/sorted_cn_list_{file_ref}.pickle', 'rb'))[0]
	
	model_name='20210704T1606'
	model = neural_network_model(input_size = 11)
	model.load(f'tsfl_models/{model_name}.model', weights_only=True)
	scaler = pickle.load(open(f"tsfl_models/{model_name}_scaler.pkl",'rb'))

	cn = MLP_wrapper(model,scaler)

	paths_x = []
	paths_y = []
	scores = []
	test_targets = range(0,1001,25)

	for i in test_targets:
		paths_x.append([])
		paths_y.append([])

		scene = Scene(1000, 1000, init_target_val = i, is_drawn=False)
		rocket = Rocket(scene, start_pos='air_center')
		controller = RocketController(rocket, physical_control = False)
		rocket.score_mult = np.array(score_weights)

		frames = 60*60
		cur_frame = 0

		while(True):
			cur_frame+=1
			if cur_frame>frames:
				# print('Timeout!')
				rocket.is_dead = True

			if not rocket.is_dead:
				decision = cn.get_decision(rocket.get_data_list())
				controller.control(decision)
				rocket.update()
				paths_x[-1].append(rocket.center_pos.x)
				paths_y[-1].append(1000-rocket.center_pos.y)

			else:
				# print("\nAll rockets dead!")
				scores.append(rocket.score())
				break

	fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12,5.4))
	ax1.plot(test_targets, scores)
	ax1.set_title('Performance over target locations (starting from air_center)')
	ax1.set_xlabel('Target position')
	ax1.set_ylabel('Distance')
	ax1.grid(True)


	i=0
	for path_x, path_y in zip(paths_x, paths_y):
		ax2.plot(path_x, path_y, color=colors[i%10])
		# ax2.scatter([test_targets[i]], [0], color=colors[i%10], marker='.')
		ax2.plot([path_x[-1], test_targets[i]], [path_y[-1], 0], color=colors[i%10], alpha=0.5)
		
		i+=1
	# temp_r=Rocket(scene, start_pos='air_center')
	# ax2.scatter([temp_r.center_pos.x], [1000-temp_r.center_pos.y], marker='x', color='black')
	
	ax2.set_title('Flight paths')
	ax2.set_xlim(0,1000)

	if save_plots:
		plt.savefig(f'{save_path}/{file_ref}_distance_flight_path.png')

	plt.show()

	# except Exception as e:
	# 	print(e)
	# 	print('Error!')