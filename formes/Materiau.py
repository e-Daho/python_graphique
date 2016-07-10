#! /usr/bin/env python
# -*-coding: utf-8-*-

class Materiau():
	'''
	classe représentant un matériau caractérisé par
	[*] sa couleur ([int, int, int])
	[*] sa spécularité (bool)
	[*] son indice de réfraction (int)
	'''

	def __init__(self, couleur, speculaire, indiceRefraction):
		self.couleur = couleur
		self.speculaire = speculaire
		self.indiceRefraction = indiceRefraction # 0 si le matériaux n'est pas transparent