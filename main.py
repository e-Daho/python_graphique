#! /usr/bin/env python
# -*-coding: utf-8-*-

from PIL import Image, ImageChops
from multiprocessing import Process, Queue, TimeoutError
from itertools import izip

from structures import Vector
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
- utiliser un éclairage diffus
'''

W = 640
H = 480
n_rebonds = 4
diffus = True
n_echantillons = 50
n_quadrants = 4


#==============================================================================


def main():
	
	# on crée une image à partir de la librairie Image
	image = Image.new( 'RGB', (W,H), "black")
	
	# on crée la scène
	lumiere  = Lumiere(Vector(-10,-20,40), 1000000000)
	camera = Camera(Vector(0,0,55), 90 * 3.14 / 180)
	
	materiau_opaque1 = Materiau([1, 0, 0], False, 0) # rouge
	materiau_opaque2 = Materiau([0, 1, 0], False, 0) # vert
	materiau_opaque3 = Materiau([0, 0, 1], False, 0) # bleu
	materiau_opaque4 = Materiau([0, 1, 1], False, 0) # cyan
	materiau_opaque5 = Materiau([1, 1, 1], False, 0) # blanc
	materiau_opaque6 = Materiau([1, 1, 0], False, 0) # jaune

	materiau_reflechissant = Materiau([1, 1, 1], True, 0)

	materiau_transparent = Materiau([1, 1, 1], False, 1.5)

	s1 = Sphere(Vector(0,-2,25), 10, materiau_opaque5)
	s2 = Sphere(Vector(0,0,1000), 940, materiau_opaque5) # arrière
	s3 = Sphere(Vector(0,0,-1000), 940, materiau_opaque5) # devant
	s4 = Sphere(Vector(1000,0,0), 940, materiau_opaque3) # droite
	s5 = Sphere(Vector(-1000,0,0), 940, materiau_opaque1) # gauche
	s6 = Sphere(Vector(0,1000,0), 990, materiau_opaque6) # dessous
	s7 = Sphere(Vector(0,-1000,0), 940, materiau_opaque2) # dessus

	scene = Scene([s1,s2,s3,s4,s5,s6,s7], lumiere)

	# variable pour le multiprocessing
	out_q = Queue()
	imageProcess = []
	imageQuadrant = []

	# on lance des process pour chaque quadran
	for i in xrange(n_quadrants):
		imageProcess.append(Process(target = scene.getImage, 
										args = (camera, image, n_rebonds, i, out_q, n_echantillons, diffus)))
		imageProcess[i].start()

	for i in xrange(n_quadrants):	
		imageQuadrant.append(out_q.get())

	for i in xrange(n_quadrants):
		imageProcess[i].join()

	# on reconstruit l'image depuis les quadrans
	image_haute = ImageChops.add(imageQuadrant[0], imageQuadrant[1])
	image_basse = ImageChops.add(imageQuadrant[2], imageQuadrant[3])
	image = ImageChops.add(image_haute, image_basse)

	image.show()
	image.save('image.jpg')


#==============================================================================


if __name__ == "__main__":

	main()

