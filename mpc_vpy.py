from visual import *
import csv

global step
step = 1.0
step_scale = 9.5/10.0
frame_rate = 40

def cross(a, b):
    return vector(a[1]*b[2]-a[2]*b[1],
                  a[2]*b[0]-a[0]*b[2],
                  a[0]*b[1]-a[1]*b[0])

def keyInput(evt):
    k = evt.key
    if   k == 'w':
        scene.scale = (1/step_scale)*scene.scale
    elif k == 's':
        scene.scale = (step_scale)*scene.scale
    elif k == 'q':
        scene.center = scene.center + step*scene.up
    elif k == 'e':
        scene.center = scene.center - step*scene.up
    elif k == 'a':
        scene.center = scene.center + step*cross(scene.up, scene.forward)
    elif k == 'd':
        scene.center = scene.center + step*cross(scene.forward, scene.up)


file_in = open("anim.txt", "r")
file_csv_in = csv.reader(file_in, delimiter="\t")

inti_line = next(file_csv_in)
CYL = int(inti_line[0]);
Lx = int(inti_line[1]);
Ly = int(inti_line[2]);
Lz = int(inti_line[3]); 
sigma = float(inti_line[4]); 
N = int(inti_line[5]);


scene = display(title='Animation', x=220, y=30, width=900, height=680,
                center=(Lx/2,Ly/2,Lz/2), background=(0,0,0), range=0.8*Lx)
scene.bind('keydown', keyInput)
scene.ambient = 0.4
scene.lights=[]
scene_light = distant_light(direction = -scene.forward, color=color.white)
#distant_light(direction = scene.up-scene.forward, color=(1,1,0))

if CYL == 1:
    rod = cylinder(pos=(0,Ly/2,Lz/2), axis=(Lx,0,0), radius=Ly/2)
    rod.color = (0.5,0.5,0.5)
    rod.opacity = 0.2
else:
    cuboid = box(pos=(Lx/2,Ly/2,Lz/2), length=Lx, height=Lz, width=Lz)
    cuboid.color = (0.5,0.5,0.5)
    cuboid.opacity = 0.2


ball = []
for i in range(N):
    ball.append(sphere(pos=vector(0,0,0), radius=0.5, color=(0.12,0.56,1), material=materials.diffuse))
ball[0].color = (1,0.4,0.4)
ball[N-1].color = (0.1,1,0.4)


for line in file_csv_in:
    rate(frame_rate)
    scene_light.direction = -scene.forward
    for i in range(N):
        X = float(line[0+i*3])
        Y = float(line[1+i*3])
        Z = float(line[2+i*3])
        ball[i].pos=vector(X,Y,Z)


print('end of program')






