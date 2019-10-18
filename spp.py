from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import os
import matplotlib.pyplot as plt
import math
import random
from myutils import *
from parameters import *

class Flock:
	def __init__(self,N):
		self.N = N
		self.boids = [Boid(L) for i in range(self.N)]

	def update(self):
		random.shuffle(self.boids)
		for boid in self.boids:
			boid.update()

	def draw(self):
		glPointSize(6)
		glLineWidth(4)
		for boid in self.boids:
			boid.draw()
		glPointSize(1)
		glLineWidth(1)

class Boid:
	size = BOIDSIZE
	utilgrid = [[[[] for k in range(UGRIDLENGTH)] for j in range(UGRIDLENGTH)] for i in range(UGRIDLENGTH)]

	def __init__(self, l):
		self.pos = l*np.random.rand(3)
		self.direction = getRandom3DUnitVector()
		# put into utilgrid
		[i, j, k] = (self.pos / UGRIDCELLSIZE).astype(int).tolist()
		Boid.utilgrid[i][j][k].append(self)

	def update(self):
		[i, j, k] = (self.pos / UGRIDCELLSIZE).astype(int).tolist()
		# potential interactors
		potinteractors = []
		ugridcellidxs = getUgridCellIndices(i,j,k)
		for [i_n,j_n,k_n] in ugridcellidxs:
			potinteractors.extend(Boid.utilgrid[i_n][j_n][k_n])
		# include only those within R
		interactors = []
		for boid in potinteractors:
			distance = np.sum(np.mod(self.pos-boid.pos,L)**2)**0.5
			if distance<R:
				interactors.append(boid)
		# calc avg direction
		avgdirection = np.zeros(3, dtype=np.float)
		for boid in interactors:
			avgdirection += boid.direction
		avgdirection /= np.sum(avgdirection**2)**0.5
		#set new direction
		self.direction = avgdirection
		newpos = np.mod(self.pos + self.direction*dT, L)
		# remove from current ugridcell
		Boid.utilgrid[i][j][k].remove(self)
		# add to new ugridcell
		[i_new, j_new, k_new] = (newpos / UGRIDCELLSIZE).astype(int).tolist()
		Boid.utilgrid[i_new][j_new][k_new].append(self)
		# set new pos
		self.pos = newpos

	def draw(self):
		p_end = self.pos-0.5*Boid.size*self.direction
		p_head = self.pos+0.5*Boid.size*self.direction
		glColor3f(1,1,1)
		glBegin(GL_POINTS)
		glVertex3fv(self.pos)
		glEnd()

		glBegin (GL_LINES)
		glColor3f(0, 0, 0)
		glVertex3fv(p_end)
		glColor3f(1, 1, 1)
		glVertex3fv(p_head)
		glEnd()

class Camera:
	def __init__(self):
		self.rotresolution = 360
		self.rot = 0
		self.centerdist = 2*L
		self.distspeed = self.centerdist*0.01
		self.x = None
		self.y = None
		self.z = None
		self.updateXYZ()
		self.setup()

	def updateXYZ(self):
		radangle = (self.rot/self.rotresolution)*2*math.pi
		self.x = L/2 + self.centerdist*math.sin(radangle)
		self.y = L/2
		self.z = L/2 + self.centerdist*math.cos(radangle)

	def move(self, key):
		if key == 'right':
			self.rot += 1
			self.rot = int(self.rot % self.rotresolution)
		if key == 'left':
			self.rot -= 1
			self.rot = int(self.rot % self.rotresolution)
		if key == 'up':
			self.centerdist -= self.distspeed
			self.centerdist = max(self.centerdist, self.distspeed)
		if key == 'down':
			self.centerdist += self.distspeed
			self.centerdist = min(self.centerdist, 5*L)
		self.updateXYZ()
		self.setup()

	def setup(self):
		glMatrixMode (GL_MODELVIEW)
		glLoadIdentity()
		gluLookAt(self.x,self.y,self.z,L/2,L/2,L/2,0,1,0) # eye, lookat, up
		glMatrixMode(GL_MODELVIEW)

class FrameBox:
	def __init__(self):
		self.framepoints = [ (0,0,0),(L,0,0),(L,L,0),(0,L,0), # back
							(0,0,L),(L,0,L),(L,L,L),(0,L,L) ]# front	
		self.framepoint_connections = ((0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7))
		self.color = (0.0, 1.0, 0.0)

	def draw(self):
		glColor3fv(self.color)
		glBegin(GL_LINES);
		for (p_idx1, p_idx2) in self.framepoint_connections:
			glVertex3fv(self.framepoints[p_idx1]);
			glVertex3fv(self.framepoints[p_idx2]);
		glEnd()

class Scene:
	def __init__(self):
		self.camera = Camera()
		self.framebox = FrameBox()
		self.flock=Flock(N)

	def draw(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		self.framebox.draw()
		self.flock.draw()

		glutSwapBuffers()

	def update(self):
		self.flock.update()
		self.draw()

def InitGL(width, height):
	glClearColor(0, 0, 0, 1.0)
	glClearDepth(1.0)
	glDepthFunc(GL_LESS)
	glEnable(GL_DEPTH_TEST)
	glShadeModel(GL_SMOOTH)
	glViewport (0,0,width,height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(width)/float(height), 0.1, L)
	glMatrixMode(GL_MODELVIEW)

def resizeGLScene (width, height):
	glViewport (0,0,width,height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(width)/float(height), 0.1, 1000.0)
	glMatrixMode(GL_MODELVIEW)

def simulation():
	pass

ESCAPE = '\033'

window = None
scene = None

#rotation
X_AXIS = 0.0
Y_AXIS = 0.0
Z_AXIS = 0.0

def keyPressed(*args):
	key = args[0].decode("utf-8")
	if key in [chr(27), 'q']:
		sys.exit()

def arrowPressed(*args):
	key = args[0]
	if key == GLUT_KEY_UP:
		scene.camera.move('up')
	elif key == GLUT_KEY_DOWN:
		scene.camera.move('down')
	elif key == GLUT_KEY_LEFT:
		scene.camera.move('left')
	elif key == GLUT_KEY_RIGHT:
		scene.camera.move('right')

def main():
	global window
	global scene
 
	glutInit()
	glutInitDisplayMode(GLUT_RGBA | GLUT_ALPHA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(W, H)
	glutGet(GLUT_SCREEN_WIDTH)
	glutInitWindowPosition(int((glutGet(GLUT_SCREEN_WIDTH)-W)/2), int((glutGet(GLUT_SCREEN_HEIGHT)-H)/2))

	window = glutCreateWindow('3D SPP model')

	scene = Scene()
	 
	glutDisplayFunc(scene.draw)
	glutIdleFunc(scene.update)
	glutKeyboardFunc(keyPressed)
	glutSpecialFunc(arrowPressed)
	glutReshapeFunc(resizeGLScene)
	InitGL(W,H)
	glutMainLoop()
 
if __name__ == "__main__":
	main() 
