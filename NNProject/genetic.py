import numpy as np
from processing_py import *
from random import uniform

from scipy.stats import norm

from scene import Scene
from rocket import Rocket
from controller import RocketController
from FNN import ControllerNetwork
from extras import Vector, normalize

class ControllerPopulation:
	# population of controller MLPs as defined in
	# FNN.py with methods to reproduce
	def __init__(self, controller_list, nn_list):
		self.controllers = controller_list
		self.population = nn_list
		self.pop_len = len(controller_list)
		self.fitnesses = np.zeros((1, self.pop_len))
		self.rep_method = self.crossover_all

	def targetted_fitness_gaus(self, value, sigma = 100):
		# for each trait, the fitness is the normal probability
		# of attaining the trait value with a mean of 0 (ideal value)
		return norm.pdf(value, loc = 0, scale = sigma)

	def calc_fitnesses(self):
		self.fitnesses = [p.rocket.score() for p in self.controllers]
		print(min(self.fitnesses))
		# print([p.rocket.get_relative_rotation() for p in self.controllers])
		sd = min(self.fitnesses)/2
		
		if sum(self.fitnesses) == 0 or 'nan' in str(self.fitnesses):
			self.fitnesses = np.array([1]*self.pop_len)
		
		self.fitnesses = np.array([self.targetted_fitness_gaus(f,sd) for f in self.fitnesses])

		if sum(self.fitnesses) == 0 or 'nan' in str(self.fitnesses):
			self.fitnesses = np.array([1]*self.pop_len)

	def roulette_wheel(self):
		self.calc_fitnesses()
		# print(self.fitnesses)
		return (self.fitnesses)/sum(self.fitnesses)


	def choose_parents_clonal(self):
		# choose nn to be cloned probabilistically
		parents = []
		probs = self.roulette_wheel()
		for i in range(self.pop_len):
			parents.append(np.random.choice(self.pop_len, p=probs))
		return parents

	def choose_parents(self, clonal = True):
		# choose parents probabilistically, on the basis of 
		# fitness, n=1 == clone of parent (crossover to be added)

		# if clonal:
		# 	return self.choose_parents_clonal()

		parents = []
		probs = self.roulette_wheel()

		# for each i of the next gen,
		# 	choose each parent
		for i in range(self.pop_len):
			parents.append([])
			for _ in range(2):
				child_index = np.random.choice(self.pop_len, p=probs)
				parents[i].append(child_index)
				if clonal:
					parents[i].append(child_index)
					break

		return parents

	def crossover_nets(self, net1, net2):
		child = ControllerNetwork(net1.size[0], net1.controls)
		crossover_point = np.random.randint(net1.size[0])
		
		child.layers[0].weights[0:crossover_point] = net1.layers[0].weights[0:crossover_point] 
		child.layers[0].weights[crossover_point:] = net2.layers[0].weights[crossover_point:]

		return child

	def crossover_all(self):
		next_gen = []
		parents = self.choose_parents()
		
		for i in range(self.pop_len):
			couple = self.population[parents[i][0]], self.population[parents[i][1]]
			child = self.crossover_nets(*couple)
			next_gen.append(child)

		return next_gen

	def clonal(self):
		# this needs to be made faster
		next_gen = []
		parents = self.choose_parents_clonal()
		for p in parents:
			parent = self.population[p]
			child = ControllerNetwork(parent.size[0], parent.controls, single_layer=False)
			for i, layer in enumerate(parent.layers):
				old_params = parent.get_layer_parameters(layer=i)

				child.add_layer(*old_params[0].shape)
				child.set_layer_parameters(layer=i, weights=old_params[0], biases=old_params[1])
			next_gen.append(child)

		return next_gen

	def mutate_array(self, arr, rate, sigma):
		to_mutate = np.round(np.random.random(arr.shape)+rate-0.5)
		changes = np.random.normal(0, sigma, arr.shape)
		mutations = np.multiply(to_mutate, changes)
		arr = np.add(mutations, arr)
		return arr

	def mutate_nn_weights_biases(self, nn, rate, sigma):
		for i in range(len(nn.layers)):
			weights = self.mutate_array(nn.layers[i].weights, rate, sigma)
			# biases = self.mutate_array(nn.layers[i].biases, rate, sigma)
			biases = nn.layers[i].biases
			nn.set_layer_parameters(layer=i, weights=weights, biases=biases)


	def mutate_all(self, rate = 1, sigma = 0.1):
		for i in range(len(self.population)):
			self.mutate_nn_weights_biases(self.population[i], rate, sigma)

	def reproduce(self):
		self.population = self.rep_method()
		# print(self.population)
		self.mutate_all()

		return self.population
# n_rockets = 3

# scene = Scene(1000, 1000)
# rockets = [Rocket(scene, start_pos=Vector(100,100)) for _ in range(n_rockets)]

# input_len = len(rockets[0].get_data_list())
# controls = ['w',' ', 's', 'a', 'd']

# controllers = [RocketController(r, physical_control = False) for r in rockets]
# cns = [ControllerNetwork(input_len, controls) for _ in range(n_rockets)]

# cp = ControllerPopulation(controllers, cns)

# print(cp.get_next_gen())