#! /usr/bin/env python
# -*-coding: utf-8-*-

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
			
