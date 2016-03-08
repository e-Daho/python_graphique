#! /usr/bin/env python
# -*-coding: utf-8-*-

from structures import Vector, Ray, Intersection
from math import tan, cos, sin, sqrt, log
import operator
from random import uniform

class Scene:
	'''
	classe représentant la scène caractérisée par
	[*] une liste de sphères ([s1, s1, ...])
	[*] un objet Lumiere (Lumiere)
	[*] un objet Camera
	'''

	def __init__(self, spheres, lumiere, camera):
		self.spheres = spheres
		self.lumiere = lumiere
		self.camera = camera
	

	def intersecte(self, ray):
		"""
		:param ray : Ray
		:returns (forme_min, intersection_min) : (Sphere, Intersection)
		"""

		distance_min = float("inf")

		# pour chaque forme de la scene
		for forme in self.spheres:
			# on regarde l'intersection entre le rayon et cette forme			
			intersection = forme.intersect(ray)

			# si cette intersection existe
			if intersection.has_intersection:
				# et que la distance associée est inférieure à la distance min trouvée
				if intersection.t < distance_min:
					# alors on redéfini intersection_min et forme_min
					intersection_min = intersection
					forme_min = forme
					distance_min = intersection.t

		# si le rayon a intersecté au moins une forme
		if distance_min != float("inf"):
			# on retourne intersection_min et forme_min
			return (forme_min, intersection_min)


	def isInShadow(self, intersection, v_lumiere, distanceCarree):
		"""
		:param intersection : Intersection
		:param v_lumiere : Vector (normalisé)
		:param distanceCarree : float, la distance au carrée entre la source de lumière et le point d'intersection
		:returns booleen
		"""

		for sphere in self.spheres:
			intersection2 = sphere.intersect(Ray(intersection.pt_intersection, v_lumiere))

			if intersection2.has_intersection:
				dist = intersection2.t
	
				# si cette d est inférieure à dist, le point est dans l'ombre, on ne fait rien
				if dist**2 < distanceCarree:
					return True
					break

		return False


	def diffuser(self, ray, intersection):
		"""
		:param ray : Ray, rayon à diffuser
		:param intersection : Intersection, le point de pénétration du rayon dans la sphère
		:returns Ray, rayon réfracté 
		"""

		# on génère deux valeures aléatoires
		r1 = uniform(0,1)
		r2 = uniform(0,1)

		# on génère un vecteur aléatoire et une base locale
		indirectDirLocal = Vector( cos(2*3.14*r1)*sqrt(1-r2), sin(2*3.14*r1)*sqrt(1-r2), sqrt(r2) )

		randomVect = Vector(uniform(0,1), uniform(0,1), uniform(0,1))

		tangent1 = intersection.normale.cross(randomVect)
		tangent2 = intersection.normale.cross(tangent1)

		# on transfert le vecteur dans la base globale
		indirectDirGlobal = (tangent1 * indirectDirLocal[0] + tangent2 * indirectDirLocal[1] + intersection.normale * indirectDirLocal[2]).getNormalized
		
		ray.origin = intersection.pt_intersection - intersection.normale * 0.0001
		ray.dir = indirectDirGlobal


	def generateRay(self, i, j, D, largeur, hauteur):
		"""
		:param i : int
		:param j : int
		:param D : int
		:return r : Ray
		"""

		x = uniform(0,1)
		y = uniform(0,1)
		R = sqrt(-2*log(x))
		u = R * cos(2*3.1416*y) * 0.5
		v = R * sin(2*3.1416*y) * 0.5

		r = Ray(self.camera.foyer,\
		 (self.camera.right * (j - largeur/2 -0.5 + u) + self.camera.up * (i - hauteur/2 - 0.5 + v) + self.camera.direction * -D) .getNormalized)

		return r



	def getColor(self, ray, n_rebonds, diffus):
		"""
		:param ray : Ray, le rayon inscident à la sphere
		:param n_rebonds : int, le nombre max de rebonds
		:param diffus : booleen, True si on veut l'éclairage diffus, False si on veut l'éclairage direct
		:returns couleur : (int, int, int)
		"""

		result = (0,0,0)

		# on regarde si le rayon intersecte une des formes de la scene
		(forme, intersection) = self.intersecte(ray)

		if intersection.has_intersection:

			# on calcule le point d'intersection entre le rayon et la forme
			intersection.pt_intersection = (ray.dir * intersection.t) + ray.origin

			# on calcule la normale à la forme au point d'intersection
			intersection.normale = forme.getNormale(intersection.pt_intersection)

			# on décale le point d'intersection pour corriger un bug d'affichage
			intersection.pt_intersection = intersection.pt_intersection + intersection.normale * 0.0001
			
			if intersection.pt_intersection.sqrNorm > 1000000:
				return (0,0,0)

			if forme.materiau.speculaire and n_rebonds > 0:
				ray.reflechir(forme, intersection)
				return self.getColor(ray, n_rebonds - 1, diffus)

			if forme.materiau.indiceRefraction != 0  and n_rebonds > 0:
				ray.refracter(forme, intersection)
				return tuple(map(operator.add, result, self.getColor(ray, n_rebonds - 1, diffus)))

			if diffus and n_rebonds > 0:
				self.diffuser(ray, intersection)
				result = tuple(map(operator.add, result, self.getColor(ray, n_rebonds - 1, diffus)))

			# on calcule le vecteur v_lumiere partant de ce point et allant vers l'origine de la lumière
			v_lumiere = (self.lumiere.origin - intersection.pt_intersection).getNormalized

			# on calcule la distance associée
			distanceCarree = (self.lumiere.origin - intersection.pt_intersection).sqrNorm

			if self.isInShadow(intersection, v_lumiere, distanceCarree):
				partie_diffuse = (0,0,0)

			else:
				# on calcule le max entre 0 et le produit scalaire du vecteur lumière et du vecteur normal
				valeur = v_lumiere.dot(intersection.normale) * self.lumiere.intensite / (2*3.14*distanceCarree) 
				valeur = max(0, valeur)

				partie_diffuse = (valeur * forme.materiau.couleur[0], valeur * forme.materiau.couleur[1], valeur * forme.materiau.couleur[2])

			return tuple(map(operator.add, result, partie_diffuse))

		return (0,0,0)


	def getImage(self, image, n_rebonds, quadrant, out_q, n_echantillons, diffus):

		"""
		:param camera : Camera
		:param image : Image, l'image à créer
		:param n_rebonds : int, nombre max de rebonds à effectuer
		:param quadrant : int (entre 0 et 3), la quart d'image à déterminer
		:out_q : Queue, la queue dans laquelle on retourne le résultat (process safe)
		:n_echantillons : int, le nombre de rayon à projeter pour chaque pixel, uniquement utile pour la lumière diffuse
		:diffus : booleen
		"""

		pixels = image.load()

		# on divise l'image en 4 quadrans
		if quadrant == 0:
			debut_i = 0
			fin_i = image.size[1]/2
			debut_j = 0
			fin_j = image.size[0]/2

		elif quadrant == 1:
			debut_i = 0
			fin_i = image.size[1]/2
			debut_j = image.size[0]/2
			fin_j = image.size[0]

		elif quadrant == 2:
			debut_i = image.size[1]/2
			fin_i = image.size[1]
			debut_j = 0
			fin_j = image.size[0]/2

		elif quadrant == 3:
			debut_i = image.size[1]/2
			fin_i = image.size[1]
			debut_j = image.size[0]/2
			fin_j = image.size[0]

		else:
			return

		D = (image.size[0]/2) / tan(self.camera.fov/2)

		for i in xrange(debut_i, fin_i):
			if quadrant == 0:
				print "[" + "=" * (i*20 /image.size[1]) + ">]" + " " + str(i*200 /image.size[1]) + "%"	

			for j in xrange(debut_j, fin_j):
				rayon = self.generateRay(i,j,D,image.size[0], image.size[1])				
				couleur = self.getColor(rayon, n_rebonds, False)

				if diffus:
					couleur_diffuse = (0,0,0)
					for k in xrange(n_echantillons):
						rayon = self.generateRay(i,j,D,image.size[0], image.size[1])
						couleur_diffuse = tuple(map(operator.add, couleur_diffuse, self.getColor(rayon, n_rebonds, True)))

					couleur_diffuse = (couleur_diffuse[0]/n_echantillons, couleur_diffuse[1]/n_echantillons, couleur_diffuse[2]/n_echantillons)
					couleur = tuple(map(operator.add, couleur_diffuse, couleur))

				# on applique la correction gamma
				pixels[j,i] = (int(couleur[0]**(1/2.2)), int(couleur[1]**(1/2.2)), int(couleur[2]**(1/2.2)))

		out_q.put(image)
