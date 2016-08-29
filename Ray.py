import math
import time
from Geometry import *

#TEMP, ADD TO OPTIONS FILE
max_depth = 5
def CastRay(position, direction, objects, lights, depth):
	if depth > max_depth:
		#print("exceeded depth")
		return Color()
	ray = Ray()
	ray.position = position
	ray.direction = direction
	ray.Normalize()
	#trace the ray
	color = Trace(ray, objects, lights, depth)
	return color

def Trace(ray, objects, lights, depth):
	#find closest object
	closest = Object()
	for object in objects:
		if object.Intersect(ray):
			#if current sphere is closest so far
			if(object.distance < closest.distance):
				closest = object
	if(closest.distance < float('inf')):
		hitPos = ray.position + (ray.direction.Stretch(closest.distance))
		normal = closest.GetNormal(hitPos)
		normal.Normalize()
		hitColor = Color()
		if(closest.material.type == "diffuse"):
			for light in lights:
				hitColor = hitColor.Add(CalculateLight(hitPos, light, normal, objects, closest))
		elif(closest.material.type == "glossy"):
			reflection = Reflect(ray.direction, normal)
			depth += 1
			hitColor.Add(CastRay(hitPos + (normal *.001), reflection, objects, lights, depth) * closest.material.reflectivity)
		elif(closest.material.type == "glass"):
			#compute fresnel
			kr = Fresnel(ray.direction, normal, closest.material.ior)
			outside = ray.direction.DotProduct(normal) < 0
			bias = normal * .001
			if(kr < 1):
				refractionDir = Refract(ray.direction, normal, closest.material.ior).Normalize()
				refractionPos = hitPos - bias if outside else hitPos + bias
				depth += 1
				refractionColor = CastRay(refractionPos, refractionDir, objects, lights, depth)
			reflectionDirection = Reflect(ray.direction, normal).Normalize()
			reflectionRayOrig = hitPos - bias if outside else hitPos + bias
			depth += 1
			reflectionColor = CastRay(reflectionRayOrig, reflectionDirection, objects, lights, depth)
			#mix the two
			hitColor = hitColor.Add((reflectionColor * kr).Add(refractionColor * (1-kr)))
		elif(closest.material.type == "phong"):
			diffuse = Color()
			specular = 0.0
			for light in lights:
				#calculate diffuse component
				diffuse = diffuse.Add(CalculateLight(hitPos, light, normal, objects, closest))
				#calculate specular component
				#get ideal reflection direction
				lightDir = (hitPos - light.position).Normalize()
				reflection = Reflect(lightDir, normal)
				vis = TestShadow(hitPos, light, objects, normal)
				specular = specular + (vis * light.intensity * (max(0.0, reflection.DotProduct(-ray.direction)) ** closest.material.smoothness))
			hitColor = (diffuse * closest.material.diffuse) + (specular * closest.material.specular)
		return hitColor
	else:
		return Color()

def Refract(incident, normal, ior):
	cosi = incident.DotProduct(normal)
	if cosi > 1:
		cosi = 1
	elif cosi < -1:
		cosi = -1
	etai = 1
	etat = ior
	n = normal
	if cosi < 0:
		cosi = -cosi
	else:
		temp = etai
		etai = etat
		etat = temp
		n = -normal
	eta = etai / etat
	k = 1 - eta*eta*(1-cosi*cosi)
	return Vector(0,0,0) if k < 0 else (incident * eta) + (n * (eta * cosi - math.sqrt(k)))
	

def Fresnel(incident, normal, ior):
	#make sure both are normalized so cosi is between -1 and 1
	incident = incident.Normalize()
	normal = incident.Normalize()
	cosi = incident.DotProduct(normal)
	ior1 = 1
	ior2 = ior
	if(cosi < 0):
		cosi = -cosi
	else:
		temp = ior1
		ior1 = ior2
		ior2 = temp
	#compute sini using snell's law
	sint = ior1 / ior2 * math.sqrt(max(0.0, 1 - cosi * cosi))
	#total internal reflection
	if(sint >= 1):
		kr = 1
		return kr
	else:
		cost = math.sqrt(max(0.0, 1-sint*sint))
		cosi = abs(cosi)
		Rs = ((ior2 * cosi) - (ior1 * cost)) / ((ior2 * cosi) + (ior1 * cost))
		Rp = ((ior1 * cosi) - (ior2 * cost)) / ((ior1 * cosi) + (ior2 * cost))
		kr = (Rs * Rs + Rp * Rp) / 2
	return kr
def Reflect(incident, normal):
	return (incident - (normal * 2 * incident.DotProduct(normal))).Normalize()

#calculates light received from point
def CalculateLight(position, light, normal, objects, object):
	if(light.type == "point"):
		light.direction = light.position - position
	light.direction.Normalize()
	lightAmount = light.direction.DotProduct(normal)
	if lightAmount < 0:
		lightAmount = 0
	#diffuse calculations
	hitColor = object.material.albedo / math.pi
	hitColor = hitColor * lightAmount
	hitColor = ComputeIntensity(position,light) * hitColor
	#shadow
	visibility = TestShadow(position, light, objects, normal)
	hitColor *= visibility
	hitColor.Multiply(object.material.color)
	return hitColor

def ComputeIntensity(position, light):
	r2 = light.position - position
	r2 = r2.Magnitude()
	r2 = r2 * r2
	#print light.color.r, light.color.g, light.color.b
	lightColor = light.color
	lightIntensity = (lightColor * light.intensity) / (4 * math.pi * r2)	
	return lightIntensity

#returns true if point is in shadow
def TestShadow(position,light, objects, normal):
	#avoiding grainy artifact
	bias = .01
	for object in objects:
		shadowRay = Ray()
		shadowRay.position = position + (normal*Vector(bias,bias,bias))
		shadowRay.direction = light.direction
		shadowRay.Normalize()
		if(object.Intersect(shadowRay)):
			#calculate light distance
			lightDist = light.position - position
			lightDist = lightDist.Magnitude()
			#make sure the object isn't farther away than the light
			if(object.distance < lightDist):
				return 0
	return 1
