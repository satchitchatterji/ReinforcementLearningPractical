# maybe replace with numpy vector

import math
import numpy as np
class Vector:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def zeros(self):
		self.x = 0
		self.y = 0

	def dist(self, other):
		return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

	def mag(self):
		return math.sqrt(self.x**2 +  self.y**2)

	def __neg__(self):
		return Vector(-self.x, -self.y)

	def __add__(self, other):
		return Vector(self.x+other.x, self.y+other.y)

	def __sub__(self, other):
		return Vector(self.x-other.x, self.y-other.y)

	def __repr__(self):
		return(f"x: {self.x}, y: {self.y}")

def normalize(v):
    norm = np.linalg.norm(np.array(v))
    if norm == 0:
       return v
    return v / norm