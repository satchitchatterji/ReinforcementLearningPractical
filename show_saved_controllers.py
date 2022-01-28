import pickle


from processing_py import *
from random import uniform

from scene import Scene
from rocket import Rocket
from controller import RocketController
from FNN import ControllerNetwork
from extras import Vector

file_ref = '20210603T1435'

continual_draw = True
n_rockets = 1

scene = Scene(1000, 1000, init_target_val = 800)
rockets = [Rocket(scene, start_pos=Vector(100,100)) for _ in range(n_rockets)]

input_len = len(rockets[0].get_data_list())
controls = ['w',' ', 's', 'a', 'd']

controllers = [RocketController(rocket, physical_control = False) for rocket in rockets]
cns = pickle.load(open(f'tests/sorted_cn_list_{file_ref}.pickle', 'rb'))[49:50]

print(cns[0].layers[0].weights)
print(cns[0].layers[0].biases)

frames = 3600
cur_frame = 0
saved_data = False

ns = {}

for c in controls:
	ns[c] = 0
scores = []

while(True):

	if saved_data:
		scene.draw()
		continue

	cur_frame+=1
	if cur_frame>frames:
		print('Timeout!')
		for rocket in rockets:
			rocket.is_dead = True

	for i in range(len(rockets)):
		rocket = rockets[i]
		controller  = controllers[i]
		cn = cns[i]

		if rocket.is_dead:
			continue

		decision = cn.get_decision(rocket.get_data_list())
		if i == 0:
			# print(decision, end = ',')
			pass
		controller.control(decision)
		ns[decision]+=1
		rocket.update()

	deaths = sum([r.is_dead for r in rockets])
	if deaths == len(rockets):
		print("\nAll rockets dead!")
		for i in range(len(rockets)):
			scores.append(rockets[i].score())

		saved_data = True
		print(rockets[0].get_data())
		print(ns)
		print(min(scores), max(scores))
		print('Saved score data!')
		print("Don't forget to close the game panel!")
	
	if continual_draw:
		scene.draw()