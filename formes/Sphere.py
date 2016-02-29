#! /usr/bin/env python
# -*-coding: utf-8-*-

from math import sqrt
from structures import Intersection

class Sphere():
	'''
	classe définissant une sphère dans l'espace caractérisée par
	[*] son origine (Vector)
	[*] son rayon (int ou float)
	[*] son matériau (Materiau)
	'''

	def __init__(self, o, r, m):
		self.origin = o
		self.rayon = r
		self.materiau = m



	def intersect(self, ray):
		# fonction testant l'intersection entre la sphère et un rayon
		# prend un ray en argument, retourne un objet intersection

		# équation de type a*t^2 + b*t +c = 0
		a = 1.
		b = 2 * ray.dir.dot(ray.origin - self.origin)
		c = (ray.origin - self.origin).sqrNorm**2 - self.rayon*self.rayon

		# on renvoie un objet intersection
		return self.poly2getIntersection(a,b,c)



	def poly2getIntersection(self, a,b,c):
		# fonction permettant de résoudre une équation polynomiale d'ordre 2
		# prend en argument trois coefficients, retourne un objet intersection

		delta = b*b - 4*a*c

		result = Intersection()

		if delta < 0:
			result.has_intersection = False

		else:
			tmin = (-b - sqrt(delta)) / (2*a)
			tmax = (-b + sqrt(delta)) / (2*a)

			if tmax < 0:
				result.has_intersection = False

			else:
				result.has_intersection = True

				if tmin < 0:
					result.t = tmax
				else:
					result.t = tmin

		return result



	def getNormale(self, pt):
		# fonction retournant le vecteur normal à la sphère en un point donné

		return (pt - self.origin).getNormalized


	