import Image
import ImageOps
from Geometry import *
from Light import *
from Ray import *
import time

#TODO: TOP AND RIGHT 1PX BORDER IS ALWAYS BLACK. FIX.

class Pixel:
	def __init__(self,x,z):
		self.r = 0.0
		self.g = 0.0
		self.b = 0.0
		self.position = Vector(x,0,z)

	def __mul__(self, pixel):
		self.r = self.r * pixel.r
		self.g = self.g * pixel.g
		self.b = self.b * pixel.b
		return self

	def SetColor(self,r,g,b):
		self.r = r
		self.g = g
		self.b = b

class Camera:
	def __init__(self, width, height):
		self.position = Vector(0,0,0);
		self.direction = Vector(0,1,0);
		self.height = height
		self.width = width
		self.SetUpPixels()

	def SetUpPixels(self):
		print("Setting up camera...")
		#calculate aspect ratio to allow images besides squares
		#this always scales the image height
		ratio = float(self.height)/self.width
		self.pixels = [[0 for x in xrange(self.height)] for x in xrange(self.width)]
		height_increment = (1.0/self.height)*ratio
		width_increment = 1.0/self.width
		currentHeight = (1-ratio)/2 + (height_increment/2)
		currentWidth = .5/self.width
		for i in xrange(0,self.width-1):
			for j in xrange(0,self.height-1):
				self.pixels[i][j] = Pixel(0,0)
				self.pixels[i][j].position.x = currentWidth
				self.pixels[i][j].position.z = currentHeight
				currentWidth = currentWidth + width_increment
				#wrap around instead of going straight
				if(currentWidth > 1-(.5/self.width)):
					currentWidth = .5/self.width
					currentHeight = currentHeight + height_increment
#				print(self.pixels[i][j].position.x, self.pixels[i][j].position.z)
	def CastRays(self, objects, lights):
		#used for progress tracking
		fraction = .1
		#convert pixels to world space and then fire ray from camera position to them
		for i in xrange(0,self.width-1):
			for j in xrange(0,self.height-1):
				#keep track of progress
				if fraction < 1:
					if(i == int(self.width * fraction) and j == int(self.height*fraction)):
						print(str(fraction*100) + "% complete")
						fraction += .1

				pixel = Pixel(0,0)
				pixel = self.pixels[i][j]
				pixel.position.x = pixel.position.x*2-1
				pixel.position.z = pixel.position.z*2-1
#				print(pixel.position.x, pixel.position.z)
				pixel.position.y = 2
				direction = pixel.position - self.position
				direction = direction.Normalize()
				depth = 0
				hitColor = CastRay(self.position, direction, objects, lights, depth)
				pixel.SetColor(hitColor.r, hitColor.g, hitColor.b)
		#convert pixels back to NDC
                pixel.position.x = (pixel.position.x+1)/2
                pixel.position.y = (pixel.position.y+1)/2
                pixel.position.y = 0	

	def Render(self, objects, lights, name):
		print("Beginning render...")
		self.CastRays(objects, lights)
		self.SaveImage(name + ".png")

	def SaveImage(self, name):
		print("Render complete. Generating image...")
		image = Image.new('RGB', (self.width, self.height))
		for i in xrange(0,self.width-1):
			for j in xrange(0,self.height-1):
				#convert pixel color data fom 0-1 range to 0-255 range
				temp = Pixel(0,0)
				temp.SetColor(255,255,255)
				pixel = Pixel(0,0)
				pixel = self.pixels[i][j]
				pixel = pixel * temp
				r = int(pixel.r)
				g = int(pixel.g)
				b = int(pixel.b)

				#clamp values
				if(r > 255):
					r = 255
				if(g > 255):
					g = 255
				if(b > 255):
					b = 255

				image.putpixel((i,j), (r, g, b))
		#image needs to be rotated 90 degrees
		rotated = image.rotate(90)
		#mirrored = ImageOps.mirror(rotated)
		rotated.save(name)
