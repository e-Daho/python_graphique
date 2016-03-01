#! /usr/bin/env python
# -*-coding: utf-8-*-

import  PIL
from PIL import Image

import numpy as np

from decors import Scene, Camera, Lumiere
from formes import Sphere, Materiau

'''
Descrition : 

Ce programme est destiné à créer des images grâce à la librairie Image de python.
Les possibilités actuelles sont les suivantes :
- tarcer des sphères dans l'espace (choisir leur centre et leur rayon)
- colorer ces sphères
- choisir l'éclairage
- afficher des ombres
- utiliser des surfaces refléchissantes
- utiliser des surfaces transparentes
'''


#==============================================================================


def main():
	
	# on crée une image à partir de la librairie Image
	W = 640
	H = 480
	image = Image.new( 'RGB', (W,H), "black")
	
	# on crée la scène
	lumiere  = Lumiere(np.array([-10,-20,40]), 5000000)
	camera = Camera(np.array([0,0,55]), 90 * 3.14 / 180)
	n_rebonds = 5 

	materiau_opaque1 = Materiau([1, 0, 0], False, 0) # rouge
	materiau_opaque2 = Materiau([0, 1, 0], False, 0) # vert
	materiau_opaque3 = Materiau([0, 0, 1], False, 0) # bleu
	materiau_opaque4 = Materiau([0, 1, 1], False, 0) # cyan
	materiau_opaque5 = Materiau([1, 1, 1], False, 0) # blanc
	materiau_opaque6 = Materiau([1, 1, 0], False, 0) # jaune

	materiau_reflechissant = Materiau([1, 1, 1], True, 0)

	materiau_transparent = Materiau([1, 1, 1], False, 1.5)

	s1 = Sphere(np.array([0,0,25]), 10, materiau_transparent)
	s2 = Sphere(np.array([0,0,1000]), 940, materiau_opaque5) # arrière
	s3 = Sphere(np.array([0,0,-1000]), 940, materiau_opaque5) # devant
	s4 = Sphere(np.array([1000,0,0]), 940, materiau_opaque3) # droite
	s5 = Sphere(np.array([-1000,0,0]), 940, materiau_opaque1) # gauche
	s6 = Sphere(np.array([0,1000,0]), 990, materiau_opaque6) # dessous
	s7 = Sphere(np.array([0,-1000,0]), 940, materiau_opaque2) # dessus

	scene = Scene([s1,s2,s3,s4,s5,s6,s7], lumiere)

	image = scene.getImage(camera, image, n_rebonds)
					
	image.show()
	

#==============================================================================


if __name__ == "__main__":

	main()

