import numpy as np

# custom MLP used for evolution,
# does not have backprop to learn

class Layer:

	# models a single layer in an MLP
	def __init__(self, n_inputs, n_neurons):
		self.weights = np.random.randn(n_inputs, n_neurons)
		self.biases = np.random.randn(1, n_neurons)
		# self.biases = np.zeros((1, n_neurons))
		self.activation_f = self.relu

	##### Activation functions #####
	
	def identity(self, x):
		return x

	def tanh(self, x):
		return np.tanh(x)

	def relu(self, x):
		return np.maximum(0, x)

	def sigmoid(self, x):
		return (1/(1 + np.exp(-x)))

	##### set and get parameters #####
	def set_parameters(self, weights, biases):
		self.weights = weights
		self.biases = biases

	def get_parameters(self):
		return self.weights, self.biases

	##### Forward pass #####
	def forward(self, inputs):
		self.outputs = self.activation_f(np.dot(inputs, self.weights) + self.biases)


class ControllerNetwork:
	# models an MLP for controlling a rocket
	def __init__(self, n_inputs, output_controls, single_layer=False, empty_net = False):
		self.size = (n_inputs, len(output_controls))
		self.controls = output_controls
		self.layers = []

		if empty_net:
			# no layers, to aid speed
			# in case they're added in via
			# the setter methods
			return

		if single_layer:
			# Just a single layer
			self.add_layer(n_inputs, len(output_controls))
		else:
			# build the architecture of the network here
			self.add_layer(n_inputs, n_inputs)
			self.add_layer(n_inputs, n_inputs)
			self.add_layer(n_inputs, len(output_controls))
			# you can add more layers here
			# make sure the nth layer ouput is the
			# same length as (n+1)th layer input
			# and the final layer has output length
			# equal to len(output_controls).

	def add_layer(self, input_size, output_size):
		# add layer to the end of the current architecture
		self.layers.append(Layer(input_size, output_size))

	##### setters and getters #####
	def set_layer_parameters(self, layer=0, weights=None, biases=None):
		self.layers[layer].set_parameters(weights, biases)

	def get_layer_parameters(self, layer=0):
		return self.layers[layer].get_parameters()

	##### forward pass through all layers #####
	def forward(self, inputs):
		last_outputs = inputs
		for i in range(len(self.layers)):
			self.layers[i].forward(last_outputs)
			last_outputs = self.layers[i].outputs

	def get_max(self):
		highest = np.argmax(self.layers[-1].outputs)
		return highest

	def get_decision(self, inputs):
		self.forward(inputs)
		return self.controls[self.get_max()]