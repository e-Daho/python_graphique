#! /usr/bin/env python
# -*-coding: utf-8-*-

class Camera():
	'''
	classe représentant la caméra caractérisée par
	[*] son foyer (Vector)
	[*] son "field of vision", c'est à dire son angle d'ouverture en radian (float)
	'''

	def __init__(self, foyer, fov, direction, up, right):
		self.foyer = foyer
		self.fov = fov
		self.direction = direction
		self.up = up
		self.right = right
