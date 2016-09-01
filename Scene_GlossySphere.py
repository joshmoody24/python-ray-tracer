from Scene import *

#CAMERA ONLY WORKS WITH SQUARES AT THE MOMENT
camera = Camera(500,500)
scene = Scene()

#object positions are x,y,z. x is left/right, y is forward/backward, z is up/down

sphere4 = Sphere()
sphere4.position = Vector(0,7,-.9)
sphere4.radius = 1.5
sphere4.material.color.SetColor(1,.2,.2)
#possible material types: diffuse, glass, glossy (which is reflective), phong (which actually looks glossy)
sphere4.material.type = "phong"
sphere4.material.smoothness = 10
sphere4.material.diffuse = .9
sphere4.material.specular = .0005
scene.AddObject(sphere4)

plane = Plane()
plane.material.color.SetColor(1,1,1)
plane.position = Vector(0,0,-2)
plane.normal = Vector(0,0,1)
scene.AddObject(plane)

wall = Plane()
wall.position = Vector(0,14,0)
wall.normal = Vector(0,-1,0)
wall.material.color.SetColor(1,1,1)
wall.name = "wall"
#wall.material.type = "glossy"
scene.AddObject(wall)

light = Light()
light.position = Vector(5,4,2)
light.intensity = 1500
light.color.SetColor(.8,1,.4)
light.direction = Vector(0,0,1)
light.type = "point"
scene.AddLight(light)

light2 = Light()
light2.position = Vector(-3, 1, 1)
light2.intensity = 300
light2.color.SetColor(1,.5,.5)
light2.type = "point"
scene.AddLight(light2)

camera.Render(scene.objects, scene.lights, "GlossySphere")
