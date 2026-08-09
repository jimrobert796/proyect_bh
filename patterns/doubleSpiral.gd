class_name PatternDoubleSpiral
extends Pattern
@export var incrementoAngulo = 0.15
var angulo = 0.0
func _ready():
	super._ready(); 
	tiempoFuego = 0.05
	duracion = 10
func disparar():
	angulo -= incrementoAngulo
	crear_bala(Vector2(cos(angulo + PI), sin(angulo + PI)))
	crear_bala(Vector2(cos(angulo + PI + 1), sin(angulo + PI + 1)))
	crear_bala(Vector2(cos(angulo + PI + 2), sin(angulo + PI + 2)))
	crear_bala(Vector2(cos(angulo + PI + 3), sin(angulo + PI + 3)))
	crear_bala(Vector2(cos(angulo + PI + 4), sin(angulo + PI + 4)))
	crear_bala(Vector2(cos(angulo + PI + 5), sin(angulo + PI + 5)))
