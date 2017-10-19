from visual import *
import wx
import csv


global step
step = 1.0
step_scale = 9.5/10.0
frame_rate = 60


def cross(a, b):
    return norm(vector(a[1]*b[2]-a[2]*b[1],
                  a[2]*b[0]-a[0]*b[2],
                  a[0]*b[1]-a[1]*b[0]))

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

def setPos(evt):
    global I
    I = s1.GetValue()

def pp(evt):
    global increment
    if increment == 1:
        increment = 0
    else:
        increment = 1

def reset(evt):
    scene.center = (Lx/2,Ly/2,Lz/2)
    scene.forward = (0,0,-1)
    scene.range = 42


file_in = open("anim.txt", "r")
file_csv_in = csv.reader(file_in, delimiter="\t")

dat = list(file_csv_in)
M = len(dat)-2
file_in.seek(0)

inti_line = next(file_csv_in)
CYL = int(inti_line[0]);
Lx = int(inti_line[1]);
Ly = int(inti_line[2]);
Lz = int(inti_line[3]); 
sigma = float(inti_line[4]); 
N = int(inti_line[5]);



w = window(menus=False, title="VPython",
           x=100, y=10, width=1005, height=710)
scene = display(window=w, title='Animation', x=0, y=0, width=900, height=680,
                center=(Lx/2,Ly/2,Lz/2), background=(0,0,0), range=0.7*Lx)
scene.bind('keydown', keyInput)
scene.ambient = 0.3
scene.lights=[]
scene_light = distant_light(direction = -scene.forward, color=color.white)
#distant_light(direction = scene.up-scene.forward, color=(1,1,0))

p=w.panel
b_play = wx.Button(p, label='Play/Pause', pos=(901,15))
b_play.Bind(wx.EVT_BUTTON, pp)
s1 = wx.Slider(p, pos=(935,40), size=(50,590), minValue=1, maxValue=M, style=wx.SL_VERTICAL)
s1.Bind(wx.EVT_SCROLL, setPos)
b_res = wx.Button(p, label='Reset View', pos=(901,635))
b_res.Bind(wx.EVT_BUTTON, reset)


if CYL == 1:
    rod = cylinder(pos=(0,Ly/2,Lz/2), axis=(Lx,0,0), radius=Ly/2)
    rod.color = (0.5,0.5,0.5)
    rod.opacity = 0.2
else:
    cuboid = box(pos=(Lx/2,Ly/2,Lz/2), length=Lx, height=Lz, width=Lz)
    cuboid.color = (0.5,0.5,0.5)
    cuboid.opacity = 0.2

arrow(pos=scene.center+(0.6*Ly)*scene.up, axis=(2.5,0,0), shaftwidth=0.2, color=(1,0,0), material=materials.diffuse)
arrow(pos=scene.center+(0.6*Ly)*scene.up, axis=(0,2.5,0), shaftwidth=0.2, color=(0,1,0), material=materials.diffuse)
arrow(pos=scene.center+(0.6*Ly)*scene.up, axis=(0,0,2.5), shaftwidth=0.2, color=(0,0.4,1),material=materials.diffuse)

ball = []
for i in range(N):
    ball.append(sphere(pos=vector(0,0,0), radius=0.5, color=(0.12,0.56,1), material=materials.diffuse))
ball[0].color = (1,0.4,0.4)
ball[N-1].color = (0.1,1,0.4)


I = 1
increment = 1
while I <= M:
    rate(frame_rate)
    scene_light.direction = -scene.forward
    for i in range(N):
        X = float(dat[I][0+i*3])
        Y = float(dat[I][1+i*3])
        Z = float(dat[I][2+i*3])
        ball[i].pos=vector(X,Y,Z)
    I = I+increment
    s1.SetValue(I)
    


print('end of program')






