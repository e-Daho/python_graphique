#! /usr/bin/env python
# -*-coding: utf-8-*-

from structures import Ray, Intersection
from math import tan
import numpy as np

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
			intersection.pt_intersection = intersection.pt_intersection + 0.01 * intersection.normale

			if forme.materiau.speculaire and n_rebonds > 0:
				return self.getColor(ray.reflechir(forme, intersection), n_rebonds - 1)

			if forme.materiau.indiceRefraction != 0  and n_rebonds > 0:
				return self.getColor(ray.refracter(forme, intersection), n_rebonds - 1)

			# on calcule le vecteur v_lumiere partant de ce point et allant vers l'origine de la lumière
			v_lumiere = self.lumiere.origin - intersection.pt_intersection
			v_lumiere = v_lumiere / np.linalg.norm(v_lumiere)

			# on calcule la distance associée
			distance = np.linalg.norm(self.lumiere.origin - intersection.pt_intersection)

			# sinon on retourne la couleur du materiau final (dernier rebond)	
			if self.isInShadow(intersection, v_lumiere, distance):
				return (0,0,0)

			# on calcule le max entre 0 et le produit scalaire du vecteur lumière et du vecteur normal
			valeur = self.lumiere.intensite / (2*3.14*distance**2) * np.dot(v_lumiere, intersection.normale) 

			# on change les pixels en fonction du calcul du produit scalaire et de la valeur d'absorbance des couleurs par la sphère
			# on élève à lapuissance 1/2.2 pour compenser la correction gamma
			return (
				max(0, int((valeur * forme.materiau.couleur[0])**(1./2.2))), 
				max(0, int((valeur * forme.materiau.couleur[1])**(1./2.2))),
				max(0, int((valeur * forme.materiau.couleur[2])**(1./2.2)))
				)		
			
		return (0,0,0)


	def getImage(self, camera, image, n_rebonds, cadran, out_q):
		"""
		:param camera : Camera
		:param image : Image, l'image à créer
		:param n_rebonds : int, nombre max de rebonds à effectuer
		:returns Image, l'image créée
		"""

		pixels = image.load()

		D = (image.size[0]/2) / tan(camera.fov/2)

		# on divise l'image en 4 quadrans
		if cadran == 0:
			debut_i = 0
			fin_i = image.size[1]/2
			debut_j = 0
			fin_j = image.size[0]/2

		elif cadran == 1:
			debut_i = 0
			fin_i = image.size[1]/2
			debut_j = image.size[0]/2
			fin_j = image.size[0]

		elif cadran == 2:
			debut_i = image.size[1]/2
			fin_i = image.size[1]
			debut_j = 0
			fin_j = image.size[0]/2

		elif cadran == 3:
			debut_i = image.size[1]/2
			fin_i = image.size[1]
			debut_j = image.size[0]/2
			fin_j = image.size[0]

		else:
			return

		for i in xrange(debut_i, fin_i):
			for j in xrange(debut_j, fin_j):

				rayon_dir = np.array([j - image.size[0]/2, i - image.size[1]/2, -D])
				rayon_dir = rayon_dir / np.linalg.norm(rayon_dir)

				# on calcule la couleur du pixel intersecté
				pixels[j,i] = self.getColor(Ray(camera.foyer, rayon_dir), n_rebonds)

		out_q.put(image)


				
