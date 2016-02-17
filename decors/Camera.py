#! /usr/bin/env python
# -*-coding: utf-8-*-

class Camera():
	'''
	classe représentant la caméra caractérisée par
	[*] son foyer (Vector)
	[*] son "field of vision", c'est à dire son angle d'ouverture en radian (float)
	'''

	def __init__(self, foyer, fov):
		self.foyer = foyer
		self.fov = fov
