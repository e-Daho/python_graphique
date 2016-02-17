#! /usr/bin/env python
# -*-coding: utf-8-*-

class Intersection():
	'''
	classe représentant l'intersection de la sphère avec la droite Ray caractérisée par
	[*] la distance entre l'origine de la caméra et la sphère t (float)
	[*] la présence ou non d'un intersection (boolean)
	[*] le point d'intersection (Vector)
	[*] la normale en ce point (Vector)
	'''

	def __init__(self):
		self.t = 0.
		self.has_intersection = False
		self.pt_intersection = None
		self.normale = None

	def __str__(self):
		return "%f, %s, %s, %s" % (self.t, self.has_intersection, str(self.pt_intersection), str(self.normale))