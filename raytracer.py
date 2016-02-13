#! /usr/bin/env python
# -*-coding: utf-8-*-

from math import sqrt, tan 
import Image


#==============================================================================


class Vector(object):
	''' 
	classe définissant un vecteur dans l'espace caractérisé par
	[*] sa coordonnée x (int ou float)
	[*] sa coordonnée y (int ou float)
	[*] sa coordonnée z (int ou float)
	'''

	def __init__(self, x, y, z):
		self.xyz = [float(0) for i in xrange(3)]
		self.xyz[0] = x
		self.xyz[1] = y
		self.xyz[2] = z

	def sqrNorm(self):
		return sqrt(self.xyz[0]*self.xyz[0] + self.xyz[1]*self.xyz[1] + self.xyz[2]*self.xyz[2])

	def getNormalized(self):
		return Vector(self[0] * (1 / self.sqrNorm()), self[1] * (1 / self.sqrNorm()), self[2] * (1 / self.sqrNorm()))

	def __getitem__(self, i):
		return self.xyz[i]

	def __add__(v1, v2):
		return Vector(v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2])

	def __sub__(v1, v2):
		return Vector(v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])

	def __mul__(self, a):
		return Vector(a * self[0], a * self[1], a * self[2])

	def __str__(self):
		return "[%f,%f,%f]" % (self[0], self[1], self[2])

	def dot(self, v2):
		return self[0] * v2[0] + self[1] * v2[1] + self[2] * v2[2]


#==============================================================================


class Sphere():
	'''
	classe définissant une sphère dans l'espace caractérisée par
	[*] son origine (Vector)
	[*] son rayon (int ou float)
	[*] son absorption aux couleurs RGB ([int, int, int])
	'''

	def __init__(self, o, r, rho):
		self.origin = o
		self.rayon = r
		self.rho = rho

	def intersect(self,ray):
		# fonction testant l'intersection entre la sphère et un rayon
		# prend un ray en argument, retourne un objet intersection

		# équation de type a*t^2 + b*t +c = 0
		a = 1.
		b = 2 * ray.dir.dot(ray.origin - self.origin)
		c = ((ray.origin - self.origin).sqrNorm())**2 - self.rayon*self.rayon

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


#==============================================================================


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


#==============================================================================


class Ray():
	'''
	classe représentant un rayon dans l'espace caractérisé par
	[*] son origin (Vector)
	[*] sa direction (Vector)
	'''

	def __init__(self, o, d):
		self.origin = o
		self.dir = d


#==============================================================================


class Camera():
	'''
	classe représentant la caméra caractérisée par
	[*] son foyer (Vector)
	[*] son "field of vision", c'est à dire son angle d'ouverture en radian (float)
	'''

	def __init__(self, foyer, fov):
		self.foyer = foyer
		self.fov = fov


#==============================================================================


class Lumiere():
	'''
	classe représentant la lumière (ponctuelle) caractérisée par
	[*] son origin (Vector)
	[*] son intensité (int entre 0 et 255)
	'''

	def __init__(self, o, i):
		self.origin = o
		self.intensite = i


#==============================================================================


def main():
	W = 640
	H = 480
	image = Image.new( 'RGB', (W,H), "black")
	pixels = image.load()

	lumiere  = Lumiere(Vector(50,50,50), 500)
	camera = Camera(Vector(0,0,55), 60 * 3.14 / 180)

	sphere1 = Sphere(Vector(0,0,0), 5, [1, 0.5, 0])
	sphere2 = Sphere(Vector(0,0,20), 15, [0, 1, 1])

	spheres = [sphere2, sphere1]

	D = (W/2) / tan(camera.fov/2)
	
	for i in range(image.size[1]):
		for j in range(image.size[0]):
			d = Vector(j - W/2, i - H/2, -D).getNormalized()

			for sphere in spheres:

				intersection = sphere.intersect(Ray(camera.foyer, d))

				if intersection.has_intersection:

					# on calcule le point d'intersection entre le rayon d et la sphère
					intersection.pt_intersection = (d * intersection.t) + camera.foyer

					# on calcule la normale à la sphère au point d'intersection
					intersection.normale = (intersection.pt_intersection - sphere.origin).getNormalized()

					# on calcule le vecteur lumière arrivant sur le point d'intersection
					v_lumiere = (lumiere.origin - intersection.pt_intersection).getNormalized()

					# on calcule la distance entre la source de lumière et le point d'intersection
					distance = (lumiere.origin - intersection.pt_intersection).sqrNorm()

					# on calcule le max entre 0 et le produit scalaire du vecteur lumière et du vecteur normal
					valeur = max(0, float(v_lumiere.dot(intersection.normale) * lumiere.intensite / (2*3.14) )/(distance**2))

					# on change les pixels en fonction du calcul du produit scalaire et de la valeur d'absorbance des couleurs par la sphère

					# pour une sphère unicolore (disque blanc)
					#pixels[j,i] = (int(valeur), int(valeur), int(valeur))

					# pour un sphère en dégradé de gris
					#pixels[j,i] = (255, 255, 255)

					# pour une sphère colorée avec effets de lumières
					pixels[j,i] = (
						max(0, int(v_lumiere.dot(intersection.normale) * lumiere.intensite * sphere.rho[0])),
						max(0, int(v_lumiere.dot(intersection.normale) * lumiere.intensite * sphere.rho[1])),
						max(0, int(v_lumiere.dot(intersection.normale) * lumiere.intensite * sphere.rho[2]))
					)
				
			
	image.show()
	

#==============================================================================


if __name__ == "__main__":

	main()

