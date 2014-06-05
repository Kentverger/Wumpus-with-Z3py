import sys
import re
from z3 import *
import pygame
import time
from cStringIO import StringIO

pygame.init()

pygame.mixer.music.load('lol.ogg')
pygame.mixer.music.play()
time.sleep(1.5)

z3_x = Int('z3_x')
z3_y = Int('z3_x')



BrisaFunction = Function('BrisaFunction', IntSort(), IntSort(), BoolSort())
PozoFunction = Function('PozoFunction', IntSort(), IntSort(), BoolSort())
HedorFunction = Function('HedorFunction', IntSort(), IntSort(), BoolSort())
WumpusFunction = Function('WumpusFunction', IntSort(), IntSort(), BoolSort())
SeguraFunction = Function('SeguraFunction', IntSort(), IntSort(), BoolSort())
ResplandorFunction = Function('ResplandorFunction', IntSort(), IntSort(), BoolSort())
OroFunction = Function('OroFunction', IntSort(), IntSort(), BoolSort())

#Para todo x y que tenga brisa implica que hay un pozo en los adyacentes
pozo = ForAll( z3_x, ForAll(z3_y, Implies( BrisaFunction( z3_x, z3_y ), Or( PozoFunction( z3_x + 1, z3_y ), PozoFunction( z3_x - 1, z3_y ), PozoFunction( z3_x, z3_y + 1 ), PozoFunction( z3_x, z3_y - 1 ) ) ) ) )
no_pozo = ForAll( [z3_x, z3_y], Implies( Not(BrisaFunction( z3_x, z3_y )), And( Not(PozoFunction( z3_x + 1, z3_y )), Not(PozoFunction( z3_x - 1, z3_y )), Not(PozoFunction( z3_x, z3_y + 1 )), Not(PozoFunction( z3_x, z3_y - 1 ) ) ) ) )

hedor = ForAll( z3_x, ForAll( z3_y, Implies( HedorFunction( z3_x, z3_y ), Or( WumpusFunction( z3_x + 1, z3_y ), WumpusFunction( z3_x - 1, z3_y ), WumpusFunction( z3_x, z3_y + 1 ), WumpusFunction( z3_x, z3_y - 1 ) ) ) ))
no_hedor = ForAll( [z3_x, z3_y], Implies( Not(HedorFunction( z3_x, z3_y )), And( Not(WumpusFunction( z3_x + 1, z3_y )), Not(WumpusFunction( z3_x - 1, z3_y )), Not(WumpusFunction( z3_x, z3_y + 1 )), Not(WumpusFunction( z3_x, z3_y - 1 ) ) ) ) )

casilla_segura = ForAll([z3_x, z3_y], Implies( And( Not( BrisaFunction( z3_x, z3_y ) ), Not( HedorFunction( z3_x, z3_y ) ), Not( PozoFunction( z3_x, z3_y ) ), Not( WumpusFunction( z3_x, z3_y ) ) ), SeguraFunction( z3_x, z3_y ) ) )

casilla_con_oro = ForAll([z3_x, z3_y], Implies(ResplandorFunction(z3_x, z3_y), OroFunction(z3_x, z3_y) ) )

reglas = And(pozo, hedor, no_pozo, no_hedor)

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
x = 1
y = 1

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

def prueba(coso):

	old_stdout = sys.stdout
	sys.stdout = mystdout = StringIO()

	prove(coso)

	cadena = sys.stdout.readline()

	sys.stdout = old_stdout

	return cadena

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
				h = HedorFunction(x, y)
			else:
				h = Not(HedorFunction(x, y))
			if m[1] == "(si)":
				b = BrisaFunction(x,y)
			else:
				b = Not(BrisaFunction(x,y))

			if m[2] == "(si)":
				r = BoolVal(True)
			else:
				r = BoolVal(False)

			if m[3] == "(si)":
				g = BoolVal(True)
			else:
				g = BoolVal(False)

			reglas = And(reglas, h, b)

			#prueba si hay hedor o brisa, para saber si avanzar
			coso = Implies(reglas, Or(Not(HedorFunction(x+1,y)), Not(BrisaFunction(x+1,y))))
			prueba(coso)


			#avanza hasta no encontar brisa, hedor o esuchar un golpe
			'''if not prueba(brisa_o_hedor, a):
				c = Casilla(True, [h, b, r, g], True, x, y)
				mapa.push(c)
				avanza()
				pass
			else:
				regresa()
				pass

			if prueba(golpe, a):
				regresa()
				pass '''

	elif line.find("EPISODE_ENDED") != -1:
		break


