import sys
import re
from z3 import *
#import pygame
#import time

#pygame.init()

#pygame.mixer.music.load('lol.ogg')
#pygame.mixer.music.play()
#time.sleep(1.5)

a = Bool("Avanzar")
ag = Bool("Agarrar")

z3_x = Ints('z3_x')
z3_y = Ints('z3_x')

BrisaFunction = Function('BrisaFunction', IntSort(), IntSort(), BoolSort())
PozoFunction = Function('PozoFunction', IntSort(), IntSort(), BoolSort())

#Para todo x y que tenga brisa implica que hay un pozo en los adyacentes
r1 = ForAll( [z3_x, z3_y], Implies( BrisaFunction( z3_x, z3_y ), Or( PozoFunction( z3_x + 1, z3_y ), PozoFunction( z3_x - 1, z3_y ), PozoFunction( z3_x, z3_y + 1 ), PozoFunction( z3_x, z3_y - 1 ) ) ) )

class Casilla:
	def __init__(self, visitada, precepcion, segura, x, y):
		self.visitada = visitada
		self.precepcion = precepcion
		self.segura = segura
		self.x = x
		self.y = y


	def yaLaVisito(self):
		return self.visitada

	def percepiones(self):
		return self.percepion

	def esSegura(self):
		return self.segura

class Lifo:
    def __init__(self, lst=[]):
        self.q = []
        self.out = 0
    def push(self, seq):
        self.q.append(seq)
    def pop(self):
        k = self.q[self.out]
        self.out += 1
        return k

mapa = Lifo()
x = 0
y = 0

ORIENTACION_NORTE = 1
ORIENTACION_SUR = 2
ORIENTACION_ESTE = 3
ORIENTACION_OESTE = 4
orientacion = ORIENTACION_ESTE

def gira(direccion):

	global orientacion

	if orientacion == ORIENTACION_ESTE and direccion == "der":
		orientacion = ORIENTACION_NORTE
	elif orientacion == ORIENTACION_ESTE and direccion == "izq":
		orientacion = ORIENTACION_SUR
	elif orientacion == ORIENTACION_OESTE and direccion == "der":
		orientacion =  ORIENTACION_NORTE
	elif orientacion == ORIENTACION_OESTE and direccion == "izq":
		orientacion = ORIENTACION_SUR
	elif orientacion == ORIENTACION_NORTE and direccion == "der":
		orientacion =  ORIENTACION_ESTE
	elif orientacion == ORIENTACION_NORTE and direccion == "izq":
		orientacion = ORIENTACION_OESTE
	elif orientacion == ORIENTACION_NORTE and direccion == "der":
		orientacion =  ORIENTACION_ESTE
	elif orientacion == ORIENTACION_NORTE and direccion == "izq":
		orientacion = ORIENTACION_OESTE

	if direccion == "der":
		sys.stdout.write("Derecha\n")
		sys.stdout.flush()
	elif direccion == "izq":
		sys.stdout.write("Izquierda\n")
		sys.stdout.flush()

def avanza():

	global x
	global y
	global orientacion

	if orientacion == ORIENTACION_ESTE:
		x+=1
	elif orientacion == ORIENTACION_OESTE:
		x-=1
	elif orientacion == ORIENTACION_NORTE:
		y+=1
	elif orientacion == ORIENTACION_SUR:
		y-=1

	sys.stdout.write("Avanzar\n")
	sys.stdout.flush()

def agarra():
	sys.stdout.write("Agarrar\n")
	sys.stdout.flush()

def prueba(coso, otrocoso):
	s = Solver()
	s.add(coso)
	s.check()

	var = s.model()

	return var[otrocoso]

def regresa():

	while True:
		c = mapa.pop()
		gira("izq")
		sys.stdin.readline()
		gira("izq")
		sys.stdin.readline()
		avanza()
		sys.stdin.readline()
					
		if c.segura:
			break

while True:
	line = sys.stdin.readline()
	if line != "SIMULATION_STARTED" and line != "EPISODE_STARTED":
		m = re.findall('\(no\)|\(si\)', line)
		if len(m) != 0:
			if m[0] == "(si)":
				h = BoolVal(True)
			else:
				h = BoolVal(False)

			if m[1] == "(si)":
				b = BoolVal(True)
			else:
				b = BoolVal(False)

			if m[2] == "(si)":
				r = BoolVal(True)
			else:
				r = BoolVal(False)

			if m[3] == "(si)":
				g = BoolVal(True)
			else:
				g = BoolVal(False)

			hedor = Implies( h, Not( a ) )
			brisa = Implies( b, Not( a ) )
			golpe = Implies( g, Not( a ) )
			resplandor = Implies( r, ag )

			brisa_o_hedor = And(hedor, brisa)

			#avanza hasta no encontar brisa, hedor o esuchar un golpe
			if not prueba(brisa_o_hedor, a):
				c = Casilla(True, [h, b, r, g], True, x, y)
				mapa.push(c)
				avanza()
				pass
			else:
				regresa()
				pass

			if prueba(golpe, a):
				regresa()
				pass

	elif line.find("EPISODE_ENDED") != -1:
		break


