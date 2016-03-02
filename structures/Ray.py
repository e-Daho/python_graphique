#! /usr/bin/env python
# -*-coding: utf-8-*-

from math import sqrt, cos, sin
from random import uniform
import Vector

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
		:param forme : Sphere, la sphere sur laquelle le rayon se réfléchi
		:param intersection : Intersection, le point de réflexion
		:returns Ray, rayon réfléchi 
		"""

		# on définit le rayon réfléchi
		direction = (self.dir - forme.getNormale(intersection.pt_intersection) * \
			2 * forme.getNormale(intersection.pt_intersection).dot(self.dir)).getNormalized
		origin = intersection.pt_intersection

		return Ray(origin, direction)



	def refracter(self, forme, intersection):
		"""
		:param forme : Sphere, la sphere dans laquelle le rayon se réfracte
		:param intersection : Intersection, le point de pénétration du rayon dans la sphère
		:returns Ray, rayon réfracté 
		"""

		# si le rayon entre dans la sphère, c'est à dire si il est orienté dans le sens inverse de la normale 
		if intersection.normale.dot(self.dir) < 0:

			# on décolle légèrement le point d'intersection de la forme pour éviter un bug
			intersection.pt_intersection = intersection.pt_intersection - forme.getNormale(intersection.pt_intersection) * 0.05

			coeff = 1 - (1 - (self.dir.dot(intersection.normale))**2) * (1 / forme.materiau.indiceRefraction)**2

			# on retourne le rayon réfracté
			direction = (self.dir * (1 / forme.materiau.indiceRefraction) - intersection.normale * \
			(self.dir.dot(intersection.normale) / forme.materiau.indiceRefraction + sqrt(coeff))).getNormalized
			origin = intersection.pt_intersection

		# sinon si le rayon sort de la sphère
		else:

			# on inverse la normale
			intersection.normale = intersection.normale * (-1)

			# on refait les opérations précédentes, en inversant les rôles des indices de réfractions
			coeff = 1 - (1 - self.dir.dot(intersection.normale)**2) * (forme.materiau.indiceRefraction)**2

			if coeff < 0:
				return self.reflechir(forme, intersection)

			direction = (self.dir * forme.materiau.indiceRefraction - intersection.normale * \
			(self.dir.dot(intersection.normale) * forme.materiau.indiceRefraction + sqrt(coeff))).getNormalized
			origin = intersection.pt_intersection

		return Ray(origin, direction)

	def diffuser(self, intersection):
		"""
		:param intersection : Intersection
		:returns ray : Ray
		"""

		# on génère deux valeures aléatoires
		r1 = uniform(0, 1.)
		r2 = uniform(0, 1.)
		
		# on génère un vecteur aléatoire et une base locale
		indirectDirLocal = Vector( cos(2*3.14*r1)*sqrt(1-r2), sin(2*3.14*r1)*sqrt(1-r2), sqrt(r2) )
		randomVect = Vector(uniform(0, 1.), uniform(0, 1.), uniform(0, 1.))
		
		tangent1 = intersection.normale.cross(randomVect).getNormalized
		tangent2 = intersection.normale.cross(tangent1).getNormalized

		# on transfert le vecteur dans la base globale
		indirectDirGlobal = tangent1 * indirectDirLocal[0] + tangent2 * indirectDirLocal[1] + intersection.normale * indirectDirLocal[2]

		return Ray(intersection.pt_intersection, indirectDirGlobal)		