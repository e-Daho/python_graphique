#! /usr/bin/env python
# -*-coding: utf-8-*-

from math import sqrt, tan 

class Vector(object):
	''' 
	classe définissant un vecteur dans l'espace caractérisé par
	[*] sa coordonnée x (int ou float)
	[*] sa coordonnée y (int ou float)
	[*] sa coordonnée z (int ou float)
	'''

	def __init__(self, x, y, z):
		self.xyz = [float(0) for i in xrange(3)]
		self.xyz[0] = x
		self.xyz[1] = y
		self.xyz[2] = z

	@property
	def sqrNorm(self):
		return sqrt(self.xyz[0]*self.xyz[0] + self.xyz[1]*self.xyz[1] + self.xyz[2]*self.xyz[2])

	@property
	def getNormalized(self):
		return Vector(self[0] * (1 / self.sqrNorm), self[1] * (1 / self.sqrNorm), self[2] * (1 / self.sqrNorm))

	def __getitem__(self, i):
		return self.xyz[i]

	def __add__(v1, v2):
		return Vector(v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2])

	def __sub__(v1, v2):
		return Vector(v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])

	def __mul__(self, a):
		return Vector(a * self[0], a * self[1], a * self[2])

	def __str__(self):
		return "[%f,%f,%f]" % (self[0], self[1], self[2])

	def dot(self, v2):
		return self[0] * v2[0] + self[1] * v2[1] + self[2] * v2[2]