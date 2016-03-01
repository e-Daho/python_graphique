#! /usr/bin/env python
# -*-coding: utf-8-*-

import numpy as np
from math import sqrt

class Ray():
	'''
	classe représentant un rayon dans l'espace caractérisé par
	[*] son origin (Vector)
	[*] sa direction (Vector)
	'''

	def __init__(self, o, d):
		self.origin = o
		self.dir = d



	def reflechir(self, forme, intersection):
		"""
		:param ray : Ray, rayon à réfléchir
		:param forme : Sphere, la sphere sur laquelle le rayon se réfléchi
		:param intersection : Intersection, le point de réflexion
		:returns Ray, rayon réfléchi 
		"""

		# on définit le rayon réfléchi
		direction = (self.dir - 2 * np.dot(self.dir, forme.getNormale(intersection.pt_intersection)) \
			* forme.getNormale(intersection.pt_intersection))
		direction = direction / np.linalg.norm(direction)

		origin = intersection.pt_intersection

		return Ray(origin, direction)



	def refracter(self, forme, intersection):
		"""
		:param ray : Ray, rayon à réfracter
		:param forme : Sphere, la sphere dans laquelle le rayon se réfracte
		:param intersection : Intersection, le point de pénétration du rayon dans la sphère
		:returns Ray, rayon réfracté 
		"""

		scalaire = np.dot(self.dir, intersection.normale)

		# si le rayon entre dans la sphère, c'est à dire si il est orienté dans le sens inverse de la normale 
		if scalaire < 0:

			# on décolle légèrement le point d'intersection de la forme pour éviter un bug
			intersection.pt_intersection = intersection.pt_intersection - 0.05 * forme.getNormale(intersection.pt_intersection)

			coeff = 1 - (1 / forme.materiau.indiceRefraction)**2 * (1 - scalaire**2)

			# on retourne le rayon réfracté
			direction = (1 / forme.materiau.indiceRefraction) * self.dir - \
			(scalaire / forme.materiau.indiceRefraction + sqrt(coeff)) * intersection.normale
			direction = direction / np.linalg.norm(direction)

			origin = intersection.pt_intersection

		# sinon si le rayon sort de la sphère
		else:
			# on inverse la normale
			intersection.normale = (-1) * intersection.normale
			scalaire = -scalaire

			# on refait les opérations précédentes, en inversant les rôles des indices de réfractions
			coeff = 1 - (forme.materiau.indiceRefraction)**2 * (1 - scalaire**2)

			if coeff < 0:
				return self.reflechir(forme, intersection)

			direction = (forme.materiau.indiceRefraction) * self.dir - \
			(scalaire * forme.materiau.indiceRefraction + sqrt(coeff)) * intersection.normale
			direction = direction / np.linalg.norm(direction)

			origin = intersection.pt_intersection

		return Ray(origin, direction)