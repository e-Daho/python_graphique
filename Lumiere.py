#! /usr/bin/env python
# -*-coding: utf-8-*-

class Lumiere():
	'''
	classe représentant la lumière (ponctuelle) caractérisée par
	[*] son origin (Vector)
	[*] son intensité (int entre 0 et 255)
	'''

	def __init__(self, o, i):
		self.origin = o
		self.intensite = i