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


	def isInShadow(self, intersection, v_lumiere, distanceCarree):
		"""
		:param intersection : Intersection
		:param v_lumiere : Vector (normalisé)
		:param distance : float, la distance entre la source de lumière et le point d'intersection
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
		r1 = uniform(0.0001, 0.99999)
		r2 = uniform(0.0001, 0.99999)

		# on génère un vecteur aléatoire et une base locale
		indirectDirLocal = Vector( cos(2*3.14*r1)*sqrt(1-r2), sin(2*3.14*r1)*sqrt(1-r2), sqrt(r2) )

		randomVect = Vector(uniform(0.0001, 0.99999), uniform(0.0001, 0.99999), uniform(0.0001, 0.99999))

		tangent1 = intersection.normale.cross(randomVect)
		tangent2 = intersection.normale.cross(tangent1)

		# on transfert le vecteur dans la base globale
		indirectDirGlobal = (tangent1 * indirectDirLocal[0] + tangent2 * indirectDirLocal[1] + intersection.normale * indirectDirLocal[2]).getNormalized
		
		ray.origin = intersection.pt_intersection - intersection.normale * 0.0001
		ray.dir = indirectDirGlobal

		return ray


	def getColor(self, ray, n_rebonds, diffus):
		"""
		:param scene : Scene, la scene concernée
		:param ray : Ray, le rayon inscident à la sphere
		:param n_rebonds : int, le nombre max de rebonds
		:param diffus : booleen, True si on veut l'éclairage diffus, False si on veut l'éclairage direct
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
			
			if intersection.pt_intersection.sqrNorm > 1000000:
				return (0,0,0)

			if forme.materiau.speculaire and n_rebonds > 0:
				ray.reflechir(forme, intersection)
				return self.getColor(ray, n_rebonds - 1, diffus)

			if forme.materiau.indiceRefraction != 0  and n_rebonds > 0:
				ray.refracter(forme, intersection)
				return self.getColor(ray, n_rebonds - 1, diffus)

			if diffus and n_rebonds > 0:
				ray = self.diffuser(ray, intersection)
				return self.getColor(ray, n_rebonds - 1, diffus)

			# on calcule le vecteur v_lumiere partant de ce point et allant vers l'origine de la lumière
			v_lumiere = (self.lumiere.origin - intersection.pt_intersection).getNormalized

			# on calcule la distance associée
			distanceCarree = (self.lumiere.origin - intersection.pt_intersection).sqrNorm

			if self.isInShadow(intersection, v_lumiere, distanceCarree):
				return (0,0,0)

			# on calcule le max entre 0 et le produit scalaire du vecteur lumière et du vecteur normal
			valeur = v_lumiere.dot(intersection.normale) * self.lumiere.intensite / (2*3.14*distanceCarree) 
			valeur = max(0, valeur)

			return (valeur * forme.materiau.couleur[0], valeur * forme.materiau.couleur[1], valeur * forme.materiau.couleur[2])

		return (0,0,0)


	def getImage(self, camera, image, n_rebonds, quadrant, out_q, n_echantillons, diffus):

		"""
		:param camera : Camera
		:param image : Image, l'image à créer
		:param n_rebonds : int, nombre max de rebonds à effectuer
		:returns Image, l'image créée
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

		D = (image.size[0]/2) / tan(camera.fov/2)
		
		rayon = Ray(camera.foyer, Vector(0,0,0))

		for i in xrange(debut_i, fin_i):
			if quadrant == 0:
				print "[" + "=" * (i*20 /image.size[1]) + ">]" + " " + str(i*200 /image.size[1]) + "%"	

			for j in xrange(debut_j, fin_j):
				rayon = Ray(camera.foyer, Vector(0,0,0))
				rayon.dir = Vector(j - image.size[0]/2, i - image.size[1]/2, -D).getNormalized
				
				couleur = self.getColor(rayon, n_rebonds, False)

				if diffus:
					couleur_diffuse = (0,0,0)
					for k in xrange(n_echantillons):
						couleur_diffuse = tuple(map(operator.add, couleur_diffuse, self.getColor(rayon, n_rebonds, True)))

					couleur_diffuse = (couleur_diffuse[0]/n_echantillons, couleur_diffuse[1]/n_echantillons, couleur_diffuse[2]/n_echantillons)
					couleur = tuple(map(operator.add, couleur_diffuse, couleur))

				# on applique la correction gamma
				pixels[j,i] = (int(couleur[0]**(1/2.2)), int(couleur[1]**(1/2.2)), int(couleur[2]**(1/2.2)))

		out_q.put(image)
