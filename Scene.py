from Geometry import *
from Camera import Camera
from Light import *
import random
import time
class Scene:
	def __init__(self):
		self.objects = list()
		self.lights = list()
	def AddObject(self,object):
		self.objects.append(object)
	def AddLight(self,object):
		self.lights.append(object)

	def RandomScene(self, numberOfObjects):
		for x in range(numberOfObjects):
			#temp
			radius = random.uniform(1,1.5)
			xPos = random.uniform(-6,6)
			yPos = random.uniform(2,8)
			zPos = random.uniform(-1,6)
			#color
			r = random.random()/2 + .5
			g = random.random()/2 + .5
			b = random.random()/2 + .5
			#generate
			sphere = Sphere()
			sphere.radius = radius
			sphere.position = Vector(xPos,yPos,zPos)
			sphere.material.color.SetColor(r,g,b)
			self.AddObject(sphere)