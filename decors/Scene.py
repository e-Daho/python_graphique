#! /usr/bin/env python
# -*-coding: utf-8-*-

from structures import Vector, Ray, Intersection
from math import tan, cos, sin, sqrt, ceil
import operator
from random import uniform

class Scene:
	'''
	classe représentant la scène caractérisée par
	[*] une liste de sphères ([s1, s1, ...])
	[*] un objet Lumiere (Lumiere)
	'''
	def __init__(self, spheres, lumiere):
		self.spheres = spheres
		self.lumiere = lumiere
	

	def intersecte(self, ray):
		# fonction prenant en argument un rayon, et retournant la forme intersectée la plus proche et le point d'inersection concerné

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


	def isInShadow(self, intersection, v_lumiere, distance):
		"""
		:param scene : Scene, la scene concernée
		:param intersection : Intersection
		:param v_lumiere : Vector (normalisé)
		:returns booleen
		"""

		for sphere in self.spheres:

			intersection2 = sphere.intersect(Ray(intersection.pt_intersection, v_lumiere))

			if intersection2.has_intersection:

				# on calcule la distance dist entre intersection 2 et la et l'origine de la lumière
				dist = intersection2.t
						
				# on compare cette distance avec la distance d1 entre le i1 et l'origine de la lumière
				# si cette d est inférieure à dist, le point est dans l'ombre, on ne fait rien
				if dist < distance:

					return True
					break

		return False


	def getColor(self, ray, n_rebonds):
		"""
		:param scene : Scene, la scene concernée
		:param ray : Ray, le rayon inscident à la sphere
		:param n_rebonds : int, le nombre max de rebonds
		:returns couleur : (int, int, int)
		"""

		# on regarde si le rayon intersecte une des formes de la scene
		(forme, intersection) = self.intersecte(ray)

		if intersection.has_intersection:

			# on calcule le point d'intersection entre le rayon et la forme
			intersection.pt_intersection = (ray.dir * intersection.t) + ray.origin

			# on calcule la normale à la forme au point d'intersection
			intersection.normale = forme.getNormale(intersection.pt_intersection)

			# on décale le point d'intersection pour corriger un bug d'affichage
			intersection.pt_intersection = intersection.pt_intersection + intersection.normale * 0.01
			
			if intersection.pt_intersection.sqrNorm > 1000:
				return (0,0,0)

			if forme.materiau.speculaire and n_rebonds > 0:
				return self.getColor(ray.reflechir(forme, intersection), n_rebonds - 1)

			if forme.materiau.indiceRefraction != 0  and n_rebonds > 0:
				return self.getColor(ray.refracter(forme, intersection), n_rebonds - 1)

			# on calcule le vecteur v_lumiere partant de ce point et allant vers l'origine de la lumière
			v_lumiere = (self.lumiere.origin - intersection.pt_intersection).getNormalized

			# on calcule la distance associée
			distance = (self.lumiere.origin - intersection.pt_intersection).sqrNorm

			# sinon on retourne la couleur du materiau final (dernier rebond)
			if self.isInShadow(intersection, v_lumiere, distance):
				couleur = (0,0,0)

			else:
				# on calcule le max entre 0 et le produit scalaire du vecteur lumière et du vecteur normal
				valeur = v_lumiere.dot(intersection.normale) * self.lumiere.intensite / (2*3.14*distance**2) 
				valeur = max(0, valeur)

				couleur = (valeur * forme.materiau.couleur[0], valeur * forme.materiau.couleur[1], valeur * forme.materiau.couleur[2])

			# contribution diffuse
			if n_rebonds > 0:
				
				# on génère deux valeures aléatoires
				r1 = uniform(0, 1.)
				r2 = uniform(0, 1.)

				# on génère un vecteur aléatoire et une base locale
				indirectDirLocal = Vector( cos(2*3.14*r1)*sqrt(1-r2), sin(2*3.14*r1)*sqrt(1-r2), sqrt(r2) ).getNormalized
				randomVect = Vector(uniform(0, 1.), uniform(0, 1.), uniform(0, 1.)).getNormalized

				tangent1 = intersection.normale.cross(randomVect).getNormalized
				tangent2 = intersection.normale.cross(tangent1).getNormalized

				# on transfert le vecteur dans la base globale
				indirectDirGlobal = tangent1 * indirectDirLocal[0] + tangent2 * indirectDirLocal[1] + intersection.normale * indirectDirLocal[2]
				ray_diffus = Ray(intersection.pt_intersection + intersection.normale * 0.01, indirectDirGlobal)
				couleur_diffuse = self.getColor(ray_diffus, n_rebonds - 1)

				couleur = tuple(map(operator.add, couleur, couleur_diffuse))
			
			return couleur
			
		return (0,0,0)


	def getImage(self, camera, image, n_rebonds, n_echantillons):
		"""
		:param camera : Camera
		:param image : Image, l'image à créer
		:param n_rebonds : int, nombre max de rebonds à effectuer
		:returns Image, l'image créée
		"""

		pixels = image.load()

		D = (image.size[0]/2) / tan(camera.fov/2)

		rayon = Ray(camera.foyer, Vector(0,0,0))
		
		for i in xrange(image.size[1]):
			print "[" + "=" * (i*10 /image.size[1]) + ">]" + " " + str(i*100 /image.size[1]) + "%"
			
			for j in xrange(image.size[0]):
				rayon.dir = Vector(j - image.size[0]/2, i - image.size[1]/2, -D).getNormalized
				couleur = (0,0,0)

				for k in xrange(n_echantillons):
					# on calcule la couleur du pixel intersecté
					couleur = tuple(map(operator.add, couleur, self.getColor(rayon, n_rebonds)))
					couleur = (int(((couleur[0])/n_echantillons)**(1/2.2)), int(((couleur[1])/n_echantillons)**(1/2.2)), int(((couleur[2])/n_echantillons)**(1/2.2)))

				pixels[j,i] = couleur

		return image
				
