#! /usr/bin/env python
# -*-coding: utf-8-*-

from math import sqrt, tan 
import Image

'''
Descrition : 
- ce programme est destiné à créer des images grâce à la librairie Image de python.
- il est pour l'instant possible de créer des shères et des hyperboloides colorées sous différents éclairages
'''

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

	@property
	def sqrNorm(self):
		return sqrt(self.xyz[0]*self.xyz[0] + self.xyz[1]*self.xyz[1] + self.xyz[2]*self.xyz[2])

	@property
	def getNormalized(self):
		return Vector(self[0] * (1 / self.sqrNorm), self[1] * (1 / self.sqrNorm), self[2] * (1 / self.sqrNorm))

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
		c = (ray.origin - self.origin).sqrNorm**2 - self.rayon*self.rayon

		# on renvoie un objet intersection
		return poly2getIntersection(a,b,c)

	def getNormale(self, pt):
		# fonction retournant le vecteur normal à la sphère en un point donné

		return (pt - self.origin).getNormalized


#==============================================================================


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

		x_0 = self.origin.xyz[0]
		y_0 = self.origin.xyz[1]
		z_0 = self.origin.xyz[2]

		u_x = ray.dir.xyz[0]
		u_y = ray.dir.xyz[1]
		u_z = ray.dir.xyz[2]

		u_x0 = ray.origin.xyz[0]
		u_y0 = ray.origin.xyz[1]
		u_z0 = ray.origin.xyz[2]

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

		x_0 = self.origin.xyz[0]
		y_0 = self.origin.xyz[1]
		z_0 = self.origin.xyz[2]

		return Vector((pt.xyz[0]-x_0)/a**2, -(pt.xyz[1]-y_0)/b**2, (pt.xyz[2]-z_0)/c**2).getNormalized


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

'''
class Scene:
	def __init__(self,sphere_vect):
		self.objets = sphere_vect
		self.lumiere = lumiere
	
	def intersect(self, ray):
		point_inter = Vector(0,0,0)
		centre_inter = Vector(0,0,0)
		distance = 'inf'

		for sphere in self.obj:
			intersection = sphere.intersect(ray)

			if intersection.has_intersection
				point_inter = (d * intersection.t) + camera.foyer
				d = ((point_inter-ray.origin).sqrNorm)**2

				if d < distance and point_inter[3] < ray.origin[3]:
			    	point_inter =(d * intersection.t) + camera.foyer
			    	sphere_inter=s
			    	dist=dist_P
			    	if dist=='inf':
			return dist
			else:
				return (sphere_inter.O,inter)
'''

#==============================================================================


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


#==============================================================================


def main():
	
	# on crée une image à partir de la librairie Image
	W = 160
	H = 120
	image = Image.new( 'RGB', (W,H), "black")
	pixels = image.load()

	#on définit la lumière, la caméra et les sphères à tracer
	lumiere  = Lumiere(Vector(-20,50,40), 1000) # luminosité entre 50000 et 500000

	camera = Camera(Vector(0,0,55), 90 * 3.14 / 180)
	s1 = Sphere(Vector(0,0,0.1), 10, [1, 1, 1])
	s2 = Sphere(Vector(0,0,1000), 940, [1, 1, 1])
	s3 = Sphere(Vector(0,0,-1000), 940, [1, 1, 1])
	s4 = Sphere(Vector(1000,0,0), 940, [1, 1, 1])
	s5 = Sphere(Vector(-1000,0,0), 940, [1, 1, 1])
	s6 = Sphere(Vector(0,1000,0), 990, [1, 1, 1])
	s7 = Sphere(Vector(0,-1000,0), 940, [1, 1, 1])
	#hyperboloide = Hyperboloide(Vector(0,0,-10), [0.5,1,0.5], [1,0.8,0])

	formes = [s1,s2,s3,s4,s5,s6,s7]

	D = (W/2) / tan(camera.fov/2)
	
	# pour chaque pixel de l'image, on regarde si le rayon projeté intersecte la sphère
	for i in range(image.size[1]):
		for j in range(image.size[0]):

			d = Vector(j - W/2, i - H/2, -D).getNormalized

			distance_min = float("inf")

			for forme in formes:				
				intersection = forme.intersect(Ray(camera.foyer, d))

				if intersection.has_intersection:
					if intersection.t < distance_min:
						intersection_min = intersection
						forme_min = forme
						distance_min = intersection.t 

			if distance_min != float("inf"):

				forme = forme_min
				intersection = intersection_min
				ombre = False

				# on calcule le point d'intersection entre le rayon d et la forme
				intersection.pt_intersection = (d * intersection.t) + camera.foyer

				# on calcule la normale à la forme au point d'intersection
				intersection.normale = forme.getNormale(intersection.pt_intersection)

				intersection.pt_intersection = intersection.pt_intersection + intersection.normale * 0.01

				# on regarde s'il est dans l'ombre d'un autre objet
				# pour cela on calcule le vecteur v1 partant de ce point et allant vers l'origine de la lumière
				v_lumiere = (lumiere.origin - intersection.pt_intersection).getNormalized

				# on calcule la distance associée
				distance = (lumiere.origin - intersection.pt_intersection).sqrNorm

				# pour chaque forme f
				for f in formes:

					# on regarde si v_lumiere intersecte f
					i2 = f.intersect(Ray(intersection.pt_intersection,v_lumiere))

					if i2.has_intersection:

						# on calcule la distance dist entre i1 et f
						dist = i2.t

						# on compare cette distance avec la distance d1 entre le i1 et l'origine de la lumière
						# si cette d est inférieure à d1, le point est dans l'ombre, on ne fait rien
						if dist < distance:

							ombre = True
							break

				if not ombre:

					# on recalcule le point d'intersection entre la forme et d en décolant le point d'intersection de la sphère
					# corrige un bug d'affichage
					#intersection.normale = forme.getNormale(intersection.pt_intersection + intersection.normale * 0.1)

					# on calcule le max entre 0 et le produit scalaire du vecteur lumière et du vecteur normal
					valeur = v_lumiere.dot(intersection.normale) * lumiere.intensite / (2*3.14) #TODO *(distance**2)
					# on change les pixels en fonction du calcul du produit scalaire et de la valeur d'absorbance des couleurs par la sphère

					# pour une forme unicolore (disque blanc)
					#pixels[j,i] = (int(valeur), int(valeur), int(valeur))

					# pour un sphère en dégradé de gris
					#pixels[j,i] = (255, 255, 255)

					# pour une sphère colorée avec effets de lumières
					pixels[j,i] = (
						max(0, int(valeur * forme.rho[0])),
						max(0, int(valeur * forme.rho[1])),
						max(0, int(valeur * forme.rho[2]))
					)
					
			
	image.show()
	

#==============================================================================


if __name__ == "__main__":

	main()

