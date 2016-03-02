#! /usr/bin/env python
# -*-coding: utf-8-*-

from PIL import Image, ImageChops
from multiprocessing import Process, Queue, TimeoutError
import numpy as np
from itertools import izip

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
	lumiere  = Lumiere(np.array([-10,-20,40]), 750000000)
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

	# variable pour le multiprocessing
	n_quadrants = 4
	out_q = Queue()
	imageProcess = []
	imageQuadran = []

	# on lance des process pour chaque quadran
	for i in xrange(n_quadrants):
		imageProcess.append(Process(target = scene.getImage, 
										args = (camera, image, n_rebonds, i, out_q)))
		imageProcess[i].start()

	for i in xrange(n_quadrants):	
		imageQuadran.append(out_q.get())

	for i in xrange(n_quadrants):
		imageProcess[i].join()

	# on reconstruit l'image depuis les quadrans
	image_haute = ImageChops.add(imageQuadran[0], imageQuadran[1])
	image_basse = ImageChops.add(imageQuadran[2], imageQuadran[3])
	image = ImageChops.add(image_haute, image_basse)

	image.show()


#==============================================================================


if __name__ == "__main__":

	main()

