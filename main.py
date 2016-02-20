#! /usr/bin/env python
# -*-coding: utf-8-*-

import Image
from math import tan, sqrt
from decors import Scene, Camera, Lumiere
from formes import Sphere, Materiau
from structures import Vector, Ray, Intersection

'''
Descrition : 

Ce programme est destiné à créer des images grâce à la librairie Image de python.
Les possibilités actuelles sont les suivantes :
- tarcer des sphères dans l'espace (choisir leur centre et leur rayon)
- colorer ces sphères
- choisir l'éclairage
- afficher des ombres
- utiliser des surfaces refléchissantes
'''


#==============================================================================


def isInShadow(scene, intersection, v_lumiere, distance):
	"""
	:param scene : Scene, la scene concernée
	:param intersection : Intersection
	:param v_lumiere : Vector (normalisé)
	:returns booleen
	"""
	
	for sphere in scene.spheres:

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


#==============================================================================


def getColor(scene, ray, n_rebonds):
	"""
	:param scene : Scene, la scene concernée
	:param ray : Ray, le rayon inscident à la sphere
	:param n_rebonds : int, le nombre max de rebonds
	:returns couleur : (int, int, int)
	"""

	# on regarde si le rayon intersecte une des formes de la scene
	(forme, intersection) = scene.intersecte(ray)

	if intersection.has_intersection:

		# on calcule le point d'intersection entre le rayon et la forme
		intersection.pt_intersection = (ray.dir * intersection.t) + ray.origin

		# on calcule la normale à la forme au point d'intersection
		intersection.normale = forme.getNormale(intersection.pt_intersection)

		# on décale le point d'intersection pour corriger un bug d'affichage
		intersection.pt_intersection = intersection.pt_intersection + intersection.normale * 0.01

		if forme.materiau.speculaire and n_rebonds > 0:
			ray.reflechir(forme, intersection)
			return getColor(scene, ray, n_rebonds - 1)

		if forme.materiau.indiceRefraction != 0  and n_rebonds > 0:
			ray.refracter(forme, intersection)
			return getColor(scene, ray, n_rebonds - 1)

		# on calcule le vecteur v_lumiere partant de ce point et allant vers l'origine de la lumière
		v_lumiere = (scene.lumiere.origin - intersection.pt_intersection).getNormalized

		# on calcule la distance associée
		distance = (scene.lumiere.origin - intersection.pt_intersection).sqrNorm

		# sinon on retourne la couleur du materiau final (dernier rebond)	
		if isInShadow(scene, intersection, v_lumiere, distance):
			return (0,0,0)

		# on calcule le max entre 0 et le produit scalaire du vecteur lumière et du vecteur normal
		valeur = v_lumiere.dot(intersection.normale) * scene.lumiere.intensite / (2*3.14*distance**2) 

		# on change les pixels en fonction du calcul du produit scalaire et de la valeur d'absorbance des couleurs par la sphère
		return (max(0, int(valeur * forme.materiau.couleur[0])), max(0, int(valeur * forme.materiau.couleur[1])), max(0, int(valeur * forme.materiau.couleur[2])))		
		
	return (0,0,0)


#==============================================================================


def main():
	
	# on crée une image à partir de la librairie Image
	W = 640
	H = 480
	image = Image.new( 'RGB', (W,H), "black")
	pixels = image.load()
	
	lumiere  = Lumiere(Vector(-10,-20,40), 5000000)
	camera = Camera(Vector(0,0,55), 90 * 3.14 / 180)
	n_rebonds = 5 

	materiau_opaque1 = Materiau([1, 0, 0], False, 0) # rouge
	materiau_opaque2 = Materiau([0, 1, 0], False, 0) # vert
	materiau_opaque3 = Materiau([0, 0, 1], False, 0) # bleu
	materiau_opaque4 = Materiau([0, 1, 1], False, 0) # cyan
	materiau_opaque5 = Materiau([1, 1, 1], False, 0) # blanc
	materiau_opaque6 = Materiau([1, 1, 0], False, 0) # jaune

	materiau_reflechissant = Materiau([1, 1, 1], True, 0)

	materiau_transparent = Materiau([1, 1, 1], False, 1.5)

	s1 = Sphere(Vector(0,0,25), 10, materiau_transparent)
	s2 = Sphere(Vector(0,0,1000), 940, materiau_opaque5) # arrière
	s3 = Sphere(Vector(0,0,-1000), 940, materiau_opaque5) # devant
	s4 = Sphere(Vector(1000,0,0), 940, materiau_opaque3) # droite
	s5 = Sphere(Vector(-1000,0,0), 940, materiau_opaque1) # gauche
	s6 = Sphere(Vector(0,1000,0), 990, materiau_opaque6) # dessous
	s7 = Sphere(Vector(0,-1000,0), 940, materiau_opaque2) # dessus

	scene = Scene([s1,s2,s3,s4,s5,s6,s7], lumiere)

	D = (W/2) / tan(camera.fov/2)
	
	# pour chaque pixel de l'image, on regarde si le rayon projeté intersecte la sphère
	
	for i in xrange(image.size[1]):
		for j in xrange(image.size[0]):

			vecteurDirecteur = Vector(j - W/2, i - H/2, -D).getNormalized

			# on calcule la couleur du pixel intersecté
			pixels[j,i] = getColor(scene, Ray(camera.foyer, vecteurDirecteur), n_rebonds)
					
	image.show()
	

#==============================================================================


if __name__ == "__main__":

	main()

