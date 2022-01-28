import sys
sys.path.append("..")
sys.path.append("NNProject")

from datetime import datetime
from processing_py import *

from SARSAAgent import SARSAAgent
from episode import run_single_episode
from plot_scores import plot_scores

from scene import Scene
from rocket import Rocket
from controller import RocketController
from extras import Vector

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


MAX_FRAMES = 20*60      # max episode length
continual_draw = False  # whether or not to draw to screen

# create environment
scene = Scene(1000, 1000, init_target_val='random', is_drawn=continual_draw)
rocket = Rocket(scene, start_pos='air_center')
controller = RocketController(rocket, physical_control=False)

input_len = len(rocket.get_data_list())
controls = ['w',' ', 's', 'a', 'd', 'p']

model_name = "betterSARSAv3"

# model = tf.keras.models.load_model('saved_models/SARSAv3.model')
model = None
agent = SARSAAgent(n_inputs=input_len, controls=controls, func_approx=model)

# for saving score data to file
cur_time = datetime.now()
last_scores = []
cumulative_scores = []

i_episode = 0

while(True):
	print(f"################# EPISODE {i_episode} #################")

	score, cumulative_score = run_single_episode(scene, rocket, controller, agent, 'random', MAX_FRAMES, continual_draw)

	print("Agent final score:", score)
	print("Agent total score:", cumulative_score)

	last_scores.append(score)
	cumulative_scores.append(cumulative_score)
	
	if i_episode%20==0:
		agent.save_model(f'better_sarsa_models/{model_name}.model')
		agent.save_details(f'better_sarsa_models/{model_name}.txt')
		try:
			plot_scores(last_scores, cumulative_scores, f'better_sarsa_models/{model_name}')
		except:
			print("WARNING: Problem plotting scores!")

		with open(f"better_sarsa_models/{model_name}_scores.txt", 'w') as f:
			f.write(cur_time.strftime("%d/%m/%Y %X")+"\n")
			f.write("Train time: "+str(datetime.now()-cur_time)+"\n")
			f.write(f"Trials: {i_episode}\n")
			f.write("\nFinal scores:\n")
			f.write(repr(last_scores))
			f.write('\n\n')
			f.write("Cumulative scores:\n")
			f.write(repr(cumulative_scores))
	
	rocket.reset_all()
	i_episode+=1
