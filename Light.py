from Geometry import *
class Light:
	def __init__(self):
		self.color = Color()
		self.color.SetColor(1,1,1)
		self.position = Vector(0,0,0)
		self.intensity = 1
		#used for point light calculations
		self.direction = Vector(0,0,0)
		self.type = "point"

class DirectionalLight(Light):
	def __init__(self):
		Light.__init__(self)
		#light goes the opposite direction of its direction
		self.direction = Vector(0,0,1)
		self.type = "directional"
