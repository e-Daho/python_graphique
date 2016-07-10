#! /usr/bin/env python
# -*-coding: utf-8-*-

from math import sqrt, tan 

class Hyperboloide():
	'''
	classe définissant une hyperboloide a deux nappes dans l'espace caractérisée par
	[*] son origine (Vector)
	[*] ses coefficients a,b et c ([int/float, int/float, int/float])
	[*] son absorption aux couleurs RGB ([int, int, int])
	'''


	def __init__(self, o, c, rho):
		self.origin = o
		self.coeff = c
		self.rho = rho


	def intersect(self,ray):
		# fonction testant l'intersection entre l'hyperboloide et un rayon
		# prend un ray en argument, retourne un objet intersection

		# équation de type m*t^2 + n*t + p = 0

		# on définit les coefficients à utiliser
		a = self.coeff[0]
		b = self.coeff[1]
		c = self.coeff[2]

		x_0 = self.origin[0]
		y_0 = self.origin[1]
		z_0 = self.origin[2]

		u_x = ray.dir[0]
		u_y = ray.dir[1]
		u_z = ray.dir[2]

		u_x0 = ray.origin[0]
		u_y0 = ray.origin[1]
		u_z0 = ray.origin[2]

		# on calcule les coefficients de l'équation
		m = (u_x/a)**2 - (u_y/b)**2 + (u_z/c)**2
		n = 2 * (u_x*(u_x0 - x_0)/a**2 - u_y*(u_y0 - y_0)/b**2 + u_z*(u_z0 - z_0)/c**2)
		p = ((x_0 - u_x0)/a)**2 - ((y_0 - u_y0)/b)**2 + ((z_0 - u_z0)/c)**2 + 1

		# on renvoie un objet intersection
		return poly2getIntersection(m,n,p)


	def getNormale(self, pt):
		# fonction retournant le vecteur normal à la sphère en un point donné

		a = self.coeff[0]
		b = self.coeff[1]
		c = self.coeff[2]

		x_0 = self.origin[0]
		y_0 = self.origin[1]
		z_0 = self.origin[2]

		return Vector((pt[0]-x_0)/a**2, -(pt[1]-y_0)/b**2, (pt[2]-z_0)/c**2).getNormalized


	def poly2getIntersection(a,b,c):
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