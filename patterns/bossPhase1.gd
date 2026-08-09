class_name PatternBossPhase1
extends Pattern
@export var incrementoAngulo = 0.15
var angulo = 0.0
var contador = 0
func _ready():
	super._ready(); tiempoFuego = 0.1; duracion = 10
func disparar():
	angulo += incrementoAngulo
	crear_bala(Vector2(cos(angulo), sin(angulo)))
	contador += 1
	if contador % 15 == 0:  # cada 15 disparos, suelta un anillo extra
		for i in range(10):
			var a = (TAU / 10) * i
			crear_bala(Vector2(cos(a), sin(a)))
		
		for a in [0.0, PI/2, PI, 3*PI/2]:
			crear_bala(Vector2(cos(a), sin(a)))
			
			
