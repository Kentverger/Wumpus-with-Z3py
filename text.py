from z3 import *

z3_x = Int('z3_x')
z3_y = Int('z3_x')



BrisaFunction = Function('BrisaFunction', IntSort(), IntSort(), BoolSort())
PozoFunction = Function('PozoFunction', IntSort(), IntSort(), BoolSort())
HedorFunction = Function('HedorFunction', IntSort(), IntSort(), BoolSort())
WumpusFunction = Function('WumpusFunction', IntSort(), IntSort(), BoolSort())
SeguraFunction = Function('SeguraFunction', IntSort(), IntSort(), BoolSort())

#Para todo x y que tenga brisa implica que hay un pozo en los adyacentes
pozo = ForAll( [z3_x, z3_y], Implies( BrisaFunction( z3_x, z3_y ), Or( PozoFunction( z3_x + 1, z3_y ), PozoFunction( z3_x - 1, z3_y ), PozoFunction( z3_x, z3_y + 1 ), PozoFunction( z3_x, z3_y - 1 ) ) ) )
#no_pozo = ForAll( [z3_x, z3_y], Implies( Not(BrisaFunction( z3_x, z3_y )), And( Not(PozoFunction( z3_x + 1, z3_y )), Not(PozoFunction( z3_x - 1, z3_y )), Not(PozoFunction( z3_x, z3_y + 1 )), Not(PozoFunction( z3_x, z3_y - 1 ) ) ) ) )

hedor = ForAll( [z3_x, z3_y], Implies( HedorFunction( z3_x, z3_y ), Or( WumpusFunction( z3_x + 1, z3_y ), WumpusFunction( z3_x - 1, z3_y ), WumpusFunction( z3_x, z3_y + 1 ), WumpusFunction( z3_x, z3_y - 1 ) ) ) )
#no_hedor = ForAll( [z3_x, z3_y], Implies( Not(HedorFunction( z3_x, z3_y )), And( Not(WumpusFunction( z3_x + 1, z3_y )), Not(WumpusFunction( z3_x - 1, z3_y )), Not(WumpusFunction( z3_x, z3_y + 1 )), Not(WumpusFunction( z3_x, z3_y - 1 ) ) ) ) )

reglas = And(pozo, hedor)

persepciones_de_la_casilla = And( Not( BrisaFunction( 1, 1 ) ), Not( HedorFunction( 1, 1 ) ), Not( WumpusFunction( 1, 1 ) ), Not( PozoFunction( 1, 1 ) ) )

persepciones_mas_reglas = And( reglas, persepciones_de_la_casilla )

casilla_segura_pregunta_pregunta = And(Not( BrisaFunction( z3_x + 1, z3_y ) ), Not( HedorFunction( z3_x + 1, z3_y ) ), Not( WumpusFunction( z3_x + 1, z3_y ) ), Not( PozoFunction( z3_x + 1, z3_y ) ) )

coso = Implies( persepciones_mas_reglas, casilla_segura_pregunta_pregunta ) 

prove(coso)

'''s = Solver()
s.add(coso)
s.check()

var = s.model()

print var'''