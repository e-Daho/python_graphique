#! /usr/bin/env python
# -*-coding: utf-8-*-

import Image
from Camera import Camera
from Intersection import Intersection
from Lumiere import Lumiere
from Ray import Ray
from Scene import Scene
from Sphere import Sphere
from Vector import Vector
from math import tan
from Materiau import Materiau


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
	# fonction calculant si un pixel donné est dans l'ombre d'une sphère
	# prend en argument la scene, l'intersection entre le rayon et la sphère, 
	# le vecteur v_lumiere et la distance entre l'intersection et l'origine de la lumière
	# retourne un booléen
	
	for sphere in scene.spheres:

		# on regarde si v_lumiere intersecte la sphere, on appel i l'intersection
		i = sphere.intersect(Ray(intersection.pt_intersection, v_lumiere))

		# si cette intersection existe
		if i.has_intersection:

			# on calcule la distance dist entre i et la et l'origine de la lumière
			dist = i.t
					
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
	:returns couleur : [int, int, int]
	"""

	# on regarde si le rayon intersecte une des formes de la scene
	(forme, intersection) = scene.intersecte(ray)

	# si une intersection a été trouvée
	if intersection.has_intersection:

		# on calcule le point d'intersection entre le rayon et la forme
		intersection.pt_intersection = (ray.dir * intersection.t) + ray.origin

		# on calcule la normale à la forme au point d'intersection
		intersection.normale = forme.getNormale(intersection.pt_intersection)

		# on décale le point d'intersection pour corriger un bug d'affichage
		intersection.pt_intersection = intersection.pt_intersection + intersection.normale * 0.01

		# on calcule le vecteur v_lumiere partant de ce point et allant vers l'origine de la lumière
		v_lumiere = (scene.lumiere.origin - intersection.pt_intersection).getNormalized

		# on calcule la distance associée
		distance = (scene.lumiere.origin - intersection.pt_intersection).sqrNorm

		# si le matériau est spéculaire et qu'on a fait moins de n rebonds
		if forme.materiau.speculaire and n_rebonds > 0:

			# alors on cherche la couleur du matériaux suivant, qui sera intersecté par le rebond du rayon
			result = getColor(scene, reflechir(ray, forme, intersection), n_rebonds - 1)
			return result

		# sinon on retourne la couleur du materiau final (dernier rebond)	
		# si le pixel n'est pas dans l'ombre d'un autre objet d'un autre objet, on le modifie
		if not isInShadow(scene, intersection, v_lumiere, distance):

			# on calcule le max entre 0 et le produit scalaire du vecteur lumière et du vecteur normal
			valeur = v_lumiere.dot(intersection.normale) * scene.lumiere.intensite / (2*3.14*distance**2)

			# on change les pixels en fonction du calcul du produit scalaire et de la valeur d'absorbance des couleurs par la sphère
			return (max(0, int(valeur * forme.materiau.couleur[0])), max(0, int(valeur * forme.materiau.couleur[1])), max(0, int(valeur * forme.materiau.couleur[2])))		
		
		return (0,0,0)

	return (0,0,0)


def reflechir(ray, forme, intersection):
	"""
	:param ray : Ray, rayon à réfléchir
	:param forme : Sphere, la sphere sur lasuelle le rayon se réfléchi
	:param intersection : Intersection, le point de réflexion
	:returns Ray, rayon réfléchi 
	"""

	# on définit le rayon réfléchi
	refl_dir = (ray.dir - forme.getNormale(intersection.pt_intersection) * \
		2 * forme.getNormale(intersection.pt_intersection).dot(ray.dir)).getNormalized
	refl_origin = intersection.pt_intersection

	return Ray(refl_origin, refl_dir)


#==============================================================================


def main():
	
	# on crée une image à partir de la librairie Image
	W = 640
	H = 480
	image = Image.new( 'RGB', (W,H), "black")
	pixels = image.load()
	
	# on définit la lumière, la caméra, le nombre max de rebonds
	lumiere  = Lumiere(Vector(-20,-40,40), 10000000)
	camera = Camera(Vector(0,0,55), 90 * 3.14 / 180)
	n_rebonds = 5 

	# matériaux opaques
	materiau_opaque1 = Materiau([1, 0, 0], False, False) # rouge
	materiau_opaque2 = Materiau([0, 1, 0], False, False) # vert
	materiau_opaque3 = Materiau([0, 0, 1], False, False) # bleu
	materiau_opaque4 = Materiau([0, 1, 1], False, False) # cyan
	materiau_opaque5 = Materiau([1, 1, 1], False, False) # blanc
	materiau_opaque6 = Materiau([1, 1, 0], False, False) # jaune

	# matériaux réfléchissant
	materiau_reflechissant = Materiau([1, 1, 1], True, False)

	# les sphères à tracer
	s1 = Sphere(Vector(0,0,0.1), 10, materiau_reflechissant)
	s2 = Sphere(Vector(0,0,1000), 940, materiau_opaque4) # arrière
	s3 = Sphere(Vector(0,0,-1000), 940, materiau_opaque5) # devant
	s4 = Sphere(Vector(1000,0,0), 940, materiau_opaque3) # droite
	s5 = Sphere(Vector(-1000,0,0), 940, materiau_opaque1) # gauche
	s6 = Sphere(Vector(0,1000,0), 990, materiau_opaque6) # dessous
	s7 = Sphere(Vector(0,-1000,0), 940, materiau_opaque2) # dessus

	# on crée la scène
	scene = Scene([s1,s2,s3,s4,s5,s6,s7], lumiere)

	D = (W/2) / tan(camera.fov/2)
	
	# pour chaque pixel de l'image, on regarde si le rayon projeté intersecte la sphère
	for i in xrange(image.size[1]):
		for j in xrange(image.size[0]):

			# on défini le vecteur directeur de notre rayon
			d = Vector(j - W/2, i - H/2, -D).getNormalized

			# on calcule la couleur du pixel intersecté
			couleur = getColor(scene, Ray(camera.foyer, d), n_rebonds)

			# pour une sphère colorée avec effets de lumières
			pixels[j,i] = couleur
					
		
	image.show()
	

#==============================================================================


if __name__ == "__main__":

	main()

