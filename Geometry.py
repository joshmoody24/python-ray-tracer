import math
class Vector:
        def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z
	def __sub__(self, vector):
		if(vector.__class__.__name__ == "Vector"):
                	return Vector(self.x - vector.x, self.y - vector.y, self.z - vector.z)
		else:
			x = self.x + vector
			y = self.y + vector
			z = self.z + vector
			return Vector(x,y,z)
	def __add__(self, vector):
		if(vector.__class__.__name__ == "Vector"):
			return Vector(self.x + vector.x, self.y + vector.y, self.z + vector.z)
		else:
			x = self.x + vector
			y = self.y + vector
			z = self.z + vector
			return Vector(x,y,z)
	def __mul__(self, vector):
		if(vector.__class__.__name__ == "Vector"):
			return Vector(self.x * vector.x, self.y * vector.y, self.z * vector.z)
		#if vector is just a value
		else:
			x = self.x * vector
			y = self.y * vector
			z = self.z * vector
			return Vector(x,y,z)
	def __neg__(self):
		return Vector(-self.x, -self.y, -self.z)

	def Stretch(self, amount):
		return Vector(self.x * amount, self.y * amount, self.z * amount)
#	def __init__(self):
        def Set(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z
        def Magnitude(self):
                return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
	def Normalize(self):
                magnitude = self.Magnitude()
                if(magnitude == 0):
                        return magnitude
                x = self.x / magnitude
                y = self.y / magnitude
                z = self.z / magnitude
                return Vector(x,y,z)
	def DotProduct(self, vector):
		return self.x*vector.x + self.y*vector.y + self.z*vector.z



class Ray:
	def __init__(self):
		self.position = Vector(0,0,0)
		self.direction = Vector(0,0,0)
	def Normalize(self):
		magnitude = self.direction.Magnitude()
		if(magnitude == 0):
			return magnitude
		self.direction.x = self.direction.x / magnitude
		self.direction.y = self.direction.y / magnitude
		self.direction.z = self.direction.z / magnitude
		return self.direction





class Color:
	#todo: Multiply and Add methods can be integrated into overloaded operators with if statement?
	def __init__(self):
		self.r = 0.0
		self.g = 0.0
		self.b = 0.0
	def __mul__(self, value):
		r = self.r * value
		g = self.g * value
		b = self.b * value
		newColor = Color()
		newColor.SetColor(r,g,b)
		return newColor
	def __add__(self, value):
		r = self.r + value
		g = self.g + value
		b = self.b + value
		newColor = Color()
		newColor.SetColor(r,g,b)
		return newColor
	def __div__(self, value):
		r = self.r / value
		g = self.g / value
		b = self.b / value
		newColor = Color()
		newColor.SetColor(r,g,b)
		return newColor
	def SetColor(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b
	#different from operator. Operator + multiplies each channel by single value
	#this method multiplies by another color instance
	def Multiply(self, color):
		self.r = self.r * color.r
		self.g = self.g * color.g
		self.b = self.b * color.b
		return self
	def Add(self, color):
		self.r = self.r + color.r
		self.g = self.g + color.g
		self.b = self.b + color.b
		return self

class Material:
	def __init__(self):
		self.type = "diffuse"
		self.color = Color()
		self.albedo = .18
		self.reflectivity = .8
		self.ior = 1.45
		self.smoothness = 10
		self.specular = .08
		self.diffuse = .08
		
class Object:
	def __init__(self):
		self.distance = float('inf')
		self.material = Material()
		self.position = Vector(0,0,0)
		self.name = "object"

class Sphere(Object):
	def __init__(self):
		Object.__init__(self)
		self.radius = 1
		#intersection distance. Used when testing intersections
	def SetRadius(self, radius):
		self.radius = radius
	def Intersect(self, ray):
		L = self.position - ray.position
		tca = L.DotProduct(ray.direction)
		d2 = L.DotProduct(L) - tca * tca
		if d2 > self.radius:
			 return False
		radius2 = self.radius*self.radius
 		thc = math.sqrt(radius2 - d2)
		t0 = tca - thc
		t1 = tca + thc
		if t0 > t1:
			temp = t0
			t0 = t1
			t1 = temp
		if(t0 < 0):
			t0 = t1 #if t0 is negative, use t1 instead
			if(t0<0):
				return False #both negative.
		self.distance = t0
		return True
	def GetNormal(self, position):
		return position -self.position

class Plane(Object):
	def __init__(self):
		Object.__init__(self)
		self.normal = Vector(0,0,1)

	def Intersect(self, ray):
		#for some reason, intersect normal is opposite the light normal. Bug. FIX. Source of bug is light for sure
		inverted = Vector(0,0,0) - self.normal
		denom = ray.direction.DotProduct(inverted)
		#if ray and plane are not very close to perpendicular
		if(denom > 0.000001):
			angle = self.position - ray.position
			t = angle.DotProduct(inverted) / denom
			self.distance = t
			return (t>=0)
		return False
	def GetNormal(self, point):
		return self.normal
