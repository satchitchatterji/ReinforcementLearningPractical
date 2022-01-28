import numpy as np

class MLP_wrapper:
	def __init__(self, mlp, scaler = None):
		self.mlp = mlp
		self.scaler = scaler

	def get_move(self, move):
		outputs = ['w', ' ', 's', 'a', 'd', 'p']
		try:
			# sklearn MLPClassifier works with this
			# as far as MLP.py is written
			return outputs[move]
		except IndexError:
			# tflearn DNN works with this
			# as far as MLP_tnsrfl.py is written
			return outputs[move]

	def scale(self, inputs):
		inputs = np.array(inputs).reshape(1, -1)
		self.scaler.transform(inputs)
		inputs = inputs.reshape(-1, 1)
		return inputs

	def get_decision(self, inputs):
		try:
			# sklearn MLPClassifier works with this
			# as far as MLP.py is written
			print(self.get_move(self.mlp.predict([inputs])))
			return self.get_move(self.mlp.predict([inputs]))

		except ValueError:
			# tflearn DNN works with this
			# as far as MLP_tnsrfl.py is written
			if self.scaler is not None:
				inputs = self.scale(inputs)
			inputs = inputs.reshape(-1,len(inputs),1)
			return self.get_move(np.argmax(self.mlp.predict(inputs)))
