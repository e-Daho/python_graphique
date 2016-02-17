#! /usr/bin/env python
# -*-coding: utf-8-*-

class Materiau():
	'''
	classe représentant un matériau caractérisé par
	[*] sa couleur ([int, int, int])
	[*] sa spécularité (bool)
	[*] sa transparence (bool)
	'''

	def __init__(self, couleur, speculaire, transparent):
		self.couleur = couleur
		self.speculaire = speculaire
		self.transparent = transparent